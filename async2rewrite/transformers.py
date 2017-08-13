import ast

easy_stateful_list = ['add_reaction', 'add_roles', 'ban', 'clear_reactions', 'create_invite', 'create_custom_emoji',
                      'create_role', 'kick', 'remove_reaction', 'remove_roles', 'prune_members', 'unban',
                      'get_message', 'estimate_pruned_members']

easy_deletes_list = ['delete_custom_emoji', 'delete_channel', 'delete_invite', 'delete_message', 'delete_role',
                     'delete_server']

easy_edits_list = ['edit_channel', 'edit_custom_emoji', 'edit_server']


class CallTransforms:

    @staticmethod
    def remove_passcontext(n):
        for d in n.decorator_list:
            if not isinstance(d, ast.Call):
                continue
            for kw in list(d.keywords):  # iterate over a copy of the list to avoid removing while iterating
                if not isinstance(kw.value, ast.NameConstant):
                    continue
                if kw.arg == 'pass_context':  # if the pass_context kwarg is set to True
                    d.keywords.remove(kw)
        return n

    @staticmethod
    def to_messageable(call):
        if not isinstance(call.func, ast.Attribute):
            return call
        if not isinstance(call.func.value, ast.Name):
            return call
        if call.func.attr == 'say':
            call.func.value.id = 'ctx'
            call.func.attr = 'send'
            return call
        elif call.func.attr == 'send_message':
            destination = call.args[0]

            wrap_attr = ast.Attribute()
            wrap_attr.value = destination
            wrap_attr.attr = 'send'
            wrap_attr.ctx = ast.Load()

            newcall = ast.Call()
            newcall.func = wrap_attr
            newcall.args = call.args[1:]
            newcall.keywords = call.keywords

            newcall = ast.copy_location(newcall, call)

            return newcall

        return call

    @staticmethod
    def easy_statefuls(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_stateful_list:
                message = call.args[0].id
                call.func.value.id = message
                call.args = call.args[1:]
        return call

    @staticmethod
    def easy_deletes(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_deletes_list:
                to_delete = call.args[0]
                call.func.value.id = to_delete.id
                call.args = call.args[1:]
                call.func.attr = 'delete'
        return call

    @staticmethod
    def easy_edits(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_edits_list:
                to_edit = call.args[0]
                call.func.value.id = to_edit.id
                call.args = call.args[1:]
                call.func.attr = 'edit'
        return call

    @staticmethod
    def stateful_change_nickname(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'change_nickname':
                member = call.args[0]
                call.func.value.id = member.id
                call.func.attr = 'edit'
                nick = call.args[1]
                call.args = []
                call.keywords = [ast.keyword(arg='nick', value=nick)]
        return call

    @staticmethod
    def stateful_pins_from(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'pins_from':
                dest = call.args[0]
                call.func.value.id = dest.id
                call.func.attr = 'pins'
                call.args = []
        return call

    @staticmethod
    def stateful_edit_role(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_role':
                to_edit = call.args[1]
                call.func.value.id = to_edit.id
                call.args = call.args[2:]
                call.func.attr = 'edit'
        return call

    @staticmethod
    def stateful_create_channel(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'create_channel':
                for kw in list(call.keywords):
                    if isinstance(kw.value, ast.Attribute):
                        channel_type = kw.value.attr
                        call.keywords.remove(kw)
                call.func.attr = f'create_{channel_type}_channel'
                guild = call.args[0].attr
                call.func.value.id = guild
        return call

    @staticmethod
    def stateful_edit_message(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_message':
                call.func.attr = 'edit'
                message = call.args[0]
                call.func.value.id = message.id
                content = call.args[1]
                call.args = call.args[2:]
                call.keywords.append(ast.keyword(arg='content', value=content))
        return call

    @staticmethod
    def stateful_edit_channel_perms(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_channel_permissions':
                call.func.attr = 'set_permissions'
                channel = call.args[0]
                call.func.value.id = channel.id
                overwrite = call.args[2]
                call.args = [call.args[1]]
                call.keywords.append(ast.keyword(arg='overwrite', value=overwrite))
        return call

    @staticmethod
    def stateful_leave_server(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'leave_guild':
                server = call.args[0].id
                call.func.value.id = server
                call.func.attr = 'leave'
                call.args = []
        return call

    @staticmethod
    def stateful_pin_message(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'pin_message':
                message = call.args[0].id
                call.func.value.id = message
                call.func.attr = 'pin'
                call.args = []
            elif call.func.attr == 'unpin_message':
                message = call.args[0].id
                call.func.value.id = message
                call.func.attr = 'unpin'
                call.args = []
        return call

    @staticmethod
    def stateful_get_bans(call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'get_bans':
                guild = call.args[0]
                call.func.value.id = guild.id
                call.func.attr = 'bans'
                call.args = []
        return call


class ExprTransforms:

    @staticmethod
    def stateful_get_all_emojis(expr):
        if not isinstance(expr.value, ast.Await):
            return expr
        if not isinstance(expr.value.value, ast.Call):
            return expr
        call = expr.value.value
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'get_all_emojis':
                new_expr = ast.Expr()
                new_expr.value = ast.Attribute()
                new_expr.value.value = ast.Name()
                new_expr.value.value.id = call.func.value.id
                new_expr.value.value.ctx = ast.Load()
                new_expr.value.attr = 'emojis'
                new_expr.value.ctx = ast.Load()

                new_expr = ast.copy_location(new_expr, expr)

                return new_expr
        return expr


class AttributeTransforms:

    @staticmethod
    def to_edited_at(attribute):
        if attribute.attr == 'edited_timestamp':
            attribute.attr = 'edited_at'

        return attribute


class CoroTransforms:

    @staticmethod
    def ext_event_changes(coro):
        if coro.name == 'on_command' or coro.name == 'on_command_completion':
            coro.args.args = coro.args.args[1:]
            return coro
        elif coro.name == 'on_command_error':
            coro.args.args.reverse()
            return coro

        return coro

    @staticmethod
    def ensure_ctx_var(coro):

        coro_args = [arg.arg for arg in coro.args.args]

        if not coro_args:
            coro.args.args.append(ast.arg(arg='ctx', annotation=None))
        elif 'self' in coro_args and 'ctx' not in coro_args:
            coro.args.args.insert(1, ast.arg(arg='ctx', annotation=None))
        elif 'self' not in coro_args and 'ctx' not in coro_args:
            coro.args.args.insert(0, ast.arg(arg='ctx', annotation=None))

        return coro


class DiscordTransformer(ast.NodeTransformer):

    def __init__(self):
        self.calltransforms = CallTransforms()
        self.exprtransforms = ExprTransforms()
        self.attributetransforms = AttributeTransforms()
        self.corotransforms = CoroTransforms()
        super().__init__()

    def visit_FormattedValue(self, node):
        self.generic_visit(node)

        return node

    def visit_Module(self, node):
        self.generic_visit(node)

        return node

    def visit_Expr(self, node):
        self.generic_visit(node)

        node = self.exprtransforms.stateful_get_all_emojis(node)

        return node

    def visit_Call(self, node):
        self.generic_visit(node)

        # this all has to do with the stateful model changes
        node = self.calltransforms.to_messageable(node)
        node = self.calltransforms.easy_statefuls(node)
        node = self.calltransforms.stateful_change_nickname(node)
        node = self.calltransforms.stateful_create_channel(node)
        node = self.calltransforms.easy_deletes(node)
        node = self.calltransforms.stateful_edit_message(node)
        node = self.calltransforms.easy_edits(node)
        node = self.calltransforms.stateful_edit_role(node)
        node = self.calltransforms.stateful_edit_channel_perms(node)
        node = self.calltransforms.stateful_leave_server(node)
        node = self.calltransforms.stateful_pin_message(node)
        node = self.calltransforms.stateful_get_bans(node)
        node = self.calltransforms.stateful_pins_from(node)

        return node

    def visit_arg(self, node):
        self.generic_visit(node)

        node.arg = node.arg.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)

        node = self.attributetransforms.to_edited_at(node)

        node.attr = node.attr.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Name(self, node):
        self.generic_visit(node)

        node.id = node.id.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Await(self, node):
        self.generic_visit(node)

        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)

        node = self.corotransforms.ext_event_changes(node)
        node = self.corotransforms.ensure_ctx_var(node)

        node.name = node.name.replace('server', 'guild').replace('Server', 'Guild')
        node = self.calltransforms.remove_passcontext(node)

        return node

    def visit_Assign(self, node):
        self.generic_visit(node)

        return node

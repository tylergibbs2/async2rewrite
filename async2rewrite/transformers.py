from collections import Counter
import warnings
import ast


easy_stateful_list = ['add_reaction', 'add_roles', 'ban', 'clear_reactions', 'create_invite', 'create_custom_emoji',
                      'create_role', 'kick', 'remove_reaction', 'remove_roles', 'prune_members', 'unban',
                      'get_message', 'estimate_pruned_members']

easy_deletes_list = ['delete_custom_emoji', 'delete_channel', 'delete_invite', 'delete_message', 'delete_role',
                     'delete_server']

easy_edits_list = ['edit_channel', 'edit_custom_emoji', 'edit_server']

stats_counter = Counter()


def prompt_change(msg: str):
    print('\n' + msg)
    result = input('> Make this change? (y/n) [y]: ')
    if result == 'n':
        return False

    return True


class DiscordTransformer(ast.NodeTransformer):
    def __init__(self, **kwargs):
        self.interactive = kwargs.pop('interactive', False)

        if self.interactive:
            print('Welcome to the async2rewrite interactive conversion process.\n\n'
                  'Make sure to read the migrating documentation to ensure that you '
                  'know what you\'re doing.\nLink: http://discordpy.readthedocs.io/en/rewrite/migrating.html\n\n'
                  'Please enter values for the possible found conversions (just press '
                  'Enter to accept a default value, if one is given in brackets).')

        super().__init__()

    def visit_FormattedValue(self, node):
        self.generic_visit(node)

        return node

    def visit_Module(self, node):
        self.generic_visit(node)

        return node

    def visit_Expr(self, node):
        self.generic_visit(node)

        node = self.stateful_get_all_emojis(node)
        node = self.attr_to_meth(node)

        return node

    def visit_Call(self, node):
        """Modify calls to their appropriate rewrite counterparts."""
        self.generic_visit(node)

        # this all has to do with the stateful model changes
        node = self.to_messageable(node)
        node = self.easy_statefuls(node)
        node = self.stateful_change_nickname(node)
        node = self.stateful_create_channel(node)
        node = self.easy_deletes(node)
        node = self.stateful_edit_message(node)
        node = self.easy_edits(node)
        node = self.stateful_edit_role(node)
        node = self.stateful_edit_channel_perms(node)
        node = self.stateful_leave_server(node)
        node = self.stateful_pin_message(node)
        node = self.stateful_get_bans(node)
        node = self.stateful_pins_from(node)
        node = self.stateful_send_typing(node)
        node = self.stateful_wait_for(node)
        node = self.to_tuple_to_to_rgb(node)
        node = self.channel_history(node)
        node = self.stateful_send_file(node)

        return node

    def visit_arg(self, node):
        self.generic_visit(node)

        if self.interactive:
            input()

        if 'server' in node.arg.lower():
            if self.interactive and not prompt_change(
                    'A possible change was found to change server to guild.'
            ):
                return node

        node.arg = node.arg.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Attribute(self, node):
        self.generic_visit(node)

        node = self.to_edited_at(node)

        if 'server' in node.attr.lower():
            if self.interactive and not prompt_change(
                    'A possible change was found to change server to guild.'
            ):
                return node

        node.attr = node.attr.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Name(self, node):
        self.generic_visit(node)

        if 'server' in node.id.lower():
            if self.interactive and not prompt_change(
                    'A possible change was found to change server to guild.'
            ):
                return node

        node.id = node.id.replace('server', 'guild').replace('Server', 'Guild')
        return node

    def visit_Await(self, node):
        self.generic_visit(node)

        return node

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)

        node = self.ext_event_changes(node)
        node = self.ensure_ctx_var(node)
        node = self.remove_passcontext(node)
        node = self.event_changes(node)

        if 'server' in node.name.lower():
            if self.interactive and not prompt_change(
                    'A possible change was found to change server to guild.'
            ):
                return node

        node.name = node.name.replace('server', 'guild').replace('Server', 'Guild')

        return node

    def visit_Assign(self, node):
        self.generic_visit(node)

        return node

    def ext_event_changes(self, coro):
        if coro.name == 'on_command' or coro.name == 'on_command_completion':
            if self.interactive and not prompt_change(
                'A possible change was found to remove the command argument from {}.'.format(coro.name)
            ):
                return coro

            coro.args.args = coro.args.args[1:]
            stats_counter['coro_changes'] += 1
            return coro
        elif coro.name == 'on_command_error':
            if self.interactive and not prompt_change(
                'A possible change was found to reverse the arguments on {}.'.format(coro.name)
            ):
                return coro

            coro.args.args.reverse()
            stats_counter['coro_changes'] += 1
            return coro

        return coro

    def event_changes(self, coro):
        if coro.name == 'on_voice_state_update':
            if self.interactive and not prompt_change(
                'A possible change was found to insert the member argument into {}.'.format(coro.name)
            ):
                return coro
            coro.args.args.insert(0, ast.arg(arg='member', annotation=None))
        elif coro.name in ['on_guild_emojis_update', 'on_member_ban']:
            if self.interactive and not prompt_change(
                'A possible change was found to insert the guild argument into {}.'.format(coro.name)
            ):
                return coro
            coro.args.args.insert(0, ast.arg(arg='guild', annotation=None))
        elif coro.name in ['on_channel_delete', 'on_channel_create', 'on_channel_update']:
            if self.interactive and not prompt_change(
                'A possible change was found to change {} to {}.'.format(
                    coro.name, coro.name.replace('on_channel', 'on_guild_channel'))
            ):
                return coro
            coro.name = coro.name.replace('on_channel', 'on_guild_channel')
        stats_counter['coro_changes'] += 1
        return coro

    def ensure_ctx_var(self, coro):

        d_list = []
        for d in coro.decorator_list:
            if isinstance(d, ast.Attribute):
                d_list.append(d.attr)
            elif isinstance(d, ast.Call):
                if isinstance(d.func, ast.Attribute):
                    d_list.append(d.func.attr)
        if 'command' not in d_list:
            return coro

        coro_args = [arg.arg for arg in coro.args.args]

        if not coro_args:
            if self.interactive and not prompt_change(
                'A possible change was found to insert the ctx into {}.'.format(coro.name)
            ):
                return coro
            coro.args.args.append(ast.arg(arg='ctx', annotation=None))
        elif 'self' in coro_args and 'ctx' not in coro_args:
            if self.interactive and not prompt_change(
                'A possible change was found to insert the ctx into {}.'.format(coro.name)
            ):
                return coro
            coro.args.args.insert(1, ast.arg(arg='ctx', annotation=None))
        elif 'self' not in coro_args and 'ctx' not in coro_args:
            if self.interactive and not prompt_change(
                'A possible change was found to insert the ctx into {}.'.format(coro.name)
            ):
                return coro
            coro.args.args.insert(0, ast.arg(arg='ctx', annotation=None))

        stats_counter['coro_changes'] += 1

        return coro

    def to_edited_at(self, attribute):
        if attribute.attr == 'edited_timestamp':
            if self.interactive and not prompt_change(
                'A possible change was found to change edited_timestamp to edited_at.'
            ):
                return attribute
            attribute.attr = 'edited_at'
            stats_counter['attribute_changes'] += 1

        return attribute

    def stateful_get_all_emojis(self, expr):
        if not isinstance(expr.value, ast.Await):
            return expr
        if not isinstance(expr.value.value, ast.Call):
            return expr
        call = expr.value.value
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'get_all_emojis':
                if self.interactive and not prompt_change(
                        'A possible change was found to make get_all_emojis stateful.'
                ):
                    return expr
                new_expr = ast.Expr()
                new_expr.value = ast.Attribute()
                new_expr.value.value = call.func.value
                new_expr.value.attr = 'emojis'
                new_expr.value.ctx = ast.Load()

                new_expr = ast.copy_location(new_expr, expr)

                stats_counter['expr_changes'] += 1
                return new_expr
        return expr

    def attr_to_meth(self, expr):
        if isinstance(expr.value, ast.Attribute):
            if expr.value.attr in ['is_ready', 'is_default', 'is_closed']:
                if self.interactive and not prompt_change(
                        'A possible change was found to change {} into a method.'.format(expr.value.attr)
                ):
                    return expr
                call = ast.Call()
                call.args = []
                call.keywords = []
                call.func = expr.value
                expr.value = call
                stats_counter['expr_changes'] += 1

        return expr

    def remove_passcontext(self, n):
        for d in n.decorator_list:
            if not isinstance(d, ast.Call):
                continue
            for kw in list(d.keywords):  # iterate over a copy of the list to avoid removing while iterating
                if not isinstance(kw.value, ast.NameConstant):
                    continue
                if kw.arg == 'pass_context':  # if the pass_context kwarg is set to True
                    if self.interactive and not prompt_change(
                            'A possible change was found to remove the pass_context decorator from {}.'.format(n.name)
                    ):
                        return n
                    d.keywords.remove(kw)
                    stats_counter['coro_changes'] += 1
        return n

    def to_messageable(self, call):
        if not isinstance(call.func, ast.Attribute):
            return call
        if call.func.attr == 'say':
            if self.interactive and not prompt_change(
                'A possible change was found to change say to send.'
            ):
                return call
            call.func.value = ast.Name(id='ctx', ctx=ast.Load())
            call.func.attr = 'send'
            stats_counter['call_changes'] += 1
        elif call.func.attr == 'send_message':
            if self.interactive and not prompt_change(
                'A possible change was found to change send_message to send.'
            ):
                return call
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
            stats_counter['call_changes'] += 1

            return newcall

        return call

    def easy_statefuls(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_stateful_list:
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                message = call.args[0]
                call.func.value = message
                call.args = call.args[1:]
                stats_counter['call_changes'] += 1
        return call

    def easy_deletes(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_deletes_list:
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                to_delete = call.args[0]
                call.func.value = to_delete
                call.args = call.args[1:]
                call.func.attr = 'delete'
                stats_counter['call_changes'] += 1
        return call

    def easy_edits(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in easy_edits_list:
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                to_edit = call.args[0]
                call.func.value = to_edit
                call.args = call.args[1:]
                call.func.attr = 'edit'
                stats_counter['call_changes'] += 1
        return call

    def stateful_send_file(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'send_file':
                if self.interactive and not prompt_change(
                        'A possible change was found to change send_file to send.'
                ):
                    return call
                dest = call.args[0]
                send_as = call.args[1]
                content = None
                filename = None
                for kw in list(call.keywords):
                    if kw.arg == 'filename':
                        filename = kw
                    if kw.arg == 'content':
                        content = kw
                if filename is None:
                    filename = ast.keyword(arg='filename', value=send_as)
                call.func.value = dest
                call.func.attr = 'send'
                call.args = []
                if content:
                    call.args.append(content.value)
                call.keywords = []
                file_kw = ast.keyword()
                file_kw.arg = 'file'
                discord_file_call = ast.Call()
                discord_file_call.func = ast.Attribute(value=ast.Name(id='discord', ctx=ast.Load()), attr='File',
                                                       ctx=ast.Load())
                discord_file_call.args = [send_as, filename.value]
                discord_file_call.keywords = []
                file_kw.value = discord_file_call
                call.keywords.append(file_kw)
                stats_counter['call_changes'] += 1

        return call

    def channel_history(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'logs_from':
                if self.interactive and not prompt_change(
                        'A possible change was found to change logs_from to history.'
                ):
                    return call
                dest = call.args[0]
                call.args = call.args[1:]
                if call.args:
                    limit = call.args[0]
                    call.keywords.append(ast.keyword(arg='limit', value=limit))
                    call.args = []
                call.func.value = dest
                call.func.attr = 'history'
                stats_counter['call_changes'] += 1
        return call

    def stateful_change_nickname(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'change_nickname':
                if self.interactive and not prompt_change(
                        'A possible change was found to make change_nickname into edit.'
                ):
                    return call
                member = call.args[0]
                call.func.value = member
                call.func.attr = 'edit'
                nick = call.args[1]
                call.args = []
                call.keywords = [ast.keyword(arg='nick', value=nick)]
                stats_counter['call_changes'] += 1
        return call

    def stateful_pins_from(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'pins_from':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                dest = call.args[0]
                call.func.value = dest
                call.func.attr = 'pins'
                call.args = []
                stats_counter['call_changes'] += 1
        return call

    def stateful_wait_for(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr in ['wait_for_message', 'wait_for_reaction']:
                if self.interactive and not prompt_change(
                        'A possible change was found to change {} into wait_for.'.format(call.func.attr)
                ):
                    return call
                event = call.func.attr.split('_')[2]
                event = 'message' if event == 'message' else 'reaction_add'
                call.func.attr = 'wait_for'
                if call.args:
                    timeout = call.args[0]
                    call.args = []
                    call.keywords.append(ast.keyword(arg='timeout', value=timeout))

                call.args.insert(0, ast.Str(s=event))
                for kw in list(call.keywords):
                    if kw.arg != 'check' and kw.arg != 'timeout':
                        call.keywords.remove(kw)
                warnings.warn('wait_for change detected. Rewrite removes the author, channel, and content '
                              'keyword arguments from this method.')
                stats_counter['call_changes'] += 1
        return call

    def stateful_edit_role(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_role':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                to_edit = call.args[1]
                call.func.value = to_edit
                call.args = call.args[2:]
                call.func.attr = 'edit'
                stats_counter['call_changes'] += 1
        return call

    def to_tuple_to_to_rgb(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'to_tuple':
                if self.interactive and not prompt_change(
                        'A possible change was found to change {} into to_rgb.'.format(call.func.attr)
                ):
                    return call
                call.func.attr = 'to_rgb'
                stats_counter['call_changes'] += 1

        return call

    def stateful_send_typing(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'send_typing':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                dest = call.args[0]
                call.func.value = dest
                call.args = call.args[1:]
                call.func.attr = 'trigger_typing'
                stats_counter['call_changes'] += 1
        return call

    def stateful_create_channel(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'create_channel':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                for kw in list(call.keywords):
                    if isinstance(kw.value, ast.Attribute):
                        channel_type = kw.value.attr
                        call.keywords.remove(kw)
                        break
                else:
                    channel_type = 'text'
                call.func.attr = 'create_{}_channel'.format(channel_type)
                guild = call.args[0]
                call.func.value = guild
                stats_counter['call_changes'] += 1
        return call

    def stateful_edit_message(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_message':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                call.func.attr = 'edit'
                message = call.args[0]
                call.func.value = message
                content = call.args[1]
                call.args = call.args[2:]
                call.keywords.append(ast.keyword(arg='content', value=content))
                stats_counter['call_changes'] += 1
        return call

    def stateful_edit_channel_perms(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'edit_channel_permissions':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                call.func.attr = 'set_permissions'
                channel = call.args[0]
                call.func.value = channel
                overwrite = call.args[2]
                call.args = [call.args[1]]
                call.keywords.append(ast.keyword(arg='overwrite', value=overwrite))
                stats_counter['call_changes'] += 1
        return call

    def stateful_leave_server(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'leave_guild':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                server = call.args[0]
                call.func.value = server
                call.func.attr = 'leave'
                call.args = []
                stats_counter['call_changes'] += 1
        return call

    def stateful_pin_message(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'pin_message':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                message = call.args[0]
                call.func.value = message
                call.func.attr = 'pin'
                call.args = []
            elif call.func.attr == 'unpin_message':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                message = call.args[0]
                call.func.value = message
                call.func.attr = 'unpin'
                call.args = []
                stats_counter['call_changes'] += 1
        return call

    def stateful_get_bans(self, call):
        if isinstance(call.func, ast.Attribute):
            if call.func.attr == 'get_bans':
                if self.interactive and not prompt_change(
                        'A possible change was found to make {} stateful.'.format(call.func.attr)
                ):
                    return call
                guild = call.args[0]
                call.func.value = guild
                call.func.attr = 'bans'
                call.args = []
                stats_counter['call_changes'] += 1
        return call


def find_stats(ast):
    DiscordTransformer().generic_visit(ast)
    return stats_counter

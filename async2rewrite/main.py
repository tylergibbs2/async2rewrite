import re
import os

import astunparse_noparen as astunparse

from .transformers import *


def get_result(code, **kwargs):
    stats = kwargs.pop('stats', False)
    include_ast = kwargs.pop('include_ast', False)

    def snowflake_repl(match):
        possible_snowflake = int(match.group(1))
        return str(possible_snowflake)

    code = re.sub(r"""['\"](\d{17,19})['\"]""", snowflake_repl,
                  code)  # str snowflakes to int snowflakes

    expr_ast = ast.parse(code)

    if stats:
        return find_stats(expr_ast)

    new_ast = DiscordTransformer().generic_visit(expr_ast)

    unparsed = astunparse.unparse(new_ast)

    unparsed = unparsed.replace('ctx.message.guild', 'ctx.guild').replace(
        'ctx.message.author', 'ctx.author')
    unparsed = unparsed.replace('ctx.message.channel', 'ctx.channel')

    final_ast = ast.parse(unparsed)

    if include_ast:
        return unparsed, final_ast
    return unparsed


def from_file(*files, **kwargs):
    res = {}

    def process_file(file):
        with open(file, 'r', encoding='utf-8') as f:
            res[file] = get_result(f.read(), **kwargs)

    for path in files:
        if path.endswith('.py'):  # it's a file
            process_file(path)
        else:  # it's a directory
            for dirpath, _, filenames in os.walk(path, followlinks=True):
                for file in filenames:
                    process_file('{}/{}'.format(dirpath, file))

    return res


def from_text(text, **kwargs):
    return get_result(text, **kwargs)

import re
import os

import astunparse_noparen as ast_unparse

from .transformers import *

# Detects 17-19 digit integers within quotes (snowflake detection)
snowflake_regex = re.compile(r"['\"](\d{17,19})['\"]")


def get_result(code, **kwargs):
    """Performs conversion of a given string of code.
    
    This attempts to parse async(str) snowflakes and convert them
    into rewrite(int) snowflakes, fix ordering for Messageables
    and converting to shorthands where available.
    """

    stats = kwargs.pop('stats', False)
    include_ast = kwargs.pop('include_ast', False)

    def snowflake_repl(match):
        # Cast the snowflake string into an integer
        # This should never fail, but this will raise in case it does.
        possible_snowflake = int(match.group(1))

        # Cast the snowflake back into a string (for substitution)
        return str(possible_snowflake)

    # Perform the substitution
    code = snowflake_regex.sub(snowflake_repl, code)

    expr_ast = ast.parse(code)

    if stats:
        return find_stats(expr_ast)

    # Instantiate a new transformer and start walking through
    # this syntax tree.
    new_ast = DiscordTransformer().generic_visit(expr_ast)

    unparsed = ast_unparse.unparse(new_ast)

    unparsed = unparsed.replace('ctx.message.guild', 'ctx.guild').replace(
        'ctx.message.author', 'ctx.author')
    unparsed = unparsed.replace('ctx.message.channel', 'ctx.channel')

    # This compiles our new code, ensuring that the syntax is valid
    # and allowing us to return the syntax tree if requested.
    final_ast = ast.parse(unparsed)

    if include_ast:
        return unparsed, final_ast
    return unparsed


def process_file(file, **kwargs):
    """Opens, reads and processes a file."""
    with open(file, 'r', encoding='utf-8') as f:
        return get_result(f.read(), **kwargs)


def from_file(*files, **kwargs):
    """Process a list of files or directories.
    
    Abstraction for get_result, returns batch results for a file or
    files in a given directory
    """
    res = {}

    for path in files:
        if path.endswith('.py'):
            # The user has passed a direct file, convert on its own.
            res[path] = process_file(path, **kwargs)
        else:
            # This is either a directory or a symlink, walk through and
            # modify any files we detect.
            for dir_path, _, file_names in os.walk(path, followlinks=True):
                for file in file_names:
                    file_path = '{}/{}'.format(dir_path, file)

                    if file_path.endswith('.py'):
                        # Only process python files
                        res[file_path] = process_file(file_path, **kwargs)

    return res


def from_text(text, **kwargs):
    """Frontend interface for processing raw text."""
    return get_result(text, **kwargs)

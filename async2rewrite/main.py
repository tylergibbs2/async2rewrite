import re
import astunparse

from transformers import *


class async2rewrite:

    def get_result(self, code):
        code = re.sub("""['\"](\d{17,18,19})['\"]""", self.snowflake_repl, code)  # str snowflakes to int snowflakes

        expr_ast = ast.parse(code)
        new_ast = DiscordTransformer().generic_visit(expr_ast)

        unparsed = astunparse.unparse(new_ast)

        unparsed = unparsed.replace('ctx.message.guild', 'ctx.guild').replace('ctx.message.author', 'ctx.author')
        unparsed = unparsed.replace('ctx.message.channel', 'ctx.channel')

        return unparsed

    @staticmethod
    def snowflake_repl(match):
        return str(int(match.group(1)))

    def from_file(self, file_path):
        with open(file_path, 'r') as f:
            code = f.read()
            return self.get_result(code)

    def from_text(self, text):
        return self.get_result(text)

file = async2rewrite().from_file('sample_code.py')
text = async2rewrite().from_text('async def on_command_error(error, ctx): pass')

print(text)
print(file)

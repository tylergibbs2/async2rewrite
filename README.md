# async2rewrite

[![PyPI](https://img.shields.io/pypi/v/async2rewrite.svg)](https://pypi.python.org/pypi/async2rewrite)

Automatically convert discord.py async branch code to rewrite branch code.

### Installation

```py
python3 -m pip install -U async2rewrite
```

### Usage

```py
import async2rewrite

file_result = async2rewrite.from_file('file/path')
print(file_result)

text_result = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
print(text_result)

result_without_parens = async2rewrite.from_file('file/path', remove_parens=True)
print(result_without_parens)

stats = async2rewrite.from_file('file/path', stats=True)
print(stats) # stats=True makes from_x return a Counter.
```

Note that the `remove_parens` kwarg can cause issues, and that it will not be perfect.
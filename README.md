# async2rewrite

[![PyPI](https://img.shields.io/pypi/v/async2rewrite.svg)](https://pypi.python.org/pypi/async2rewrite)

Automatically convert discord.py async branch code to rewrite branch code.

## Installation

```py
python3 -m pip install -U async2rewrite
```

### Usage

```py
import async2rewrite

result = async2rewrite.from_file('file/path')
print(result)

result2 = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
print(result2)

result_without_parens = async2rewrite.from_file('file/path', remove_parens=True)
print(result_without_parens)
```

Note that the `remove_parens` kwarg can cause issues, and that it will not be perfect.
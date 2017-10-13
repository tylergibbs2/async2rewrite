# async2rewrite

[![PyPI](https://img.shields.io/pypi/v/async2rewrite.svg)](https://pypi.python.org/pypi/async2rewrite)

Automatically convert discord.py async branch code to rewrite branch code.

## Installation

```py
python3 -m pip install -U async2rewrite
```

## Usage

### Converting a File
```py
import async2rewrite

file_result = async2rewrite.from_file('file/path')
print(file_result) # file_result contains the converted code.
```

### Converting from Text
```py
text_result = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
print(text_result) # text_result contains the converted code.
```

### Getting Statistics
```py
stats = async2rewrite.from_file('file/path', stats=True)
print(stats) # stats=True makes from_x return a collections Counter.
```

[Pantsu has generously forked and edited astunparse](https://github.com/nitros12/astunparse) to not insert parens in most places they are not needed. For example:

```py
>>> async2rewrite.from_text("async def test(): a = await (await (await b.c).d)[await a.b]")
"async def test(): a = await (await (await b.c).d)[await a.b]"
```

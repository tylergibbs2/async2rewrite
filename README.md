<p align="center">
    <img src="https://github.com/TheTrain2000/async2rewrite/blob/master/logo.png?raw=true" alt="async2rewrite">
</p>

[![PyPI](https://img.shields.io/pypi/v/async2rewrite.svg)](https://pypi.python.org/pypi/async2rewrite)

Automatically convert discord.py async branch code to rewrite branch code.

## Installation

```py
python -m pip install -U async2rewrite
```

## Usage

### Command Line

When converting files via the command line, async2rewrite will create a new Python
file with the specified suffix. If no suffix is specified, the default suffix is used.

For file paths, a path to a directory may also be passed. The library will locate all 
Python files recursively inside of the passed directory.

#### Single File

```
python -m async2rewrite file/path
```

#### Multiple Files

async2rewrite can automatically convert multiple files at once.

```
python -m async2rewrite file/path1 file/path2 ...
```

#### Specifying a Suffix

Use the `--suffix` flag to denote a custom suffix to add the the new file. 
The default suffix is `.a2r.py`.

Example:

```
python -m async2rewrite file/path --suffix '.my_suffix.py'
```

### Module

#### Converting a File
```py
import async2rewrite

file_result = async2rewrite.from_file('file/path')
print(file_result) # file_result contains the converted code.
```

Multiple files can be converted by passing an unpacked list into `from_file()`.

Example:

```py
async2rewrite.from_file('file/path', 'file/path2', 'file/path3', ...)
```

#### Converting from Text
```py
import async2rewrite

text_result = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
print(text_result) # text_result contains the converted code.
```

#### Getting Statistics
```py
import async2rewrite

stats = async2rewrite.from_file('file/path', stats=True)
print(stats) # stats=True makes from_x return a collections Counter.
```

---

[Pantsu has generously forked and edited astunparse](https://github.com/nitros12/astunparse) to not insert parens in most places they are not needed. For example:

```py
>>> import async2rewrite
>>> async2rewrite.from_text("async def test(): a = await (await (await b.c).d)[await a.b]")
"async def test(): a = await (await (await b.c).d)[await a.b]"
```

<sub>Reina thought of the logo idea so props to Reina, for real. I could not have thought of anything
 more imaginative or creative. I have no idea where this project would be without the creative lead of
 such an experienced individual. The agreed upon terms were that I would be allowed to design a logo using
 the exquisite creativity of Reina so long as I provide Reina with *exposure*. This paragraph here is the
 exposure that Reina so desires.</sub>
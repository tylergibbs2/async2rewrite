# async2rewrite

Automatically convert discord.py async branch code to rewrite branch code.

### Usage

```py
import async2rewrite

result = async2rewrite.Converter().from_file('file/path')
print(result)
result2 = async2rewrite.Converter().from_text('async def on_command_error(ctx, error): pass')
print(result2)
```
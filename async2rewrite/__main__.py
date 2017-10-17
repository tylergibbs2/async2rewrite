import argparse

from async2rewrite.main import from_file

parser = argparse.ArgumentParser(description='Automatically convert discord.py async branch code to rewrite.')

parser.add_argument('paths', type=str, nargs='+')
parser.add_argument('--suffix', dest='suffix', action='store', type=str, default='.a2r.py',
                    help='the suffix to use for file names when writing (default: \'.a2r.py\'')

results = parser.parse_args()

converted = from_file(*results.paths)

for key, value in converted.items():
    with open(key + results.suffix, 'w', encoding='utf-8') as f:
        f.write(value)

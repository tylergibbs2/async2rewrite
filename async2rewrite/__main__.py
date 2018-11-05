import os
import platform
import argparse
import difflib

from async2rewrite.main import from_file

parser = argparse.ArgumentParser(description='Automatically convert discord.py async branch code to rewrite.')

parser.add_argument('paths', type=str, nargs='*')
parser.add_argument('--suffix', dest='suffix', action='store', type=str, default='.a2r.py',
                    help='the suffix to use for file names when writing (default: \'.a2r.py\'')
parser.add_argument('--print', dest='print', action='store_true',
                    help='print the output instead of writing for a file (default: false)')
parser.add_argument('--diff', dest='diff', action='store_true',
                    help='create a diff file for every file converted (default: false)')
parser.add_argument('--gui', dest='gui', action='store_true',
                    help='launch the GUI extension of async2rewrite (default: true)')
parser.set_defaults(print=False, interactive=False, diff=False, gui=True)

results = parser.parse_args()

if not (results.print or results.diff):
    from application.launcher import setup
    setup()
else:
    results.gui = False

converted = from_file(*results.paths, interactive=results.interactive)
d = difflib.Differ()

for key, value in converted.items():
    if not results.print:
        with open(key + results.suffix, 'w', encoding='utf-8') as f:
            f.write(value)
    else:
        print('{}\n{}'.format(key + results.suffix, value))

    if results.diff:
        with open(key, 'r', encoding='utf-8') as f:
            original = f.readlines()
        with open(key + results.suffix, 'r', encoding='utf-8') as f:
            new = f.readlines()

        differences = d.compare(original, new)
        with open(key + '.diff', 'w', encoding='utf-8') as f:
            f.writelines(differences)

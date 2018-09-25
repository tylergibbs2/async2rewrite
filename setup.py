import os
from distutils.core import setup

# Thanks Laura
rootpath = os.path.abspath(os.path.dirname(__file__))


def extract_version(module='async2rewrite'):
    version = None
    fname = os.path.join(rootpath, module, '__init__.py')
    with open(fname) as f:
        for line in f:
            if line.startswith('__version__'):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters.
                break
    return version


version = extract_version()

setup(
    name='async2rewrite',
    packages=['async2rewrite'],
    version=version,
    description='Convert discord.py code using abstract syntax trees.',
    author='Tyler Gibbs',
    author_email='gibbstyler7@gmail.com',
    url='https://github.com/TheTrain2000/async2rewrite',
    download_url='https://github.com/TheTrain2000/async2rewrite/archive/{}.tar.gz'.format(version),
    keywords=['discord', 'discordpy', 'ast'],
    classifiers=[],
    install_requires=['astunparse-noparen>=1.5.6', 'yapf'],
    test_requires=['pytest', 'pytest-cov']
)

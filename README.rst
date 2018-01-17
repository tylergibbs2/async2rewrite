.. image:: https://github.com/TheTrain2000/async2rewrite/blob/master/logo.png?raw=true
    :align: center

.. image:: https://img.shields.io/pypi/v/async2rewrite.svg
    :target: https://pypi.python.org/pypi/async2rewrite

Automatically convert discord.py async branch code to rewrite branch code.

async2rewrite does not complete 100% of the necessary conversions. It is a tool designed to minimize the amount of
tedious work required. async2rewrite will warn upon changes that it cannot make itself. Make sure to read the migration
documentation for rewrite when using this tool.

`Migration Documentation`_

.. _Migration Documentation: https://discordpy.readthedocs.io/en/rewrite/migrating.html

Installation
------------

.. code:: sh

    python -m pip install -U async2rewrite

Usage
-----

Command Line
~~~~~~~~~~~~

When converting files via the command line, async2rewrite will create a new Python
file with the specified suffix. If no suffix is specified, the default suffix is used.

For file paths, a path to a directory may also be passed. The library will locate all 
Python files recursively inside of the passed directory.

Single File
^^^^^^^^^^^

.. code:: sh

    python -m async2rewrite file/path

Multiple Files
^^^^^^^^^^^^^^

async2rewrite can automatically convert multiple files at once.

.. code:: sh

    python -m async2rewrite file/path1 file/path2 ...

Specifying a Suffix
^^^^^^^^^^^^^^^^^^^

Use the ``--suffix`` flag to denote a custom suffix to add the the new file.
The default suffix is ``.a2r.py``.

Example:

.. code:: sh

    python -m async2rewrite file/path --suffix .my_suffix.py

Printing the Output
^^^^^^^^^^^^^^^^^^^

If you would like to print the output instead of writing to a new file,
the ``--print`` flag can be used.

Example:

.. code:: sh

    python -m async2rewrite file/path --print

Running Interactive Mode
^^^^^^^^^^^^^^^^^^^^^^^^

async2rewrite provides an option to convert using an interactive mode.
The interactive mode will prompt your before every change that it makes.

Example:

.. code:: sh

    python -m async2rewrite file/path --interactive

Module
~~~~~~

Converting a File
^^^^^^^^^^^^^^^^^

.. code:: py

    import async2rewrite

    file_result = async2rewrite.from_file('file/path')
    print(file_result) # file_result contains the converted code.

Multiple files can be converted by passing an unpacked list into ``from_file()``.

Example:

.. code:: py

    async2rewrite.from_file('file/path', 'file/path2', 'file/path3', ...)

Converting from Text
^^^^^^^^^^^^^^^^^^^^

.. code:: py

    import async2rewrite

    text_result = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
    print(text_result) # text_result contains the converted code.

Getting Statistics
^^^^^^^^^^^^^^^^^^

.. code:: py

    import async2rewrite

    stats = async2rewrite.from_file('file/path', stats=True)
    print(stats) # stats=True makes from_x return a collections Counter.

Thanks
------

* Pantsu for forking and editing `astunparse <https://github.com/nitros12/astunparse>`_ to not insert unnecessary parentheses.
* Reina for the logo idea
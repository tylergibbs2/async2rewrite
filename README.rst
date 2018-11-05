DEPRECATED
----------
It was fun while it lasted, everyone. async2rewrite will remain here as an archived repo. It will still be on pip (for
the time being), and it will still work for converting some of async to rewrite. This project will receive no more updates.

.. image:: https://github.com/TheTrain2000/async2rewrite/blob/master/logo.png?raw=true
    :align: center

.. image:: https://img.shields.io/pypi/v/async2rewrite.svg
    :target: https://pypi.python.org/pypi/async2rewrite
.. image:: https://img.shields.io/codecov/c/github/TheTrain2000/async2rewrite.svg
    :target: https://codecov.io/gh/TheTrain2000/async2rewrite

Automatically convert discord.py async branch code to rewrite branch code.

async2rewrite does not complete 100% of the necessary conversions. It is a tool designed to minimize the amount of
tedious work required. async2rewrite will warn upon changes that it cannot make itself. Make sure to read the migration
documentation for rewrite when using this tool.

`Migration Documentation`_
`Commercial 1`_

.. _Migration Documentation: https://discordpy.readthedocs.io/en/rewrite/migrating.html

.. _Commercial 1: https://youtu.be/R-ZLNU-MQL8

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

Module
~~~~~~

Converting a File
^^^^^^^^^^^^^^^^^

The ``from_file()`` method returns a dictionary. The dictionary keys are the file names,
and the values can either be a tuple or a string. If ``stats=True`` or ``include_ast=True``, then
``from_file()`` will return a tuple. The 0th index in the tuple will always be the converted code.

.. code:: py

    import async2rewrite

    file_result = async2rewrite.from_file('file/path')
    print(file_result['file/path'])  # file_result contains the converted code.

Multiple files can be converted by passing an unpacked list into ``from_file()``.

Example:

.. code:: py

    results = async2rewrite.from_file('file/path', 'file/path2', 'file/path3', ...)

    for converted_file in results:  # from_file() returns a dictionary.
        print(converted_file)  # Print out the result of each file.

Converting from Text
^^^^^^^^^^^^^^^^^^^^

.. code:: py

    import async2rewrite

    text_result = async2rewrite.from_text('async def on_command_error(ctx, error): pass')
    print(text_result)  # text_result contains the converted code.

Getting Statistics
^^^^^^^^^^^^^^^^^^

.. code:: py

    import async2rewrite

    stats = async2rewrite.from_file('file/path', stats=True)
    print(stats['file/path'])  # stats=True makes from_x return a collections Counter.

Thanks
------

* Pantsu for forking and editing `astunparse <https://github.com/nitros12/astunparse>`_ to not insert unnecessary parentheses.
* Reina for the logo idea
* Beta for making sweet commercials
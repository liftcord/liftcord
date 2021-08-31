.. image:: assets/liftcord-banner.png
   :alt: Liftcord

.. image:: https://discord.com/api/guilds/881118111967883295/embed.png
   :target: https://discord.gg/ZebatWssCB
   :alt: Discord server invite
.. image:: https://img.shields.io/pypi/v/nextcord.svg
   :target: https://pypi.python.org/pypi/nextcord
   :alt: PyPI version info
.. image:: https://img.shields.io/pypi/pyversions/nextcord.svg
   :target: https://pypi.python.org/pypi/nextcord
   :alt: PyPI supported Python versions

Liftcord is a modern, easy to use, feature-rich, and async ready API wrapper for Discord written in Python.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library without full voice support, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U nextcord

    # Windows
    py -3 -m pip install -U nextcord

Otherwise to get voice support you should run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U "nextcord[voice]"

    # Windows
    py -3 -m pip install -U nextcord[voice]


To install the development version, do the following:

.. code:: sh

    $ git clone https://github.com/nextcord/nextcord/
    $ cd nextcord
    $ python3 -m pip install -U .[voice]


Optional Packages
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (for voice support)

Please note that on Linux installing voice you must install the following packages via your favourite package manager (e.g. ``apt``, ``dnf``, etc) before running the above commands:

* libffi-dev (or ``libffi-devel`` on some systems)
* python-dev (e.g. ``python3.6-dev`` for Python 3.6)


Quick Example
~~~~~~~~~~~~~

.. code:: py

    from liftcord.ext import commands


    bot = commands.Bot(command_prefix='&')

    @bot.command()
    async def say_it(ctx):
        await ctx.reply('Liftcord!')

    bot.run('TOKEN')


You can find more examples in the examples directory.

**NOTE:** It is not advised to leave your TOKEN directly in your code, as it allows anyone with it to access your bot. If you intend to make your code public you should `store it securely <https://github.com/nextcord/nextcord/blob/master/examples/secure_token_storage.py/>`_.

Links
------

- `Documentation <https://liftcord.readthedocs.io/en/latest/>`_
- `Official Discord Server <https://discord.gg/------->`_
- `Discord API <https://discord.gg/discord-api>`_

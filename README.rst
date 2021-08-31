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

Liftcord это современная, простая в использовании, многофункциональная и асинхронная готовая оболочка API для Discord, написанная на Python.

Ключевые особенности
-------------

- Современное Python использование ``async`` и ``await``.
- Proper rate limit handling.
- Optimised in both speed and memory.

Установка
----------

**Python 3.8 или выше обязательно**

Чтобы установить библиотеку без полной голосовой поддержки, вы можете просто выполнить одну из следующих команд:

.. code:: sh

    # Windows
    py -3 -m pip install -U nextcord
    pip install -U nextcord

    # Linux/macOS
    python3 -m pip install -U nextcord

В противном случае, чтобы получить голосовую поддержку, вам следует выполнить следующую команду:

.. code:: sh

    # Windows
    py -3 -m pip install -U nextcord[voice]
    pip install -U nextcord[voice]

    # Linux/macOS
    python3 -m pip install -U "nextcord[voice]"


Чтобы установить разрабатываемую версию делайте следующее:

.. code:: sh

    $ git clone https://github.com/liftcord/liftcord/
    $ cd liftcord
    $ python3 -m pip install -U .[voice]


Необязательные библиотеки
~~~~~~~~~~~~~~~~~~

* `PyNaCl <https://pypi.org/project/PyNaCl/>`__ (для голосовой поддержки)

Пожалуйста, обратите внимание, что при установке голосовой связи в Linux вы должны установить следующие пакеты через ваш любимый менеджер пакетов (например, `apt`, `dnf` и т.д.) Перед выполнением вышеуказанных команд:

* libffi-dev (или ``libffi-devel`` на некоторых системах)
* python-dev (например: ``python3.6-dev`` для Python 3.6)


Быстрый пример
~~~~~~~~~~~~~

.. code:: py

    from liftcord.ext import commands


    bot = commands.Bot(command_prefix='&')

    @bot.command()
    async def say_it(ctx):
        await ctx.reply('Liftcord!')

    bot.run('TOKEN')


Вы можете найти больше примеров в директории примеров.

**ПРИМЕЧАНИЕ:** Не рекомендуется оставлять свой ТОКЕН непосредственно в коде, так как это позволяет любому, у кого он есть, получить доступ к вашему боту. Если вы намерены сделать свой код общедоступным, " вы должны надежно хранить его <https://github.com/liftcord/liftcord/blob/master/examples/secure_token_storage.py/>`_.

Ссылки
------

- `Документация <https://liftcord.readthedocs.io/en/latest/>`_
- `Официальный Дискорд сервер <https://discord.gg/------->`_
- `Discord API <https://discord.gg/discord-api>`_

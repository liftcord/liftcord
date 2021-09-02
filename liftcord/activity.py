"""
The MIT License (MIT)

Copyright (c) 2021 xXSergeyXx

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.

----------------------------------------------------------------------

Авторские права (c) 2021 xXSergeyXx

Данная лицензия разрешает лицам, получившим копию данного программного
обеспечения и сопутствующей документации (в дальнейшем именуемыми «Программное обеспечение»), 
безвозмездно использовать Программное обеспечение без ограничений, включая неограниченное 
право на использование, копирование, изменение, слияние, публикацию, распространение, 
сублицензирование и/или продажу копий Программного обеспечения, а также лицам, которым 
предоставляется данное Программное обеспечение, при соблюдении следующих условий:

Указанное выше уведомление об авторском праве и данные условия должны быть включены во 
все копии или значимые части данного Программного обеспечения.

ДАННОЕ ПРОГРАММНОЕ ОБЕСПЕЧЕНИЕ ПРЕДОСТАВЛЯЕТСЯ «КАК ЕСТЬ», БЕЗ КАКИХ-ЛИБО ГАРАНТИЙ, ЯВНО ВЫРАЖЕННЫХ 
ИЛИ ПОДРАЗУМЕВАЕМЫХ, ВКЛЮЧАЯ ГАРАНТИИ ТОВАРНОЙ ПРИГОДНОСТИ, СООТВЕТСТВИЯ ПО ЕГО КОНКРЕТНОМУ 
НАЗНАЧЕНИЮ И ОТСУТСТВИЯ НАРУШЕНИЙ, НО НЕ ОГРАНИЧИВАЯСЬ ИМИ. НИ В КАКОМ СЛУЧАЕ АВТОРЫ ИЛИ ПРАВООБЛАДАТЕЛИ 
НЕ НЕСУТ ОТВЕТСТВЕННОСТИ ПО КАКИМ-ЛИБО ИСКАМ, ЗА УЩЕРБ ИЛИ ПО ИНЫМ ТРЕБОВАНИЯМ, В ТОМ ЧИСЛЕ, ПРИ 
ДЕЙСТВИИ КОНТРАКТА, ДЕЛИКТЕ ИЛИ ИНОЙ СИТУАЦИИ, ВОЗНИКШИМ ИЗ-ЗА ИСПОЛЬЗОВАНИЯ ПРОГРАММНОГО 
ОБЕСПЕЧЕНИЯ ИЛИ ИНЫХ ДЕЙСТВИЙ С ПРОГРАММНЫМ ОБЕСПЕЧЕНИЕМ.
"""

from __future__ import annotations

import datetime
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union, overload

from .asset import Asset
from .enums import ActivityType, try_enum
from .colour import Colour
from .partial_emoji import PartialEmoji
from .utils import _get_as_snowflake

__all__ = (
    'BaseActivity',
    'Activity',
    'Streaming',
    'Game',
    'Spotify',
    'CustomActivity',
)

"""Если вам интересно, это текущая схема для действия.

Это довольно долго, поэтому я задокументирую это здесь:

Все ключи являются необязательными.

state: str (max: 128),
details: str (max: 128)
timestamps: dict
    start: int (min: 1)
    end: int (min: 1)
assets: dict
    large_image: str (max: 32)
    large_text: str (max: 128)
    small_image: str (max: 32)
    small_text: str (max: 128)
party: dict
    id: str (max: 128),
    size: List[int] (max-length: 2)
        elem: int (min: 1)
secrets: dict
    match: str (max: 128)
    join: str (max: 128)
    spectate: str (max: 128)
instance: bool
application_id: str
name: str (max: 128)
url: str
type: int
sync_id: str
session_id: str
flags: int
buttons: list[dict]
    label: str (max: 32)
    url: str (max: 512)

Существуют также флаги активности, которые в основном неинтересны для библиотечного использования.

t.ActivityFlags = {
    INSTANCE: 1,
    JOIN: 2,
    SPECTATE: 4,
    JOIN_REQUEST: 8,
    SYNC: 16,
    PLAY: 32
}
"""

if TYPE_CHECKING:
    from .types.activity import (
        Activity as ActivityPayload,
        ActivityTimestamps,
        ActivityParty,
        ActivityAssets,
        ActivityButton,
    )


class BaseActivity:
    """Базовое действие, от которого наследуются все настраиваемые пользователем действия.
    Настраиваемое пользователем действие-это действие, которое можно использовать в :meth:`Client.change_presence`.

    Следующие типы в настоящее время считаются настраиваемыми пользователем:

    - :class:`Activity`
    - :class:`Game`
    - :class:`Streaming`
    - :class:`CustomActivity`

    Обратите внимание, что, хотя эти типы считаются настраиваемыми пользователем библиотекой,
    Discord обычно игнорирует определенные комбинации действий в зависимости от того,
    что установлено в данный момент. Это поведение может измениться в будущем, поэтому нет
    никаких гарантий того, что Discord действительно позволит вам устанавливать эти типы.
    .. versionadded:: 1.0.2
    """

    __slots__ = ('_created_at',)

    def __init__(self, **kwargs):
        self._created_at: Optional[float] = kwargs.pop('created_at', None)

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Сообщает о том когда пользователь поставил данную активность.

        .. versionadded:: 1.0.2
        """
        if self._created_at is not None:
            return datetime.datetime.fromtimestamp(self._created_at / 1000, tz=datetime.timezone.utc)

    def to_dict(self) -> ActivityPayload:
        raise NotImplementedError


class Activity(BaseActivity):
    """Представляет собой деятельность в Discord.

    Это может быть такая деятельность, как стриминг, игра, прослушивание
    или просмотр.

    В целях оптимизации памяти некоторые виды деятельности предлагаются в уменьшенном
    нижние версии:

    - :class:`Game`
    - :class:`Streaming`

    Аттрибуты
    ------------
    application_id: Необязательно[:class:`int`]
        ID приложения игры.
    name: Необязательно[:class:`str`]
        Название Активности.
    url: Необязательно[:class:`str`]
        URL-адрес трансляции, который может выполнять Активность.
    type: :class:`ActivityType`
        Вид активности, осуществляемой в настоящее время.
    state: Необязательно[:class:`str`]
        Текущее состояние пользователя. Например, "В игре".
    details: Необязательно[:class:`str`]
        Подробная информация о текущей Активности пользователя.
    timestamps: :class:`dict`
        Словарь временных меток. Он содержит следующие дополнительные ключи:

        - ``start``: Соответствует моменту, когда пользователь начал выполнять
        действия в миллисекундах с эпохи Unix.
        - ``end``: Соответствует моменту, когда пользователь завершит выполнение
        действия в миллисекундах с эпохи Unix.

    assets: :class:`dict`
        Словарь, представляющий изображения и их текст при наведении курсора на Активность.
        Он содержит следующие дополнительные ключи:

        - ``large_image``: строка, представляющая идентификатор ресурса большого изображения.
        - ``large_text`: строка, представляющая текст при наведении указателя мыши на ресурс большого изображения.
        - ``small_image``: строка, представляющая идентификатор ресурса небольшого изображения.
        - ``small_text``: строка, представляющая текст при наведении указателя мыши на небольшое изображение.

    party: :class:`dict`
        Словарь, представляющий мероприятие Активности. Он содержит следующие необязательные ключи:

        - ``id``: строка, представляющая идентификатор участника мероприятия.
        - ``size``: список до двух целых элементов, обозначающих (current_size, maximum_size).

    buttons: List[:class:`dict`]
        Список словарей, представляющих пользовательские кнопки, отображается в расширенном виде.
        Каждый словарь содержит следующие ключи:

        - ``label``: строка, представляющая текст, отображаемый на кнопке.
        - ``url``: строка, представляющая URL-адрес, открытый при нажатии на кнопку.

        .. versionadded:: 1.0.2

    emoji: Необязательно[:class:`PartialEmoji`]
        Эмодзи который пренадлежит этой Активности.
    """

    __slots__ = (
        'state',
        'details',
        '_created_at',
        'timestamps',
        'assets',
        'party',
        'flags',
        'sync_id',
        'session_id',
        'type',
        'name',
        'url',
        'application_id',
        'emoji',
        'buttons',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.state: Optional[str] = kwargs.pop('state', None)
        self.details: Optional[str] = kwargs.pop('details', None)
        self.timestamps: ActivityTimestamps = kwargs.pop('timestamps', {})
        self.assets: ActivityAssets = kwargs.pop('assets', {})
        self.party: ActivityParty = kwargs.pop('party', {})
        self.application_id: Optional[int] = _get_as_snowflake(kwargs, 'application_id')
        self.name: Optional[str] = kwargs.pop('name', None)
        self.url: Optional[str] = kwargs.pop('url', None)
        self.flags: int = kwargs.pop('flags', 0)
        self.sync_id: Optional[str] = kwargs.pop('sync_id', None)
        self.session_id: Optional[str] = kwargs.pop('session_id', None)
        self.buttons: List[ActivityButton] = kwargs.pop('buttons', [])

        activity_type = kwargs.pop('type', -1)
        self.type: ActivityType = (
            activity_type if isinstance(activity_type, ActivityType) else try_enum(ActivityType, activity_type)
        )

        emoji = kwargs.pop('emoji', None)
        self.emoji: Optional[PartialEmoji] = PartialEmoji.from_dict(emoji) if emoji is not None else None

    def __repr__(self) -> str:
        attrs = (
            ('type', self.type),
            ('name', self.name),
            ('url', self.url),
            ('details', self.details),
            ('application_id', self.application_id),
            ('session_id', self.session_id),
            ('emoji', self.emoji),
        )
        inner = ' '.join('%s=%r' % t for t in attrs)
        return f'<Activity {inner}>'

    def to_dict(self) -> Dict[str, Any]:
        ret: Dict[str, Any] = {}
        for attr in self.__slots__:
            value = getattr(self, attr, None)
            if value is None:
                continue

            if isinstance(value, dict) and len(value) == 0:
                continue

            ret[attr] = value
        ret['type'] = int(self.type)
        if self.emoji:
            ret['emoji'] = self.emoji.to_dict()
        return ret

    @property
    def start(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Когда пользователь начал выполнять эту Активность в UTC, если применимо."""
        try:
            timestamp = self.timestamps['start'] / 1000
        except KeyError:
            return None
        else:
            return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    @property
    def end(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Когда пользователь закончит выполнять эту Активность в UTC, если применимо."""
        try:
            timestamp = self.timestamps['end'] / 1000
        except KeyError:
            return None
        else:
            return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc)

    @property
    def large_image_url(self) -> Optional[str]:
        """Необязательно[:class:`str`]: Возвращает URL-адрес, указывающий на ресурс большого изображения этой Активности, если применимо."""
        if self.application_id is None:
            return None

        try:
            large_image = self.assets['large_image']
        except KeyError:
            return None
        else:
            return Asset.BASE + f'/app-assets/{self.application_id}/{large_image}.png'

    @property
    def small_image_url(self) -> Optional[str]:
        """Необязательно[:class:`str`]: Возвращает URL-адрес, указывающий на ресурс маленького изображения этой Активности, если применимо."""
        if self.application_id is None:
            return None

        try:
            small_image = self.assets['small_image']
        except KeyError:
            return None
        else:
            return Asset.BASE + f'/app-assets/{self.application_id}/{small_image}.png'

    @property
    def large_image_text(self) -> Optional[str]:
        """Необязательно[:class:`str`]: Возвращает текст наведения курсора на большое изображение этой Активности, если применимо."""
        return self.assets.get('large_text', None)

    @property
    def small_image_text(self) -> Optional[str]:
        """Необязательно[:class:`str`]: Возвращает текст наведения курсора на маленькое изображение этой Активности, если применимо."""
        return self.assets.get('small_text', None)


class Game(BaseActivity):
    """Уменьшенная версия :class:`Activity`, которая представляет собой игру в Discord.

    Обычно это отображается через **Играет** на официальном клиенте Discord.

    .. container:: operations

        .. describe:: x == y

            Проверяет эквивалентны ли две игры друг другу.

        .. describe:: x != y

            Проверяет не эквивалентны ли две игры друг другу.


        .. describe:: hash(x)

            Возвращает хэш игры.

        .. describe:: str(x)

            Возвращает название игры

    Параметры
    -----------
    name: :class:`str`
        Название игры.

    Аттрибуты
    -----------
    name: :class:`str`
        Название игры.
    """

    __slots__ = ('name', '_end', '_start')

    def __init__(self, name: str, **extra):
        super().__init__(**extra)
        self.name: str = name

        try:
            timestamps: ActivityTimestamps = extra['timestamps']
        except KeyError:
            self._start = 0
            self._end = 0
        else:
            self._start = timestamps.get('start', 0)
            self._end = timestamps.get('end', 0)

    @property
    def type(self) -> ActivityType:
        """:class:`ActivityType`: Возвращает тип игры. Для совместимости с :class:`Activity`.

        Всегда возращает :attr:`ActivityType.playing`.
        """
        return ActivityType.playing

    @property
    def start(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Когда пользователь начал играть в эту Игру в UTC, если применимо."""
        if self._start:
            return datetime.datetime.fromtimestamp(self._start / 1000, tz=datetime.timezone.utc)
        return None

    @property
    def end(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Когда пользователь закончил играть в эту Игру в UTC, если применимо."""
        if self._end:
            return datetime.datetime.fromtimestamp(self._end / 1000, tz=datetime.timezone.utc)
        return None

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Game name={self.name!r}>'

    def to_dict(self) -> Dict[str, Any]:
        timestamps: Dict[str, Any] = {}
        if self._start:
            timestamps['start'] = self._start

        if self._end:
            timestamps['end'] = self._end

        # fmt: off
        return {
            'type': ActivityType.playing.value,
            'name': str(self.name),
            'timestamps': timestamps
        }
        # fmt: on

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Game) and other.name == self.name

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.name)


class Streaming(BaseActivity):
    """Уменьшенная версия :class:`Activity`, представляющая статус трансляции Discord.

    Обычно это отображается с помощью **Стримит** на официальном клиенте Discord.

    .. container:: operations

        .. describe:: x == y

            Проверяет эквивалентны ли две трансляции друг другу.

        .. describe:: x != y

            Проверяет не эквивалентны ли две трансляции друг другу.

        .. describe:: hash(x)

            Возвращает хэш трансляции.

        .. describe:: str(x)

            Возвращает название трансляции.

    Attributes
    -----------
    platform: Необязательно[:class:`str`]
        Платформа с которой стримит пользователь (т.е. YouTube, Twitch).

        .. versionadded:: 1.0.2

    name: Необязательно[:class:`str`]
        Название трансляции.
    details: Необязательно[:class:`str`]
        Псевдоним для :attr:`name`.
    game: Необязательно[:class:`str`]
        Игра которая транслируется.

        .. versionadded:: 1.0.2

    url: :class:`str`
        URL-адрес трансляции.
    assets: :class:`dict`
        Словарь содержащие ключи аналогичные ключам в :attr:`Activity.assets`.
    """

    __slots__ = ('platform', 'name', 'game', 'url', 'details', 'assets')

    def __init__(self, *, name: Optional[str], url: str, **extra: Any):
        super().__init__(**extra)
        self.platform: Optional[str] = name
        self.name: Optional[str] = extra.pop('details', name)
        self.game: Optional[str] = extra.pop('state', None)
        self.url: str = url
        self.details: Optional[str] = extra.pop('details', self.name)  # compatibility
        self.assets: ActivityAssets = extra.pop('assets', {})

    @property
    def type(self) -> ActivityType:
        """:class:`ActivityType`: Возвращает тип трансляции. Для совместимости с :class:`Activity`.

        Всегда возращает :attr:`ActivityType.streaming`.
        """
        return ActivityType.streaming

    def __str__(self) -> str:
        return str(self.name)

    def __repr__(self) -> str:
        return f'<Streaming name={self.name!r}>'

    @property
    def twitch_name(self):
        """Необязательно[:class:`str`]: Если указано, имя пользователя twitch для трансляции.

        Это соответствует ключу ``large_image`` в :attr:`Streaming.assets`
        словаре, если он начинается с ``twitch:``. Обычно устанавливается клиентом Discord.
        """

        try:
            name = self.assets['large_image']
        except KeyError:
            return None
        else:
            return name[7:] if name[:7] == 'twitch:' else None

    def to_dict(self) -> Dict[str, Any]:
        # fmt: off
        ret: Dict[str, Any] = {
            'type': ActivityType.streaming.value,
            'name': str(self.name),
            'url': str(self.url),
            'assets': self.assets
        }
        # fmt: on
        if self.details:
            ret['details'] = self.details
        return ret

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Streaming) and other.name == self.name and other.url == self.url

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.name)


class Spotify:
    """Представляет Активность прослушивания Spotify от Discord. Это особый случай
    :class:`Activity`, что облегчает работу с интеграцией Spotify.

    .. container:: operations

        .. describe:: x == y

            Проверяет эквивалентны ли две Активности друг другу.

        .. describe:: x != y

            Проверяет не эквивалентны ли две Активности друг другу.


        .. describe:: hash(x)

            Возвращает хэш Активности

        .. describe:: str(x)

            Возвращает строку 'Spotify'.
    """

    __slots__ = ('_state', '_details', '_timestamps', '_assets', '_party', '_sync_id', '_session_id', '_created_at')

    def __init__(self, **data):
        self._state: str = data.pop('state', '')
        self._details: str = data.pop('details', '')
        self._timestamps: Dict[str, int] = data.pop('timestamps', {})
        self._assets: ActivityAssets = data.pop('assets', {})
        self._party: ActivityParty = data.pop('party', {})
        self._sync_id: str = data.pop('sync_id')
        self._session_id: str = data.pop('session_id')
        self._created_at: Optional[float] = data.pop('created_at', None)

    @property
    def type(self) -> ActivityType:
        """:class:`ActivityType`: Возвращает тип Активности. Для совместимости с :class:`Activity`.

        Всегда возращает :attr:`ActivityType.listening`.
        """
        return ActivityType.listening

    @property
    def created_at(self) -> Optional[datetime.datetime]:
        """Необязательно[:class:`datetime.datetime`]: Когда пользователь начал слушать в UTC.

        .. versionadded:: 1.0.2
        """
        if self._created_at is not None:
            return datetime.datetime.fromtimestamp(self._created_at / 1000, tz=datetime.timezone.utc)

    @property
    def colour(self) -> Colour:
        """:class:`Colour`: Возвращает интегрированый цвет Spotify, в виде :class:`Colour`.

        Это псевдоним для :attr:`color`"""
        return Colour(0x1DB954)

    @property
    def color(self) -> Colour:
        """:class:`Colour`: Возвращает интегрированый цвет Spotify, в виде :class:`Colour`.

        Это псевдоним для :attr:`colour`"""
        return self.colour

    def to_dict(self) -> Dict[str, Any]:
        return {
            'flags': 48,  # SYNC | PLAY
            'name': 'Spotify',
            'assets': self._assets,
            'party': self._party,
            'sync_id': self._sync_id,
            'session_id': self._session_id,
            'timestamps': self._timestamps,
            'details': self._details,
            'state': self._state,
        }

    @property
    def name(self) -> str:
        """:class:`str`: Название Активности. Всегда возвращает "Spotify"."""
        return 'Spotify'

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, Spotify)
            and other._session_id == self._session_id
            and other._sync_id == self._sync_id
            and other.start == self.start
        )

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self._session_id)

    def __str__(self) -> str:
        return 'Spotify'

    def __repr__(self) -> str:
        return f'<Spotify title={self.title!r} artist={self.artist!r} track_id={self.track_id!r}>'

    @property
    def title(self) -> str:
        """:class:`str`: Название исполняемой песни."""
        return self._details

    @property
    def artists(self) -> List[str]:
        """List[:class:`str`]: Исполнители данной песни"""
        return self._state.split('; ')

    @property
    def artist(self) -> str:
        """:class:`str`: Исполнитель данной песни.

        Это не попытка разделить информацию об исполнителе на
        несколько исполнителей. Полезно, если есть только один исполнитель.
        """
        return self._state

    @property
    def album(self) -> str:
        """:class:`str`: Альбом, которому пренадлежит воспроизводящаяся песня"""
        return self._assets.get('large_text', '')

    @property
    def album_cover_url(self) -> str:
        """:class:`str`: URL-адрес изображения обложки альбома с CDN Spotify."""
        large_image = self._assets.get('large_image', '')
        if large_image[:8] != 'spotify:':
            return ''
        album_image_id = large_image[8:]
        return 'https://i.scdn.co/image/' + album_image_id

    @property
    def track_id(self) -> str:
        """:class:`str`: ID трека, используемый Spotify для идентификации этой песни."""
        return self._sync_id

    @property
    def track_url(self) -> str:
        """:class:`str`: URL-адрес трека для прослушивания на Spotify.

        .. versionadded:: 1.0.2
        """
        return f'https://open.spotify.com/track/{self.track_id}'

    @property
    def start(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Когда пользователь начал прослушивать эту песню в UTC"""
        return datetime.datetime.fromtimestamp(self._timestamps['start'] / 1000, tz=datetime.timezone.utc)

    @property
    def end(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Когда пользователь закончит прослушивать эту песню в UTC"""
        return datetime.datetime.fromtimestamp(self._timestamps['end'] / 1000, tz=datetime.timezone.utc)

    @property
    def duration(self) -> datetime.timedelta:
        """:class:`datetime.timedelta`: Продолжительность воспроизводимой песни."""
        return self.end - self.start

    @property
    def party_id(self) -> str:
        """:class:`str`: ID вечеринки участника вечеринки прослушивания."""
        return self._party.get('id', '')


class CustomActivity(BaseActivity):
    """Представляет собственную Активность из Discord.

    .. container:: operations

        .. describe:: x == y

            Проверяет эквивалентны ли две Активности друг другу.

        .. describe:: x != y

            Проверяет не эквивалентны ли две Активности друг другу.

        .. describe:: hash(x)

            Возвращает хэш Активности.

        .. describe:: str(x)

            Возвращает собственный текст статуса.

    .. versionadded:: 1.0.2

    Аттрибуты
    -----------
    name: Необязательно[:class:`str`]
        Название Активности.
    emoji: Необязательно[:class:`PartialEmoji`]
        Смайлик для перехода к Активности, если таковой имеется.
    """

    __slots__ = ('name', 'emoji', 'state')

    def __init__(self, name: Optional[str], *, emoji: Optional[PartialEmoji] = None, **extra: Any):
        super().__init__(**extra)
        self.name: Optional[str] = name
        self.state: Optional[str] = extra.pop('state', None)
        if self.name == 'Custom Status':
            self.name = self.state

        self.emoji: Optional[PartialEmoji]
        if emoji is None:
            self.emoji = emoji
        elif isinstance(emoji, dict):
            self.emoji = PartialEmoji.from_dict(emoji)
        elif isinstance(emoji, str):
            self.emoji = PartialEmoji(name=emoji)
        elif isinstance(emoji, PartialEmoji):
            self.emoji = emoji
        else:
            raise TypeError(f'Ожидалось str, PartialEmoji, или None, получено {type(emoji)!r} вместо этого.')

    @property
    def type(self) -> ActivityType:
        """:class:`ActivityType`: Возвращает тип Активности. Для совместимости с :class:`Activity`.

        Всегда возвращает :attr:`ActivityType.custom`.
        """
        return ActivityType.custom

    def to_dict(self) -> Dict[str, Any]:
        if self.name == self.state:
            o = {
                'type': ActivityType.custom.value,
                'state': self.name,
                'name': 'Custom Status',
            }
        else:
            o = {
                'type': ActivityType.custom.value,
                'name': self.name,
            }

        if self.emoji:
            o['emoji'] = self.emoji.to_dict()
        return o

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, CustomActivity) and other.name == self.name and other.emoji == self.emoji

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.name, str(self.emoji)))

    def __str__(self) -> str:
        if self.emoji:
            if self.name:
                return f'{self.emoji} {self.name}'
            return str(self.emoji)
        else:
            return str(self.name)

    def __repr__(self) -> str:
        return f'<CustomActivity name={self.name!r} emoji={self.emoji!r}>'


ActivityTypes = Union[Activity, Game, CustomActivity, Streaming, Spotify]

@overload
def create_activity(data: ActivityPayload) -> ActivityTypes:
    ...

@overload
def create_activity(data: None) -> None:
    ...

def create_activity(data: Optional[ActivityPayload]) -> Optional[ActivityTypes]:
    if not data:
        return None

    game_type = try_enum(ActivityType, data.get('type', -1))
    if game_type is ActivityType.playing:
        if 'application_id' in data or 'session_id' in data:
            return Activity(**data)
        return Game(**data)
    elif game_type is ActivityType.custom:
        try:
            name = data.pop('name')
        except KeyError:
            return Activity(**data)
        else:
            # we removed the name key from data already
            return CustomActivity(name=name, **data) # type: ignore
    elif game_type is ActivityType.streaming:
        if 'url' in data:
            # the url won't be None here
            return Streaming(**data) # type: ignore
        return Activity(**data)
    elif game_type is ActivityType.listening and 'sync_id' in data and 'session_id' in data:
        return Spotify(**data)
    return Activity(**data)

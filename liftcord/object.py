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

from . import utils
from .mixins import Hashable

from typing import (
    SupportsInt,
    TYPE_CHECKING,
    Union,
)

if TYPE_CHECKING:
    import datetime

    SupportsIntCast = Union[SupportsInt, str, bytes, bytearray]

__all__ = ("Object",)


class Object(Hashable):
    """Represents a generic Discord object.

    The purpose of this class is to allow you to create 'miniature'
    versions of data classes if you want to pass in just an ID. Most functions
    that take in a specific data class with an ID can also take in this class
    as a substitute instead. Note that even though this is the case, not all
    objects (if any) actually inherit from this class.

    There are also some cases where some websocket events are received
    in :issue:`strange order <21>` and when such events happened you would
    receive this class rather than the actual data class. These cases are
    extremely rare.

    .. container:: operations

        .. describe:: x == y

            Checks if two objects are equal.

        .. describe:: x != y

            Checks if two objects are not equal.

        .. describe:: hash(x)

            Returns the object's hash.

    Attributes
    -----------
    id: :class:`int`
        The ID of the object.
    """

    def __init__(self, id: SupportsIntCast):
        try:
            id = int(id)
        except ValueError:
            raise TypeError(f"id parameter must be convertable to int not {id.__class__!r}") from None
        else:
            self.id = id

    def __repr__(self) -> str:
        return f"<Object id={self.id!r}>"

    def __int__(self) -> int:
        return self.id

    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the snowflake's creation time in UTC."""
        return utils.snowflake_time(self.id)

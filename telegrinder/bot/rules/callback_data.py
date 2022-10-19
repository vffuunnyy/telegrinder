from .abc import ABCRule, EventScheme
from telegrinder.modules import json
from telegrinder.types import Update
from telegrinder.bot.cute_types import CallbackQueryCute
import msgspec
import typing

CallbackQuery = CallbackQueryCute


class CallbackDataEq(ABCRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: Update, ctx: dict) -> bool:
        return event.callback_query.data == self.value


class CallbackDataJsonEq(ABCRule):
    def __init__(self, d: dict):
        self.d = d

    async def check(self, event: Update, ctx: dict) -> bool:
        if not event.callback_query.data:
            return False
        try:
            # todo: use msgspec
            return json.loads(event.callback_query.data) == self.d
        except:
            return False


class CallbackDataJsonModel(ABCRule[CallbackQuery]):
    __event__ = EventScheme("callback_query", CallbackQuery)

    def __init__(self, model: typing.Type[msgspec.Struct]):
        self.decoder = msgspec.json.Decoder(type=model)

    async def check(self, event: CallbackQuery, ctx: dict) -> bool:
        try:
            ctx["data"] = self.decoder.decode(event.data.encode())
            return True
        except msgspec.DecodeError:
            return False

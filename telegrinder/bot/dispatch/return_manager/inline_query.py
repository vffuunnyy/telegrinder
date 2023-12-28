from telegrinder.bot.cute_types import InlineQueryCute

from .abc import BaseReturnManager, register_manager


class InlineQueryReturnManager(BaseReturnManager[InlineQueryCute]):         
    @register_manager(dict)
    @staticmethod
    async def dict_manager(value: dict, event: InlineQueryCute, ctx: dict) -> None:
        await event.answer(**value)

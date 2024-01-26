from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from database.database import Database


class DBMiddleware(BaseMiddleware):
    """ Это MVP только для примера """

    def __init__(self) -> None:
        super().__init__()
        self.db = Database("bot")

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        data['db'] = self.db
        return await handler(event, data)

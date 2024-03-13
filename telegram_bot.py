import sys
from typing import Any

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters.callback_data import CallbackData

from configuration.config import BOT_TOKEN
from models import add_new_grade, add_new_user

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


class GradeCallback(CallbackData, prefix="grade_keyboard"):
    grade: str
    tg_link: str


@dp.message(F.text)
async def real_dispatcher(message: types.Message) -> Any:
    result = add_new_user(message.from_user.id)
    if result:
        await message.answer("✅ Вы успешно подписались на обновления чёрных списков.")


@dp.callback_query()
async def grade_callback_query(information):
    await information.message.answer(add_new_grade(information))


async def start_bot():
    await dp.start_polling(bot)
    sys.exit(0)

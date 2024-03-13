import asyncio
import random
import time

from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

from models import (
    check_new_links,
    get_grades,
    get_telltrue_links,
    get_users,
    get_vklader_links,
)
from telegram_bot import GradeCallback, bot, start_bot

logger.add(
    "logs/errors.log",
    rotation="1 day",
    compression="zip",
    level="INFO",
    format="{time} - {message}",
)


def inline_keyboard(tg_link: str):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="👍", callback_data=GradeCallback(grade="like", tg_link=tg_link)
    )
    builder.button(
        text="👎", callback_data=GradeCallback(grade="dislike", tg_link=tg_link)
    )
    return builder.as_markup()


async def logic() -> None:
    while True:
        try:
            telltrue, vklader = get_telltrue_links(), get_vklader_links()
            unique_telegram_links = list(set(telltrue + vklader))
            for link in check_new_links(unique_telegram_links):
                for user in get_users():
                    time.sleep(random.randint(0, 1))
                    await bot.send_message(
                        chat_id=str(user),
                        text=f"В чёрном списке замечена новая ссылка: {link}",
                        reply_markup=inline_keyboard(link),
                    )
            await asyncio.sleep(60)
        except Exception as exc:
            logger.warning(exc)


async def main_iterator():
    f1 = loop.create_task(start_bot())
    f2 = loop.create_task(logic())
    await asyncio.wait([f1, f2])


if __name__ == "__main__":
    with open("grades_data.json", "w") as file:
        file.write(str(get_grades()))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_iterator())
    loop.close()

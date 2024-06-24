import logging
import os

from aiogram import Router
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

from routers.handlers import ArtificialIntelligence, CustomCallback

router = Router()
logger = logging.getLogger("aiogram")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Startup command, to add user to database and give information about the bot.

    Params:
    - message: Message - Telegram message
    """

    await message.answer(
        "👋 Хай. Я нейро-мережа інтегрована в телеграм. Дізнайтесь про мене більше, за допомогою кнопок нижче.",
        reply_markup=(
            InlineKeyboardBuilder()
            .button(text="❓ Допомога", callback_data=CustomCallback(data="help"))
            .button(
                text="🌐 Додаткова інформація",
                callback_data=CustomCallback(data="additional"),
            )
            .as_markup()
        ),
    )


@router.message(Command("image"))
async def image_handler(message: Message, command: CommandObject) -> None:
    """
    A command to generate an image using DALL·E.

    Params:
    - message: Message - Telegram message
    """

    text: str = command.args

    if not text:
        await message.answer(
            'Помилка. Будь ласка, введіть текст для генерації картинки. (Приклад: "/image city") - підтримується лише англійська мова'
        )
        return

    ai = ArtificialIntelligence()
    uri = ai.generate_image(text)
    msg = await message.answer("Генерую...")
    await msg.edit_text(f"<a href='{uri}'>✅</a> Успішно")


@router.message(Command("answer"))
async def answer_handler(message: Message, command: CommandObject) -> None:
    """
    A command to generate an answer using OpenAI.

    Params:
    - message: Message - Telegram message
    """

    text: str = command.args

    if not text:
        await message.answer(
            'Помилка. Будь ласка, введіть текст для генерації тексту. (Приклад: "/answer хто я?")'
        )
        return

    ai = ArtificialIntelligence()
    msg = await message.answer("Генерую...")
    answer = (
        ai.generate_response(text)
        .replace("$@$v=v1.10-rv1$@$", " ")
        .replace("$@$v=undefined-rv1$@$", " ")
    )
    await msg.edit_text(answer, parse_mode="Markdown")


@router.message(Command("tts"))
async def tts_handler(message: Message, command: CommandObject) -> None:
    """
    A command to generate an audio message using OpenAI.

    Params:
    - message: Message - Telegram message
    """

    text: str = command.args

    if not text:
        await message.answer(
            'Помилка. Будь ласка, введіть текст для генерації гс. (Приклад: "/tts Привіт")'
        )

    ai = ArtificialIntelligence()
    voice_file = BufferedInputFile(ai.text_to_speech(text), filename="output.mp3")

    await message.answer_voice(voice_file)

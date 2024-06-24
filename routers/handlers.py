from langdetect import detect
import traceback
import logging
import requests

from aiogram import Router
from aiogram.filters import callback_data
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from gtts import gTTS

import g4f
import g4f.Provider
import g4f.providers

router = Router()
logger = logging.getLogger("aiogram")


class CustomCallback(callback_data.CallbackData, prefix="data"):
    data: str

@router.callback_query(CustomCallback.filter())
async def my_callback_foo(query: CallbackQuery, callback_data: CustomCallback):
    """
    Callback query handler for "/" prefixed commands.

    Params:
    - query: CallbackQuery - Telegram callback query
    """

    match callback_data.data:
        case "help":
            await query.message.edit_text(
                "🔧 <b>Ось мої команди, які ви можете використовувати</b>\n\n"
                "/answer - Згенерувати відповідь від OpenAI\n"
                "/tts - Згенерувати звукове повідомлення з тексту\n"
                "/image -  Згенерувати картинку за використанням DALLE (підтримується лише англійська мова)\n\n",
                parse_mode="html",
                reply_markup=(
                    InlineKeyboardBuilder()
                    .button(text="◀️ Назад", callback_data=CustomCallback(data="back"))
                    .as_markup()
                ),
            )
        case "additional":
            await query.message.edit_text(
                "♾️ <b>Тут буде додаткова інформація...</b>\n\n",
                parse_mode="html",
                reply_markup=(
                    InlineKeyboardBuilder()
                    .button(text="◀️ Назад", callback_data=CustomCallback(data="back"))
                    .as_markup()
                )
            )
        case "back":
            await query.message.edit_text(
                "👋 Хай. Я нейро-мережа інтегрована в телеграм. Дізнайтесь про мене більше, за допомогою кнопок нижче.",
                reply_markup=(
                    InlineKeyboardBuilder()
                    .button(text="❓ Допомога", callback_data=CustomCallback(data="help"))
                    .button(
                        text="🌐 Додаткова інформація", callback_data=CustomCallback(data="additional")
                    )
                    .as_markup()
                ),
            )
        case _:
            await query.message.reply(
                f"<a href='https://shorturl.at/svIT4'>❓</a> Сталася помилка, повідомте про неї на тех. підтримці!\n"
            )
            logger.error(callback_data.data)


class ArtificialIntelligence:
    def __init__(self):
        self.response: str = ""

    def generate_response(self, prompt: str) -> str:
        """
        Generates a response to the given prompt using the GPT-4 model.
        """
        response = ""
        try:
            response = g4f.ChatCompletion.create(
                model=g4f.models.blackbox,
                messages=[{"role": "user", "content": prompt}],
                stream=True,
            )
            for message in response:
                self.response += message

            return self.response
        except BaseException:
            traceback.print_exc()
            return "Oops! Something went wrong. Please try again later."
        
    def text_to_speech(self, text: str) -> str:
        """
        Generates an audio message using the Google Text-to-Speech API.
        """
        try:
            lang = detect(text)
        except BaseException:
            lang = "en"

        voice = gTTS(text=text, lang=lang)
        file_in_bytes = b''.join([byte for byte in voice.stream()])
        return file_in_bytes
        
    def generate_image(self, prompt: str) -> str:
        """
        Generates an image using the DALL·E model.
        """
        url = f'https://picsum.photos/800/600?grayscale&blur=2&random={prompt}'
        response = requests.get(url)
        
        if response.status_code == 200:
            image_url = response.url
            return image_url
        else:
            print(f"Failed to fetch image. Status code: {response.status_code}")
            return None


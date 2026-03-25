import asyncio
import random
import json
import os
from aiohttp import web  # Нужно для "обмана" Render
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile

# Импорты ваших данных
try:
    from quotes import QUOTES
    from songs import SONGS, ITEMS_PER_PAGE, PRESAVE_SONG
except ImportError:
    QUOTES = ["Цитата не найдена"]
    SONGS = []
    ITEMS_PER_PAGE = 5
    PRESAVE_SONG = {"title": "Скоро!", "url": "https://t.me/w0cxod", "is_presave": True}

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ========== НАСТРОЙКИ ==========
ADMINS = [1107815483]
USERS_FILE = "users.json"

LEXICON = {
    "ru": {
        "btn_quote": "📖 Случайная цитата",
        "btn_songs": "🎧 Слушать песни",
        "btn_merch": "🛍️ Каталог мерча",
        "btn_concert": "🎫 Ближайший концерт",
        "btn_share": "📸 Как поделиться?",
        "btn_settings": "⚙️ Настройки",
        "btn_newsletter": "📨 Рассылка",
        "btn_main": "🏠 Главное меню",
        "btn_lang": "🌐 Изменить язык",
        "welcome": "🎵 **Привет! Я бот группы Восход**\n\nНажимай на кнопки внизу! 👇",
        "quote_prefix": "🎤 Вот твоя цитата:\n\n",
        "quote_suffix": "\n\n✨ Сохрани ее или поделись!",
        "songs_list": "🎵 **Список песен**\nСтраница {page} из {total}\n\nНажми на название:",
        "btn_next": "Вперед ▶️",
        "btn_prev": "◀️ Назад",
        "concert_info": "🎫 **Ближайший концерт**\n\n3 мая | Екатеринбург",
        "share_info": "📸 **Как поделиться?**\nСкопируй текст и вставь в сторис!",
        "settings_text": "⚙️ **Настройки**",
        "newsletter_menu": "📨 **Рассылка**\n\n{sub_status}",
        "btn_inline_sub": "🔔 Подписаться",
        "btn_inline_unsub": "🔕 Отписаться",
        "status_sub": "✅ Вы подписаны",
        "status_unsub": "❌ Вы отписаны",
        "main_menu_prompt": "🎵 **Главное меню**",
        "merch_catalog": "🛍️ **Каталог мерча**",
        "contact_manager": "📩 Менеджер",
        "back_to_catalog": "◀️ Назад",
        "btn_patches": "⚫ Нашивки",
        "btn_bracelets": "📿 Браслеты",
        "btn_pins": "🔘 Значки",
        "btn_stickers": "🌅 Наклейки",
        "btn_postcards": "💌 Открытки",
        "item_not_found": "Товар не найден",
        "price": "💰 Цена:",
        "order_prompt": "📩 Для заказа: @wocx0d",
        "promo_concert": "🎫 У нас скоро концерт в Екб!",
        "promo_presave": "🎵 Сделай пресейв нового трека!",
        "presave_msg": "🎁 **Новый трек уже скоро!**\n\n🔗 [Пресейв]({url})",
        "listen_stream": "🎵 **{title}**\n\n🔗 [Слушать]({url})",
        "choose_lang": "🌐 Выберите язык:",
        "lang_changed": "✅ Язык изменен!"
    },
    "en": {
        "btn_quote": "📖 Random Quote",
        "btn_songs": "🎧 Listen to Songs",
        "btn_merch": "🛍️ Merch Catalog",
        "btn_concert": "🎫 Next Concert",
        "btn_share": "📸 How to share?",
        "btn_settings": "⚙️ Settings",
        "btn_newsletter": "📨 Newsletter",
        "btn_main": "🏠 Main Menu",
        "btn_lang": "🌐 Change Language",
        "welcome": "🎵 **Hello! I'm the Voskhod bot**",
        "quote_prefix": "🎤 Quote:\n\n",
        "quote_suffix": "\n\n✨ Share it!",
        "songs_list": "🎵 **Song List**\nPage {page} of {total}",
        "btn_next": "Next ▶️",
        "btn_prev": "◀️ Back",
        "concert_info": "🎫 **Next Concert**\nMay 3 | Yekaterinburg",
        "share_info": "📸 **How to share?**\nCopy and paste to Stories!",
        "settings_text": "⚙️ **Settings**",
        "newsletter_menu": "📨 **Newsletter**\n\n{sub_status}",
        "btn_inline_sub": "🔔 Subscribe",
        "btn_inline_unsub": "🔕 Unsubscribe",
        "status_sub": "✅ Subscribed",
        "status_unsub": "❌ Unsubscribed",
        "main_menu_prompt": "🎵 **Main Menu**",
        "merch_catalog": "🛍️ **Merch Catalog**",
        "contact_manager": "📩 Manager",
        "back_to_catalog": "◀️ Back",
        "btn_patches": "⚫ Patches",
        "btn_bracelets": "📿 Bracelets",
        "btn_pins": "🔘 Pins",
        "btn_stickers": "🌅 Stickers",
        "btn_postcards": "💌 Postcards",
        "item_not_found": "Not found",
        "price": "💰 Price:",
        "order_prompt": "📩 Order: @wocx0d",
        "promo_concert": "🎫 Concert soon!",
        "promo_presave": "🎵 Presave our new track!",
        "presave_msg": "🎁 **New track soon!**\n\n🔗 [Presave]({url})",
        "listen_stream": "🎵 **{title}**\n\n🔗 [Listen]({url})",
        "choose_lang": "🌐 Choose language:",
        "lang_changed": "✅ Language changed!"
    }
}

# ========== ЛОГИКА ПОЛЬЗОВАТЕЛЕЙ ==========

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                return json.load(f)
        except: return {}
    return {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

users = load_users()
quote_counter = {}

def get_user_lang(user_id: int) -> str:
    uid_str = str(user_id)
    if uid_str not in users:
        users[uid_str] = {"lang": "ru", "sub": True}
        save_users()
    return users[uid_str].get("lang", "ru")

def get_text(user_id: int, key: str, **kwargs) -> str:
    lang = get_user_lang(user_id)
    text = LEXICON.get(lang, LEXICON["ru"]).get(key, key)
    return text.format(**kwargs) if kwargs else text

# ========== МЕРЧ И КЛАВИАТУРЫ (СОКРАЩЕНО ДЛЯ КРАТКОСТИ) ==========

MERCH_ITEMS = {
    "patch_white": {"name": {"ru": "⚪ Нашивка", "en": "⚪ Patch"}, "price": 450, "category": "patches"},
    "bracelet": {"name": {"ru": "📿 Браслет", "en": "📿 Bracelet"}, "price": 200, "category": "bracelets"},
}

def main_reply_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text=get_text(user_id, "btn_quote")), KeyboardButton(text=get_text(user_id, "btn_songs"))],
        [KeyboardButton(text=get_text(user_id, "btn_merch")), KeyboardButton(text=get_text(user_id, "btn_concert"))],
        [KeyboardButton(text=get_text(user_id, "btn_share")), KeyboardButton(text=get_text(user_id, "btn_settings"))]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# ========== ОБРАБОТЧИКИ ==========

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "welcome"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

# Использование F.text.in_ вместо Text()
@dp.message(F.text.in_([LEXICON["ru"]["btn_quote"], LEXICON["en"]["btn_quote"]]))
async def get_quote_reply(message: types.Message):
    user_id = message.from_user.id
    quote = random.choice(QUOTES)
    await message.answer(get_text(user_id, "quote_prefix") + quote + get_text(user_id, "quote_suffix"))

@dp.message(F.text.in_([LEXICON["ru"]["btn_settings"], LEXICON["en"]["btn_settings"]]))
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "settings_text"), reply_markup=main_reply_keyboard(user_id))

# ========== ХАК ДЛЯ RENDER (HEALTH CHECK) ==========
async def handle_hc(request):
    return web.Response(text="I am alive")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_hc)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render дает порт в переменную окружения PORT
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv("PORT", 8080)))
    await site.start()
    print(f"✅ Web server started on port {os.getenv('PORT', 8080)}")

# ========== ЗАПУСК ==========

async def main():
    # Запускаем веб-сервер в фоне
    asyncio.create_task(start_web_server())
    
    print("🚀 Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот остановлен")

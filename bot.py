import asyncio
import random
import json
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import FSInputFile

from quotes import QUOTES
from songs import SONGS, ITEMS_PER_PAGE, PRESAVE_SONG

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
# ========== НАСТРОЙКИ ==========
ADMINS = [1107815483]
USERS_FILE = "users.json"

# ========== СЛОВАРЬ ПЕРЕВОДОВ (LEXICON) ==========
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
        
        "welcome": "🎵 **Привет! Я бот группы Восход**\n\nЧто я умею:\n• 📖 Давать цитаты из песен\n• 🎧 Отправлять ссылки на наши треки\n• 🎫 Рассказывать о ближайших концертах\n• 🛍️ Показывать каталог мерча\n• 📸 Помогать делиться в сторис\n\nНажимай на кнопки внизу экрана! 👇",
        "quote_prefix": "🎤 Вот твоя цитата:\n\n",
        "quote_suffix": "\n\n✨ Сохрани ее или поделись в сторис!",
        "songs_list": "🎵 **Список песен**\nСтраница {page} из {total}\nВсего песен: {count}\n\nНажми на название, чтобы получить ссылку:",
        "btn_next": "Вперед ▶️",
        "btn_prev": "◀️ Назад",
        "concert_info": "🎫 **Ближайший концерт группы Восход**\n\n**«Солнечные сны»**\n\n📅 **Дата:** 3 мая\n📍 **Место:** ЦК Орджоникидзевский, ул. Культуры, 3 | г. Екатеринбург\n🚪 **Начало:** 19:00\n\n🎟️ **Билеты:** [Купить билет](https://t.me/QticketsBuyBot/buy?startapp=220348)\n\n✨ Ждём тебя! 🔥\n\n💫 *Подпишись на наш Telegram-канал:*\nhttps://t.me/w0cxod",
        "share_info": "📸 **Как поделиться цитатой в сторис?**\n\n1️⃣ Скопируй цитату (нажми и удержи на тексте)\n2️⃣ Открой социальную сеть\n3️⃣ Вставь текст в сторис\n4️⃣ Добавь фон, стикеры или нашу музыку\n5️⃣ Отметь нас\n\nМы обязательно посмотрим и зарепостим лучшие! 🔥",
        "settings_text": "⚙️ **Настройки**\n\nТекущий язык: 🇷🇺 Русский\n\nЗдесь вы можете управлять подпиской на новости и языком бота.",
        
        # Тексты для рассылки
        "newsletter_menu": "📨 **Управление рассылкой**\n\n{sub_status}\n\nХотите изменить статус?",
        "btn_inline_sub": "🔔 Подписаться",
        "btn_inline_unsub": "🔕 Отписаться",
        "status_sub": "✅ **Вы подписаны на рассылку**",
        "status_unsub": "❌ **Вы отписаны от рассылки**",
        "toast_sub": "Подписка оформлена!",
        "toast_unsub": "Вы отписались от новостей.",
        
        "main_menu_prompt": "🎵 **Главное меню**\n\nВыбери действие:",
        "merch_catalog": "🛍️ **Каталог мерча группы Восход**\n\nВыберите категорию товара:\n\n• ⚫ Нашивки — от 450 ₽\n• 📿 Браслеты — 200 ₽\n• 🔘 Значки — 150 ₽\n• 🌅 Наклейки — 150 ₽\n• 💌 Открытки — 100 ₽\n\n📩 По вопросам заказа пишите @wocx0d\n\n⚡ *Цены указаны без учёта стоимости доставки*",
        "contact_manager": "📩 Связаться с менеджером",
        "back_to_catalog": "◀️ Назад в каталог",
        "btn_patches": "⚫ Нашивки",
        "btn_bracelets": "📿 Браслеты",
        "btn_pins": "🔘 Значки",
        "btn_stickers": "🌅 Наклейки",
        "btn_postcards": "💌 Открытки",
        "item_not_found": "Товар не найден",
        "price": "💰 **Цена:**",
        "order_prompt": "📩 **Для заказа:** напишите @wocx0d\nУкажите название товара и количество.\n\n⚡ *Цена указана без учёта стоимости доставки*",
        "promo_concert": "🎫 **Кстати!** У нас скоро концерт в Екатеринбурге!\n\n📅 3 мая | 🏢 ЦК Орджоникидзевский\nНажми кнопку «🎫 Ближайший концерт» в главном меню!",
        "promo_presave": "🎵 **Кстати!** Мы готовим новый трек «Музыка любви»!\n\n🔥 Сделай пресейв: [Сделать пресейв](https://band.link/musiquedamour)",
        "presave_msg": "🎁 **«Музыка любви» — уже 8 апреля!** 🎁\n\n✨ **Сделай пресейв сейчас:**\n→ Трек попадёт в твой плейлист автоматически\n→ Не нужно искать в день релиза\n→ Это бесплатно и занимает 10 секунд\n\nВаша поддержка очень ценна для нас!\n\n🔗 [Сделать пресейв]({url})\n\n💝 Поделись ссылкой с друзьями!",
        "listen_stream": "🎵 **{title}**\n\nСлушать на стримингах:\n🔗 [Страница песни]({url})\n\n✨ Поделись этой песней с друзьями!\n\n",
        "choose_lang": "🌐 Выберите язык / Choose language:",
        "lang_changed": "✅ Язык успешно изменен на Русский!"
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
        
        "welcome": "🎵 **Hello! I'm the Voskhod band bot**\n\nWhat I can do:\n• 📖 Give quotes from songs\n• 🎧 Send links to our tracks\n• 🎫 Tell you about upcoming concerts\n• 🛍️ Show the merch catalog\n• 📸 Help you share in stories\n\nTap the buttons below! 👇",
        "quote_prefix": "🎤 Here is your quote:\n\n",
        "quote_suffix": "\n\n✨ Save it or share it in your stories!",
        "songs_list": "🎵 **Song List**\nPage {page} of {total}\nTotal songs: {count}\n\nClick on a title to get the link:",
        "btn_next": "Next ▶️",
        "btn_prev": "◀️ Back",
        "concert_info": "🎫 **Voskhod's Next Concert**\n\n**«Sunny Dreams»**\n\n📅 **Date:** May 3\n📍 **Location:** CC Ordzhonikidzevsky, Kultury st, 3 | Yekaterinburg\n🚪 **Doors:** 19:00\n\n🎟️ **Tickets:** [Buy ticket](https://t.me/QticketsBuyBot/buy?startapp=220348)\n\n✨ We are waiting for you! 🔥\n\n💫 *Subscribe to our Telegram channel:*\nhttps://t.me/w0cxod",
        "share_info": "📸 **How to share a quote in Stories?**\n\n1️⃣ Copy the quote (tap and hold on the text)\n2️⃣ Open your social network\n3️⃣ Paste the text into Stories\n4️⃣ Add background, stickers, or our music\n5️⃣ Tag us\n\nWe will definitely watch and repost the best ones! 🔥",
        "settings_text": "⚙️ **Settings**\n\nCurrent language: 🇬🇧 English\n\nHere you can manage your newsletter subscription and bot language.",
        
        # Тексты для рассылки
        "newsletter_menu": "📨 **Newsletter Management**\n\n{sub_status}\n\nDo you want to change your status?",
        "btn_inline_sub": "🔔 Subscribe",
        "btn_inline_unsub": "🔕 Unsubscribe",
        "status_sub": "✅ **You are subscribed to the newsletter**",
        "status_unsub": "❌ **You are unsubscribed from the newsletter**",
        "toast_sub": "Successfully subscribed!",
        "toast_unsub": "You have unsubscribed.",
        
        "main_menu_prompt": "🎵 **Main Menu**\n\nChoose an action:",
        "merch_catalog": "🛍️ **Voskhod Merch Catalog**\n\nChoose a product category:\n\n• ⚫ Patches — from 450 ₽\n• 📿 Bracelets — 200 ₽\n• 🔘 Pins — 150 ₽\n• 🌅 Stickers — 150 ₽\n• 💌 Postcards — 100 ₽\n\n📩 For orders, text @wocx0d\n\n⚡ *Prices do not include shipping costs*",
        "contact_manager": "📩 Contact Manager",
        "back_to_catalog": "◀️ Back to catalog",
        "btn_patches": "⚫ Patches",
        "btn_bracelets": "📿 Bracelets",
        "btn_pins": "🔘 Pins",
        "btn_stickers": "🌅 Stickers",
        "btn_postcards": "💌 Postcards",
        "item_not_found": "Item not found",
        "price": "💰 **Price:**",
        "order_prompt": "📩 **To order:** message @wocx0d\nSpecify the item name and quantity.\n\n⚡ *Price does not include shipping*",
        "promo_concert": "🎫 **By the way!** We have a concert in Yekaterinburg soon!\n\n📅 May 3 | 🏢 CC Ordzhonikidzevsky\nClick «🎫 Next Concert» in the main menu!",
        "promo_presave": "🎵 **By the way!** We are preparing a new track «Music of Love»!\n\n🔥 Presave now: [Presave](https://band.link/musiquedamour)",
        "presave_msg": "🎁 **«Music of Love» — coming April 8!** 🎁\n\n✨ **Presave it now:**\n→ The track will drop into your playlist automatically\n→ No need to search on release day\n→ It's free and takes 10 seconds\n\nYour support is very valuable to us!\n\n🔗 [Presave here]({url})\n\n💝 Share the link with friends!",
        "listen_stream": "🎵 **{title}**\n\nListen on streaming platforms:\n🔗 [Song Page]({url})\n\n✨ Share this song with your friends!\n\n",
        "choose_lang": "🌐 Выберите язык / Choose language:",
        "lang_changed": "✅ Language successfully changed to English!"
    }
}

# ========== РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ==========

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list): # Миграция со старой версии
                    return {str(uid): {"lang": "ru", "sub": True} for uid in data}
                return data
        except:
            return {}
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
    if kwargs:
        return text.format(**kwargs)
    return text

# ========== ДАННЫЕ МЕРЧА ==========

MERCH_IMAGES = {
    "patch_white": "merch_images/patch_white.jpg",
    "patch_black": "merch_images/patch_black.jpg",
    "patch_color": "merch_images/patch_color.jpg",
    "bracelet": "merch_images/bracelet.jpg",
    "sticker_set1": "merch_images/sticker_set1.jpg",
    "sticker_set2": "merch_images/sticker_set2.jpg",
    "pin_logo_black": "merch_images/pin_logo_black.jpg",
    "pin_logo_white": "merch_images/pin_logo_white.jpg",
    "pin_stepa": "merch_images/pin_stepa.jpg",
    "pin_danya": "merch_images/pin_danya.jpg",
    "pin_liza": "merch_images/pin_liza.jpg",
    "pin_kirya": "merch_images/pin_kirya.jpg",
    "pin_lenya": "merch_images/pin_lenya.jpg",
    "pin_love": "merch_images/pin_love.jpg",
    "pin_oda": "merch_images/pin_oda.jpg",
    "postcard": "merch_images/postcard.jpg",
}

MERCH_ITEMS = {
    "patch_white": {"name": {"ru": "⚪ Нашивка белая", "en": "⚪ White Patch"}, "price": 450, "desc": {"ru": "Белая нашивка с логотипом группы. Диаметр: 6 см.", "en": "White patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "patch_black": {"name": {"ru": "⚫ Нашивка черная", "en": "⚫ Black Patch"}, "price": 450, "desc": {"ru": "Черная нашивка с логотипом группы. Диаметр: 6 см.", "en": "Black patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "patch_color": {"name": {"ru": "🟣 Нашивка цветная", "en": "🟣 Color Patch"}, "price": 600, "desc": {"ru": "Цветная нашивка с логотипом группы. Диаметр: 6 см.", "en": "Color patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "bracelet": {"name": {"ru": "📿 Браслет", "en": "📿 Bracelet"}, "price": 200, "desc": {"ru": "Браслет силиконовый подростковый (180×12×2мм, Ø57 мм).", "en": "Teen silicone bracelet (180×12×2mm, Ø57 mm)."}, "category": "bracelets"},
    "sticker_set1": {"name": {"ru": "🌅 Наклейки (набор 1)", "en": "🌅 Stickers (Set 1)"}, "price": 150, "desc": {"ru": "Наклейки с обложками и участниками группы Восход. Размер: А6", "en": "Stickers with covers and band members. Size: A6"}, "category": "stickers"},
    "sticker_set2": {"name": {"ru": "🌅 Наклейки (набор 2)", "en": "🌅 Stickers (Set 2)"}, "price": 150, "desc": {"ru": "Наклейки с обложками и участниками группы Восход. Размер: А6", "en": "Stickers with covers and band members. Size: A6"}, "category": "stickers"},
    "pin_logo_black": {"name": {"ru": "🔘 Значок логотип черный", "en": "🔘 Black Logo Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_logo_white": {"name": {"ru": "🔘 Значок логотип белый", "en": "🔘 White Logo Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_stepa": {"name": {"ru": "🔘 Значок Стёпа", "en": "🔘 Stepa Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_danya": {"name": {"ru": "🔘 Значок Музыcan't", "en": "🔘 Musican't Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_liza": {"name": {"ru": "🔘 Значок Lizzy", "en": "🔘 Lizzy Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_kirya": {"name": {"ru": "🔘 Значок Kirya Kote", "en": "🔘 Kirya Kote Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_lenya": {"name": {"ru": "🔘 Значок Лёня", "en": "🔘 Lenya Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_love": {"name": {"ru": "🔘 Значок «Любовь...»", "en": "🔘 Love Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_oda": {"name": {"ru": "🔘 Значок «Ода»", "en": "🔘 Oda Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "postcard": {"name": {"ru": "💌 Авторская открытка", "en": "💌 Postcard"}, "price": 100, "desc": {"ru": "Открытки с логотипом группы. Размер: А5", "en": "Postcards with band logo. Size: A5"}, "category": "postcards"},
}

# ========== КЛАВИАТУРЫ ==========

def main_reply_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text=get_text(user_id, "btn_quote")), KeyboardButton(text=get_text(user_id, "btn_songs"))],
        [KeyboardButton(text=get_text(user_id, "btn_merch")), KeyboardButton(text=get_text(user_id, "btn_concert"))],
        [KeyboardButton(text=get_text(user_id, "btn_share")), KeyboardButton(text=get_text(user_id, "btn_settings"))]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def settings_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text=get_text(user_id, "btn_newsletter"))],
        [KeyboardButton(text=get_text(user_id, "btn_lang"))],
        [KeyboardButton(text=get_text(user_id, "btn_main"))]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def catalog_main_keyboard(user_id: int):
    buttons = [
        [InlineKeyboardButton(text=get_text(user_id, "btn_patches"), callback_data="category_patches")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_bracelets"), callback_data="merch_bracelet")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_pins"), callback_data="category_pins")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_stickers"), callback_data="category_stickers")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_postcards"), callback_data="merch_postcard")],
        [InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def category_items_keyboard(user_id: int, category: str):
    lang = get_user_lang(user_id)
    items = [item_id for item_id, item in MERCH_ITEMS.items() if item.get("category") == category]
    buttons = []
    for item_id in items:
        item = MERCH_ITEMS[item_id]
        buttons.append([InlineKeyboardButton(text=f"{item['name'][lang]} — {item['price']} ₽", callback_data=f"view_{item_id}")])
    buttons.append([InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")])
    buttons.append([InlineKeyboardButton(text=get_text(user_id, "back_to_catalog"), callback_data="back_to_catalog")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def songs_inline_keyboard(user_id: int, page: int = 0):
    display_songs = [PRESAVE_SONG] + SONGS
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, len(display_songs))
    buttons = []
    for i in range(start_idx, end_idx):
        song = display_songs[i]
        button_text = f"🎁 {song['title']}" if song.get("is_presave") else f"🎵 {song['title']}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"play_song_{i}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text=get_text(user_id, "btn_prev"), callback_data=f"songs_page_{page - 1}"))
    if end_idx < len(display_songs):
        nav_buttons.append(InlineKeyboardButton(text=get_text(user_id, "btn_next"), callback_data=f"songs_page_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

async def show_item(callback: types.CallbackQuery, item_id: str):
    user_id = callback.from_user.id
    lang = get_user_lang(user_id)
    item = MERCH_ITEMS.get(item_id)
    
    if not item:
        await callback.answer(get_text(user_id, "item_not_found"))
        return
        
    image_path = MERCH_IMAGES.get(item_id)
    text = (
        f"🛍️ **{item['name'][lang]}**\n\n"
        f"{item['desc'][lang]}\n\n"
        f"{get_text(user_id, 'price')} {item['price']} ₽\n\n"
        f"{get_text(user_id, 'order_prompt')}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")],
        [InlineKeyboardButton(text=get_text(user_id, "back_to_catalog"), callback_data="back_to_catalog")]
    ])
    
    try:
        photo = FSInputFile(image_path)
        await callback.message.delete()
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

async def send_random_promotion(message: types.Message):
    user_id = message.from_user.id
    if random.choice([True, False]):
        await message.answer(get_text(user_id, "promo_concert"), parse_mode="Markdown")
    else:
        await message.answer(get_text(user_id, "promo_presave"), parse_mode="Markdown", disable_web_page_preview=True)

# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    get_user_lang(user_id) 
    await message.answer(get_text(user_id, "welcome"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

@dp.message(Command("send_all"))
async def send_to_all(message: types.Message):
    if message.from_user.id not in ADMINS: return
    text = message.text.replace("/send_all", "").strip() if message.text else message.caption.replace("/send_all", "").strip() if message.caption else ""
    if not text and not message.photo:
        await message.answer("❌ Отправь текст или фото с подписью.")
        return
    status_msg = await message.answer(f"📤 Начинаю рассылку...")
    success, failed = 0, 0
    for uid, data in users.items():
        if not data.get("sub", True): continue # Пропускаем отписавшихся
        try:
            if message.photo:
                await bot.send_photo(uid, photo=message.photo[-1].file_id, caption=text, parse_mode="Markdown")
            else:
                await bot.send_message(uid, text, parse_mode="Markdown")
            success += 1
            await asyncio.sleep(0.05)
        except Exception: failed += 1
    await status_msg.edit_text(f"✅ Рассылка завершена!\n📤 Отправлено: {success}\n❌ Ошибок: {failed}")

# ========== ОБРАБОТЧИКИ ТЕКСТОВЫХ КНОПОК ==========

@dp.message(Text([LEXICON["ru"]["btn_quote"], LEXICON["en"]["btn_quote"]]))
async def get_quote_reply(message: types.Message):
    user_id = message.from_user.id
    quote = random.choice(QUOTES) 
    response = get_text(user_id, "quote_prefix") + quote + get_text(user_id, "quote_suffix")
    await message.answer(response, reply_markup=main_reply_keyboard(user_id))
    
    quote_counter[user_id] = quote_counter.get(user_id, 0) + 1
    if quote_counter[user_id] % 5 == 0:
        await send_random_promotion(message)

@dp.message(Text([LEXICON["ru"]["btn_songs"], LEXICON["en"]["btn_songs"]]))
async def list_songs_reply(message: types.Message):
    user_id = message.from_user.id
    count = 1 + len(SONGS)
    total = (count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    text = get_text(user_id, "songs_list", page=1, total=total, count=count)
    await message.answer(text, reply_markup=songs_inline_keyboard(user_id, 0), parse_mode="Markdown")

@dp.message(Text([LEXICON["ru"]["btn_concert"], LEXICON["en"]["btn_concert"]]))
async def concert_info(message: types.Message):
    user_id = message.from_user.id
    caption = get_text(user_id, "concert_info")
    try:
        photo = FSInputFile("Afisha.jpg")
        await message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown")
    except:
        await message.answer(caption, parse_mode="Markdown")

@dp.message(Text([LEXICON["ru"]["btn_merch"], LEXICON["en"]["btn_merch"]]))
async def merch_catalog(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")

@dp.message(Text([LEXICON["ru"]["btn_share"], LEXICON["en"]["btn_share"]]))
async def how_to_share_reply(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "share_info"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

@dp.message(Text([LEXICON["ru"]["btn_settings"], LEXICON["en"]["btn_settings"]]))
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    text = get_text(user_id, "settings_text")
    await message.answer(text, reply_markup=settings_keyboard(user_id), parse_mode="Markdown")

# ========== НАСТРОЙКИ: РАССЫЛКА ==========
@dp.message(Text([LEXICON["ru"]["btn_newsletter"], LEXICON["en"]["btn_newsletter"]]))
async def newsletter_menu(message: types.Message):
    user_id = message.from_user.id
    uid_str = str(user_id)
    is_sub = users.get(uid_str, {}).get("sub", True)
    
    sub_status = get_text(user_id, "status_sub") if is_sub else get_text(user_id, "status_unsub")
    text = get_text(user_id, "newsletter_menu", sub_status=sub_status)
    
    btn_text = get_text(user_id, "btn_inline_unsub") if is_sub else get_text(user_id, "btn_inline_sub")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, callback_data="toggle_sub")]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# ========== НАСТРОЙКИ: ЯЗЫК ==========
@dp.message(Text([LEXICON["ru"]["btn_lang"], LEXICON["en"]["btn_lang"]]))
async def change_lang_menu(message: types.Message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")]
    ])
    await message.answer(get_text(user_id, "choose_lang"), reply_markup=keyboard)

@dp.message(Text([LEXICON["ru"]["btn_main"], LEXICON["en"]["btn_main"]]))
async def back_to_menu(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "main_menu_prompt"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

# ========== ОБЩИЙ ОБРАБОТЧИК INLINE-КНОПОК ==========

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if callback.data == "back_to_catalog":
        try:
            await callback.message.edit_text(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")
        except:
            await callback.message.delete()
            await callback.message.answer(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")
        await callback.answer()
        return
    
    elif callback.data == "category_patches":
        await callback.message.edit_text(f"⚫ **{get_text(user_id, 'btn_patches').replace('⚫ ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "patches"), parse_mode="Markdown")
    elif callback.data == "merch_bracelet":
        await show_item(callback, "bracelet")
    elif callback.data == "category_pins":
        await callback.message.edit_text(f"🔘 **{get_text(user_id, 'btn_pins').replace('🔘 ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "pins"), parse_mode="Markdown")
    elif callback.data == "category_stickers":
        await callback.message.edit_text(f"🌅 **{get_text(user_id, 'btn_stickers').replace('🌅 ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "stickers"), parse_mode="Markdown")
    elif callback.data == "merch_postcard":
        await show_item(callback, "postcard")
    
    elif callback.data.startswith("view_"):
        item_id = callback.data.replace("view_", "")
        await show_item(callback, item_id)
    
    elif callback.data.startswith("show_songs_") or callback.data.startswith("songs_page_"):
        page = int(callback.data.split("_")[2])
        count = 1 + len(SONGS)
        total = (count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        text = get_text(user_id, "songs_list", page=page+1, total=total, count=count)
        await callback.message.edit_text(text, reply_markup=songs_inline_keyboard(user_id, page), parse_mode="Markdown")
    
    elif callback.data.startswith("play_song_"):
        song_index = int(callback.data.split("_")[2])
        all_songs = [PRESAVE_SONG] + SONGS
        if song_index < len(all_songs):
            song = all_songs[song_index]
            if song.get("is_presave"):
                text = get_text(user_id, "presave_msg", url=song['url'])
            else:
                text = get_text(user_id, "listen_stream", title=song['title'], url=song['url'])
                
            after_play_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=get_text(user_id, "btn_songs"), callback_data="show_songs_0")]
            ])
            await callback.message.answer(text, reply_markup=after_play_keyboard, parse_mode="Markdown")
            
    await callback.answer()

@dp.message()
async def any_message(message: types.Message):
    if not message.text.startswith('/'):
        user_id = message.from_user.id
        await message.answer("👋", reply_markup=main_reply_keyboard(user_id))

# ========== ЗАПУСК ==========

async def main():
    print("🚀 Бот запускается...")
    print(f"👥 Загружено пользователей: {len(users)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise Exception("BOT_TOKEN не найден в переменных окружения!")

bot = Bot(token=TOKEN)
dp = Dispatcher()
# ========== НАСТРОЙКИ ==========
ADMINS = [1107815483]
USERS_FILE = "users.json"

# ========== СЛОВАРЬ ПЕРЕВОДОВ (LEXICON) ==========
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
        
        "welcome": "🎵 **Привет! Я бот группы Восход**\n\nЧто я умею:\n• 📖 Давать цитаты из песен\n• 🎧 Отправлять ссылки на наши треки\n• 🎫 Рассказывать о ближайших концертах\n• 🛍️ Показывать каталог мерча\n• 📸 Помогать делиться в сторис\n\nНажимай на кнопки внизу экрана! 👇",
        "quote_prefix": "🎤 Вот твоя цитата:\n\n",
        "quote_suffix": "\n\n✨ Сохрани ее или поделись в сторис!",
        "songs_list": "🎵 **Список песен**\nСтраница {page} из {total}\nВсего песен: {count}\n\nНажми на название, чтобы получить ссылку:",
        "btn_next": "Вперед ▶️",
        "btn_prev": "◀️ Назад",
        "concert_info": "🎫 **Ближайший концерт группы Восход**\n\n**«Солнечные сны»**\n\n📅 **Дата:** 3 мая\n📍 **Место:** ЦК Орджоникидзевский, ул. Культуры, 3 | г. Екатеринбург\n🚪 **Начало:** 19:00\n\n🎟️ **Билеты:** [Купить билет](https://t.me/QticketsBuyBot/buy?startapp=220348)\n\n✨ Ждём тебя! 🔥\n\n💫 *Подпишись на наш Telegram-канал:*\nhttps://t.me/w0cxod",
        "share_info": "📸 **Как поделиться цитатой в сторис?**\n\n1️⃣ Скопируй цитату (нажми и удержи на тексте)\n2️⃣ Открой социальную сеть\n3️⃣ Вставь текст в сторис\n4️⃣ Добавь фон, стикеры или нашу музыку\n5️⃣ Отметь нас\n\nМы обязательно посмотрим и зарепостим лучшие! 🔥",
        "settings_text": "⚙️ **Настройки**\n\nТекущий язык: 🇷🇺 Русский\n\nЗдесь вы можете управлять подпиской на новости и языком бота.",
        
        # Тексты для рассылки
        "newsletter_menu": "📨 **Управление рассылкой**\n\n{sub_status}\n\nХотите изменить статус?",
        "btn_inline_sub": "🔔 Подписаться",
        "btn_inline_unsub": "🔕 Отписаться",
        "status_sub": "✅ **Вы подписаны на рассылку**",
        "status_unsub": "❌ **Вы отписаны от рассылки**",
        "toast_sub": "Подписка оформлена!",
        "toast_unsub": "Вы отписались от новостей.",
        
        "main_menu_prompt": "🎵 **Главное меню**\n\nВыбери действие:",
        "merch_catalog": "🛍️ **Каталог мерча группы Восход**\n\nВыберите категорию товара:\n\n• ⚫ Нашивки — от 450 ₽\n• 📿 Браслеты — 200 ₽\n• 🔘 Значки — 150 ₽\n• 🌅 Наклейки — 150 ₽\n• 💌 Открытки — 100 ₽\n\n📩 По вопросам заказа пишите @wocx0d\n\n⚡ *Цены указаны без учёта стоимости доставки*",
        "contact_manager": "📩 Связаться с менеджером",
        "back_to_catalog": "◀️ Назад в каталог",
        "btn_patches": "⚫ Нашивки",
        "btn_bracelets": "📿 Браслеты",
        "btn_pins": "🔘 Значки",
        "btn_stickers": "🌅 Наклейки",
        "btn_postcards": "💌 Открытки",
        "item_not_found": "Товар не найден",
        "price": "💰 **Цена:**",
        "order_prompt": "📩 **Для заказа:** напишите @wocx0d\nУкажите название товара и количество.\n\n⚡ *Цена указана без учёта стоимости доставки*",
        "promo_concert": "🎫 **Кстати!** У нас скоро концерт в Екатеринбурге!\n\n📅 3 мая | 🏢 ЦК Орджоникидзевский\nНажми кнопку «🎫 Ближайший концерт» в главном меню!",
        "promo_presave": "🎵 **Кстати!** Мы готовим новый трек «Музыка любви»!\n\n🔥 Сделай пресейв: [Сделать пресейв](https://band.link/musiquedamour)",
        "presave_msg": "🎁 **«Музыка любви» — уже 8 апреля!** 🎁\n\n✨ **Сделай пресейв сейчас:**\n→ Трек попадёт в твой плейлист автоматически\n→ Не нужно искать в день релиза\n→ Это бесплатно и занимает 10 секунд\n\nВаша поддержка очень ценна для нас!\n\n🔗 [Сделать пресейв]({url})\n\n💝 Поделись ссылкой с друзьями!",
        "listen_stream": "🎵 **{title}**\n\nСлушать на стримингах:\n🔗 [Страница песни]({url})\n\n✨ Поделись этой песней с друзьями!\n\n",
        "choose_lang": "🌐 Выберите язык / Choose language:",
        "lang_changed": "✅ Язык успешно изменен на Русский!"
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
        
        "welcome": "🎵 **Hello! I'm the Voskhod band bot**\n\nWhat I can do:\n• 📖 Give quotes from songs\n• 🎧 Send links to our tracks\n• 🎫 Tell you about upcoming concerts\n• 🛍️ Show the merch catalog\n• 📸 Help you share in stories\n\nTap the buttons below! 👇",
        "quote_prefix": "🎤 Here is your quote:\n\n",
        "quote_suffix": "\n\n✨ Save it or share it in your stories!",
        "songs_list": "🎵 **Song List**\nPage {page} of {total}\nTotal songs: {count}\n\nClick on a title to get the link:",
        "btn_next": "Next ▶️",
        "btn_prev": "◀️ Back",
        "concert_info": "🎫 **Voskhod's Next Concert**\n\n**«Sunny Dreams»**\n\n📅 **Date:** May 3\n📍 **Location:** CC Ordzhonikidzevsky, Kultury st, 3 | Yekaterinburg\n🚪 **Doors:** 19:00\n\n🎟️ **Tickets:** [Buy ticket](https://t.me/QticketsBuyBot/buy?startapp=220348)\n\n✨ We are waiting for you! 🔥\n\n💫 *Subscribe to our Telegram channel:*\nhttps://t.me/w0cxod",
        "share_info": "📸 **How to share a quote in Stories?**\n\n1️⃣ Copy the quote (tap and hold on the text)\n2️⃣ Open your social network\n3️⃣ Paste the text into Stories\n4️⃣ Add background, stickers, or our music\n5️⃣ Tag us\n\nWe will definitely watch and repost the best ones! 🔥",
        "settings_text": "⚙️ **Settings**\n\nCurrent language: 🇬🇧 English\n\nHere you can manage your newsletter subscription and bot language.",
        
        # Тексты для рассылки
        "newsletter_menu": "📨 **Newsletter Management**\n\n{sub_status}\n\nDo you want to change your status?",
        "btn_inline_sub": "🔔 Subscribe",
        "btn_inline_unsub": "🔕 Unsubscribe",
        "status_sub": "✅ **You are subscribed to the newsletter**",
        "status_unsub": "❌ **You are unsubscribed from the newsletter**",
        "toast_sub": "Successfully subscribed!",
        "toast_unsub": "You have unsubscribed.",
        
        "main_menu_prompt": "🎵 **Main Menu**\n\nChoose an action:",
        "merch_catalog": "🛍️ **Voskhod Merch Catalog**\n\nChoose a product category:\n\n• ⚫ Patches — from 450 ₽\n• 📿 Bracelets — 200 ₽\n• 🔘 Pins — 150 ₽\n• 🌅 Stickers — 150 ₽\n• 💌 Postcards — 100 ₽\n\n📩 For orders, text @wocx0d\n\n⚡ *Prices do not include shipping costs*",
        "contact_manager": "📩 Contact Manager",
        "back_to_catalog": "◀️ Back to catalog",
        "btn_patches": "⚫ Patches",
        "btn_bracelets": "📿 Bracelets",
        "btn_pins": "🔘 Pins",
        "btn_stickers": "🌅 Stickers",
        "btn_postcards": "💌 Postcards",
        "item_not_found": "Item not found",
        "price": "💰 **Price:**",
        "order_prompt": "📩 **To order:** message @wocx0d\nSpecify the item name and quantity.\n\n⚡ *Price does not include shipping*",
        "promo_concert": "🎫 **By the way!** We have a concert in Yekaterinburg soon!\n\n📅 May 3 | 🏢 CC Ordzhonikidzevsky\nClick «🎫 Next Concert» in the main menu!",
        "promo_presave": "🎵 **By the way!** We are preparing a new track «Music of Love»!\n\n🔥 Presave now: [Presave](https://band.link/musiquedamour)",
        "presave_msg": "🎁 **«Music of Love» — coming April 8!** 🎁\n\n✨ **Presave it now:**\n→ The track will drop into your playlist automatically\n→ No need to search on release day\n→ It's free and takes 10 seconds\n\nYour support is very valuable to us!\n\n🔗 [Presave here]({url})\n\n💝 Share the link with friends!",
        "listen_stream": "🎵 **{title}**\n\nListen on streaming platforms:\n🔗 [Song Page]({url})\n\n✨ Share this song with your friends!\n\n",
        "choose_lang": "🌐 Выберите язык / Choose language:",
        "lang_changed": "✅ Language successfully changed to English!"
    }
}

# ========== РАБОТА С ПОЛЬЗОВАТЕЛЯМИ ==========

def load_users():
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list): # Миграция со старой версии
                    return {str(uid): {"lang": "ru", "sub": True} for uid in data}
                return data
        except:
            return {}
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
    if kwargs:
        return text.format(**kwargs)
    return text

# ========== ДАННЫЕ МЕРЧА ==========

MERCH_IMAGES = {
    "patch_white": "merch_images/patch_white.jpg",
    "patch_black": "merch_images/patch_black.jpg",
    "patch_color": "merch_images/patch_color.jpg",
    "bracelet": "merch_images/bracelet.jpg",
    "sticker_set1": "merch_images/sticker_set1.jpg",
    "sticker_set2": "merch_images/sticker_set2.jpg",
    "pin_logo_black": "merch_images/pin_logo_black.jpg",
    "pin_logo_white": "merch_images/pin_logo_white.jpg",
    "pin_stepa": "merch_images/pin_stepa.jpg",
    "pin_danya": "merch_images/pin_danya.jpg",
    "pin_liza": "merch_images/pin_liza.jpg",
    "pin_kirya": "merch_images/pin_kirya.jpg",
    "pin_lenya": "merch_images/pin_lenya.jpg",
    "pin_love": "merch_images/pin_love.jpg",
    "pin_oda": "merch_images/pin_oda.jpg",
    "postcard": "merch_images/postcard.jpg",
}

MERCH_ITEMS = {
    "patch_white": {"name": {"ru": "⚪ Нашивка белая", "en": "⚪ White Patch"}, "price": 450, "desc": {"ru": "Белая нашивка с логотипом группы. Диаметр: 6 см.", "en": "White patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "patch_black": {"name": {"ru": "⚫ Нашивка черная", "en": "⚫ Black Patch"}, "price": 450, "desc": {"ru": "Черная нашивка с логотипом группы. Диаметр: 6 см.", "en": "Black patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "patch_color": {"name": {"ru": "🟣 Нашивка цветная", "en": "🟣 Color Patch"}, "price": 600, "desc": {"ru": "Цветная нашивка с логотипом группы. Диаметр: 6 см.", "en": "Color patch with band logo. Diameter: 6 cm."}, "category": "patches"},
    "bracelet": {"name": {"ru": "📿 Браслет", "en": "📿 Bracelet"}, "price": 200, "desc": {"ru": "Браслет силиконовый подростковый (180×12×2мм, Ø57 мм).", "en": "Teen silicone bracelet (180×12×2mm, Ø57 mm)."}, "category": "bracelets"},
    "sticker_set1": {"name": {"ru": "🌅 Наклейки (набор 1)", "en": "🌅 Stickers (Set 1)"}, "price": 150, "desc": {"ru": "Наклейки с обложками и участниками группы Восход. Размер: А6", "en": "Stickers with covers and band members. Size: A6"}, "category": "stickers"},
    "sticker_set2": {"name": {"ru": "🌅 Наклейки (набор 2)", "en": "🌅 Stickers (Set 2)"}, "price": 150, "desc": {"ru": "Наклейки с обложками и участниками группы Восход. Размер: А6", "en": "Stickers with covers and band members. Size: A6"}, "category": "stickers"},
    "pin_logo_black": {"name": {"ru": "🔘 Значок логотип черный", "en": "🔘 Black Logo Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_logo_white": {"name": {"ru": "🔘 Значок логотип белый", "en": "🔘 White Logo Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_stepa": {"name": {"ru": "🔘 Значок Стёпа", "en": "🔘 Stepa Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_danya": {"name": {"ru": "🔘 Значок Музыcan't", "en": "🔘 Musican't Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_liza": {"name": {"ru": "🔘 Значок Lizzy", "en": "🔘 Lizzy Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_kirya": {"name": {"ru": "🔘 Значок Kirya Kote", "en": "🔘 Kirya Kote Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_lenya": {"name": {"ru": "🔘 Значок Лёня", "en": "🔘 Lenya Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_love": {"name": {"ru": "🔘 Значок «Любовь...»", "en": "🔘 Love Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "pin_oda": {"name": {"ru": "🔘 Значок «Ода»", "en": "🔘 Oda Pin"}, "price": 150, "desc": {"ru": "Металлический значок. Диаметр: 37 мм.", "en": "Metal pin. Diameter: 37 mm."}, "category": "pins"},
    "postcard": {"name": {"ru": "💌 Авторская открытка", "en": "💌 Postcard"}, "price": 100, "desc": {"ru": "Открытки с логотипом группы. Размер: А5", "en": "Postcards with band logo. Size: A5"}, "category": "postcards"},
}

# ========== КЛАВИАТУРЫ ==========

def main_reply_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text=get_text(user_id, "btn_quote")), KeyboardButton(text=get_text(user_id, "btn_songs"))],
        [KeyboardButton(text=get_text(user_id, "btn_merch")), KeyboardButton(text=get_text(user_id, "btn_concert"))],
        [KeyboardButton(text=get_text(user_id, "btn_share")), KeyboardButton(text=get_text(user_id, "btn_settings"))]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def settings_keyboard(user_id: int):
    buttons = [
        [KeyboardButton(text=get_text(user_id, "btn_newsletter"))],
        [KeyboardButton(text=get_text(user_id, "btn_lang"))],
        [KeyboardButton(text=get_text(user_id, "btn_main"))]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def catalog_main_keyboard(user_id: int):
    buttons = [
        [InlineKeyboardButton(text=get_text(user_id, "btn_patches"), callback_data="category_patches")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_bracelets"), callback_data="merch_bracelet")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_pins"), callback_data="category_pins")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_stickers"), callback_data="category_stickers")],
        [InlineKeyboardButton(text=get_text(user_id, "btn_postcards"), callback_data="merch_postcard")],
        [InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def category_items_keyboard(user_id: int, category: str):
    lang = get_user_lang(user_id)
    items = [item_id for item_id, item in MERCH_ITEMS.items() if item.get("category") == category]
    buttons = []
    for item_id in items:
        item = MERCH_ITEMS[item_id]
        buttons.append([InlineKeyboardButton(text=f"{item['name'][lang]} — {item['price']} ₽", callback_data=f"view_{item_id}")])
    buttons.append([InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")])
    buttons.append([InlineKeyboardButton(text=get_text(user_id, "back_to_catalog"), callback_data="back_to_catalog")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def songs_inline_keyboard(user_id: int, page: int = 0):
    display_songs = [PRESAVE_SONG] + SONGS
    start_idx = page * ITEMS_PER_PAGE
    end_idx = min(start_idx + ITEMS_PER_PAGE, len(display_songs))
    buttons = []
    for i in range(start_idx, end_idx):
        song = display_songs[i]
        button_text = f"🎁 {song['title']}" if song.get("is_presave") else f"🎵 {song['title']}"
        buttons.append([InlineKeyboardButton(text=button_text, callback_data=f"play_song_{i}")])
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(InlineKeyboardButton(text=get_text(user_id, "btn_prev"), callback_data=f"songs_page_{page - 1}"))
    if end_idx < len(display_songs):
        nav_buttons.append(InlineKeyboardButton(text=get_text(user_id, "btn_next"), callback_data=f"songs_page_{page + 1}"))
    if nav_buttons:
        buttons.append(nav_buttons)
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========

async def show_item(callback: types.CallbackQuery, item_id: str):
    user_id = callback.from_user.id
    lang = get_user_lang(user_id)
    item = MERCH_ITEMS.get(item_id)
    
    if not item:
        await callback.answer(get_text(user_id, "item_not_found"))
        return
        
    image_path = MERCH_IMAGES.get(item_id)
    text = (
        f"🛍️ **{item['name'][lang]}**\n\n"
        f"{item['desc'][lang]}\n\n"
        f"{get_text(user_id, 'price')} {item['price']} ₽\n\n"
        f"{get_text(user_id, 'order_prompt')}"
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text(user_id, "contact_manager"), url="https://t.me/wocx0d")],
        [InlineKeyboardButton(text=get_text(user_id, "back_to_catalog"), callback_data="back_to_catalog")]
    ])
    
    try:
        photo = FSInputFile(image_path)
        await callback.message.delete()
        await callback.message.answer_photo(photo=photo, caption=text, reply_markup=keyboard, parse_mode="Markdown")
    except Exception:
        await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    await callback.answer()

async def send_random_promotion(message: types.Message):
    user_id = message.from_user.id
    if random.choice([True, False]):
        await message.answer(get_text(user_id, "promo_concert"), parse_mode="Markdown")
    else:
        await message.answer(get_text(user_id, "promo_presave"), parse_mode="Markdown", disable_web_page_preview=True)

# ========== ОБРАБОТЧИКИ КОМАНД ==========

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_id = message.from_user.id
    get_user_lang(user_id) 
    await message.answer(get_text(user_id, "welcome"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

@dp.message(Command("send_all"))
async def send_to_all(message: types.Message):
    if message.from_user.id not in ADMINS: return
    text = message.text.replace("/send_all", "").strip() if message.text else message.caption.replace("/send_all", "").strip() if message.caption else ""
    if not text and not message.photo:
        await message.answer("❌ Отправь текст или фото с подписью.")
        return
    status_msg = await message.answer(f"📤 Начинаю рассылку...")
    success, failed = 0, 0
    for uid, data in users.items():
        if not data.get("sub", True): continue # Пропускаем отписавшихся
        try:
            if message.photo:
                await bot.send_photo(uid, photo=message.photo[-1].file_id, caption=text, parse_mode="Markdown")
            else:
                await bot.send_message(uid, text, parse_mode="Markdown")
            success += 1
            await asyncio.sleep(0.05)
        except Exception: failed += 1
    await status_msg.edit_text(f"✅ Рассылка завершена!\n📤 Отправлено: {success}\n❌ Ошибок: {failed}")

# ========== ОБРАБОТЧИКИ ТЕКСТОВЫХ КНОПОК ==========

@dp.message(F.text.in_([LEXICON["ru"]["btn_quote"], LEXICON["en"]["btn_quote"]]))
async def get_quote_reply(message: types.Message):
    user_id = message.from_user.id
    quote = random.choice(QUOTES) 
    response = get_text(user_id, "quote_prefix") + quote + get_text(user_id, "quote_suffix")
    await message.answer(response, reply_markup=main_reply_keyboard(user_id))
    
    quote_counter[user_id] = quote_counter.get(user_id, 0) + 1
    if quote_counter[user_id] % 5 == 0:
        await send_random_promotion(message)

@dp.message(F.text.in_([LEXICON["ru"]["btn_songs"], LEXICON["en"]["btn_songs"]]))
async def list_songs_reply(message: types.Message):
    user_id = message.from_user.id
    count = 1 + len(SONGS)
    total = (count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
    text = get_text(user_id, "songs_list", page=1, total=total, count=count)
    await message.answer(text, reply_markup=songs_inline_keyboard(user_id, 0), parse_mode="Markdown")

@dp.message(F.text.in_([LEXICON["ru"]["btn_concert"], LEXICON["en"]["btn_concert"]]))
async def concert_info(message: types.Message):
    user_id = message.from_user.id
    caption = get_text(user_id, "concert_info")
    try:
        photo = FSInputFile("Afisha.jpg")
        await message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown")
    except:
        await message.answer(caption, parse_mode="Markdown")

@dp.message(F.text.in_([LEXICON["ru"]["btn_merch"], LEXICON["en"]["btn_merch"]]))
async def merch_catalog(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")

@dp.message(F.text.in_([LEXICON["ru"]["btn_share"], LEXICON["en"]["btn_share"]]))
async def how_to_share_reply(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "share_info"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

@dp.message(F.text.in_([LEXICON["ru"]["btn_settings"], LEXICON["en"]["btn_settings"]]))
async def settings_menu(message: types.Message):
    user_id = message.from_user.id
    text = get_text(user_id, "settings_text")
    await message.answer(text, reply_markup=settings_keyboard(user_id), parse_mode="Markdown")

# ========== НАСТРОЙКИ: РАССЫЛКА ==========
@dp.message(F.text.in_([LEXICON["ru"]["btn_newsletter"], LEXICON["en"]["btn_newsletter"]]))
async def newsletter_menu(message: types.Message):
    user_id = message.from_user.id
    uid_str = str(user_id)
    is_sub = users.get(uid_str, {}).get("sub", True)
    
    sub_status = get_text(user_id, "status_sub") if is_sub else get_text(user_id, "status_unsub")
    text = get_text(user_id, "newsletter_menu", sub_status=sub_status)
    
    btn_text = get_text(user_id, "btn_inline_unsub") if is_sub else get_text(user_id, "btn_inline_sub")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, callback_data="toggle_sub")]
    ])
    
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

@dp.callback_query(Text("toggle_sub"))
async def process_toggle_sub(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    uid_str = str(user_id)
    
    # Меняем статус подписки на противоположный
    current_status = users.get(uid_str, {}).get("sub", True)
    users[uid_str]["sub"] = not current_status
    save_users()
    
    is_sub = users[uid_str]["sub"]
    
    # Обновляем сообщение
    sub_status = get_text(user_id, "status_sub") if is_sub else get_text(user_id, "status_unsub")
    text = get_text(user_id, "newsletter_menu", sub_status=sub_status)
    
    btn_text = get_text(user_id, "btn_inline_unsub") if is_sub else get_text(user_id, "btn_inline_sub")
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=btn_text, callback_data="toggle_sub")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="Markdown")
    
    # Всплывающее уведомление (Toast)
    toast_msg = get_text(user_id, "toast_sub") if is_sub else get_text(user_id, "toast_unsub")
    await callback.answer(toast_msg)

# ========== НАСТРОЙКИ: ЯЗЫК ==========
@dp.message(F.text.in_([LEXICON["ru"]["btn_lang"], LEXICON["en"]["btn_lang"]]))
async def change_lang_menu(message: types.Message):
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇺🇸 English", callback_data="lang_en")]
    ])
    await message.answer(get_text(user_id, "choose_lang"), reply_markup=keyboard)

@dp.callback_query(Text(startswith="lang_"))
async def process_lang_change(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    new_lang = callback.data.split("_")[1]
    
    uid_str = str(user_id)
    if uid_str not in users: users[uid_str] = {}
    users[uid_str]["lang"] = new_lang
    save_users()
    
    await callback.message.delete()
    await callback.message.answer(get_text(user_id, "lang_changed"), reply_markup=main_reply_keyboard(user_id))
    await callback.answer()

@dp.message(F.text.in_([LEXICON["ru"]["btn_main"], LEXICON["en"]["btn_main"]]))
async def back_to_menu(message: types.Message):
    user_id = message.from_user.id
    await message.answer(get_text(user_id, "main_menu_prompt"), reply_markup=main_reply_keyboard(user_id), parse_mode="Markdown")

# ========== ОБЩИЙ ОБРАБОТЧИК INLINE-КНОПОК ==========

@dp.callback_query()
async def handle_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    
    if callback.data == "back_to_catalog":
        try:
            await callback.message.edit_text(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")
        except:
            await callback.message.delete()
            await callback.message.answer(get_text(user_id, "merch_catalog"), reply_markup=catalog_main_keyboard(user_id), parse_mode="Markdown")
        await callback.answer()
        return
    
    elif callback.data == "category_patches":
        await callback.message.edit_text(f"⚫ **{get_text(user_id, 'btn_patches').replace('⚫ ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "patches"), parse_mode="Markdown")
    elif callback.data == "merch_bracelet":
        await show_item(callback, "bracelet")
    elif callback.data == "category_pins":
        await callback.message.edit_text(f"🔘 **{get_text(user_id, 'btn_pins').replace('🔘 ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "pins"), parse_mode="Markdown")
    elif callback.data == "category_stickers":
        await callback.message.edit_text(f"🌅 **{get_text(user_id, 'btn_stickers').replace('🌅 ', '')}**\n\n", reply_markup=category_items_keyboard(user_id, "stickers"), parse_mode="Markdown")
    elif callback.data == "merch_postcard":
        await show_item(callback, "postcard")
    
    elif callback.data.startswith("view_"):
        item_id = callback.data.replace("view_", "")
        await show_item(callback, item_id)
    
    elif callback.data.startswith("show_songs_") or callback.data.startswith("songs_page_"):
        page = int(callback.data.split("_")[2])
        count = 1 + len(SONGS)
        total = (count + ITEMS_PER_PAGE - 1) // ITEMS_PER_PAGE
        text = get_text(user_id, "songs_list", page=page+1, total=total, count=count)
        await callback.message.edit_text(text, reply_markup=songs_inline_keyboard(user_id, page), parse_mode="Markdown")
    
    elif callback.data.startswith("play_song_"):
        song_index = int(callback.data.split("_")[2])
        all_songs = [PRESAVE_SONG] + SONGS
        if song_index < len(all_songs):
            song = all_songs[song_index]
            if song.get("is_presave"):
                text = get_text(user_id, "presave_msg", url=song['url'])
            else:
                text = get_text(user_id, "listen_stream", title=song['title'], url=song['url'])
                
            after_play_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text=get_text(user_id, "btn_songs"), callback_data="show_songs_0")]
            ])
            await callback.message.answer(text, reply_markup=after_play_keyboard, parse_mode="Markdown")
            
    await callback.answer()

@dp.message()
async def any_message(message: types.Message):
    if not message.text.startswith('/'):
        user_id = message.from_user.id
        await message.answer("👋", reply_markup=main_reply_keyboard(user_id))

# ========== ЗАПУСК ==========

async def main():
    print("🚀 Бот запускается...")
    print(f"👥 Загружено пользователей: {len(users)}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

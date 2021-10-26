import logging

from telegram import Update, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import data_scraping
import datetime

from src.constants import (
    hand_emoji,
    MENU, TOPS_SUBMENU, TOPS_QUESTION, PLATFORM_SUBMENU, PLATFORM_QUESTION, PLAYSTATION_SUBMENU,
    greetings_text, using_buttons_text, select_top_text, select_platform_text,
    want_see_tops_text, want_see_platforms_text, help_text,
    keyboard_MENU, keyboard_TOPS, keyboard_PLATFORMS, keyboard_QUESTION_TOPS,
    keyboard_QUESTION_PLATFORMS, keyboard_ON_GAME, keyboard_PLAYSTATION_SUBMENU, keyboard_XBOX_SUBMENU, XBOX_SUBMENU,
)

# Логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    """Отправить сообщение на `/start`."""
    user = update.message.from_user.full_name
    logger.info("User <%s> started the conversation.", user)
    update.message.reply_text(
        hand_emoji + fr'Привет, {user}!'
    )
    update.message.reply_text(greetings_text)
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Отправка сообщения с текстом и добавлением InlineKeyboard
    update.message.reply_text(using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU


def start_over(update: Update, context: CallbackContext) -> int:
    """Выдает тот же текст и клавиатуру, что и `start`, но не как новое сообщение"""
    # Получить запрос обратного вызова из обновления
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    # Вместо отправки нового сообщения редактируем сообщение, которое
    # породило запрос обратного вызова.
    query.edit_message_text(text=using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU


def tops(update: Update, context: CallbackContext) -> int:
    """Показать кнопоки топов видеоигр"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_TOPS)
    query.edit_message_text(text=select_top_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние TOPS_SUBMENU
    return TOPS_SUBMENU


def platforms(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора платформы"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLATFORMS)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние PLATFORM_SUBMENU
    return PLATFORM_SUBMENU


def current_year(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр этого года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)

    top___by_year = data_scraping.get_top_5_by_year(datetime.datetime.now().year)
    out_text = ''
    for game in top___by_year[:5]:
        out_text += game.get_string_without_date() + "\n"
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def year_2020(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр 2020 года, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)
    top___by_last_year = data_scraping.get_top_5_by_year(datetime.datetime.now().year - 1)
    out_text = ''
    for game in top___by_last_year[:5]:
        out_text += game.get_string_without_date() + "\n"
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def decade(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр десятилетия, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_TOPS)
    top___by_year_decade = data_scraping.get_top_50_for_decade()
    out_text = ''
    for game in top___by_year_decade[:10]:
        out_text += game.get_string_without_date() + "\n"
    query.edit_message_text(
        text=out_text + want_see_tops_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние TOPS_QUESTION
    return TOPS_QUESTION


def pc_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на PC, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. OPUS: Echo of Starsong\n' +
        'METASCORE: 91\n\n' +
        '2. Psychonauts 2\n' +
        'METASCORE: 89\n\n' +
        '3. Streets of Rage 4: Mr. X Nightmare\n' +
        'METASCORE: 88\n\n' +
        '4. Deathloop\n' +
        'METASCORE: 88\n\n' +
        '5. Townscaper\n' +
        'METASCORE: 86\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def playstation_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Playstation"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_PLAYSTATION_SUBMENU)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние PLAYSTATION_SUBMENU
    return PLAYSTATION_SUBMENU


def ps4_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation 4, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Synth Riders\n' +
        'METASCORE: 89\n\n' +
        '2. Quake Remastered\n' +
        'METASCORE: 88\n\n' +
        '3. Psychonauts 2\n' +
        'METASCORE: 87\n\n' +
        '4. Flynn: Son of Crimson\n' +
        'METASCORE: 85\n\n' +
        '5. Castlevania Advance Collection\n' +
        'METASCORE: 84\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def ps5_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Playstation 5, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Hades\n' +
        'METASCORE: 93\n\n' +
        '2. Deathloop\n' +
        'METASCORE: 88\n\n' +
        '3. Ghost of Tsushima: Director\'s Cut\n' +
        'METASCORE: 88\n\n' +
        '4. Bonfire Peaks\n' +
        'METASCORE: 88\n\n' +
        '5. Tales of Arise\n' +
        'METASCORE: 87\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_func(update: Update, context: CallbackContext) -> int:
    """Показать кнопки выбора Xbox"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_XBOX_SUBMENU)
    query.edit_message_text(text=select_platform_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние XBOX_SUBMENU
    return XBOX_SUBMENU


def xbox_one_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox One, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Psychonauts 2\n' +
        'METASCORE: 91\n\n' +
        '2. The Forgotten City\n' +
        'METASCORE: 88\n\n' +
        '3. UnMetal\n' +
        'METASCORE: 87\n\n' +
        '4. Sam & Max Save the World Remastered\n' +
        'METASCORE: 84\n\n' +
        '5. Insurgency: Sandstorm\n' +
        'METASCORE: 84\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def xbox_series_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Xbox Series X, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. Hades\n' +
        'METASCORE: 93\n\n' +
        '2. Microsoft Flight Simulator\n' +
        'METASCORE: 90\n\n' +
        '3. Fuga: Melodies of Steel\n' +
        'METASCORE: 89\n\n' +
        '4. Psychonauts 2\n' +
        'METASCORE: 87\n\n' +
        '5. Tales of Arise\n' +
        'METASCORE: 87\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def switch_func(update: Update, context: CallbackContext) -> int:
    """Информация по топу игр на Switch, затем показать новый выбор кнопок"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_QUESTION_PLATFORMS)
    # Здесь будет запрос данных с метакритики, пока что хардкод
    query.edit_message_text(
        text=
        '1. A Monster\'s Expedition\n' +
        'METASCORE: 92\n\n' +
        '2. Spelunky 2\n' +
        'METASCORE: 92\n\n' +
        '3. Streets of Rage 4: Mr. X Nightmare\n' +
        'METASCORE: 88\n\n' +
        '4. Metroid Dread\n' +
        'METASCORE: 88\n\n' +
        '5. Quake Remastered\n' +
        'METASCORE: 87\n\n' +
        want_see_platforms_text,
        reply_markup=reply_markup_keyboard
    )
    # Переход в состояние PLATFORM_QUESTION
    return PLATFORM_QUESTION


def help_func(update: Update, context: CallbackContext):
    """Возвращает информацию о всех командах и функциях"""
    update.message.reply_text(text=help_text)


def echo_func(update: Update, context: CallbackContext):
    """Возвращает введенное сообщение"""
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_ON_GAME)
    text = update.message.text
    update.message.reply_text(text, reply_markup=reply_markup_keyboard)


def new_start(update: Update, context: CallbackContext):
    """Возвращает текст и клавиатуру к главному меню"""
    query = update.callback_query
    query.answer()
    reply_markup_keyboard = InlineKeyboardMarkup(keyboard_MENU)
    query.edit_message_text(text=using_buttons_text, reply_markup=reply_markup_keyboard)
    # Переход в состояние MENU
    return MENU

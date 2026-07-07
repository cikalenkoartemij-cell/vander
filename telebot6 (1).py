import telebot
from telebot import types
import requests
BOT_TOKEN = '8485436590:AAHupnyMNXxM3UaCcET5RExoC9qIcrXJEyM'
API_KEY = "67fbbb0011f824754dacfcc8"
bot = telebot.TeleBot(BOT_TOKEN)
user_data = {}
strings = {
    'ru': {
        'lang_select': "Выберите язык / Choose language:",
        'start': "Привет! Выбери исходную валюту:",
        'target': "Выбрано: {}. Теперь выбери целевую валюту:",
        'options': "Переводим из {} в {}. Что вы хотите сделать?",
        'btn_get_rate': "📈 Просто узнать курс",
        'enter_amount': "Введите сумму для конвертации:",
        'result_rate': "📊 Курс: **1 {} = {:.4f} {}**",
        'result_total': "✅ {} {} = **{:.2f} {}**",
        'error_api': "❌ Ошибка получения курса.",
        'error_num': "⚠️ Введите число (например, 100 или 50.5)",
        'restart': "Нажмите /start для нового расчета.",
        'help': "Пропишите /start для начала работы."
    },
    'en': {
        'lang_select': "Choose language / Выберите язык:",
        'start': "Hello! Choose the base currency:",
        'target': "Selected: {}. Now choose the target currency:",
        'options': "Converting from {} to {}. What would you like to do?",
        'btn_get_rate': "📈 Just get the rate",
        'enter_amount': "Enter the amount to convert:",
        'result_rate': "📊 Rate: **1 {} = {:.4f} {}**",
        'result_total': "✅ {} {} = **{:.2f} {}**",
        'error_api': "❌ Error getting exchange rate.",
        'error_num': "⚠️ Please enter a number (e.g., 100 or 50.5)",
        'restart': "Press /start to try again.",
        'help': "Type /start to begin."
    }
}

def get_exchange_rate(base, target):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base.upper()}'
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        if response.status_code == 200:
            return data['conversion_rates'].get(target.upper())
    except Exception as e:
        print(f"Ошибка API: {e}")
    return None
def main_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    btns = [types.KeyboardButton(s) for s in ['USD', 'EUR', 'KZT', 'RUB', 'GBP', 'JPY']]
    markup.add(*btns)
    return markup
def options_markup(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(strings[lang]['btn_get_rate']))
    return markup
def lang_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("Русский 🇷🇺", callback_data="lang_ru"),
        types.InlineKeyboardButton("English 🇺🇸", callback_data="lang_en")
    )
    return markup
@bot.message_handler(commands=['start'])
def start(message):
    user_data[message.chat.id] = {}
    bot.send_message(message.chat.id, strings['ru']['lang_select'], reply_markup=lang_markup())


@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def callback_lang(call):
    lang_code = call.data.split('_')[1]
    user_data[call.message.chat.id] = {'lang': lang_code}
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, strings[lang_code]['start'], reply_markup=main_markup())


@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    if chat_id not in user_data or 'lang' not in user_data[chat_id]:
        bot.send_message(chat_id, "Нажми /start")
        return

    lang = user_data[chat_id]['lang']
    text = message.text

    if 'from' not in user_data[chat_id]:
        user_data[chat_id]['from'] = text.upper()
        bot.send_message(chat_id, strings[lang]['target'].format(text.upper()), reply_markup=main_markup())

    elif 'to' not in user_data[chat_id]:
        user_data[chat_id]['to'] = text.upper()
        bot.send_message(
            chat_id,
            strings[lang]['options'].format(user_data[chat_id]['from'], text.upper()),
            reply_markup=options_markup(lang)
        )

    else:
        base = user_data[chat_id]['from']
        target = user_data[chat_id]['to']

        if text == strings[lang]['btn_get_rate']:
            rate = get_exchange_rate(base, target)
            if rate:
                bot.send_message(chat_id, strings[lang]['result_rate'].format(base, rate, target),
                                 parse_mode='Markdown')
                bot.send_message(chat_id, strings[lang]['enter_amount'], reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(chat_id, strings[lang]['error_api'])

        else:
            try:
                amount = float(text.replace(',', '.'))
                rate = get_exchange_rate(base, target)
                if rate:
                    res = amount * rate
                    bot.send_message(chat_id, strings[lang]['result_total'].format(amount, base, res, target),
                                     parse_mode='Markdown')
                    user_data[chat_id] = {'lang': lang}
                    bot.send_message(chat_id, strings[lang]['restart'])
                else:
                    bot.send_message(chat_id, strings[lang]['error_api'])
            except ValueError:
                bot.send_message(chat_id, strings[lang]['error_num'])


if __name__ == '__main__':
    bot.polling(none_stop=True)
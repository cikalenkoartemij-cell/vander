import sys
import re
import telebot
from telebot import types
if len(sys.argv) > 1:
    BOT_TOKEN = sys.argv[1]
else:
    BOT_TOKEN = "8982275673:AAHJgbo_uENnFMEbxJxMytkz73FZYKNs3Go"

bot = telebot.TeleBot(BOT_TOKEN)
INFO_ABOUT = "🙋‍♂️ Меня зовут Артем. Мне 15 лет. Я с города Уральск. Пишу на Python, изучаю Django. Мой юз - @achievementTTT"
INFO_GOAL = "🎯 Моя цель — стать Middle Backend разработчиком в будущем."
INFO_HISTORY = ("🚀 В IT я пришел через интерес к созданию игр, программ. С раннего детства любил смотреть фильмы про хакеров, про роботов и технологии. Где то в 12-13 лет я пошел на бесплатные курсы по пайтону но мне там не понравилось(оно и понятно курсы то бесплатные были) и как то забил на программирование. Этой зимой я сходил на форум CapEducation и я сразу понял, что это то что мне надо. И по сегодняшний день я обучаюсь в этой онлайн школе мне все нравится. Благодаря этой школе я научился писать сложные коды и самое главное понимать что я делаю")
INFO_MENTOR = "🧠 Мой ментор — куратор и учитель курса, которые научили меня правильно программировать и писать чистый код."
INFO_PROGRESS = "📈 Точка А: Знал циклы, мог создать простенькую программку например: калькулятор.\n📈 Точка Б: Пишу ботов, создаю игры и в данный момент изучаю веб-фрейморк Django."
INFO_HOBBY = "🎸 В свободное время я гуляю, играю в игры(cs2 и Majestic RP) и люблю поспать."
INFO_PROJECTS = "💻 Мои работы:\n1. Игра на Pygame( Dino ) - https://capeducation.getcourse.ru/pl/teach/control/lesson/view?id=335941303&editMode=0\n2.Телеграмм бот для конвертации валют - https://capeducation.getcourse.ru/pl/teach/control/lesson/view?id=336194357&editMode=0\n3. Симмуляция банкомата - https://capeducation.getcourse.ru/pl/teach/control/lesson/view?id=335941292&editMode=0"
INFO_GITHUB = "🌐 Мой GitHub с проектами: https://github.com/cikalenkoartemij-cell"
waiting_for_email = {}
def get_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("ℹ️ О себе", "🎯 Моя цель")
    markup.add("🚀 История", "🧠 Ментор")
    markup.add("📈 Прогресс", "🎸 Хобби")
    markup.add("💻 Работы", "🌐 GitHub")
    return markup
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я бот-портфолио. Выбери пункт меню:",
        reply_markup=get_menu()
    )
@bot.message_handler(func=lambda msg: True)
def handle_text(message):
    text = message.text
    chat_id = message.chat.id
    if text == "ℹ️ О себе":
        bot.send_message(chat_id, INFO_ABOUT)
    elif text == "🎯 Моя цель":
        bot.send_message(chat_id, INFO_GOAL)
    elif text == "🚀 История":
        bot.send_message(chat_id, INFO_HISTORY)
    elif text == "🧠 Ментор":
        bot.send_message(chat_id, INFO_MENTOR)
    elif text == "📈 Прогресс":
        bot.send_message(chat_id, INFO_PROGRESS)
    elif text == "🎸 Хобби":
        bot.send_message(chat_id, INFO_HOBBY)
    elif text == "💻 Работы":
        bot.send_message(chat_id, INFO_PROJECTS)
    elif text == "🌐 GitHub":
        bot.send_message(chat_id, INFO_GITHUB)
    else:
        bot.send_message(chat_id, "⚠️ Неизвестная команда. Пожалуйста, выберите пункт на кнопках или напишите /start")
if __name__ == "__main__":
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
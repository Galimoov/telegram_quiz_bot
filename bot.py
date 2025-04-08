from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# 🔐 Токен бота
TOKEN = '7825832074:AAG4ToVxI0ywTuBeOeN6jS3XCfXCZLa4rdA'

# 📚 Вопросы квиза
quiz = [
    {
        'question': 'Что такое unit-тестирование?',
        'options': ['Тестирование интерфейса', 'Тестирование отдельных модулей', 'Регрессионное тестирование'],
        'answer': 'Тестирование отдельных модулей'
    },
    {
        'question': 'Что такое баг-репорт?',
        'options': ['Описание ошибки', 'Отчёт о тестировании', 'План тестирования'],
        'answer': 'Описание ошибки'
    }
]

user_answers = {}

# 🟢 Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_answers[user_id] = {'current': 0, 'score': 0}

    await send_question(update, context)

# 🧠 Отправка вопроса
async def send_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    current = user_answers[user_id]['current']
    
    if current < len(quiz):
        q = quiz[current]
        reply_markup = ReplyKeyboardMarkup.from_column(q['options'], resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(f"Вопрос {current + 1}: {q['question']}", reply_markup=reply_markup)
    else:
        score = user_answers[user_id]['score']
        await update.message.reply_text(f"Квиз окончен! Ты набрал {score} из {len(quiz)}.")
        del user_answers[user_id]

# ✅ Обработка ответов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_answers:
        await update.message.reply_text("Напиши /start чтобы начать квиз.")
        return

    current = user_answers[user_id]['current']
    answer = update.message.text
    correct_answer = quiz[current]['answer']

    if answer == correct_answer:
        user_answers[user_id]['score'] += 1
        await update.message.reply_text("✅ Верно!")
    else:
        await update.message.reply_text(f"❌ Неверно. Правильный ответ: {correct_answer}")

    user_answers[user_id]['current'] += 1
    await send_question(update, context)

# 🚀 Запуск бота
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен! Ожидаю пользователей...")
    app.run_polling()


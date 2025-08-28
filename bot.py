import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Отримуємо токени з Environment Variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! 👋 Я твій бот на основі ChatGPT. Можеш писати мені будь-які повідомлення!")

# Обробка текстових повідомлень через OpenAI
async def chat_with_gpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-mini",  # можна замінити на gpt-4 або gpt-3.5-turbo
            messages=[
                {"role": "system", "content": "Ти ввічливий помічник."},
                {"role": "user", "content": user_text}
            ]
        )
        answer = response['choices'][0]['message']['content']
    except Exception as e:
        answer = "Вибач, сталася помилка при обробці твоєї відповіді."

    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Команди
    app.add_handler(CommandHandler("start", start))
    # Повідомлення
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    print("✅ Бот запущено. Очікую повідомлення...")
    app.run_polling()

if __name__ == "__main__":
    main()

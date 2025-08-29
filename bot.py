import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI
import os

# ЛОГІНГ для дебагу
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# БЕРЕМО КЛЮЧІ
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")  # твій Telegram-токен
OPENAI_KEY = os.getenv("OPENAI_API_KEY")  # твій OpenAI API-ключ

# СТВОРЮЄМО КЛІЄНТА OpenAI
client = OpenAI(api_key=OPENAI_KEY)


# /start команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Я твій AI-бот. Напиши мені щось 😉")


# ОБРОБКА ВСІХ ПОВІДОМЛЕНЬ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # ВИКЛИК OpenAI
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти дружній Telegram-бот."},
                {"role": "user", "content": user_message},
            ],
            max_tokens=300,
            temperature=0.7,
        )

        reply = response.choices[0].message.content
        await update.message.reply_text(reply)

    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        await update.message.reply_text("⚠️ Вибач, сталася помилка при обробці твоєї відповіді.")


# ГОЛОВНА ФУНКЦІЯ
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Команди
    app.add_handler(CommandHandler("start", start))

    # Всі повідомлення
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск
    app.run_polling()


if __name__ == "__main__":
    main()

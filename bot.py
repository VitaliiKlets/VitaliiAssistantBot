import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Отримуємо токен з Environment Variable
TOKEN = os.getenv("BOT_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! 👋 Я твій бот і готовий працювати!")

# Обробка будь-якого текстового повідомлення
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Ти написав: {update.message.text}")

def main():
    # Створюємо застосунок
    app = ApplicationBuilder().token(TOKEN).build()

    # Додаємо команди та обробники
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Вивід у консоль для відладки
    print("✅ Бот запущено. Очікую повідомлення...")

    # Запускаємо бота
    app.run_polling()

if __name__ == "__main__":
    main()

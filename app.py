from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import openai

# مقداردهی کلید API
openai.api_key = os.getenv("openai_key")
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام! هر پیامی که ارسال کنید را دریافت می‌کنم.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text    
    answer = ask_chatgpt(user_message)
    await update.message.reply_text(f"هوش مصنوعی: {answer}")

def ask_chatgpt(prompt):
    """
    این تابع یک سؤال از ChatGPT می‌پرسد و پاسخ آن را برمی‌گرداند.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    print("ربات در حال اجرا است...")
    app.run_polling()

if __name__ == "__main__":
    main()

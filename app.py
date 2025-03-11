import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# تنظیمات لاگ برای دیباگ کردن
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

# توکن ربات تلگرام (از BotFather بگیر و جایگزین کن)
TELEGRAM_BOT_TOKEN = "7033061082:AAGo9mPYZHOS2TSgRtcyZX2PfTiZA7mkiCw"

# API Key مربوط به AIML API
AIML_API_KEY = "f808979fe04642109ef5e80a7be09e8a"
AIML_API_URL = "https://api.aimlapi.com/v1/images/generations"

async def generate_image(prompt: str):
    """ارسال درخواست به AIML API برای تولید تصویر"""
    headers = {
        "Authorization": f"Bearer {AIML_API_KEY}",
        "Content-Type": "application/json",
    }
    json_data = {
        "prompt": prompt,
        "model": "flux/schnell",
    }

    response = requests.post(AIML_API_URL, headers=headers, json=json_data)
    
    if response.status_code == 200:
        return response.json().get("image_url")
    else:
        return None

async def start(update: Update, context: CallbackContext) -> None:
    """دستور /start"""
    await update.message.reply_text("سلام! من یک بات هوش مصنوعی هستم. یک متن ارسال کن تا تصویر بسازم!")

async def handle_message(update: Update, context: CallbackContext) -> None:
    """وقتی کاربر متنی ارسال کرد"""
    prompt = update.message.text
    await update.message.reply_text(f"در حال تولید تصویر برای: {prompt} ...")

    image_url = await generate_image(prompt)

    if image_url:
        await update.message.reply_photo(photo=image_url, caption=f"🔹 تصویر برای: {prompt}")
    else:
        await update.message.reply_text("❌ خطایی رخ داد، لطفاً دوباره امتحان کن.")

def main():
    """اجرای بات"""
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # اضافه کردن دستورات به بات
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # اجرای بات
    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

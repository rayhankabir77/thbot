import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Environment Variable থেকে বটের টোকেন নেওয়া হচ্ছে
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# /start কমান্ড হ্যান্ডলার
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("ওয়েলকাম! আমি একটি টেলিগ্রাম বট।")

# Back4app Health Check এর জন্য একটি ছোট HTTP সার্ভার
async def handle_health_check(request):
    return web.json_response({"status": "running"})

async def main():
    print("Bot is running...")
    
    # HTTP সার্ভার সেটআপ (Back4app পোর্ট এক্সপোজ করার জন্য)
    app = web.Application()
    app.router.add_get('/', handle_health_check)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Back4app এর পোর্ট হ্যান্ডেল করা
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # বট স্টার্ট করা
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

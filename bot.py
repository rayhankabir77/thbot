import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiohttp import web

# Environment Variable থেকে বটের টোকেন নেওয়া
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN environment variable is missing!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# টেলিগ্রামে কেউ /start দিলে শুধু ওয়েলকাম মেসেজ দেবে
@dp.message(CommandStart())
async def command_start_handler(message: types.Message):
    await message.reply("ওয়েলকাম! আমি রিকোয়েস্ট প্রোসেস করার জন্য প্রস্তুত।")


# ব্যাকফোরঅ্যাপের লাইভ রাখার জন্য হেলথ চেক রুট
async def handle_health_check(request):
    return web.json_response({"status": "running"})


# ১. Ads Earnings Withdrawal রুট (wd-gp-1, wd-gp-2, wd-mt-1, wd-mt-2, wd-ag-1, wd-ag-2)
async def handle_ads_withdraw(request):
    try:
        data = await request.json()
        uid = data.get("uid")
        amount = data.get("amount")
        status = data.get("status")
        
        if not uid or not amount or not status:
            return web.json_response({"error": "uid, amount, and status are required"}, status=400)
        
        msg_text = f"Your ads earnings have been withdrawn {amount}RBL {status}."
        await bot.send_message(chat_id=uid, text=msg_text)
        return web.json_response({"status": "success", "message": "Ads withdraw message sent"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# ২. Website Visit Earnings Withdrawal রুট (wd-lv)
async def handle_lv_withdraw(request):
    try:
        data = await request.json()
        uid = data.get("uid")
        amount = data.get("amount")
        status = data.get("status")
        
        if not uid or not amount or not status:
            return web.json_response({"error": "uid, amount, and status are required"}, status=400)
        
        msg_text = f"Your website visit earnings have been withdrawn {amount}RBL {status}."
        await bot.send_message(chat_id=uid, text=msg_text)
        return web.json_response({"status": "success", "message": "Website visit withdraw message sent"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# ৩. Main Account Withdrawal রুট (withdraw)
async def handle_main_withdraw(request):
    try:
        data = await request.json()
        uid = data.get("uid")
        amount = data.get("amount")
        status = data.get("status")
        number = data.get("number") # পোস্ট রিকোয়েস্ট থেকে নাম্বার নেওয়া হচ্ছে
        
        if not uid or not amount or not status or not number:
            return web.json_response({"error": "uid, amount, status, and number are required"}, status=400)
        
        msg_text = f"Your main account withdrawal has been {status}. Payment number: {number}, amount: {amount}."
        await bot.send_message(chat_id=uid, text=msg_text)
        return web.json_response({"status": "success", "message": "Main withdraw message sent"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


# ৪. Notice রুট (notice) - যেখানে /n/ থাকলে একলাইন নিচে নামিয়ে সাজানো হবে
async def handle_notice(request):
    try:
        data = await request.json()
        uid = data.get("uid")
        raw_message = data.get("message")
        
        if not uid or not raw_message:
            return web.json_response({"error": "uid and message are required"}, status=400)
        
        # /n/ কে নিউ-লাইন বা একলাইন নিচে নামানোর কোড (\n) দিয়ে পরিবর্তন করা হচ্ছে
        formatted_message = raw_message.replace("/n/", "\n")
        
        await bot.send_message(chat_id=uid, text=formatted_message)
        return web.json_response({"status": "success", "message": "Notice message sent"})
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)


async def main():
    print("Bot starting with your custom paths...")
    app = web.Application()
    
    # আপনার আইডিয়া অনুযায়ী প্রতিটি পাথ (Path) এবং রুট সেটআপ
    app.router.add_get('/', handle_health_check)
    
    # Ads Withdraw Paths
    app.router.add_post('/rbl/wd-gp-1', handle_ads_withdraw)
    app.router.add_post('/rbl/wd-gp-2', handle_ads_withdraw)
    app.router.add_post('/rbl/wd-mt-1', handle_ads_withdraw)
    app.router.add_post('/rbl/wd-mt-2', handle_ads_withdraw)
    app.router.add_post('/rbl/wd-ag-1', handle_ads_withdraw)
    app.router.add_post('/rbl/wd-ag-2', handle_ads_withdraw)
    
    # Website Visit Path
    app.router.add_post('/rbl/wd-lv', handle_lv_withdraw)
    
    # Main Withdraw Path
    app.router.add_post('/rbl/withdraw', handle_main_withdraw)
    
    # Notice Path
    app.router.add_post('/rbl/notice', handle_notice)
    
    runner = web.AppRunner(app)
    await runner.setup()
    
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())

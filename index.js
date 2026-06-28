export default {
  async fetch(request, env, ctx) {
    // শুধু POST রিকোয়েস্ট (টেলিগ্রাম মেসেজ) হ্যান্ডেল করবে
    if (request.method === "POST") {
      try {
        const botToken = "8871803641:AAFsAkyh7Vq_UgC2HCSnVoUB9Dj3CpvxnvA";
        const update = await request.json();

        if (update.message) {
          const chatId = update.message.chat.id;
          const messageText = update.message.text ? update.message.text.trim() : "";
          
          let reply = "আপনি লিখেছেন: " + messageText;

          if (messageText === "/start") {
            reply = "হ্যালো! Cloudflare Workers ও GitHub এর জুটিতে আপনার EarnGlow বট এখন সুপারফাস্ট! 🚀";
          } else if (messageText === "/help") {
            reply = "সাহায্যের জন্য আমাদের সাপোর্ট গ্রুপে যোগাযোগ করুন।";
          }

          // টেলিগ্রামে মেসেজ পাঠানো
          const telegramUrl = `https://api.telegram.org/bot${botToken}/sendMessage`;
          await fetch(telegramUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              chat_id: chatId,
              text: reply
            })
          });
        }
      } catch (err) {
        return new Response("Error processing Telegram update", { status: 500 });
      }
    }

    // ব্রাউজারে সরাসরি ভিজিট করলে (GET Request) এই মেসেজ দেখাবে
    return new Response("EarnGlow Cloudflare Worker is Running Live!", { status: 200 });
  }
};

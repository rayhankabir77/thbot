const userMessageCounter = {};

export default {
  async fetch(request, env, ctx) {
    if (request.method === "POST") {
      try {
        const botToken = "8871803641:AAFsAkyh7Vq_UgC2HCSnVoUB9Dj3CpvxnvA";
        const update = await request.json();

        if (update.message) {
          const chatId = update.message.chat.id;
          const userId = update.message.from?.id || chatId;
          const messageText = update.message.text ? update.message.text.trim() : "";

          // ১. শুধুমাত্র /start প্রসেস হবে
          if (messageText !== "/start") {
            return new Response("Ignored non-start command", { status: 200 });
          }

          // ২. ইন-মেমোরি স্প্যাম প্রোটেকশন
          if (!userMessageCounter[userId]) {
            userMessageCounter[userId] = 0;
          }
          userMessageCounter[userId]++;

          if (userMessageCounter[userId] > 10) {
            return new Response("Rate limit exceeded", { status: 200 });
          }

          // ৩. আপনার ডকস অনুযায়ী KV-তে ইউজার আইডি (UID) রাইট (Write) করা
          // এখানে 'KEY' এর জায়গায় 'user:UID' আর 'VALUE' এর জায়গায় জাস্ট 'active' রাখছি
          await env.KV.put(`user:${userId}`, "active");

          // ৪. টেলিগ্রাম মেসেজ রেসপন্স
          let reply = "হ্যালো! আপনার আইডি আমাদের ক্লাউডফ্লেয়ার KV ডেটাবেজে সফলভাবে সেভ হয়েছে। 🚀";

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

    // ব্রাউজারে সরাসরি রুট ইউআরএল ভিজিট করলে কি দেখাবে (ডকসের মতো গেট/লিস্ট টেস্ট করার জন্য)
    return new Response("EarnGlow Telegram Bot inside Cloudflare Workers is running live!", { status: 200 });
  }
};

import telebot  #install "pyTelegramBotAPI"
import requests  #install "request"



BOT_TOKEN ="YOUR_BOT_TOEKN"
BOT_OWNER_ID = 8029966196  # Replace with your Telegram User ID

# Initialize bot

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="Markdown")

# ✅ Allowed groups & promotion messages storage

allowed_groups = set()
promotion_messages = {}

# 🛠 Function to check if the user is the bot owner

def is_bot_owner(message):
    return message.from_user.id == BOT_OWNER_ID

# 🟢 /allow Command (Bot Owner Only)

@bot.message_handler(commands=["allow"])
def allow_group(message):
    if not is_bot_owner(message):
        return bot.reply_to(message, "❌ You are not the bot owner!")
    chat_id = message.chat.id
    allowed_groups.add(chat_id)
    bot.reply_to(message, "✅ This group is now allowed to use the bot!")

# 🔴 /remove Command (Bot Owner Only)

@bot.message_handler(commands=["remove"])
def remove_group(message):
    if not is_bot_owner(message):
        return bot.reply_to(message, "❌ You are not the bot owner!")
    chat_id = message.chat.id
    if chat_id in allowed_groups:
        allowed_groups.remove(chat_id)
        bot.reply_to(message, "❌ This group has been removed from using the bot!")
    else:
        bot.reply_to(message, "ℹ️ This group is not in the allowed list!")

# 📌 /setpromotion Command (Bot Owner Only)

@bot.message_handler(commands=["setpromotion"])
def set_promotion(message):
    if not is_bot_owner(message):
        return bot.reply_to(message, "❌ You are not the bot owner!")
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ Usage: `/setpromotion Your promotion message`")
    chat_id = message.chat.id
    promotion_messages[chat_id] = args[1]
    bot.reply_to(message, "✅ Promotion message set successfully!")

# 🔍 /checkban Command (Anyone in Allowed Groups Can Use)

@bot.message_handler(commands=["checkban"])
def check_ban(message):
    chat_id = message.chat.id
    if chat_id not in allowed_groups:
        return bot.reply_to(message, "❌ This group is not allowed to use this command!")
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ Usage: `/checkban UID`")
    uid = args[1]
    api_url = f"https://nishantbancheck.vercel.app/api/isbanned?uid={uid}"
    try:
        response = requests.get(api_url)
        data = response.json()
        if "status" not in data:
            raise ValueError("Invalid API response")

        # 📊 Format API response

        result_msg = f"""
📌 **Ban Check Result**
━━━━━━━━━━━━━━━━━━━━
👤 **Nickname:** `{data.get('nickname', 'Unknown')}`
🌍 **Region:** `{data.get('region', 'Unknown')}`
🚫 **Ban Status:** `{data.get('ban_message', 'Unknown')}`
⏳ **Ban Period:** `{data.get('ban_period', 0)} Days`
🔗 **Group Link:** [Join Now]({data.get('My Group', '#')})
━━━━━━━━━━━━━━━━━━━━

🤖 **Bot Owner:** @nishantsarkar10k

"""

        # ➕ Add promotion message if available

        if chat_id in promotion_messages:
            result_msg += f"\n💎 **Promotion:** {promotion_messages[chat_id]}"
        bot.reply_to(message, result_msg, disable_web_page_preview=True)
    except Exception as e:
        bot.reply_to(message, f"⚠️ Unknown error occurred!\n\n🤖 **Bot Owner:** @nishantsarkar10k")

# ✅ Run bot
# DON'T FORGET TO INSTALL THE REQUIREMENTS 
print("✅ Bot is running...")
bot.polling()
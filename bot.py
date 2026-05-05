from telethon import TelegramClient, events
import re

# 🔑 TELEGRAM API (⚠️ regenerate these after sharing)
api_id = 35433634
api_hash = "a9468f9a7654ae557f8eb8ce74b2c79f"

# 📥 SOURCES
source_channel = -1003808509407   # your main channel
extra_chat = 5673453687            # your personal chat OR group ID

# 📤 TARGET
target_channel = -1003944179057

# 🤖 CLIENT
client = TelegramClient("session", api_id, api_hash)


# 🔍 PARSE SIGNAL
def parse_signal(text):
    text = text.upper()

    signal = re.search(r"(BUY|SELL)", text)
    ticker = re.search(r"(GOLD|XAUUSD)", text)
    entry = re.search(r"ENTER IN\s*=\s*([\d\-\s]+)", text)
    sl = re.search(r"SL\s*=\s*(\d+)", text)
    tps = re.findall(r"TP\d*\s*=\s*(\d+)", text)

    entry_value = entry.group(1).strip() if entry else ""
    entry_value = entry_value.replace(" ", "").replace("-", " - ")

    return {
        "signal": signal.group(1) if signal else "",
        "ticker": "XAUUSD",
        "entry": entry_value,
        "sl": sl.group(1) if sl else "",
        "tp1": tps[0] if len(tps) > 0 else "",
        "tp2": tps[1] if len(tps) > 1 else "",
        "tp3": tps[2] if len(tps) > 2 else "",
        "tp4": tps[3] if len(tps) > 3 else "",
    }


# 🧾 FORMAT MESSAGE
def format_message(d):
    tp_lines = "\n".join(
        [f"🎯 TP{i+1}: {tp}" for i, tp in enumerate(
            [d['tp1'], d['tp2'], d['tp3'], d['tp4']]
        ) if tp]
    )

    return f"""📢 SIGNAL ALERT

🔔 Signal: {d['signal']}
📊 Ticker: {d['ticker']}

🎯 Entry: {d['entry']}

{tp_lines}

🛑 SL: {d['sl']}"""


# 🚀 HANDLER (CHANNEL + EXTRA CHAT)
@client.on(events.NewMessage(chats=[source_channel, extra_chat]))
async def handler(event):
    text = event.message.message

    if not text:
        return

    # 🔒 OPTIONAL: only your messages from personal chat
    # if event.chat_id == extra_chat and not event.out:
    #     return

    data = parse_signal(text)

    if data["signal"] and data["entry"] and data["sl"]:
        msg = format_message(data)
        await client.send_message(target_channel, msg)


# ▶️ START BOT
client.start()
print("🤖 Bot running...")
client.run_until_disconnected()
from telethon import TelegramClient, events
import re

api_id = 35433634  # replace
api_hash = "a9468f9a7654ae557f8eb8ce74b2c79f"  # replace

source_channel = "-1003808509407"
target_channel = "-1003864471994"

client = TelegramClient("session", api_id, api_hash)

def parse_signal(text):
    signal = re.search(r"(BUY|SELL)", text)
    entry = re.search(r"ENTER IN\s*=\s*([\d\-\s]+)", text)
    sl = re.search(r"SL\s*=\s*(\d+)", text)
    tp1 = re.search(r"TP1\s*=\s*(\d+)", text)
    tp2 = re.search(r"TP2\s*=\s*(\d+)", text)
    tp3 = re.search(r"TP3\s*=\s*(\d+)", text)

    return {
        "signal": signal.group(1) if signal else "",
        "entry": entry.group(1).strip() if entry else "",
        "sl": sl.group(1) if sl else "",
        "tp1": tp1.group(1) if tp1 else "",
        "tp2": tp2.group(1) if tp2 else "",
        "tp3": tp3.group(1) if tp3 else "",
    }

def format_message(d):
    return f"""📢 SIGNAL ALERT

🔔 Signal: {d['signal']}
📊 Ticker: XAUUSD

🎯 Entry: {d['entry']}

🎯 TP1: {d['tp1']}
🎯 TP2: {d['tp2']}
🎯 TP3: {d['tp3']}

🛑 SL: {d['sl']}"""

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    text = event.message.message

    data = parse_signal(text)

    if data["signal"] and data["entry"]:
        msg = format_message(data)
        await client.send_message(target_channel, msg)

client.start()
print("Bot running...")
client.run_until_disconnected()
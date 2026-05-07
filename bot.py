from telethon import TelegramClient, events
import re

# =========================================
# TELEGRAM API
# =========================================
api_id = 35433634
api_hash = "a9468f9a7654ae557f8eb8ce74b2c79f"

# =========================================
# SOURCE CHATS
# =========================================
source_channel = -1003808509407

extra_chat_1 = 8282485136
extra_chat_2 = 5673453687

# =========================================
# TARGET CHANNEL
# =========================================
target_channel = -1003944179057

# =========================================
# TELEGRAM CLIENT
# =========================================
client = TelegramClient(
    "session",
    api_id,
    api_hash
)

# =========================================
# PARSE SIGNAL
# =========================================
def parse_signal(text):

    text = text.upper()

    # BUY / SELL
    signal = re.search(
        r"\b(BUY|SELL)\b",
        text
    )

    # ENTRY
    entry = re.search(
        r"(ENTER IN|ENTRY)\s*[:=]?\s*([\d\.\-\s]+)",
        text
    )

    # SL
    sl = re.search(
        r"SL\s*[:=]?\s*([\d\.]+)",
        text
    )

    # TPS
    tps = re.findall(
        r"TP\d*\s*[:=]?\s*([\d\.]+)",
        text
    )

    # FORMAT ENTRY
    entry_value = entry.group(2).strip() if entry else ""

    entry_value = (
        entry_value
        .replace(" ", "")
        .replace("-", " - ")
    )

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

# =========================================
# FORMAT MESSAGE
# =========================================
def format_message(d):

    tp_lines = "\n".join(

        [
            f"🎯 TP{i+1}: {tp}"

            for i, tp in enumerate([

                d['tp1'],
                d['tp2'],
                d['tp3'],
                d['tp4']

            ])

            if tp
        ]
    )

    return f"""📢 SIGNAL ALERT

🔔 Signal: {d['signal']}
📊 Ticker: {d['ticker']}

🎯 Entry: {d['entry']}

{tp_lines}

🛑 SL: {d['sl']}"""

# =========================================
# HANDLE MESSAGES
# =========================================
@client.on(events.NewMessage(chats=[
    source_channel,
    extra_chat_1,
    extra_chat_2
]))
async def handler(event):

    text = event.message.message

    print("\n📩 NEW MESSAGE")
    print("CHAT ID:", event.chat_id)
    print("TEXT:", text)

    if not text:
        return

    # PARSE
    data = parse_signal(text)

    print("\n📊 PARSED DATA")
    print(data)

    # VALIDATE
    if (
        data["signal"]
        and data["entry"]
        and data["sl"]
    ):

        msg = format_message(data)

        await client.send_message(
            target_channel,
            msg
        )

        print("✅ SIGNAL FORWARDED")

    else:

        print("❌ INVALID SIGNAL - SKIPPED")

# =========================================
# START BOT
# =========================================
client.start()

print("🤖 Bot running...")

client.run_until_disconnected()
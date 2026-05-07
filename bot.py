from telethon import TelegramClient, events
import MetaTrader5 as mt5
import asyncio
import re

# 🔑 TELEGRAM API
api_id = 35433634
api_hash = "a9468f9a7654ae557f8eb8ce74b2c79f"

# 📥 SOURCES
source_channel = -1003808509407
extra_chat_1 = 8282485136
extra_chat_2 = 5673453687

# 📤 TARGET
target_channel = -1003944179057

# 🤖 CLIENT
client = TelegramClient("session", api_id, api_hash)

# 📊 ACTIVE TRADES
active_trades = []

# 🔌 CONNECT MT5
if not mt5.initialize():
    print("❌ MT5 initialization failed")
    quit()

print("✅ MT5 Connected")


# 🔍 PARSE SIGNAL
def parse_signal(text):
    text = text.upper()

    signal = re.search(r"\b(BUY|SELL)\b", text)

    # Decimal support
    entry = re.search(
        r"(ENTER IN|ENTRY)\s*[:=]?\s*([\d\.\-\s]+)",
        text
    )

    sl = re.search(
        r"SL\s*[:=]?\s*([\d\.]+)",
        text
    )

    tps = re.findall(
        r"TP\d*\s*[:=]?\s*([\d\.]+)",
        text
    )

    entry_value = entry.group(2).strip() if entry else ""
    entry_value = entry_value.replace(" ", "").replace("-", " - ")

    return {
        "signal": signal.group(1) if signal else "",
        "ticker": "XAUUSD",
        "entry": entry_value,
        "sl": float(sl.group(1)) if sl else 0,
        "tp1": float(tps[0]) if len(tps) > 0 else 0,
        "tp2": float(tps[1]) if len(tps) > 1 else 0,
        "tp3": float(tps[2]) if len(tps) > 2 else 0,
        "tp4": float(tps[3]) if len(tps) > 3 else 0,
    }


# 🧾 FORMAT MESSAGE
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


# 🚀 HANDLE SIGNALS
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

    data = parse_signal(text)

    print("PARSED:", data)

    if data["signal"] and data["entry"] and data["sl"]:

        # SAVE TRADE
        active_trades.append({
            "type": data["signal"],
            "tp1": data["tp1"],
            "tp2": data["tp2"],
            "tp3": data["tp3"],
            "tp4": data["tp4"],
            "sl": data["sl"],

            "tp1_hit": False,
            "tp2_hit": False,
            "tp3_hit": False,
            "tp4_hit": False,
            "sl_hit": False
        })

        msg = format_message(data)

        await client.send_message(
            target_channel,
            msg
        )

        print("✅ SIGNAL FORWARDED")

    else:
        print("❌ INVALID SIGNAL - SKIPPED")


# 📈 MONITOR PRICE
async def monitor_prices():

    while True:

        tick = mt5.symbol_info_tick("XAUUSD")

        if tick:

            # You can use ask too
            price = tick.bid

            for trade in active_trades:

                trade_type = trade["type"]

                # ================= BUY =================
                if trade_type == "BUY":

                    # TP1
                    if (
                        trade["tp1"]
                        and not trade["tp1_hit"]
                        and price >= trade["tp1"]
                    ):
                        trade["tp1_hit"] = True

                        await client.send_message(
                            target_channel,
                            "✅ TP1 HIT — XAUUSD"
                        )

                    # TP2
                    if (
                        trade["tp2"]
                        and not trade["tp2_hit"]
                        and price >= trade["tp2"]
                    ):
                        trade["tp2_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🔥 TP2 HIT — XAUUSD"
                        )

                    # TP3
                    if (
                        trade["tp3"]
                        and not trade["tp3_hit"]
                        and price >= trade["tp3"]
                    ):
                        trade["tp3_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🚀 TP3 HIT — XAUUSD"
                        )

                    # TP4
                    if (
                        trade["tp4"]
                        and not trade["tp4_hit"]
                        and price >= trade["tp4"]
                    ):
                        trade["tp4_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🏆 TP4 HIT — XAUUSD"
                        )

                    # SL
                    if (
                        not trade["sl_hit"]
                        and price <= trade["sl"]
                    ):
                        trade["sl_hit"] = True

                        await client.send_message(
                            target_channel,
                            "❌ SL HIT — XAUUSD"
                        )

                # ================= SELL =================
                elif trade_type == "SELL":

                    # TP1
                    if (
                        trade["tp1"]
                        and not trade["tp1_hit"]
                        and price <= trade["tp1"]
                    ):
                        trade["tp1_hit"] = True

                        await client.send_message(
                            target_channel,
                            "✅ TP1 HIT — XAUUSD"
                        )

                    # TP2
                    if (
                        trade["tp2"]
                        and not trade["tp2_hit"]
                        and price <= trade["tp2"]
                    ):
                        trade["tp2_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🔥 TP2 HIT — XAUUSD"
                        )

                    # TP3
                    if (
                        trade["tp3"]
                        and not trade["tp3_hit"]
                        and price <= trade["tp3"]
                    ):
                        trade["tp3_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🚀 TP3 HIT — XAUUSD"
                        )

                    # TP4
                    if (
                        trade["tp4"]
                        and not trade["tp4_hit"]
                        and price <= trade["tp4"]
                    ):
                        trade["tp4_hit"] = True

                        await client.send_message(
                            target_channel,
                            "🏆 TP4 HIT — XAUUSD"
                        )

                    # SL
                    if (
                        not trade["sl_hit"]
                        and price >= trade["sl"]
                    ):
                        trade["sl_hit"] = True

                        await client.send_message(
                            target_channel,
                            "❌ SL HIT — XAUUSD"
                        )

        await asyncio.sleep(1)


# ▶️ MAIN
async def main():

    asyncio.create_task(
        monitor_prices()
    )

    print("🤖 Bot running...")

    await client.run_until_disconnected()


with client:
    client.loop.run_until_complete(main())
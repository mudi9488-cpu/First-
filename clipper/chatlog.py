"""Log a Twitch channel's chat anonymously to JSONL, reconnecting on drops.

usage: python3 -I chatlog.py <channel> <out.jsonl> <seconds>
"""
import json, sys, time
import websocket

chan, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
end = time.time() + dur

def connect():
    ws = websocket.create_connection("wss://irc-ws.chat.twitch.tv:443", timeout=30)
    ws.send("NICK justinfan%d" % (int(time.time()) % 100000))
    ws.send("JOIN #" + chan)
    return ws

with open(out, "a") as f:
    while time.time() < end:
        try:
            ws = connect()
            while time.time() < end:
                try:
                    data = ws.recv()
                except websocket.WebSocketTimeoutException:
                    continue
                if not data:
                    raise ConnectionError("closed")
                for line in data.split("\r\n"):
                    if line.startswith("PING"):
                        ws.send("PONG :tmi.twitch.tv")
                    elif "PRIVMSG" in line:
                        msg = line.split(" :", 1)[1] if " :" in line else ""
                        f.write(json.dumps({"t": time.time(), "m": msg}) + "\n")
                        f.flush()
        except Exception as e:  # reconnect after any drop
            print("reconnect after:", repr(e), flush=True)
            time.sleep(3)

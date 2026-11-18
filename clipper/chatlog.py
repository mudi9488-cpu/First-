import sys, time, websocket, json
chan, out, dur = sys.argv[1], sys.argv[2], float(sys.argv[3])
ws = websocket.create_connection("wss://irc-ws.chat.twitch.tv:443", timeout=30)
ws.send("NICK justinfan%d" % (int(time.time()) % 100000))
ws.send("JOIN #" + chan)
end = time.time() + dur
with open(out, "a") as f:
    while time.time() < end:
        try:
            data = ws.recv()
        except websocket.WebSocketTimeoutException:
            continue
        for line in data.split("\r\n"):
            if line.startswith("PING"):
                ws.send("PONG :tmi.twitch.tv")
            elif "PRIVMSG" in line:
                msg = line.split(" :", 1)[1] if " :" in line else ""
                f.write(json.dumps({"t": time.time(), "m": msg}) + "\n"); f.flush()

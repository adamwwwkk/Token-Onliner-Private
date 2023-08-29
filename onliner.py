import json
import random
import time
import threading
import base64
try:
    from colorama import Fore, init 
    from websocket import WebSocketApp
except:
    import os
    os.system("pip install websocket colorama")
init(True, True)

print_lock = threading.Lock()

def print_with_lock(text):
    print_lock.acquire()
    print(text)
    print_lock.release()

class Printer():
    def content(text, content):
        print_with_lock(f"({Fore.LIGHTCYAN_EX}+{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}: {Fore.CYAN}{content}{Fore.RESET}")

    def cinput(text):
        content = input(f"({Fore.CYAN}~{Fore.RESET}) {Fore.CYAN}{text}{Fore.RESET}")
        return content

    def error(text):
        print_with_lock(f"({Fore.LIGHTRED_EX}-{Fore.RESET}) {Fore.RED}{text}{Fore.RESET}")

class Onliner():
    def __init__(self, token, i):
        self.token = token 
        self.i = i
        self.connect_to_ws(token)

    def get_random_presence(self):
        presence_types = ['Playing', 'Streaming', 'Listening to', 'Watching', 'Nothing']
        type = random.choice(presence_types)
        status = random.choice(["online", "dnd", "idle"])
        
        if type == "Playing":
            file_name = random.choice(['main.py', 'bot.py', 'main.js', 'index.js', 'ban.py', 'mute.py', 'gen.py'])
            language = "Python" if file_name.endswith(".py") else "JavaScript"
            details = f"Editing {file_name}"
            workspace = "Discord Bot"  # Replace this with your desired workspace name
            elapsed_time = time.strftime("%H:%M", time.gmtime(random.randint(0, 3600)))  # Random elapsed time between 0 and 1 hour
            large_image_key = "python-logo-notext_svg"  # Replace with your Python image key for the custom image
            large_image_text = "Python"  # Replace with your custom text for the image
            small_image_key = "visual_studio_code_1_35_icon_svg"  # Replace with your Visual Studio Code image key for the custom image
            small_image_text = "Visual Studio Code"  # Replace with your custom text for the image

            gamejson = {
                "name": "Visual Studio Code",
                "type": 0,
                "details": details,
                "state": f"Workspace: {workspace}",
                "timestamps": {
                    "start": int(time.time())
                },
                "assets": {
                    "large_image": large_image_key,
                    "large_text": large_image_text,
                    "small_image": small_image_key,
                    "small_text": small_image_text
                }
            }
        elif type == 'Streaming':
            gamejson = {
                "name": "On twitch.tv",
                "type": 1,
                "url": "https://www.twitch.tv/"
            }
        elif type == "Listening to":
            gamejson = {
                "name": "Spotify | " + random.choice(['Angry Birds', 'Sweden', 'Married Life', 'Erika']),
                "type": 2
            }
        elif type == "Watching":
            gamejson = {
                "name": "Youtube",
                "type": 3
            }
        elif type == "Nothing":
            gamejson = None
        
        return {"game": gamejson, "status": status, "since": 0, "activities": [], "afk": False}
    
    def connect_to_ws(self, token):
        from websocket import WebSocketApp
        
        def keep_alive(ws, interval):
            while True:
                time.sleep(interval / 1000)
                try:
                    ws.send(json.dumps({"op": 1, "d": None}))
                except:
                    break
        
        def on_message(ws: WebSocketApp, msg):
            msg = json.loads(msg)
            if msg["op"] == 10:
                payload = {
                    "op": 2,
                    "d": {
                        "token": token,
                        "properties": {
                            "os": "Windows",
                            "browser": "Chrome",
                            "device": "",
                            "system_locale": "en-US",
                            "os_version": "10"
                        },
                        "presence": self.get_random_presence(),
                        "compress": False,
                    }
                }
                ws.send(json.dumps(payload))
                Printer.content("Onlined", token + f" {Fore.RESET}|{Fore.BLUE} {self.i}")
                threading.Thread(target=keep_alive, args=(ws, msg['d']['heartbeat_interval'])).start()
        
        WebSocketApp("wss://gateway.discord.gg/?encoding=json&v=9", on_message=on_message).run_forever()

if __name__ == "__main__":
    for i, token in enumerate(open("tokens.txt", "r+").read().splitlines()):
        threading.Thread(target=Onliner, args=(token, i)).start()
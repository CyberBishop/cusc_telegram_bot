import os
import time
from typing import List

from .mongo import insert_new_user, get_ids, change_media_id, get_media_id

import telebot
from flask import Flask, request

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ["TOKEN"]
APP_URL = os.environ["RENDER_EXTERNAL_URL"]

CHMN = int(os.environ["CHMN"])
VCM = int(os.environ["VCM"])
VCF = int(os.environ["VCF"])
EXECSEC = int(os.environ["EXECSEC"])
PRO = int(os.environ["PRO"])

ADMIN = [CHMN, VCM, VCF, EXECSEC, PRO]
server = Flask(__name__)

categories = {
    "500": ["DAN", "EIE500", "EEE22", "CU2022"],
    "gen": ["CHAP", "AEIES", "CUMCH", "CUCHM", "CUMD", "CUSC"],
    "100": ["FRESH"],
    "200": ["CU2425"],
    "300": ["CU300"],
    "400": ["DAN", "EIE400"]
}

new_group_ids = {
    # CHAP AEIES CUMCH CUCHM CUMD CUSC 
    "gen": [-1001158265107, -1001318860489, -1001433686986, -1001490202977, -1001785807218, -1001682826754],
    # FRESH DEB
    "100": [-1001655184402, -1001536886384],
    # CU2425 DEB MARY
    "200": [-1001444929539, -1001536886384, -1001494532036],
    # CU300 DEB MARY
    "300": [-1001218549305, -1001536886384, -1001494532036],
    # EIE400 DAN 
    "400": [-1001315029935, -1001563004586],
    # DAN EIE500 CU2022 EEE22 
    "500": [-1001563004586, -1001406974184, -1001572957944, -100398271332]
}

bot = telebot.TeleBot(TOKEN)
start_message_text = """Hi there \!\!\! 👋\n\nI'm CUSC bot 🤖, the official bot of the CU Student Council\.
I'm here to give you first hand information and news concerning student life on campus 🏫\.
You can also connect with the student council through the [official Instagram page](https://www.instagram.com/studentcouncil_cu/):\n\nStay tuned\!\!\! 💥
"""

admin_start_message = """
All messages to this bot should follow either of these two formats:

1\) To broadcast a message:
\[categories\]
\[message\]

2\) To broadcast a message with an attachment \(photo or document\):
/sendmedia
\[categories\]
\[message\]
\[media_type\]

Here are the meanings and possible values of each field above:

\- categories
Is a comma\-separated list of groupings you wish to broadcast your message to
Can be any combination of gen,100,200,300,400,500,private,all

gen comprises of all general groups
100 comprises of all 100 level groups
200 comprises of all 200 level groups
300 comprises of all 300 level groups
400 comprises of all 400 level groups
500 comprises of all 500 level groups
private comprises of all DMs
all comprises of all groups and DMs

**NOTE:**
    The "all" and "private" categories cannot be used with any other category

\- message
Is the message content you wish to broadcast

\- media_type
Specifies what type of attachment you are including with your message
Can be either photo or document

Example
```
private
Chapel Service is by 10pm today
```
    This would send the message "Chapel Service is by 10pm today" to only DMs

```
/sendmedia
100,200,300
I am the CUSC Bot
photo
```
    This would send the a photo with the caption "I am the CUSC Bot" to "FRESH", "CU2425" and "CU300"

```
/sendmedia
all
Revalidation Form
document
```
    This would send the a file with the caption "Revalidation Form" to all groups and private users
"""

message_dict = dict()

def send_messages(ids: List[str], func, **kwargs):
    message_dict.clear()
    count = 0
    for id in ids:
        try:
            message_object = func(id, **kwargs)
            count += 1
            message_dict[message_object.chat.id] = message_object.id
        except:
            continue
        if count % 20 == 0:
            time.sleep(.7)

@bot.message_handler(commands=['start'])
def start_message_handler(message):
    chat = message.chat
    insert_new_user(chat.id, chat.type)

    if chat.type != "private":
        return
    if chat.id not in ADMIN:
        bot.reply_to(message=message, text=start_message_text,
                     parse_mode="MarkdownV2")
        return
    bot.reply_to(message=message,
                 text=f"Hello {chat.first_name.split(' ')[0].title()},\n"+admin_start_message, parse_mode="MarkdownV2")


@bot.message_handler(commands=["deletemessage"])
def delete_messages(message):
    chat = message.chat
    if chat.id not in ADMIN:
        return

    for chat_id, message_id in message_dict.items():
        bot.delete_message(chat_id=chat_id, message_id=message_id)


@bot.message_handler(func=lambda message: message.text.startswith("/sendmedia"))
def broadcast_photo(message):
    chat = message.chat

    if chat.id not in ADMIN:
        return

    # Initialise items
    receivers = message.text.split('\n')[1].strip().lower()
    type = message.text.split('\n')[-1].strip().lower()
    media_id = get_media_id(type=type)

    # Get message text
    message_text = '\n'.join(message.text.split('\n')[2:-1])

    if type == "photo":
        func = bot.send_photo
        kw_args = {
            "caption": message_text,
            "photo": media_id,
        }
    elif type == "document":
        func = bot.send_document
        kw_args = {
            "caption": message_text,
            "document": media_id,
        }

    # Broadcast to all users
    if receivers == "all":
        ids = get_ids()
        send_messages(ids, func, **kw_args)
        return

    # Broadcast to dms only
    if receivers == "private":
        ids = get_ids(chat_type="private")
        send_messages(ids, func, **kw_args)
        return

    # Broadcast to groups only
    if receivers == "groups":
        ids = get_ids(chat_type="supergroup")
        send_messages(ids, func, **kw_args)
        return

    # Get a list of receivers categories
    receivers_list = [reciever.strip() for reciever in receivers.split(",")]
    group_ids = [
        group_id for item in receivers_list for group_id in new_group_ids[item]]

    # Broadcast Photo to all categories
    # group_ids = get_group_ids(group_names)
    send_messages(group_ids, func, kw_args)


@bot.message_handler(func=lambda message: message.chat.id in ADMIN)
def broadcast_message(message):
    # Get a list of receivers categories
    receivers = message.text.split('\n')[0].strip().lower()

    receivers_list = [reciever.strip() for reciever in receivers.split(",")]

    # Get message text
    message_text = '\n'.join(message.text.split('\n')[1:])

    # Broadcast to all users
    if receivers == "all":
        ids = get_ids()
        send_messages(ids, bot.send_message,
                      text=message_text)
        return

    # Broadcast to dms only
    if receivers == "private":
        ids = get_ids(chat_type="private")
        send_messages(ids, bot.send_message,
                      text=message_text)
        return

    # Broadcast to groups only
    if receivers == "groups":
        ids = get_ids(chat_type="supergroup")
        send_messages(ids, bot.send_message,
                      text=message_text)
        return

    # Broadcast to custom set of groups
    group_ids = [
        group_id for item in receivers_list for group_id in new_group_ids[item]]

    # group_ids = get_group_ids(group_names)
    send_messages(group_ids, bot.send_message,
                  text=message_text)


@bot.message_handler(content_types=["photo", "document"])
def save_new_media(message):
    chat = message.chat

    if chat.id not in ADMIN:
        return

    if message.photo:
        media_id = message.photo[0].file_id
        type = "photo"
    elif message.document:
        type = "document"
        media_id = message.document.file_id
    change_media_id(media_id, type=type)


@server.route("/" + TOKEN, methods=["POST"])
def getMessage():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL + "/" + TOKEN)
    return "!", 200

# if __name__ == "__main__":
#   server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

print("Bot is alive")
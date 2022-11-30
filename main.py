from random import random
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.raw.types.update_channel_participant import UpdateChannelParticipant
from pyrogram.raw.types.channel_participant_left import ChannelParticipantLeft
from pyrogram import filters
from decouple import config
import sqlite3
import uuid
import random

_db_address = '/etc/x-ui-english/x-ui-english.db'
_tls_domain = 'v2ray.mousiolvpn.tk'

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH'),
    bot_token=config('BOT_TOKEN'),
)

def join_status(_, __, query: CallbackQuery):
    try:
        user = __.get_chat_member(-1001522544079, query.from_user.id)
        return True
    except:
        query.answer("You are not join in the channel!", show_alert=True)
        return False

def blacklist(_, __, query: CallbackQuery):
    black_list = open('blacklist.txt', 'r').read().splitlines()
    for i in black_list:
        if int(i.strip()) == query.from_user.id:
            query.answer("You are blacklisted!", show_alert=True)
            return False

    else:
        return True

# Check if user got a free account
def check_account(_, __, query: CallbackQuery):
    conn = sqlite3.connect(_db_address)
    c = conn.cursor()
    c.execute("SELECT * FROM inbounds WHERE remark = ?", (f"u{query.from_user.id}",))
    if c.fetchone() is None:
        return True
    else:
        query.answer("You already have a free account!", show_alert=True)
        return False

# Check the update object is a UpdateChannelParticipant
def check_update(_, update):
    return isinstance(update, UpdateChannelParticipant)


@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text(
        "Hello dear!😁\n"
        "I'm Fantasy Premier League Bot, I can give you a free and fast v2ray account.\n"
        "Just click below button to get your account.\n"
        "If you have any questions, please describe it in our support group.\n\n"
        "⭕️Note that for getting a new account, **you must join our channel** first.\n"
        "If you have already joined, please click the button below to get your account.\n"
        "If you have not joined, please join our channel first using Join button, then click the Get VPN button to get your account.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Join Channel", url="https://t.me/F_PremierLeague"
                )],
                [InlineKeyboardButton(
                    "Group", url="https://t.me/+6QxSYV_Oh9FlYmI0"
                )],
                [InlineKeyboardButton(
                    "Get VPN", callback_data="get_vpn"
                )],
            ]
        )
    )

@app.on_callback_query(filters.regex("get_vpn") & filters.create(join_status) & filters.create(blacklist) & filters.create(check_account))
def get_vpn(client: Client, callback_query: CallbackQuery):
    callback_query.answer("Please wait...")
    conn = sqlite3.connect(_db_address)

    rand_uuid = str(uuid.uuid4())

    settings = '''{
  "clients": [
      {
      "id": "''' + rand_uuid + '''",
      "alterId": 0,
      "email": "",
      "limitIp": 0,
      "totalGB": 0,
      "expiryTime": ""
      }
  ],
  "disableInsecureEncryption": false
}'''

    stream_settings = '''{
  "network": "ws",
  "security": "tls",
  "tlsSettings": {
      "serverName": "''' + _tls_domain + '''",
      "certificates": [
      {
          "certificateFile": "/etc/letsencrypt/live/v2ray.mousiolvpn.tk/fullchain.pem",
          "keyFile": "/etc/letsencrypt/live/v2ray.mousiolvpn.tk/privkey.pem"
      }
      ],
      "alpn": []
  },
  "wsSettings": {
      "acceptProxyProtocol": false,
      "path": "/",
      "headers": {}
  }
}'''

    siniffing = """{
  "enabled": true,
  "destOverride": [
      "http",
      "tls"
  ]
}"""
    
    port_number = 0

    while True:
        port_number = random.randint(10001, 65535)
        try:
            cursor = conn.execute(f"INSERT INTO inbounds (user_id, up, down, total, remark, enable, expiry_time, listen, port, protocol, settings, stream_settings, tag, sniffing ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (1, 0, 0, 0, f'u{callback_query.from_user.id}', 1, 0, '', port_number, 'vless', settings, stream_settings, f'inbound-{callback_query.from_user.id}', siniffing))

            conn.commit()
            conn.close()
            break

        except:
            continue

    v2ray_qrcode = f"`vless://{rand_uuid}@{_tls_domain}:{port_number}?type=ws&security=tls&path=%2F&sni={_tls_domain}#u{callback_query.from_user.id}`"

    callback_query.edit_message_text(
        "Congratulations!🥳\n"
        "Your account is ready, please scan the QR code below to get your account.\n"
        "If you can't scan the QR code, please **copy the link below and paste it to your v2ray client**.👇🏻",
    )

    client.send_message(
        callback_query.from_user.id,
        v2ray_qrcode,
    )

    client.send_message(
        callback_query.from_user.id,
        "⁉️If you have any questions, please describe your problem in detail and group.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Group", url="https://t.me/+6QxSYV_Oh9FlYmI0"
                )],
            ]
        )
    )

# Check if the user has left the channel via rae updates
@app.on_raw_update()
def check_left_channel(client: Client, update, users, chats):
    print(isinstance(update.new_participant, ChannelParticipantLeft))
    print(type(update.new_participant))
    print(type(update.prev_participant))
    if isinstance(update, UpdateChannelParticipant):
        conn = sqlite3.connect(_db_address)
        print(update.channel_id == -1001522544079)
        if update.channel_id == -1001522544079 and update.new_participant == None:
            print("kos nanat")
            try:
                client.send_message(
                    update.participant.user_id,
                    "LOOOOL\n😂"
                    "You have left the channel",
                    "Receive your free account and leave the channel?🤣🤣🤣\n"
                    "Do u think we are donkey?🤔\n"
                    "So stupid! mother f***\n\n😏"
                    "❌You have been banned from using this bot for **EVER** and your account has been deleted.❌\n"

                    "Go and F*** yourself!😊",
                )
            except:
                pass
            
            cursor = conn.execute(f"DELETE FROM inbounds WHERE remark = 'u{update.participant.user_id}'")
            open("blacklist.txt", "a").write(f"{update.participant.user_id}\n")

# Remove from blacklist by owner
# @app.on_message(filters.command("unban") & filters.user(OWNER_ID))
# def unban(client: Client, message: Message):
#     if not message.reply_to_message:
#         message.reply_text("Reply to the user's message to unban him.")
#         return

#     if message.reply_to_message.from_user.id in open("blacklist.txt").read().splitlines():
#         open("blacklist.txt", "w").write(
#             open("blacklist.txt").read().replace(f"{message.reply_to_message.from_user.id}"),
#         )

app.run()
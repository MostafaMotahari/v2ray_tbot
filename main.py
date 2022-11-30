from random import random
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
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

@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text(
        "Hello dear!😁\n"
        "I'm Fantasy Premier League Bot, I can give you a free and fast v2ray account.\n"
        "Just click below button to get your account.\n"
        "If you have any questions, please contact @v2raybot.\n\n"
        "⭕️Note that for getting a new account, **you must join our channel** first.\n"
        "If you have already joined, please click the button below to get your account.\n"
        "If you have not joined, please join our channel first using Join button, then click the Get VPN button to get your account.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Join Channel", url="https://t.me/F_PremierLeague"
                )],
                [InlineKeyboardButton(
                    "Get VPN", callback_data="get_vpn"
                )],
            ]
        )
    )

@app.on_callback_query(filters.regex("get_vpn") & filters.create(join_status))
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
        "Congratulations!🥳"
        "Your account is ready, please scan the QR code below to get your account."
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

app.run()
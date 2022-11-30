from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import filters
from decouple import config
import sqlite3
import uuid

_db_address = '/etc/x-ui-english/x-ui-english.db'
_tls_domain = 'sila.ml'
_tls_port = 443

app = Client(
    "my_account",
    api_id=config('API_ID'),
    api_hash=config('API_HASH'),
    bot_token=config('BOT_TOKEN'),
)

@app.on_message(filters.command("start"))
def start(client: Client, message: Message):
    message.reply_text(
        "Hello dear!"
        "I'm Fantasy Premier League Bot, I can give you a free and fast v2ray account."
        "Just click below button to get your account."
        "If you have any questions, please contact @v2raybot.\n\n"
        "Note that for getting a new account, you must join our channel first."
        "If you have already joined, please click the button below to get your account."
        "If you have not joined, please join our channel first using Join button, then click the Get VPN button to get your account.",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Join Channel", url="https://t.me/v2raybot"
                )],
                [InlineKeyboardButton(
                    "Get VPN", callback_data="get_vpn"
                )],
            ]
        )
    )

@app.on_callback_query(filters.regex("get_vpn"))
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
              "certificateFile": "/ets/lsdfhsdlkjfksldf/dsfdf",
              "keyFile": "/sdfds/lsdkfj/dfsd"
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
    
    cursor = conn.execute(f"INSERT INTO inbounds (user_id, up, down, total, remark, enable, expiry_time, listen, port, protocol, settings, stream_settings, tag, sniffing ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (1, 0, 0, 0, f'u{callback_query.from_user.id}', 1, 0, '', 25007, 'v2ray', settings, stream_settings, f'inbound-{callback_query.from_user.id}', siniffing))

    conn.commit()
    conn.close()

    v2ray_qrcode = f"vless://{rand_uuid}@{_tls_domain}:{_tls_port}?type=ws&security=tls&path=%2F&sni={_tls_domain}#u{callback_query.from_user.id}"

    callback_query.edit_message_text(
        "Your account is ready, please scan the QR code below to get your account."
        "If you can't scan the QR code, please copy the link below and paste it to your v2ray client."
        "```code : {}```".format(v2ray_qrcode),
    )

app.run()
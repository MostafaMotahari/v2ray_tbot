import curses
from email import message
from pyrogram.client import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import filters
import requests
import sqlite3

_db_address = '/etc/x-ui-english/x-ui-english.db'
_tls_domain = 'example.com'
_tls_port = 443

app = Client(
    "my_account",
    api_id=123456,
    api_hash="0123456789abcdef0123456789abcdef"   
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
    stream_settings = """{
        "network": "ws",
        "security": "tls",
        "tlsSettings": {
            "serverName": """ + _tls_domain + """,
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
    }"""
    
    cursor = conn.execute(f"insert into inbounds (remark, port, protocol, stream_settings) values ('u{callback_query.from_user.id}', 25000, 'vless', '{stream_settings}') returning settings")
    conn.commit()
    client_settings = cursor.execute(f"select settings from inbounds where remark = 'u{callback_query.from_user.id}'")
    v2ray_qrcode = f"vless://{client_settings}@{_tls_domain}:{_tls_port}?type=ws&security=tls&path=%2F&sni={_tls_domain}#u{callback_query.from_user.id}"

    callback_query.edit_message_text(
        "Your account is ready, please scan the QR code below to get your account."
        "If you can't scan the QR code, please copy the link below and paste it to your v2ray client."
        "```{}```".format(v2ray_qrcode),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(
                    "Get QR Code", url=f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={v2ray_qrcode}" 
                )],
            ]
        )
    )

app.run()
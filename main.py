import pyrogram
import os
import asyncio

# Define a default value for app_id if it's not provided
app_id = os.environ.get("app_id", None)
if app_id is None:
    print("⚠️ App ID is not provided.")
    exit()

api_hash = os.environ.get("api_hash", None)
bot_token = os.environ.get("bot_token", None)
custom_caption = os.environ.get("custom_caption", "`{file_name}`")

AutoCaptionBot = pyrogram.Client(
    name="AutoCaptionBot", api_id=app_id, api_hash=api_hash, bot_token=bot_token
)

start_message = """
<b>👋Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>All you have to do is add me to your channel and I will show you my power</b>
<b>@Mo_Tech_YT</b>"""

about_message = """
<b>• Name : [AutoCaption V1](t.me/{username})</b>
<b>• Developer : [Muhammed](https://github.com/PR0FESS0R-99)</b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href=https://t.me/Mo_Tech_YT>Click Here</a></b>
<b>• Source Code : <a href=https://github.com/PR0FESS0R-99/AutoCaption-Bot>Click Here</a></b>"""

def remove_renamer(text):
    return text.replace('🧞 Renamer', '')

@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("start"))
def strat_callback(bot, update):
    update.message.edit(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot = bot.get_me()
    update.message.edit(
        about_message.format(version=pyrogram.__version__, username=bot.mention),
        reply_markup=about_buttons(bot, update.message),
        parse_mode=pyrogram.enums.ParseMode.HTML,
        disable_web_page_preview=True,
    )

@AutoCaptionBot.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: pyrogram.types.Message):
    try:
        # Check if the update is a regular message object
        if isinstance(update, pyrogram.types.Message):
            # Get the original caption
            original_caption = update.caption or ""
            
            # Replace the username with '@Cash_scope'
            if update.from_user:
                modified_caption = original_caption.replace(update.from_user.username, '@Cash_scope')
            else:
                modified_caption = original_caption
            
            # Print original and modified captions for debugging
            print("Original caption:", original_caption)
            print("Modified caption:", modified_caption)
            
            # Check if the message has a valid message_id before editing the caption
            if update.message_id:
                bot.edit_message_text(
                    chat_id=update.chat.id,
                    message_id=update.message_id,
                    text=update.text,  # Preserve the original text
                    caption=modified_caption,
                    parse_mode="HTML",
                )
            else:
                print("Invalid message ID, unable to edit caption.")
        else:
            print("Not a regular message object, unable to edit caption.")
    except Exception as e:
        print("Error editing caption:", e)

def get_file_details(update: pyrogram.types.Message):
    if update.media:
        for message_type in (
            "photo",
            "animation",
            "audio",
            "document",
            "video",
            "video_note",
            "voice",
            # "contact",
            # "dice",
            # "poll",
            # "location",
            # "venue",
            "sticker",
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id

def start_buttons(bot, update):
    bot = bot.get_me()
    buttons = [
        [
            pyrogram.types.InlineKeyboardButton(
                "Updates", url="t.me/Mo_Tech_YT"
            ),
            pyrogram.types.InlineKeyboardButton("About 🤠", callback_data="about"),
        ],
        [
            pyrogram.types.InlineKeyboardButton(
                "➕️ Add To Your Channel ➕️",
                url=f"http://t.me/{bot.username}?startchannel=true",
            )
        ],
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

def about_buttons(bot, update):
    buttons = [
        [
            pyrogram.types.InlineKeyboardButton(
                "🏠 Back To Home 🏠", callback_data="start"
            )
        ]
    ]
    return pyrogram.types.InlineKeyboardMarkup(buttons)

print("Telegram AutoCaption V1 Bot Start")
print("Bot Created By https://github.com/PR0FESS0R-99")

AutoCaptionBot.run()
import os
from telegram import *
from telegram.ext import *
import users
import afk

def get_mentioned_id(update):
	message = update.effective_message
	userc = update.effective_user
	userc_id = userc.id
	
	if message.entities and message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION]):
		entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
		for ent in entities:
			if ent.type == MessageEntity.TEXT_MENTION:
				return ent.user.id
			if ent.type == MessageEntity.MENTION:
				return int(users.get(message.text[ent.offset:ent.offset + ent.length].replace("@", "")))

def get_mentioned_mention(update):
	message = update.effective_message
	userc = update.effective_user
	userc_id = userc.id
	
	if message.entities and message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION]):
		entities = message.parse_entities([MessageEntity.TEXT_MENTION, MessageEntity.MENTION])
		for ent in entities:
			if ent.type == MessageEntity.TEXT_MENTION:
				return f'<a href="tg://user?id={ent.user.id}">{ent.user.first_name}</a>'
			if ent.type == MessageEntity.MENTION:
				return message.text[ent.offset:ent.offset + ent.length]

def group(update, context):
	text = update.message.text
	user_id = update.message.from_user.id
	user_name = update.message.from_user.first_name
	
	if afk.get(user_id):
		afk.rm(user_id)
	
	try:
		replied_user_id = update.message.reply_to_message.from_user.id
		replied_user_name = update.message.reply_to_message.from_user.first_name
		mention = f'<a href="tg://user?id={replied_user_id}">{replied_user_name}</a>'
		reason = afk.get(replied_user_id)
		if reason and reason != "None":
			update.message.reply_text("""
{} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(mention, reason), parse_mode = "HTML")
		elif reason:
			update.message.reply_text("""
{} is <b>AFK</b>!
		""".format(mention), parse_mode = "HTML")
		return
	except:
		print()
	reason = afk.get(get_mentioned_id(update))
	if reason and reason != "None":
		update.message.reply_text("""
{} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(get_mentioned_mention(update), reason), parse_mode = "HTML")
	elif reason:
			update.message.reply_text("""
{} is <b>AFK</b>!
		""".format(get_mentioned_mention(update)), parse_mode = "HTML")
	
	if text.startswith("/afk"):
		text = text.replace("/afk", "")
		text = text.strip()
		reason = "None"
		if text != "":
			reason = text
		afk.add(afk.AFK(user_id = user_id, reason = reason))
		mention = f'<a href="tg://user?id={user_id}">{user_name}</a>'
		
		if reason == "None":
			update.message.reply_text(f"{mention} is <b>AFK</b>!", parse_mode = "HTML")
		else:
			update.message.reply_text("""
{} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(mention, reason), parse_mode = "HTML")

def private(update, context):
	reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Bot Repository", url = "https://github.com/pranaovs/afk-telegram-bot")]])
	update.message.reply_text("Hello. This bot has no functions in PM.\nTo use this bot in your groups, you must fork it. Detailed guide given in bot repository", reply_markup = reply_markup)

def main(update, context):
	if update.message.from_user.username:
		users.add(users.User(user_id = update.message.from_user.id, username = update.message.from_user.username))
	if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
		return group(update, context)
	elif update.message.chat.type == "private":
		return private(update, context)

def new_member(update, context):
	for member in update.message.new_chat_members:
		if update.message.chat.id != int(os.environ.get("CHAT_ID")):
			caption = """This bot isn't made for this group.

To use AFK features, you will need to host your own bot. Detailed instructions given in Bot's repository.

If you don't wish to clone and self host, you can try @MissStella_bot instead, which has integrated AFK Features."""
			reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "Bot Repository", url = "https://github.com/pranaovs/afk-telegram-bot")]])
			update.message.reply_document("https://raw.githubusercontent.com/pranaovs/afk-telegram-bot/master/docs/EC04BA5E-7D75-47A6-A302-8176AA9EFA96.gif", caption = caption, reply_markup = reply_markup)
			context.bot.leave_chat(update.message.chat.id)

updater = Updater(os.environ.get("TOKEN"), use_context = True)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, main))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

updater.start_polling()
updater.idle()

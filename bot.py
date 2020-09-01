from telegram import *
from telegram.ext import *
import afk

def group(update, context):
	text = update.message.text
	user_id = update.message.from_user.id
	user_name = update.message.from_user.full_name
	
	try:
		replied_user_id = update.message.reply_to_message.from_user.id
		replied_user_name = update.message.reply_to_message.from_user.full_name
		reason = afk.get(replied_user_id)
		if reason and reason != "None":
			update.message.reply_text("""
{} is <b>AFK</b>!

Reason:\n<b>{}</b>
		""".format(replied_user_name, reason), parse_mode = "HTML")
		elif reason:
			update.message.reply_text("""
{} is <b>AFK</b>!
		""".format(replied_user_name), parse_mode = "HTML")
	except:
		print()
	if text.startswith("/afk"):
		text = text.replace("/afk", "")
		text = text.strip()
		reason = "None"
		if text != "":
			reason = text
		afk.add(afk.AFK(user_id = user_id, reason = reason))
		
		if reason == "None":
			context.bot.send_message(update.message.chat.id, f"{user_name} is <b>AFK</b>!", parse_mode = "HTML")
		else:
			context.bot.send_message(update.message.chat.id, """
{} is <b>AFK</b>!

Reason:\n<b>{}</b>
		""".format(user_name, reason), parse_mode = "HTML")
	elif afk.get(user_id):
		afk.rm(user_id)

def private(update, context):
	update.message.reply_text("Hello you!")

def main(update, context):
	if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
		return group(update, context)
	elif update.message.chat.type == "private":
		return private(update, context)

def new_member(update, context):
	for member in update.message.new_chat_members:
		if member.username == "CAPS_TV_AFKBot":
			update.message.reply_text("Hola")

updater = Updater("1142396420:AAERZKChnVfogO2c8FIt8WNB8v1YGZONbdQ", use_context = True)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, main))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

updater.start_polling()
updater.idle()

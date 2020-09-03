import os
from telegram import *
from telegram.ext import *
import users
import afk
import random

# Get the first mentioned user's user_id
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

# Get the first mentioned user's permanent link
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

# Respond to updates coming from groups or supergroups
def group(update, context):
	text = update.message.text
	user_id = update.message.from_user.id
	user_name = update.message.from_user.first_name
	
	mention = f'<a href="tg://user?id={update.message.from_user.id}">{update.message.from_user.first_name}</a>'
	
	# If the message was from an AFK user
	if afk.get(user_id):
		# Remove the record of that user in the database
		afk.rm(user_id)
	
	# Try and tell if the replied user is AFK
	try:
		replied_user_id = update.message.reply_to_message.from_user.id
		replied_user_name = update.message.reply_to_message.from_user.first_name
		rmention = f'<a href="tg://user?id={replied_user_id}">{replied_user_name}</a>'
		reason = afk.get(replied_user_id)
		if reason and reason != "None":
			update.message.reply_text("""
Hey {}, {} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(mention, rmention, reason), parse_mode = "HTML")
		elif reason:
			update.message.reply_text("""
Hey {}, {} is <b>AFK</b>!
		""".format(mention, rmention), parse_mode = "HTML")
		return
	except:
		print() # I just dunno why that's here :/
	
	# Try and tell if the first mentioned user is AFK
	reason = afk.get(get_mentioned_id(update))
	if reason and reason != "None":
		update.message.reply_text("""
Hey {}, {} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(mention, get_mentioned_mention(update), reason), parse_mode = "HTML")
	elif reason:
			update.message.reply_text("""
Hey {}, {} is <b>AFK</b>!
		""".format(mention, get_mentioned_mention(update)), parse_mode = "HTML")
	
	# Marking a user as AFK
	if text.startswith("/afk"):
		text = text.split(" ")
		del text[0]
		text = " ".join(text)
		reason = "None"
		if text != "":
			reason = text
		afk.add(afk.AFK(user_id = user_id, reason = reason))
		
		if reason == "None":
			update.message.reply_text(f"{mention} is <b>AFK</b>!", parse_mode = "HTML")
		else:
			update.message.reply_text("""
{} is <b>AFK</b>!

Reason: <b>{}</b>
		""".format(mention, reason), parse_mode = "HTML")

# Respond to updates coming from private chats
def private(update, context):
	reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "🛠 Bot Repository", url = "https://github.com/pranaovs/afk-telegram-bot")]])
	update.message.reply_text("Hello. This AFK bot has no functions in PM.\nTo use AFK Features in your groups, you must fork it. Detailed guide given in bot repository.", reply_markup = reply_markup)

def main(update, context):
	# If the user had a username
	if update.message.from_user.username:
		# Save the ID and username in the table to recognize it next time
		users.add(users.User(user_id = update.message.from_user.id, username = update.message.from_user.username))
	
	if update.message.chat.type == "supergroup" or update.message.chat.type == "group":
		return group(update, context)
	elif update.message.chat.type == "private":
		return private(update, context)

def new_member(update, context):
	for member in update.message.new_chat_members:
		# If the chat wasn't the one that the bot is dedicated to
		if update.message.chat.id != int(os.environ.get("CHAT_ID")):
			caption = """This bot isn't made for this group.\nTo use AFK features, you will need to host your own bot.\nDetailed instructions given in Bot's repository.\n\nIf you don't wish to clone and self host, you can try @MissStella_bot instead, which has integrated AFK features."""
			reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text = "🛠 Bot Repository", url = "https://github.com/pranaovs/afk-telegram-bot")]])
			
			# Say something
			update.message.reply_document("https://raw.githubusercontent.com/pranaovs/afk-telegram-bot/master/files/gif/leave/" + str(random.randrange(1,3)) + ".gif", caption = caption, reply_markup = reply_markup)
			
			# And leave the chat
			context.bot.leave_chat(update.message.chat.id)

TOKEN = os.environ.get("TOKEN")
PORT = os.environ.get("PORT", "8443")
APP_NAME = os.environ.get("APP_NAME")
updater = Updater(TOKEN, use_context = True)

dp = updater.dispatcher
dp.add_handler(MessageHandler(Filters.text, main))
dp.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))

updater.start_webhook(listen = "0.0.0.0", port = PORT, url_path = TOKEN)
updater.bot.set_webhook(f"https://{APP_NAME}.herokuapp.com/{TOKEN}")
updater.idle()

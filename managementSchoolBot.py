import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
	Updater,
	CommandHandler,
	MessageHandler,
	Filters,
	ConversationHandler,
	CallbackContext,
)
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import InlineQueryHandler
from managementSchoolProgramme import *

ID = [  ]#insert the telegram id of the administrator

#START METHOD

def start(update: Update, context: CallbackContext) -> None:
	"""Send a greeting message when the command /start is issued."""
	if update.effective_chat.id in ID:
		user = update.effective_user
		name = user["first_name"]
		surname = user["last_name"]
		
		if surname != None:
			update.message.reply_text('Hi %s %s' %(name, surname))
		else:
			update.message.reply_text('Hi %s' %name)

		update.message.reply_text("The commands available are 4:\n"
				"/insert    for introducing new students into the school\n"
				"/exit      when a students exit from the school\n"
				"/findname  for searching whether a student is or not in the school at the moment\n"
				"/number    view the number of students inside the school"
				)
	else: 
		update.message.reply_text("Ops... it looks like you haven't the permission to use this bot."
				"if you think this may be an error please write to the organization")

def heeelp(update: Update, context: CallbackContext):
	"""Show the commands available"""
	if update.effective_chat.id in ID:
		update.message.reply_text("The commands available are 4:\n"
				"/insert    for introducing new students into the school\n"
				"/exit      when a students exit from the school\n"
				"/findname  for searching whether a student is or not in the school at the moment\n"
				"/number    view the number of students inside the school"
				)
	else: 
		update.message.reply_text("Ops... it looks like you haven't the permission to use this bot."
				"if you think this may be an error please write to the organization")


#INSERT CONVERSATION
NAME, SURE_NAME = range(2) 


def insert(update: Update, context: CallbackContext) -> int:
	"""Explain the mode and ask the name"""
	if update.effective_chat.id in ID:
		update.message.reply_text(
			'Hi! This is the insert mode\n'
			'Send /CANCEL to quit from this command.\n\n'
			'Write name and surname'
		)

		return NAME 


def name_insert(update: Update, context: CallbackContext) -> int:
	"""Check if the name is correct"""
	reply_keyboard = [[update.message.text.lower(), '/CANCEL']] 
	user = update.message.from_user
	string1 = f"So {update.message.text} has just entered in the school?"
	string2 = f"Is this the correct name? {update.message.text}"
	update.message.reply_text(
		string1,
		reply_markup=ReplyKeyboardMarkup(
			reply_keyboard, one_time_keyboard=True, input_field_placeholder='Correct name?')
		)

	return SURE_NAME


def finally_insert(update: Update, context: CallbackContext) -> int:
	"""Insert the name"""
	inserted = InsertName(update.message.text)
	update.message.reply_text(
		inserted,
		reply_markup=ReplyKeyboardRemove()
	)

	return ConversationHandler.END


def cancel_insert(update: Update, context: CallbackContext) -> int:
	"""Cancels and ends the conversation."""
	user = update.message.from_user
	update.message.reply_text(
		'Bye! You have quitted /insert mode', reply_markup=ReplyKeyboardRemove()
	)

	return ConversationHandler.END







#EXIT CONVERSATION
NAME, SURE_NAME = range(2) 


def exit(update: Update, context: CallbackContext) -> int:
	"""Explain the mode and ask the name"""
	if update.effective_chat.id in ID:
		update.message.reply_text(
			'Hi! This is the exit mode\n'
			'Send /CANCEL to quit from this command.\n\n'
			'Write name and surname'
		)

		return NAME 


def name_exit(update: Update, context: CallbackContext) -> int:
	"""Check if the name is correct"""    
	reply_keyboard = [[update.message.text.lower(), '/CANCEL']] 
	user = update.message.from_user
	string1 = f"So {update.message.text.lower()} has just left the school?"
	update.message.reply_text(
		string1,
		reply_markup=ReplyKeyboardMarkup(
			reply_keyboard, one_time_keyboard=True, input_field_placeholder='Correct name?')
		)

	return SURE_NAME


def finally_exit(update: Update, context: CallbackContext) -> int:
	"""Insert the name"""
	removed = ExitName(update.message.text)
	update.message.reply_text(
		removed,
		reply_markup=ReplyKeyboardRemove()
	)

	return ConversationHandler.END


def cancel_exit(update: Update, context: CallbackContext) -> int:
	"""Cancels and ends the conversation."""
	user = update.message.from_user
	update.message.reply_text(
		'Bye! You have quitted /exit mode', reply_markup=ReplyKeyboardRemove()
	)

	return ConversationHandler.END







#FINDNAME CONVERSATION
NAME = range(1) 


def findname(update: Update, context: CallbackContext) -> int:
	"""Explain the mode and ask the name"""
	if update.effective_chat.id in ID:
		update.message.reply_text(
			'Hi! This is the findname mode\n'
			'Send /CANCEL to quit from this command.\n\n'
			'Write name and surname'
		)

		return NAME 


def name_find(update: Update, context: CallbackContext) -> int:
	"""Search the student"""    
	user = update.message.from_user
	student = update.message.text.lower()
	string1 = f"Looking for {student}..."
	update.message.reply_text(
			string1,
			reply_markup = ReplyKeyboardRemove()
			)
	string2 = SearchPeople(student)
	update.message.reply_text(
		string2,
		reply_markup=ReplyKeyboardRemove()
		)

	return ConversationHandler.END


def cancel_find(update: Update, context: CallbackContext) -> int:
	"""Cancels and ends the conversation."""
	user = update.message.from_user
	update.message.reply_text(
		'Bye! You have quitted /findname mode', reply_markup = ReplyKeyboardRemove()
	)

	return ConversationHandler.END





#NUMBER COMMAND


def number(update: Update, context: CallbackContext) -> int:
	"""Return the number of students"""
	if update.effective_chat.id in ID:
		number = Number_of_people()
		update.message.reply_text(
				number,
				reply_markup = ReplyKeyboardRemove()
		)


#SEND FILES COMMAND

def send_file(update: Update, context: CallbackContext) -> int:
	"""send partecipants.txt and timetables.txt"""
	if update.effective_chat.id in [614900728, 241470758]:
		user = update.message.from_user
		with open("./partecipants.txt", "rb") as fi:
			context.bot.send_document(
					chat_id = update.effective_chat.id,
					document = fi,
					filename = "PARTECIPANTS")

		with open("./timetable.txt", "rb") as fi:
			context.bot.send_document(
					chat_id = update.effective_chat.id,
					document = fi,
					filename = "TIMETABLE"
					)


# ADD ID COMMAND

def add_id(update: Update, context: CallbackContext) -> None:
	"""Add an user ID to the list."""
	if update.effective_chat.id in [614900728, 241470758]:
		try:
			new_id = int(update.message.text[8:])
		except ValueError:
			pass
		else:
			ID.append(new_id)
			update.message.reply_text(str(new_id) + " added to the authorized user of this bot")
		
	else: 
		update.message.reply_text("Ops... it looks like you haven't the permission to use this command."
				"if you think this may be an error please write to the organization")




def main() -> None:
	"""Start the bot."""
	# Create the Updater and pass it your bot's token.
	updater = Updater("insert your bot token",)

	# Get the dispatcher to register handlers
	dispatcher = updater.dispatcher

	#Create the conversation handlers
	insert_handler = ConversationHandler(
		entry_points=[CommandHandler('insert', insert)],
		states={
			NAME: [MessageHandler(Filters.regex(".* .*"), name_insert)],
			SURE_NAME: [MessageHandler(Filters.regex(".* .*"), finally_insert)], 

		},
		fallbacks=[CommandHandler('CANCEL', cancel_insert)],
	)

	exit_handler = ConversationHandler(
		entry_points=[CommandHandler('exit', exit)],
		states={
			NAME: [MessageHandler(Filters.regex(".* .*"), name_exit)],
			SURE_NAME: [MessageHandler(Filters.regex(".* .*"), finally_exit)], 

		},
		fallbacks=[CommandHandler('CANCEL', cancel_exit)],
	)
   
	findname_handler = ConversationHandler(
			entry_points=[CommandHandler('findname', findname)],
		states={
			NAME: [MessageHandler(Filters.regex(".* .*"), name_find)],
		},
		fallbacks=[CommandHandler('CANCEL', cancel_find)],
	)



	# on different commands - answer in Telegram
	dispatcher.add_handler(CommandHandler("start", start)) # start command for the beginnig 
	dispatcher.add_handler(CommandHandler("help", heeelp))
	dispatcher.add_handler(CommandHandler("number", number))
	dispatcher.add_handler(CommandHandler("send_files", send_file))
	dispatcher.add_handler(CommandHandler("add_id", add_id))
	dispatcher.add_handler(insert_handler) # add to dispatcher the insert conversation handler
	dispatcher.add_handler(exit_handler)
	dispatcher.add_handler(findname_handler)

	
	# Start the Bot
	updater.start_polling()

	# Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
	# start_polling() is non-blocking and will stop the bot gracefully.
	updater.idle()




if __name__ == '__main__':
	main()

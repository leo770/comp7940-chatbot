from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,CallbackContext)
# import configparser
import logging
import redis
import os

'''
import os # using in google conlab to import .py
path = "/content"
os.chdir(path)
'''

from ChatGPT_HKBU import HKBU_ChatGPT

global redis1
def main():
  # Load your token and create an Updater for your Bot
  # config = configparser.ConfigParser()
  # config.read('config.ini')
  # updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
  updater = Updater(token=(os.environ['ACCESS_TOKEN']), use_context=True)
  dispatcher = updater.dispatcher
  global redis1
  redis1 = redis.Redis(host=(os.environ['HOST']),
    password=(os.environ['PASSWORD']),
    port=(os.environ['REDISPORT']))


  # You can set this logging module, so you will know when
  # and why things do not work as expected Meanwhile, update your config.ini as:
  logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
  # register a dispatcher to handle message: here we register an echo dispatcher
  # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
  # dispatcher.add_handler(echo_handler)
  # on different commands - answer in Telegram
  dispatcher.add_handler(CommandHandler("add", add))
  dispatcher.add_handler(CommandHandler("set", set))
  dispatcher.add_handler(CommandHandler("get", get))
  dispatcher.add_handler(CommandHandler("delete", delete))
  dispatcher.add_handler(CommandHandler("hello", hello))
  dispatcher.add_handler(CommandHandler("hkstory", hkstory))
  dispatcher.add_handler(CommandHandler("help", help_command))

  # dispatcher for chatgpt
  global chatgpt
  chatgpt = HKBU_ChatGPT()
  chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equiped_chatgpt)
  dispatcher.add_handler(chatgpt_handler)

  # To start the bot:
  updater.start_polling()
  updater.idle()




def echo(update, context):
  reply_message = update.message.text.upper()
  logging.info("Update: " + str(update))
  logging.info("context: " + str(context))
  context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /help is issued."""
  update.message.reply_text('Helping you helping you.')
def add(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /add is issued."""
  try:
    global redis1
    logging.info(context.args[0])
    msg = context.args[0] # /add keyword <-- this should store the keyword
    redis1.incr(msg)
    update.message.reply_text('You have said ' + msg + ' for ' +
    redis1.get(msg).decode('UTF-8') + ' times.')
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /add <keyword>')

def set(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /add is issued."""
  try:
    global redis1
    logging.info(context.args[0])
    msg = context.args[0] # /add keyword <-- this should store the keyword
    redis1.set(msg, 0)
    update.message.reply_text('You have set ' + msg + ' for ' +
    redis1.get(msg).decode('UTF-8') + ' times.')
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /set <keyword>')

def get(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /add is issued."""
  try:
    global redis1
    logging.info(context.args[0])
    msg = context.args[0] # /add keyword <-- this should store the keyword
    update.message.reply_text('Now the Key words ' + msg + ' is ' +
    redis1.get(msg).decode('UTF-8') + ' times.')
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /get <keyword>')

def delete(update: Update, context: CallbackContext) -> None:
  """Send a message when the command /add is issued."""
  try:
    global redis1
    logging.info(context.args[0])
    msg = context.args[0] # /add keyword <-- this should store the keyword
    redis1.delete(msg)
    update.message.reply_text('You have deleted ' + msg + ' from the database ')
  except (IndexError, ValueError):
    update.message.reply_text('Usage: /delete <keyword>')

def equiped_chatgpt(update, context):
  global chatgpt
  reply_message = chatgpt.submit(update.message.text)
  logging.info("Update: " + str(update))
  logging.info("context: " + str(context))
  context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def hello(update, context):
  msg = context.args[0]
  update.message.reply_text('Good day, ' + msg)

def hkstory(update, context):
  msg = context.args[0]
  if msg == "由乱及治" :
    update.message.reply_text('由治及兴')
  else :
    update.message.reply_text('要支持香港，请输入由乱及治')



if __name__ == '__main__':
  main()
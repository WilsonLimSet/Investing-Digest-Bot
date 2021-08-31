"""
Simple Bot to send Tweets as Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
"""

#Twitter setup
import tweepy as tw
import pandas as pd
from tweepy import OAuthHandler

consumer_key = 'Input Your Own'
consumer_secret = 'Input Your Own'
access_token = 'Input Your Own'
access_secret = 'Input Your Own'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tw.API(auth, wait_on_rate_limit=True)

timeline = api.home_timeline(count =10)
json_data = [r._json for r in timeline]
df = pd.json_normalize(json_data)
df['created_at'] = df['created_at'].str.slice(start=0,stop=10)
df["key"] = "On " + df['created_at'] + ", " + df['user.name'] + " Said " + df['text']
print(df.head())
key = df['key'].astype(str)
key = key.to_string(index = False)

df.to_excel('tweets.xlsx',index = False)
#Twitter Setup

import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('I am a bot sending you Tweets from Investors such as Chamath and Naval!')

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def tweet(update, context):
        "Tweet."
        update.message.reply_text(key)

def main():
    "Start the bot."
    # Create the Updater and pass it your bot's token.
    updater = Updater("1593215372:AAGFSWskvPB-cKV6iBj_0d5iBxZlKlBxfL0", use_context=True, request_kwargs={'read_timeout': 6, 'connect_timeout': 7})

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler('help', help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(CommandHandler('tweet', tweet))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()

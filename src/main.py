from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import openai
import os

openai.api_key = 'YOUR_OPENAI_API_KEY'

chat_history = {}

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет, {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

def echo(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    user_message = update.message.text

    if user_id not in chat_history:
        chat_history[user_id] = []

    chat_history[user_id].append(f"User: {user_message}")

    prompt = "\n".join(chat_history[user_id]) + "\nAI:"

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )

    bot_reply = response.choices[0].text.strip()

    chat_history[user_id].append(f"AI: {bot_reply}")

    update.message.reply_text(bot_reply)

def main() -> None:
    updater = Updater("YOUR_TELEGRAM_API_TOKEN")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

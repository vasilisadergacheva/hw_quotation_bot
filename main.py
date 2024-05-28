from _token._token import TOKEN
from utils.utils import PhotoConverter

from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes

converter = PhotoConverter()


async def unknown_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id, text="Привет, загрузи фотографию"
    )


async def set_text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global converter
    converter.text = update.message.text


async def handle_file(file, update: Update, context: ContextTypes.DEFAULT_TYPE):
    file_name = "files/" + str(update.effective_chat.id)
    chat_id = update.effective_chat.id
    await file.download_to_drive(file_name)
    await context.bot.send_message(chat_id=chat_id, text="Файл получен")

    try:
        converter(file_name)
        await context.bot.send_document(chat_id=chat_id, document=file_name + ".png")
    except Exception as e:
        await context.bot.send_message(
            chat_id=chat_id, text="Ошибка обработки:\n" + str(e)
        )
        return None


async def file_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.document)
    await handle_file(file, update, context)


async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    await handle_file(file, update, context)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    """
    Work with user.
    """

    file_handler = MessageHandler(filters.Document.ALL, file_handler)
    application.add_handler(file_handler)

    photo_handler_instance = MessageHandler(filters.PHOTO, photo_handler)
    application.add_handler(photo_handler_instance)

    """
    Text.
    """

    unknown_handler_for_text = MessageHandler(filters.TEXT, set_text_handler)
    application.add_handler(unknown_handler_for_text)

    """
    For unknown.
    """
    unknown_handler_for_command = MessageHandler(filters.COMMAND, unknown_handler)
    application.add_handler(unknown_handler_for_command)

    application.run_polling()

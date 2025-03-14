import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext

# 🔹 CONFIGURACIÓN: PON TU API KEY DE GEMINI Y TELEGRAM AQUÍ
GEMINI_API_KEY = "AIzaSyBgUVi8PvjKqfiCJCJxhynzuorBJwnciXM"
TELEGRAM_BOT_TOKEN = "7599284560:AAE8PwZ1kx37ByQIfMOZbe4XOJDYrG2iHDM"

# 🔹 Configurar la API de Gemini
genai.configure(api_key=GEMINI_API_KEY)

# 🔹 Configurar los logs (para ver errores o mensajes en la terminal)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# 🔹 Función para manejar mensajes con Gemini
async def handle_message(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text  # Captura el mensaje del usuario
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # Modelo actualizado de Gemini
        response = model.generate_content(user_message)
        bot_response = response.text if response else "No pude generar una respuesta."
        await update.message.reply_text(bot_response)  # Envía la respuesta al usuario
    except Exception as e:
        logger.error(f"Error al llamar a la API de Gemini: {e}")
        await update.message.reply_text("Hubo un problema al procesar tu solicitud.")

# 🔹 Función para iniciar el bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('¡Hola! Soy tu bot de Mimenticos con Gemini AI. ¿En qué puedo ayudarte?')

# 🔹 Función principal para configurar el bot de Telegram
def main() -> None:
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Bot en funcionamiento...")
    application.run_polling()

if __name__ == '__main__':
    main()

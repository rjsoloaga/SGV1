# main_with_webhook.py

from webhook_listener import app
import threading

def iniciar_webhook():
    app.run(port=5000)

webhook_thread = threading.Thread(target=iniciar_webhook)
webhook_thread.daemon = True
webhook_thread.start()
import firebase_admin
from firebase_admin import credentials, messaging
import os
import logging

# Log ayarları
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_firebase():
    if not firebase_admin._apps:
        basedir = os.path.abspath(os.path.dirname(__file__))
        cred_path = os.path.join(basedir, '..', 'ai-discount-notifier-main-firebase-adminsdk-fbsvc-d6162fb703.json')
        cred_path = os.path.abspath(cred_path)

        if not os.path.exists(cred_path):
            logger.error(f"Firebase credentials dosyası bulunamadı: {cred_path}")
            return False

        try:
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            logger.info("Firebase başarıyla başlatıldı.")
            return True
        except Exception as e:
            logger.exception("Firebase başlatılırken hata oluştu:")
            return False
    else:
        logger.info("Firebase zaten başlatılmış.")
        return True


def send_notification(title, body, topic=None, token=None):
    if not init_firebase():
        return

    if not topic and not token:
        logger.warning("Bildirim göndermek için en az bir topic veya token belirtmelisin.")
        return

    try:
        notification = messaging.Notification(title=title, body=body)

        if topic:
            message = messaging.Message(notification=notification, topic=topic)
        elif token:
            message = messaging.Message(notification=notification, token=token)

        response = messaging.send(message)
        logger.info(f"Bildirim gönderildi: {response}")
    except Exception as e:
        logger.exception("Bildirim gönderilirken hata oluştu:")


def subscribe_to_topic(token, topic):
    if not init_firebase():
        return

    try:
        response = messaging.subscribe_to_topic([token], topic)
        logger.info(f"{response.success_count} cihaz '{topic}' konusuna abone oldu.")
    except Exception as e:
        logger.exception("Cihaz abone edilirken hata oluştu:")


# Test amaçlı direkt çalıştırma
if __name__ == "__main__":
    if init_firebase():
        send_notification("Test Bildirim", "Bu bir testtir", topic="fiyatTakip")

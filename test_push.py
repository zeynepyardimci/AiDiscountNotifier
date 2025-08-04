from backend.notifications import push_sender

def test_push():
    push_sender.init_firebase()
    push_sender.send_notification("Test Bildirim", "Bu bir test bildirimidir.")

if __name__ == "__main__":
    test_push() 
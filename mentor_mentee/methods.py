import threading
from typing import List

from django.conf import settings
from django.core.mail import send_mail


def send_email_custom(to: List[str], subject: str, body: str):
    t = threading.Thread(target=send_mail, kwargs= {
        'subject': subject,
        'message': body,
        'from_email': settings.EMAIL_HOST_USER,
        'recipient_list': to
    })
    t.setDaemon(True)  # TODO check if these threads are discarded upon completion or not
    t.start()

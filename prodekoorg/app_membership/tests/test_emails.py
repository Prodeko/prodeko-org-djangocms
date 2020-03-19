from django.core import mail

from ..views import send_email
from .test_data import TestData


class EmailTest(TestData):
    def test_send_email(self):
        user = self.test_pendinguser_model

        # Send message.
        send_email(user)

        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)

        # Verify that the subject of the first message is correct.
        subject = f"Uusi jäsenhakemus - {user.first_name} {user.last_name}"
        self.assertEqual(mail.outbox[0].subject, subject)

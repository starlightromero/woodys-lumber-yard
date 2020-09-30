"""Import flask, flask_mail, and flask_blog."""
from flask import url_for
from flask_mail import Message
from online_store import mail


def send_reset_email(user):
    """Send password reset email to given user."""
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request",
        recipients=[user.email],
    )
    msg.body = f"""To reset your password, visit the following link:

{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email.
"""
    mail.send(msg)

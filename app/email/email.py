from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

from flask import current_app, flash
from app.config import EMAIL_HOST, EMAIL_PORT, EMAIL_PASSWORD, EMAIL_ADDRESS
from werkzeug.security import generate_password_hash
import random 
import string


def send_email(to_address, subject, message, cc_addresses=None):
    
    email = MIMEMultipart()
    email['From'] = current_app.config['EMAIL_ADDRESS']
    email['To'] = to_address
    email['Subject'] = subject

    if cc_addresses:
        email['Cc'] = ', '.join(cc_addresses)
    else:
        cc_addresses = []  

    email.attach(MIMEText(message, 'html'))

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.ehlo()
        server.starttls()
        server.login(current_app.config['EMAIL_ADDRESS'], current_app.config['EMAIL_PASSWORD'])
        server.sendmail(email['From'], [to_address] + cc_addresses, email.as_string())
        server.quit()
        flash("E-mail envoyé avec succès !")
    except smtplib.SMTPAuthenticationError:
        flash("Erreur d'authentification : Vérifiez l'adresse e-mail et le mot de passe.")
    except smtplib.SMTPConnectError:
        flash("Erreur de connexion : Impossible de se connecter au serveur SMTP.")
    except smtplib.SMTPException as e:
        flash(f"Erreur SMTP : {e}")
    except Exception as e:
        flash(f"Erreur générale : {e}")


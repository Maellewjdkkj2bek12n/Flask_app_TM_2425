from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

from app.db.db import get_db, close_db
import os

from werkzeug.utils import secure_filename

# Routes /...
creation_bp = Blueprint('creation', __name__)

# Route /affichage
@creation_bp.route('/affichage', methods=('GET', 'POST'))
def affichage():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    db = get_db()  
    username = session.get('user_id')  # Récupère l'utilisateur en cours
    image = db.execute(
        "SELECT chemin_fichier FROM oeuvres WHERE utilisateur = ? ORDER BY id_oeuvre DESC LIMIT 1", (username,)).fetchone()

    if image:
        image_url = image['chemin_fichier']  # Récupère le chemin stocké
    else:
        image_url = None  # Si aucun fichier trouvé, mettre à None

    return render_template('creation/affichage.html', image_url=image_url, photo=photo)


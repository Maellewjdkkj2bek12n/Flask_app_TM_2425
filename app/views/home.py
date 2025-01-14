from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

from app.db.db import get_db, close_db
import os

from werkzeug.utils import secure_filename

# Routes /...
home_bp = Blueprint('home', __name__)



# Route /
@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    user_id = session.get('user_id')
    
    if user_id: 
        db = get_db()
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]

        exclusion_ids.append(user_id)

        if exclusion_ids:
           photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur NOT IN ({})".format(', '.join('?' for _ in exclusion_ids)), exclusion_ids).fetchall()
        
        else:
            photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur != ?", (user_id,)).fetchall()
        
        close_db()

    
    if not user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
        close_db()
    
    return render_template('home/index.html', photo=photo, categories=categories, )

# Gestionnaire d'erreur 404 pour toutes les routes inconnues
@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404




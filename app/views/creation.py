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
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    user_id = session.get('user_id')
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE NOT utilisateur = ?",(user_id,)).fetchall() 
    close_db()
    
    db = get_db()
    photoagrandie_id = request.args.get('photogrand_id', )
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    close_db()
    
    db = get_db()
    user_id = photoagrandie['utilisateur']
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
    close_db()
    return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user)


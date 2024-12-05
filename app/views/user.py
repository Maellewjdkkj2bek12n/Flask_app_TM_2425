from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

from app.db.db import get_db, close_db
import os

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profil_autre', methods=('GET', 'POST')) 
def show_autreprofile() :
    
    page_type = 'profil_autre'
    return render_template('user/profil autre.html', page_type=page_type)


@user_bp.route('/profil', methods=('GET', 'POST'))
def show_profile():
    
    page_type = 'profil'
    return render_template('user/profil.html', page_type=page_type, user=g.user)

#Ici c'est où je pense qu'il y a le problème, normalement grâce à ça la bio devrait changer mais ça ne fonctionne pas
@user_bp.route('/profil', methods=('GET', 'POST'))
def modifier_bio ():
    page_type = 'profil'
    
    if request.method == 'POST':
        bio = request.form['bio']
        user_id = session.get('user_id')
        
        if bio:
            db = get_db()
            try:
                db.execute('UPDATE utilisateurs SET bio = ? WHERE id_utilisateur = ?', (bio, user_id))
                db.commit()
            
            finally:
                db = close_db()
                return redirect(url_for('user.show_profile'))
    
    # Affichage du formulaire quand la requête est GET
    return render_template('user/profil.html', page_type=page_type, user=g.user)
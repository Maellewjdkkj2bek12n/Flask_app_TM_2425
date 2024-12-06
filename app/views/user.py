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
    return render_template('user/profil autre.html')


@user_bp.route('/profil', methods=('GET', 'POST'))
@login_required
def show_profile():
    return render_template('user/profil.html', user=g.user)

@user_bp.route('/bio', methods=('GET', 'POST'))
def change_bio():
    if request.method == 'POST':
        bio = request.form.get('bio', '').strip()
        user_id = session.get('user_id')
        
        if bio:
            
            db = get_db()
            try:
                db.execute('UPDATE utilisateurs SET bio = ? WHERE id_utilisateur = ?', (bio, user_id))
                db.commit()
                
            except db.IntegrityError:
                error = "Oups, la bio est trop longue."
                flash(error)
                return redirect(url_for("user.show_profile"))
            
            finally:
                db = close_db()
                return redirect(url_for('user.show_profile'))
    return render_template('user/profil.html', user=g.user)

@user_bp.route('/username', methods=('GET', 'POST'))
def change_username():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        user_id = session.get('user_id')
        
        if username:
            db = get_db()
            try:
                db.execute('UPDATE utilisateurs SET nom_utilisateur = ? WHERE id_utilisateur = ?', (username, user_id))
                db.commit()
            
            except db.IntegrityError:
                error = "Oups, l'utilisateur {username} déjà enregistré."
                flash(error)
                return redirect(url_for("user.show_profile"))
            
            finally:
                db = close_db()
                return redirect(url_for('user.show_profile'))
    return render_template('user/profil.html', user=g.user)
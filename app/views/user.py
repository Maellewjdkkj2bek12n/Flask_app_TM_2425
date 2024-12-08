from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

from app.db.db import get_db, close_db
import os

from werkzeug.utils import secure_filename

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profil_autre', methods=('GET', 'POST')) 
def show_autreprofile() :
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    return render_template('user/profil autre.html',photo=photo)


@user_bp.route('/profil', methods=('GET', 'POST'))
@login_required
def show_profile():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    return render_template('user/profil.html', user=g.user,photo=photo)

@user_bp.route('/bio', methods=('GET', 'POST'))
def change_bio():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
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
    return render_template('user/profil.html', user=g.user, photo=photo)

@user_bp.route('/username', methods=('GET', 'POST'))
def change_username():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
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
    return render_template('user/profil.html', user=g.user, photo=photo)

@user_bp.route('/chemin_fichier', methods=('GET', 'POST'))
def chemin_fichier():
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    upload = request.form['upload']
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        
        if upload :
            db = get_db()
            try:
                db.execute("INSERT INTO oeuvres (chemin_fichier, utilisateur) VALUES (?, ?)",(upload , user_id))
                db.commit()
            finally:
                db = close_db()
                image_url = upload
                return render_template('user/upload.html', image_url=image_url, categories=categories)

    return render_template('user/upload.html', image_url=image_url, categories=categories)

@user_bp.route('/photo_profil', methods=('GET', 'POST'))
def change_photo_profil():  
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    photo_profil = request.form['photo_profil']
    user_id = session.get('user_id')
    if request.method == 'POST':
        
        if photo_profil :
            db = get_db()  
            try:
                    db.execute('UPDATE utilisateurs SET photo_profil = ? WHERE id_utilisateur = ?', (photo_profil, user_id))
                    db.commit()
                
            except db.IntegrityError:
                    error = "Oups, l'utilisateur {username} déjà enregistré."
                    flash(error)
                    return redirect(url_for("user.show_profile"))
                
            finally:
                    db = close_db()
                    return redirect(url_for('user.show_profile'))

    return render_template('user/profil.html', user=g.user,photo=photo)
    


    
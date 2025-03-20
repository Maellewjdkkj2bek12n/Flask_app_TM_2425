from enum import auto
from mailbox import Message
import random
import string
from flask import (Blueprint, current_app, flash, g, jsonify, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route /auth/register
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    if request.method == 'POST':
        mail = request.form['mail'] 
        #code = request.form['code'] 
        username = request.form['username'] 
        password = request.form['password'] 
        confirm_password = request.form['confirm_password']
        db = get_db()
        if username and password and mail and confirm_password :
            
            if password != confirm_password: 
                error = "Les mots de passe ne correspondent pas." 
                flash(error) 
                return redirect(url_for("auth.register"))
             
            #if code != session.get('confirmation_code'): 
            #    flash('Code de confirmation incorrect.') 
            #    return redirect(url_for("auth.register"))
            
            try:
                db.execute("INSERT INTO utilisateurs (adresse_mail, nom_utilisateur, mot_passe) VALUES (?, ?, ?)",(mail, username, generate_password_hash(password)))
                db.commit()
                close_db()
              
            except db.IntegrityError:
                error = f"Oups, l'utilisateur \"{username}\" ou le mail \"{mail}\" est déjà enregistré."
                flash(error)

                return redirect(url_for("auth.register"))
            
            return redirect(url_for("auth.login"))
         
        else:
            error = "Remplir tout les champs"
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('home/index.html', photo=photo)

# Route /auth/login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = ?', (username,)).fetchone()
        close_db()
        error = None
        if user is None:
            error = "Le nom d'utilisateur est incorrect."
        elif not check_password_hash(user['mot_passe'], password):
            error = "Le mot de passe est incorrect."
        if error is None:
            session.clear()
            session['user_id'] = user['id_utilisateur']
            return redirect("/")
        
        else:
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('home/index.html', photo=photo)

# Route /auth/logout
@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@auth_bp.before_app_request
def load_logged_in_user():

    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        db = get_db()
        g.user = db.execute('SELECT * FROM utilisateurs WHERE id_utilisateur = ?', (user_id,)).fetchone()
        close_db()
        
        
@auth_bp.route('/MDP', methods=['GET', 'POST'])
def MDP():
    user_id = session.get('user_id')
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    if request.method == 'POST':
        mail = request.form['nom']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not mail or not password or not confirm_password:
            flash("Veuillez remplir tous les champs.")
            return redirect(url_for('auth.MDP'))

        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for('auth.MDP'))

        db = get_db()
        
        user = db.execute('SELECT * FROM utilisateurs WHERE adresse_mail = ?', (mail,)).fetchone()
        if user_id :
            if user_id != user['id_utilisateur'] :
                flash("Cette adresse mail n'est pas attribuée à ce compte")
                return redirect(url_for('auth.MDP'))

        if user:
            hashed_password = generate_password_hash(password)

            try:
                db.execute('UPDATE utilisateurs SET mot_passe = ? WHERE adresse_mail = ?', (hashed_password, mail))
                db.commit()
                return redirect(url_for('auth.logout'))  
            except Exception as e:
                db.rollback()  
                flash("Une erreur est survenue lors de la mise à jour du mot de passe.")
            finally:
                db = close_db()
                return render_template('home/index.html', photo=photo)
        else:
            flash("Aucun utilisateur enregistré avec cet e-mail.")
            db = close_db()
            page_type= "MDP"
            return redirect(url_for('auth.MDP', page_type=page_type))
        
        
    else:

        page_type= "MDP"
        random.shuffle(photo)
        return render_template('auth/MDP.html', photo=photo, page_type=page_type)

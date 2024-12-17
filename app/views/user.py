from flask import (Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for)
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
    db = get_db()
    user_id = request.args.get('user')
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
    close_db()
    
    return render_template('user/profil autre.html',photo_user=photo_user, user=user)

@user_bp.route('/profil', methods=('GET', 'POST'))
@login_required
def show_profile():
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    close_db()
    
    return render_template('user/profil.html', user=g.user,photo_user=photo_user)

#pour changer la bio
@user_bp.route('/bio', methods=('GET', 'POST'))
def change_bio():
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
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
    return render_template('user/profil.html', user=g.user, photo_user=photo_user)

#pour changer le nom d'utilisateur
@user_bp.route('/username', methods=('GET', 'POST'))
def change_username():
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
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
    return render_template('user/profil.html', user=g.user, photo_user=photo_user)

#pour changer la photo de profil
@user_bp.route('/photo_profil', methods=('GET', 'POST'))
def change_photo_profil():  
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    close_db()
    
    if request.method == 'POST':
        if 'image' not in request.files:
            return "Aucun fichier envoyé", 400

        file = request.files['image']

        if file.filename == '':
            return "Fichier sans nom", 400
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

        if not allowed_file(file.filename):
            return "Type de fichier non autorisé", 400

        if file:
            filename = file.filename
            filepath = os.path.join(current_app.config['IMAGE_FOLDER'], filename)

            
            if not os.path.exists(current_app.config['IMAGE_FOLDER']):
                os.makedirs(current_app.config['IMAGE_FOLDER'])

            try:
                file.save(filepath)
            except Exception as e:
                return f"Erreur lors de la sauvegarde du fichier : {e}", 500

            photo_profil = url_for('static', filename=f'images/{filename}', _external=True)

            user_id = session.get('user_id') 
            if user_id is None:
                return "Utilisateur non connecté", 403
        
            if photo_profil :
                db = get_db()  
                try:
                        db.execute('UPDATE utilisateurs SET photo_profil = ? WHERE id_utilisateur = ?', (photo_profil, user_id))
                        db.commit()
                    
                except db.IntegrityError:
                        error = "Oups, l'utilisateur {username} est déjà enregistré."
                        flash(error)
                        return redirect(url_for("user.show_profile"))
                    
                finally:
                        db = close_db()
                        return redirect(url_for('user.show_profile'))

        return render_template('user/profil.html', user=g.user,photo_user=photo_user)

#pour ajouter des oeuvres
@user_bp.route('/chemin_fichier', methods=('GET', 'POST'))
def chemin_fichier():
    db = get_db()

    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    if request.method == 'POST':
        if 'upload' not in request.files:
            return "Aucun fichier envoyé", 400

        file = request.files['upload']

        if file.filename == '':
            return "Fichier sans nom", 400
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

        if not allowed_file(file.filename):
            return "Type de fichier non autorisé", 400

        if file:
            filename = file.filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)

            # Vérifiez si le répertoire existe, sinon créez-le
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            try:
                file.save(filepath)
            except Exception as e:
                return f"Erreur lors de la sauvegarde du fichier : {e}", 500

            # Utilisez url_for pour générer l'URL du fichier
            image_url = url_for('static', filename=f'uploads/{filename}', _external=True)

            user_id = session.get('user_id') 
            if user_id is None:
                return "Utilisateur non connecté", 403

            if image_url and user_id: 
                db = get_db()
                try:
                    db.execute(
                        "INSERT INTO oeuvres (chemin_fichier, utilisateur) VALUES (?, ?)", (image_url, user_id))
                    db.commit()
                except Exception as e:
                    db.rollback()
                    return f"Erreur lors de l'enregistrement : {e}", 500
                finally:
                    close_db()
                return render_template('user/upload.html', image_url=image_url, categories=categories)


# pour selectionner les catégories 
@user_bp.route('/change_categorie', methods=('GET', 'POST'))
def change_categorie():
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    close_db()
    
    categorie_id = request.form.get('categorie_id')
    image_url = request.args.get("image_url")
    oeuvre = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE chemin_fichier = ?", (image_url,)).fetchone()
    oeuvre_id = oeuvre['id_oeuvre']
    if not image_url:
        return "Erreur : aucune œuvre trouvée pour ce chemin de fichier.", 404
    if categorie_id :
        db = get_db()
        db.execute("INSERT INTO categorisations (categorie, oeuvre) VALUES (?, ?)",(categorie_id , oeuvre_id))
        db.commit()
        db = close_db()
        return redirect(url_for('user.show_profile'))
    return render_template('user/profil.html', user=g.user,photo_user=photo_user)


    


    
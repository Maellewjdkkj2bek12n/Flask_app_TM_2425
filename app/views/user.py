from flask import (Blueprint, current_app, flash, g, json, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash
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
@login_required
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
@login_required
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
                error = "Oups, l'utilisateur est déjà enregistré."
                flash(error)
                return redirect(url_for("user.show_profile"))
            
            finally:
                db = close_db()
                return redirect(url_for('user.show_profile'))
    return render_template('user/profil.html', user=g.user, photo_user=photo_user)

#pour changer la photo de profil
@user_bp.route('/photo_profil', methods=('GET', 'POST'))
@login_required
def change_photo_profil():  
    user_id = session.get('user_id')
    db = get_db()  
    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    close_db()
    
    if request.method == 'POST':
        if 'image' not in request.files:
            error = "Aucune image selectionnée."
            flash(error)
            return redirect(url_for("user.show_profile"))

        file = request.files['image']

        if file.filename == '':
            error ="Veuillez nommer votre fichier."
            flash(error)
            return redirect(url_for("user.chemin_fichier"))
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

        if not allowed_file(file.filename):
            error= "Type de fichier non autorisé."
            flash(error)
            return redirect(url_for("user.show_profile"))

        if file:
            filename = file.filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            base_name, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(filepath):
                # Ajouter un suffixe sous la forme _1, _2, etc.
                filename = f"{base_name}_{count}{extension}"
                filepath = os.path.join(current_app.config['IMAGE_FOLDER'], filename)
                count += 1

            if not os.path.exists(current_app.config['IMAGE_FOLDER']):
                os.makedirs(current_app.config['IMAGE_FOLDER'])

            try:
                file.save(filepath)
            except Exception as e:
                error = "Erreur lors de la sauvegarde du fichier."
                flash(error)
                return redirect(url_for("user.show_profile"))

            photo_profil = url_for('static', filename=f'images/{filename}', _external=True)

            user_id = session.get('user_id') 
           
        
            if photo_profil :
                db = get_db()  
                try:
                        db.execute('UPDATE utilisateurs SET photo_profil = ? WHERE id_utilisateur = ?', (photo_profil, user_id))
                        db.commit()
                    
                except db.IntegrityError:
                        error = "Erreur lors de la sauvegarde du fichier."
                        flash(error)
                        return redirect(url_for("user.show_profile"))
                    
                finally:
                        db = close_db()
                        return redirect(url_for('user.show_profile'))

        return render_template('user/profil.html', user=g.user,photo_user=photo_user)

#pour ajouter des oeuvres
@user_bp.route('/chemin_fichier', methods=('GET', 'POST'))
@login_required
def chemin_fichier():
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    if request.method == 'POST':
        if 'upload' not in request.files:
            error= "Aucun fichier envayé."
            flash(error)
            return redirect(url_for("user.show_profile"))

        file = request.files['upload']

        if file.filename == '':
            error= "Veuillez nommer votre fichier."
            flash(error)
            return redirect(url_for("user.show_profile"))
        
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

        if not allowed_file(file.filename):
            error= "Type de fichier non autorisé."
            flash(error)
            return redirect(url_for("user.show_profile"))

        if file:
            filename = file.filename
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            
            base_name, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(filepath):
                # Ajouter un suffixe sous la forme _1, _2, etc.
                filename = f"{base_name}_{count}{extension}"
                filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                count += 1

            # Vérifiez si le répertoire existe, sinon créez-le
            if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
                os.makedirs(current_app.config['UPLOAD_FOLDER'])

            try:
                file.save(filepath)
            except Exception as e:
                close_db()
                error ="Erreur lors de la sauvegarde du fichier"
                flash(error)
                return redirect(url_for("user.chemin_fichier"))

            # Utilisez url_for pour générer l'URL du fichier
            image_url = url_for('static', filename=f'uploads/{filename}', _external=True)
            user_id = session.get('user_id') 

            if image_url and user_id: 
                db = get_db()
                try:
                    db.execute("INSERT INTO oeuvres (chemin_fichier, utilisateur, nom) VALUES (?, ?, ?)", (image_url, user_id, filename))
                    db.commit()
                except Exception as e:
                    db.rollback()
                    close_db()
                    error ="Erreur lors de l'enregistrement"
                    flash(error)
                    return redirect(url_for("user.chemin_fichier"))
                finally:
                    oeuvres = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE chemin_fichier = ?", (image_url ,)).fetchone()
                    close_db()
                return render_template('user/upload.html',image_url=image_url, oeuvres=oeuvres, categories=categories)
    return render_template('user/upload.html', categories=categories)


# pour selectionner les catégories 
@user_bp.route('/change_categorie', methods=['POST'])
@login_required
def change_categorie():
    clicked_categories = request.form.get('clicked_categories')
    db = get_db()
    oeuvre_id = request.args.get('oeuvre_id', )
    
    if not clicked_categories:
        error = "Veuillez sélectionner au moins une catégorie."
        flash(error)
        return redirect(url_for("user.chemin_fichier"))
    
    if not chemin_fichier:
        error = "Veuillez sélectionner un fichier."
        flash(error)
        return redirect(url_for("user.chemin_fichier"))

    if clicked_categories and oeuvre_id :
        # Convertir la chaîne JSON en liste
        clicked_categories = json.loads(clicked_categories)
        
        db = get_db()

        try:
            # Traiter les catégories cliquées, par exemple, les enregistrer dans la base de données
            for id_categories in clicked_categories:
                # Exemple d'ajout à la base de données
                db.execute("INSERT INTO categorisations (oeuvre, categorie) VALUES (?, ?)", (id_categories, oeuvre_id))
            db.commit()

            # Retourner un message de succès ou rediriger
            return redirect(url_for('user.chemin_fichier'))

        except Exception as e:
            db.rollback()
            close_db()
            error ="Erreur lors de la séléction des catégories"
            flash(error)
            return redirect(url_for("user.chemin_fichier"))
        finally:
            close_db()
            return redirect(url_for('user.show_profile'))
    
    return redirect(url_for('user.show_profile'))

@user_bp.route('/supprimer_utilisateur', methods=['POST'])
@login_required
def supprimer_utilisateur():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    password = request.form.get('password')
    user_id = session.get('user_id') 

    if not password:
        flash("Le mot de passe est requis pour supprimer votre compte.", "error")
        return redirect(url_for("user.show_profile"))

    db = get_db()

    try:
        user = db.execute('SELECT * FROM utilisateurs WHERE id_utilisateur = ?', (user_id,)).fetchone()

        if not user:
            flash("Utilisateur introuvable.", "error")
            return redirect(url_for("user.show_profile"))

        if not check_password_hash(user['mot_passe'], password):
            flash("Le mot de passe est incorrect.", "error")
            return redirect(url_for("user.show_profile"))

        db.execute("DELETE FROM utilisateurs WHERE id_utilisateur = ?", (user_id,))
        db.commit()
        db.execute("DELETE FROM oeuvres WHERE utilisateur = ?", (user_id,))
        db.commit()
        flash("Votre compte a été supprimé avec succès.", "success")
        
        session.clear()
        return render_template('home/index.html', photo=photo)

    except Exception as e:
        db.rollback() 
        flash("Une erreur est survenue lors de la suppression de votre compte.", "error")
        return redirect(url_for("user.show_profile"))

    finally:
        close_db()  


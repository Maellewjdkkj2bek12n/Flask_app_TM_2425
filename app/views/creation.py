from flask import (Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for,)
from flask import Flask
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.utils import *
from app.db.db import get_db, close_db
import sqlite3
import os
import sqlite3

# Routes /...
creation_bp = Blueprint('creation', __name__)

# Route /affichage
@creation_bp.route('/affichage', methods=('GET', 'POST'))
@login_required
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

@creation_bp.route('/affichage_perso', methods=('GET', 'POST'))
@login_required
def affichage_perso():
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    user_id = session.get('user_id')
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall() 
    close_db()
    
    db = get_db()
    photoagrandie_id = request.args.get('photogrand_id', )
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    close_db()
    
    db = get_db()
    user_id = photoagrandie['utilisateur']
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
    close_db()
    return render_template('creation/affichage_perso.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user)


@creation_bp.route('/supprimer_oeuvre', methods=('GET', 'POST'))
@login_required
def supprimer_oeuvre():
    photoeuvre_id = request.args.get('photogrand_id')
    filename = request.args.get('filename')
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    
    if not photoeuvre_id or not filepath:
        flash("ID de l'œuvre ou chemin du fichier manquant.", "error")
        return redirect(url_for("user.show_profile"))
    
    db = get_db()
    
    try:
        db.execute("DELETE FROM oeuvres WHERE id_oeuvre = ?", (photoeuvre_id,))
        db.execute("DELETE FROM categorisations WHERE oeuvre = ?", (photoeuvre_id,))
        db.commit()  
     
        
        if os.path.exists(filepath):  
            os.remove(filepath)
        else:
            flash(f"Le fichier à supprimer n'existe pas à l'emplacement : {filepath}", "error")
        
        return redirect(url_for("user.show_profile"))
    
    except Exception as e:
        db.rollback() 
        flash(f"Une erreur est survenue lors de la suppression de votre photo. {e}", "error")
        return redirect(url_for("user.show_profile"))
    
    finally:
        close_db()  
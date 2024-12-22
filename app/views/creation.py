from flask import (Blueprint, current_app, flash, g, redirect, render_template, request, session, url_for,)
from flask import Flask
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from app.utils import *
from app.db.db import get_db, close_db
import sqlite3
import os
import sqlite3

creation_bp = Blueprint('creation', __name__)

# Route /affichage
@creation_bp.route('/affichage', methods=('GET', 'POST'))
@login_required
def affichage():
    photoagrandie_id = request.args.get('photogrand_id')
    db = get_db()
 
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    user_id = session.get('user_id')
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? and utilisateur != ?", (photoagrandie_id, user_id,)).fetchall()
    
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()

    categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
    categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
    if categorie_ids:
        categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
    else:
        categorie_oeuvre = []

    user_id_autre = photoagrandie['utilisateur']
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()

    close_db()

    return render_template(
        'creation/affichage.html', 
        photoagrandie=photoagrandie, 
        photo=photo, 
        categories=categories, 
        user=user, 
        categorie_oeuvre=categorie_oeuvre
    )
@creation_bp.route('/affichage_perso', methods=('GET', 'POST'))
@login_required
def affichage_perso():
    photoagrandie_id = request.args.get('photogrand_id', )
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    user_id = session.get('user_id')
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre!= ? and utilisateur = ?",(photoagrandie_id , user_id,)).fetchall() 
    close_db()
    
    db = get_db()
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
        
@creation_bp.route('/filtrer', methods=('GET', 'POST'))
def filtrer():
    user_id = session.get('user_id')
    categorie_id = request.args.get('categorie_id')

    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    
    if categorie_id:
        photo_ids = db.execute("SELECT oeuvre FROM categorisations WHERE categorie = ?", (categorie_id,)).fetchall()
        
        if photo_ids:
            photo_ids_list = [photo[0] for photo in photo_ids]  
            
            if photo_ids_list:
                placeholders = ','.join(['?'] * len(photo_ids_list))  
                photo = db.execute(f"SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({placeholders}) AND utilisateur != ?", tuple(photo_ids_list) + (user_id,)).fetchall()
            else:
                photo = []
                flash('Aucune image dans cette catégorie')

    close_db()

    return render_template('home/index.html', photo=photo, categories=categories)
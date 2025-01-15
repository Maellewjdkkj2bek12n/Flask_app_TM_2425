from flask import (Blueprint, current_app, flash, g, json, redirect, render_template, request, session, url_for,)
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
    exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
    exclusion_ids = [row[0] for row in exclusions]

    exclusion_ids.append(user_id)

    if exclusion_ids:
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? AND utilisateur NOT IN ({})".format(', '.join('?' for _ in exclusion_ids)), [photoagrandie_id] + exclusion_ids).fetchall()

    else:
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? and utilisateur != ?", (photoagrandie_id, user_id,)).fetchall()
    
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()

    categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
    categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
    if categorie_ids:
        categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
    else:
        categorie_oeuvre = []

    user_id_autre = photoagrandie['utilisateur']
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()

    close_db()

    return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre)

@creation_bp.route('/affichage_autres', methods=('GET', 'POST'))
@login_required
def affichage_autres():
    photoagrandie_id = request.args.get('photogrand_id')
    db = get_db()
 
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    user_id_autre = photoagrandie['utilisateur']
    
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? and utilisateur = ?", (photoagrandie_id, user_id_autre,)).fetchall()

    categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
    categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
    if categorie_ids:
        categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
    else:
        categorie_oeuvre = []

    user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()

    close_db()

    return render_template('creation/affichage_autre.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre)


#affichage de nos oeuvres
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
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    close_db()
    
    db = get_db()
    categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
    categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
    if categorie_ids:
        categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
    else:
        categorie_oeuvre = []
    close_db()
    
    db = get_db()
    user_id = photoagrandie['utilisateur']
    user = db.execute("SELECT nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
    close_db()
    return render_template('creation/affichage_perso.html', categorie_oeuvre=categorie_oeuvre, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user)


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
        
 
@creation_bp.route('/filtrer', methods=['POST'])
@login_required
def filtrer():
    user_id = session.get('user_id') 
    categories_filtrer = request.form.get('categories_filtrer')  

    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    
    categories_filtrer = json.loads(categories_filtrer) 
    
    photo_ids_list = []  
    
    if categories_filtrer:

        try:
            for category_id in categories_filtrer:
                photo_ids = db.execute("SELECT oeuvre FROM categorisations WHERE categorie = ?", (category_id,)).fetchall()  
                photo_ids_list.extend([photo[0] for photo in photo_ids])  
                
                
            if not photo_ids_list:
                flash("Aucune œuvre trouvée pour les catégories sélectionnées.")
                close_db()  
                return redirect(url_for("home.landing_page"))

        except Exception as e:
            flash("Une erreur est survenue lors du filtrage des œuvres.")
            print("Erreur:", e)
            close_db()
            return redirect(url_for("home.landing_page"))
        
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur != ?".format(','.join('?' for _ in photo_ids_list)),tuple(photo_ids_list + [user_id])).fetchall()
        close_db()  

        return render_template('home/index.html', photo=photo, categories=categories)
    
    else: 
        flash("Aucun filtre sélectionné")
        close_db()  
        return redirect(url_for("home.landing_page"))

@creation_bp.route('/filtrer_rapide/<int:categorie_id>', methods=['GET', 'POST'])
@login_required
def filtrer_rapide(categorie_id):
    user_id = session.get('user_id')  
    categories_filtrer = categorie_id  

    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    if not categories_filtrer:
        flash("Aucun filtre sélectionné")
        close_db()  
        return redirect(url_for("home.landing_page"))
    
    photo_ids_list = []  

    try:
        photo_ids = db.execute("SELECT oeuvre FROM categorisations WHERE categorie = ?", (categories_filtrer,)).fetchall()
        photo_ids_list.extend([photo[0] for photo in photo_ids])  

    except Exception as e:
        flash("Une erreur est survenue lors du filtrage des œuvres.")
        print("Erreur:", e)
        close_db()
        return redirect(url_for("home.landing_page"))
    
    if not photo_ids_list:
        flash("Aucune œuvre trouvée pour la catégorie sélectionnée.")
        close_db()  
        return redirect(url_for("home.landing_page"))
    
    try:
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur != ?".format(','.join('?' for _ in photo_ids_list)),tuple(photo_ids_list + [user_id])).fetchall()
    except Exception as e:
        flash("Une erreur est survenue lors de la récupération des œuvres.")
        print("Erreur:", e)
        close_db()
        return redirect(url_for("home.landing_page"))
    
    close_db() 

    return render_template('home/index.html', photo=photo, categories=categories)

@creation_bp.route('/chercher', methods=['GET', 'POST'])
@login_required
def chercher():
    chercher = request.form.get('chercher', '').strip() 
    photo_ids_list = []
    user_id = session.get('user_id')
    db = get_db() 
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    if chercher:  
        
        photo_ids = db.execute("SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ? AND utilisateur != ?",('%' + chercher + '%', user_id)).fetchall()
        photo_ids_list.extend([photo[0] for photo in photo_ids]) 

        if not photo_ids: 
            flash("Aucun utilisateur trouvé pour le terme recherché.")
            return redirect(url_for("home.landing_page"))

        try:
            photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur != ?".format(','.join('?' for _ in photo_ids_list)),tuple(photo_ids_list + [user_id])).fetchall()
        
        except Exception as e:
            flash("Une erreur est survenue lors de la récupération des œuvres.")
            print("Erreur:", e)
            close_db()
            return redirect(url_for("home.landing_page"))
        
        close_db() 
        return render_template('home/index.html', photo=photo, categories=categories)

    else: 
        close_db()
        flash("Le champ de recherche est vide. Veuillez entrer un terme.")
        return redirect(url_for("home.landing_page"))

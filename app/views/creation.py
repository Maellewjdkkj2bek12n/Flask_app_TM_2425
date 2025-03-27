import random
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

@creation_bp.route('/affichage', methods=('GET', 'POST'))
@login_required
def affichage():
    photoagrandie_id = request.args.get('photogrand_id')
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    user_id = session.get('user_id')
    chercher = request.args.get('chercher')
    categories_filtrer = request.args.getlist('categories_filtrer')
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    user_id_autre = photoagrandie['utilisateur']
    
    if not categories_filtrer and not chercher:
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]

        if exclusion_ids:
            photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? AND utilisateur NOT IN ({})".format(', '.join('?' for _ in exclusion_ids)), [photoagrandie_id] + exclusion_ids).fetchall()

        else:
            photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ?", (photoagrandie_id,)).fetchall()
        
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
        random.shuffle(photo)
        if user_id_autre == user_id :
            photo_perso = user_id
            return render_template('creation/affichage.html',photo_perso=photo_perso, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre)
        return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre)

    elif categories_filtrer and chercher:
        photo_ids_list = []  
        photo_ids_list2 = [] 
        common_ids = []  
        try:
            photo_ids = db.execute(
                "SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ?",
                ('%' + chercher + '%',)
            ).fetchall()
            photo_ids_list.extend([photo[0] for photo in photo_ids])  
        
        except Exception as e:
            flash("Une erreur est survenue lors de la récupération des œuvres.")
            print("Erreur:", e)
            close_db()
            return redirect(url_for("home.landing_page"))
        
        try:
            for category_id in categories_filtrer:
                photo_ids2 = db.execute(
                    "SELECT oeuvre FROM categorisations WHERE categorie = ?",
                    (category_id,)
                ).fetchall()
                photo_ids_list2.extend([photo[0] for photo in photo_ids2]) 
            
            if not photo_ids_list2:
                flash("Aucune œuvre trouvée pour les catégories sélectionnées.")
                close_db()
                return redirect(url_for("home.landing_page", chercher=chercher))
            
            common_ids = list(set(photo_ids_list) & set(photo_ids_list2))

        except ValueError:
            flash("Erreur lors de la conversion des IDs.")
            close_db()
            return redirect(url_for("home.landing_page"))
        
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]

        if exclusion_ids:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ? AND utilisateur NOT IN ({})".format(
                    ', '.join('?' for _ in common_ids), 
                    ', '.join('?' for _ in exclusion_ids)   
                ),
                tuple(common_ids+ [photoagrandie_id] + exclusion_ids)  
            ).fetchall()
        else:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ?".format(
                    ', '.join('?' for _ in common_ids)  
                ),
                tuple(common_ids + [photoagrandie_id])  
            ).fetchall()
        
        photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()

        categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
        categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
        if categorie_ids:
            categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
        else:
            categorie_oeuvre = []

        user_id_autre = photoagrandie['utilisateur']
        user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()
        random.shuffle(photo)
        close_db()
        
        if user_id_autre == user_id :
            photo_perso = user_id
            return render_template('creation/affichage.html', photo_perso=photo_perso, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, categories_filtrer=categories_filtrer, chercher=chercher)
        return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, categories_filtrer=categories_filtrer, chercher=chercher)
             
    elif chercher and not categories_filtrer:
        photo_ids_list = []  
        try:
            photo_ids = db.execute(
                "SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ?",
                ('%' + chercher + '%',)
            ).fetchall()
            photo_ids_list.extend([photo[0] for photo in photo_ids])  
        
        except Exception as e:
            flash("Une erreur est survenue lors de la récupération des œuvres.")
            print("Erreur:", e)
            close_db()
            return redirect(url_for("home.landing_page"))
        
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]

        if exclusion_ids:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ? AND utilisateur NOT IN ({})".format(
                    ', '.join('?' for _ in photo_ids_list), 
                    ', '.join('?' for _ in exclusion_ids)   
                ),
                tuple(photo_ids_list+ [photoagrandie_id] + exclusion_ids)  
            ).fetchall()
        else:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ?".format(
                    ', '.join('?' for _ in photo_ids_list)  
                ),
                tuple(photo_ids_list + [photoagrandie_id])  
            ).fetchall()
        
        photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()

        categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
        categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
        if categorie_ids:
            categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
        else:
            categorie_oeuvre = []

        user_id_autre = photoagrandie['utilisateur']
        user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()

        random.shuffle(photo)
        close_db()
        if user_id_autre == user_id :
            photo_perso = user_id
            return render_template('creation/affichage.html', photo_perso=photo_perso, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, chercher=chercher)
    
        return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, chercher=chercher)
    
    elif categories_filtrer and not chercher:
        photo_ids_list = []    
        try:
            for category_id in categories_filtrer:
                photo_ids = db.execute(
                    "SELECT oeuvre FROM categorisations WHERE categorie = ?",
                    (category_id,)
                ).fetchall()
                photo_ids_list.extend([photo[0] for photo in photo_ids]) 
            
            if not photo_ids_list:
                flash("Aucune œuvre trouvée pour les catégories sélectionnées.")
                close_db()
                return redirect(url_for("home.landing_page", chercher=chercher))

        except ValueError:
            flash("Erreur lors de la conversion des IDs.")
            close_db()
            return redirect(url_for("home.landing_page"))
        
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]

        if exclusion_ids:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ? AND utilisateur NOT IN ({})".format(
                    ', '.join('?' for _ in photo_ids_list), 
                    ', '.join('?' for _ in exclusion_ids)   
                ),
                tuple(photo_ids_list+ [photoagrandie_id] + exclusion_ids)  
            ).fetchall()
        else:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND id_oeuvre != ?".format(
                    ', '.join('?' for _ in photo_ids_list)  
                ),
                tuple(photo_ids_list + [photoagrandie_id])  
            ).fetchall()
        
        photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()

        categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
        categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
        if categorie_ids:
            categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
        else:
            categorie_oeuvre = []

        user_id_autre = photoagrandie['utilisateur']
        user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()
        random.shuffle(photo)
        close_db()
        if user_id_autre == user_id :
            photo_perso = user_id
            return render_template('creation/affichage.html', photo_perso=photo_perso, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, categories_filtrer=categories_filtrer)
        

        return render_template('creation/affichage.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre, categories_filtrer=categories_filtrer)
        
@creation_bp.route('/affichage_autres', methods=('GET', 'POST'))
@login_required
def affichage_autres():
    photoagrandie_id = request.args.get('photogrand_id')
    user_id = session.get('user_id')
    db = get_db()
 
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    
    photoagrandie = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
    user_id_autre = photoagrandie['utilisateur']
    
    if user_id_autre == user_id :
          close_db()
          return redirect(url_for('creation.affichage_perso', photogrand_id=photoagrandie_id))

    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre != ? and utilisateur = ?", (photoagrandie_id, user_id_autre,)).fetchall()

    categorisation_oeuvre = db.execute("SELECT categorie FROM categorisations WHERE oeuvre = ?", (photoagrandie_id,)).fetchall()
    categorie_ids = [c['categorie'] for c in categorisation_oeuvre]
    if categorie_ids:
        categorie_oeuvre = db.execute("SELECT id_categorie, nom FROM categories_oeuvres WHERE id_categorie IN ({})".format(','.join(['?'] * len(categorie_ids))),tuple(categorie_ids)).fetchall()
    else:
        categorie_oeuvre = []

    user = db.execute("SELECT nom_utilisateur, bio, photo_profil FROM utilisateurs WHERE id_utilisateur = ?", (user_id_autre,)).fetchone()

    close_db()
    random.shuffle(photo)
    return render_template('creation/affichage_autre.html', photoagrandie=photoagrandie, photo=photo, categories=categories, user=user, categorie_oeuvre=categorie_oeuvre)

@creation_bp.route('/affichage_perso', methods=('GET', 'POST'))
@login_required
def affichage_perso():
    photoagrandie_id = request.args.get('photogrand_id', )
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    close_db()
    
    user_id = session.get('user_id')
    db = get_db() 
    
    photo = db.execute("SELECT id_oeuvre, chemin_fichier, nom FROM oeuvres WHERE id_oeuvre!= ? and utilisateur = ?",(photoagrandie_id , user_id,)).fetchall() 
    close_db()
    
    db = get_db()
    photoagrandie = db.execute("SELECT nom, id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?", (photoagrandie_id,)).fetchone()
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
    random.shuffle(photo)
    close_db()
    return render_template('creation/affichage_perso.html', categorie_oeuvre=categorie_oeuvre, photoagrandie=photoagrandie, photo=photo, categories=categories, user=user)
        
 
@creation_bp.route('/filtrer', methods=['POST'])
@login_required
def filtrer():
    user_id = session.get('user_id')  
    chercher = request.args.get('chercher', '').strip()  
    categories_filtrer = request.form.getlist('categories_filtrer')
    
    db = get_db() 
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()  
    
    if not chercher:
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
            
            exclusions = db.execute(
                "SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", 
                (user_id, user_id)
            ).fetchall()
            exclusion_ids = [row[0] for row in exclusions]
            
            if exclusion_ids:
                photo = db.execute(
                    "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})".format(
                        ', '.join('?' for _ in photo_ids_list),
                        ', '.join('?' for _ in exclusion_ids)
                    ),
                    tuple(photo_ids_list + exclusion_ids)
                ).fetchall()
            else:
                photo = db.execute(
                    "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})".format(
                        ', '.join('?' for _ in photo_ids_list)
                    ),
                    tuple(photo_ids_list)
                ).fetchall()
            
            close_db() 
            
            if not photo:
                flash("Aucune œuvre trouvée pour les catégories sélectionnées.")
                return redirect(url_for("home.landing_page"))
            else:
                random.shuffle(photo)
                return render_template('home/index.html', photo=photo, categories=categories, categories_filtrer=categories_filtrer)
        
        else:
            flash("Aucun filtre sélectionné.")
            close_db()
            return redirect(url_for("home.landing_page"))
    
    if chercher:
        photo_ids_list = []  
        photo_ids_list2 = [] 
        common_ids = [] 
        
        try:
            photo_ids = db.execute(
                "SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ?",
                ('%' + chercher + '%',)
            ).fetchall()
            photo_ids_list.extend([photo[0] for photo in photo_ids])  
            
            if not photo_ids_list:
                flash("Aucune œuvre trouvée pour le terme recherché.")
                close_db()
                return redirect(url_for("home.landing_page", chercher=chercher))
        except Exception as e:
            flash("Une erreur est survenue lors de la récupération des œuvres.")
            print("Erreur:", e)
            close_db()
            return redirect(url_for("home.landing_page"))
        
        if categories_filtrer:
            try:
               
                for category_id in categories_filtrer:
                    photo_ids2 = db.execute(
                        "SELECT oeuvre FROM categorisations WHERE categorie = ?",
                        (category_id,)
                    ).fetchall()
                    photo_ids_list2.extend([photo[0] for photo in photo_ids2]) 
                
                if not photo_ids_list2:
                    flash("Aucune œuvre trouvée pour les catégories sélectionnées.")
                    close_db()
                    return redirect(url_for("home.landing_page", chercher=chercher))
                
               
                common_ids = list(set(photo_ids_list) & set(photo_ids_list2))
                
                if not common_ids:
                    flash("Aucune œuvre trouvée correspondant au terme recherché et aux catégories.")
                    close_db()
                    return redirect(url_for("home.landing_page", chercher=chercher))
                
                exclusions = db.execute(
                    "SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?",
                    (user_id, user_id)
                ).fetchall()
                exclusion_ids = [row[0] for row in exclusions]
                
                if exclusion_ids:
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})".format(
                            ', '.join('?' for _ in common_ids),
                            ', '.join('?' for _ in exclusion_ids)
                        ),
                        tuple(common_ids + exclusion_ids)
                    ).fetchall()
                else:
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})".format(
                            ', '.join('?' for _ in common_ids)
                        ),
                        tuple(common_ids)
                    ).fetchall()
            except Exception as e:
                flash("Une erreur est survenue lors du filtrage des œuvres.")
                print("Erreur:", e)
                close_db()
                return redirect(url_for("home.landing_page"))
            
            close_db()  
            
            if not photo:
                flash("Aucune œuvre trouvée correspondant au terme recherché et aux catégories.")
                return redirect(url_for("home.landing_page", chercher=chercher))
            else:
                random.shuffle(photo)
                return render_template('home/index.html', photo=photo, categories=categories, chercher=chercher, categories_filtrer=categories_filtrer)
        else:
            flash("Aucun filtre sélectionné.")
            close_db()
            return redirect(url_for("home.landing_page", chercher=chercher))

             

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
        exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]
        if exclusion_ids:
            photo = db.execute(
                "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})".format(
                    ', '.join('?' for _ in photo_ids_list),  
                    ', '.join('?' for _ in exclusion_ids) 
                ), 
                tuple(photo_ids_list + exclusion_ids) 
            ).fetchall()
        else :
            photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})".format(','.join('?' for _ in photo_ids_list)),tuple(photo_ids_list)).fetchall()
    
    except Exception as e:
        flash("Une erreur est survenue lors de la récupération des œuvres.")
        print("Erreur:", e)
        close_db()
        return redirect(url_for("home.landing_page"))
    
    close_db() 
    if not photo: 
        flash("Aucune oeuvre trouvée pour le terme recherché.")
        return redirect(url_for("home.landing_page"))
    else:
        random.shuffle(photo)
        return render_template('home/index.html', photo=photo, categories=categories, categories_filtrer=categories_filtrer)

@creation_bp.route('/chercher', methods=['GET', 'POST'])
@login_required
def chercher():
    chercher = request.form.get('chercher', '').strip()  
    categories_filtrer = request.args.getlist('categories_filtrer')
    user_id = session.get('user_id') 
    db = get_db()  
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall() 
    
    if not categories_filtrer:
        photo_ids_list = []  
        
        if chercher:  
           
            photo_ids = db.execute("SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ?", 
                                   ('%' + chercher + '%',)).fetchall()
            photo_ids_list.extend([photo[0] for photo in photo_ids])  

            if not photo_ids_list:  
                flash("Aucune oeuvre trouvée pour le terme recherché.")
                return redirect(url_for("home.landing_page"))

            try:
                
                exclusions = db.execute(
                    "SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", 
                    (user_id, user_id)
                ).fetchall()
                exclusion_ids = [row[0] for row in exclusions] 
                
                if exclusion_ids:  
                    
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})".format(
                            ', '.join('?' for _ in photo_ids_list),
                            ', '.join('?' for _ in exclusion_ids)
                        ),
                        tuple(photo_ids_list + exclusion_ids)  
                    ).fetchall()
                else:
                   
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})".format(
                            ','.join('?' for _ in photo_ids_list)
                        ),
                        tuple(photo_ids_list)  
                    ).fetchall()

            except Exception as e:
                flash("Une erreur est survenue lors de la récupération des œuvres.")
                print("Erreur:", e)
                close_db() 
                return redirect(url_for("home.landing_page"))
            
            close_db()  
            if not photo:  
                flash("Aucune oeuvre trouvée pour le terme recherché.")
                return redirect(url_for("home.landing_page"))
            else:
                random.shuffle(photo)
                return render_template('home/index.html', photo=photo, categories=categories, chercher=chercher)
        
        else: 
            close_db()
            flash("Le champ de recherche est vide. Veuillez entrer un terme.")
            return redirect(url_for("home.landing_page"))
    
    
    if categories_filtrer:
        photo_ids_list = [] 
        photo_ids_list2 = []  
        common_ids = [] 
        
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
        
        if chercher:
           
            try:
                photo_ids2 = db.execute("SELECT id_oeuvre FROM oeuvres WHERE description_oeuvre LIKE ?", 
                                        ('%' + chercher + '%',)).fetchall()
                photo_ids_list2.extend([photo[0] for photo in photo_ids2])  
                
                if not photo_ids_list2: 
                    flash("Aucune œuvre trouvée pour le terme recherché.")
                    close_db()  
                    return redirect(url_for("home.landing_page", categories_filtrer=categories_filtrer))

                common_ids = list(set(photo_ids_list2) & set(photo_ids_list))

                if not common_ids:  
                    flash("Aucune œuvre de ce type trouvée pour le terme recherché.")
                    close_db() 
                    return redirect(url_for("home.landing_page", categories_filtrer=categories_filtrer))
                
              
                exclusions = db.execute(
                    "SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", 
                    (user_id, user_id)
                ).fetchall()
                exclusion_ids = [row[0] for row in exclusions]
                
                if exclusion_ids:  
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})".format(
                            ', '.join('?' for _ in common_ids),
                            ', '.join('?' for _ in exclusion_ids)
                        ),
                        tuple(common_ids + exclusion_ids)  
                    ).fetchall()
                else:
                    
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})".format(
                            ', '.join('?' for _ in common_ids)
                        ),
                        tuple(common_ids) 
                    ).fetchall()

            except Exception as e:
                flash("Une erreur est survenue lors de la récupération des œuvres.")
                print("Erreur:", e)
                close_db()  
                return redirect(url_for("home.landing_page"))

            close_db() 
            if not photo:  
                flash("Aucune oeuvre trouvée pour le terme recherché.")
                return redirect(url_for("home.landing_page", categories_filtrer=categories_filtrer))
            else:
                random.shuffle(photo)
                return render_template('home/index.html', photo=photo, categories=categories, chercher=chercher, categories_filtrer=categories_filtrer)

        else: 
            flash("Le champ de recherche est vide. Veuillez entrer un terme.")
            close_db()
            return redirect(url_for("home.landing_page", categories_filtrer=categories_filtrer))

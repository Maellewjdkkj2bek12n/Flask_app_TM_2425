import random
from flask import (Blueprint, flash, g, json, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

from app.db.db import get_db, close_db
import os

from werkzeug.utils import secure_filename

home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=('GET', 'POST'))
def landing_page():
    user_id = session.get('user_id')
    db = get_db()
    categories = db.execute("SELECT * FROM categories_oeuvres").fetchall()
    close_db()  
    if user_id: 
        chercher = request.args.get('chercher')
        categories_filtrer = request.args.getlist('categories_filtrer')
        db = get_db()

        if not categories_filtrer and not chercher:
            exclusions = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? UNION SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id, user_id)).fetchall()
            exclusion_ids = [row[0] for row in exclusions]

            if exclusion_ids:
                photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur NOT IN ({}) ORDER BY RANDOM() LIMIT 30".format(', '.join('?' for _ in exclusion_ids)), exclusion_ids).fetchall()
            else:
                photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres ORDER BY RANDOM() LIMIT 30").fetchall()

            random.shuffle(photo)
            close_db()  
            return render_template('home/index.html', photo=photo, categories=categories)
        
        if categories_filtrer and chercher:
            photo_ids_list = []  
            photo_ids_list2 = [] 
            common_ids = []  
            try:
                
                for category_id in categories_filtrer:
                    photo_ids2 = db.execute(
                        "SELECT oeuvre FROM categorisations WHERE categorie = ?",
                        (category_id,)
                    ).fetchall()
                    photo_ids_list2.extend([photo[0] for photo in photo_ids2])  

            except Exception as e:
                flash("Une erreur est survenue lors de la récupération des œuvres.")
                print("Erreur:", e)
                close_db() 
                return redirect(url_for("home.landing_page"))
            
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
                    "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({}) ORDER BY RANDOM() LIMIT 30".format(
                        ', '.join('?' for _ in common_ids),
                        ', '.join('?' for _ in exclusion_ids)
                    ),
                    tuple(common_ids + exclusion_ids)
                ).fetchall()
            else:
                photo = db.execute(
                    "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) ORDER BY RANDOM() LIMIT 30".format(
                        ', '.join('?' for _ in common_ids)
                    ),
                    tuple(common_ids)
                ).fetchall()
            random.shuffle(photo)
            close_db()  
            return render_template('home/index.html', photo=photo, categories=categories, categories_filtrer=categories_filtrer, chercher=chercher)

        elif chercher and not categories_filtrer:
            photo_ids_list = []    
            
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
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) AND utilisateur NOT IN ({})  ORDER BY RANDOM() LIMIT 30".format(
                            ', '.join('?' for _ in photo_ids_list),
                            ', '.join('?' for _ in exclusion_ids)
                        ),
                        tuple(photo_ids_list + exclusion_ids)  
                    ).fetchall()
                else:
                    photo = db.execute(
                        "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({})  ORDER BY RANDOM() LIMIT 30".format(
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
    
        elif categories_filtrer and not chercher:
            photo_ids_list = [] 
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
                    "SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE id_oeuvre IN ({}) ORDER BY RANDOM() LIMIT 30".format(
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
    
    if not user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres ORDER BY RANDOM() LIMIT 30").fetchall()  
        close_db() 
        random.shuffle(photo)
        return render_template('home/index.html', photo=photo, categories=categories)

@home_bp.route('/<path:text>', methods=['GET', 'POST'])
def not_found_error(text):
    return render_template('home/404.html'), 404
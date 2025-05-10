import random
import shutil
from flask import (Blueprint, current_app, flash, g, json, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.security import check_password_hash
import sqlite3

from app.db.db import get_db, close_db
import os

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/profil_autre', methods=('GET', 'POST')) 
def show_autreprofile() :
    db = get_db()
    user_id = request.args.get('user')
    abonnés = db.execute("SELECT COUNT(*) FROM suivre WHERE suivi = ?", (user_id,)).fetchone()[0]
    abonnements = db.execute("SELECT COUNT(*) FROM suivre WHERE suiveur = ?", (user_id,)).fetchone()[0]

    user = session.get('user_id')
    if str(user_id) == str(user):
        close_db()
        return redirect(url_for("user.show_profile"))

    blocage = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? AND bloqué = ?", (user_id, user)).fetchone()
    if blocage :  
        blocage = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        user = db.execute("SELECT id_utilisateur, nom_utilisateur  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        close_db()
        return render_template('user/profil autre.html', user=user, nul=blocage)
    else: 
        bloquer= db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? AND bloqué = ?", (user, user_id)).fetchone()
        if bloquer :  
            bloque = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
            user = db.execute("SELECT id_utilisateur, nom_utilisateur  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
            close_db()
            return render_template('user/profil autre.html', user=user, bloque=bloque)
        else: 
            suivre= db.execute("SELECT suivi FROM suivre WHERE suiveur = ? AND suivi = ?", (user, user_id)).fetchone()
            if suivre : 
                suivi = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
                photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
                user = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
                close_db()
                return render_template('user/profil autre.html',photo_user=photo_user, user=user, suivi=suivi,  abonnés = abonnés, abonnements =abonnements)
            else :
                photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
                user = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
                close_db()
                return render_template('user/profil autre.html',photo_user=photo_user, user=user,  abonnés = abonnés, abonnements =abonnements)

@user_bp.route('/profil', methods=('GET', 'POST'))
@login_required
def show_profile():
    user_id = session.get('user_id')
    db = get_db()  
    abonnés = db.execute("SELECT COUNT(*) FROM suivre WHERE suivi = ?", (user_id,)).fetchone()[0]
    abonnements = db.execute("SELECT COUNT(*) FROM suivre WHERE suiveur = ?", (user_id,)).fetchone()[0]

    photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
    close_db()
    
    return render_template('user/profil.html', user=g.user,photo_user=photo_user, abonnés = abonnés, abonnements =abonnements)

@user_bp.route('/bio', methods=('GET', 'POST'))
@login_required
def change_bio():
    user_id = session.get('user_id')
    
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
                return redirect(url_for("user.changer_profil"))
            
            finally:
                close_db()
                return redirect(url_for("user.changer_profil"))
    return redirect(url_for("user.changer_profil"))

@user_bp.route('/username', methods=('GET', 'POST'))
@login_required
def change_username():
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        user_id = session.get('user_id')
        
        if username:
            db = get_db()
            try:
                db.execute('UPDATE utilisateurs SET nom_utilisateur = ? WHERE id_utilisateur = ?', (username, user_id))
                db.commit()
            
            except db.IntegrityError:
                error = "Oups, le nom d'utilisateur est déjà utilisé."
                flash(error)
                return redirect(url_for("user.changer_profil"))
            
            finally:
                close_db()
                return redirect(url_for('user.changer_profil'))
    return redirect(url_for("user.changer_profil"))

@user_bp.route('/change_photo_profil', methods=('GET', 'POST'))
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
        nom_fichier = request.args.get('nom_fichier')
        if nom_fichier :
            chemin = os.path.join('app/static/upload' , str(user_id), nom_fichier)
            if os.path.exists(chemin):  
                os.remove(chemin)

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
            filepath = os.path.join('app/static/upload' , str(user_id), filename)
            
            base_name, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(filepath):
                filename = f"{base_name}_{count}{extension}"
                filepath = os.path.join('app/static/upload' , str(user_id) , filename)
                count += 1

            user_dir = os.path.join('app/static/upload' , str(user_id))
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            try:
                file.save(filepath)
            except Exception as e:
                error = "Erreur lors de la sauvegarde du fichier."
                flash(error)
                return redirect(url_for("user.show_profile"))
            
            photo_profil = url_for('static', filename=f'upload/{user_id}/{filename}', _external=True)

            user_id = session.get('user_id') 
           
        
            if photo_profil :
                db = get_db()  
                try:
                        db.execute('UPDATE utilisateurs SET photo_profil = ? WHERE id_utilisateur = ?', (photo_profil, user_id))
                        db.execute('UPDATE utilisateurs SET nom_photo_profil = ? WHERE id_utilisateur = ?', (filename, user_id))
                        db.commit()
                    
                except db.IntegrityError:
                        error = "Erreur lors de la sauvegarde du fichier."
                        flash(error)
                        return redirect(url_for("user.changer_profil"))
                    
                finally:
                        close_db()
                        return redirect(url_for('user.changer_profil'))

        return render_template('user/profil.html', user=g.user,photo_user=photo_user)

@user_bp.route('/supprimer_photo_profil', methods=('GET', 'POST'))
@login_required
def supprimer_photo_profil(): 
    user_id = session.get('user_id') 
    nom_fichier = request.args.get('nom_fichier')
    if nom_fichier:
        chemin = os.path.join('app/static/upload' , str(user_id), nom_fichier)
        if os.path.exists(chemin):  
            os.remove(chemin)
        db = get_db() 
        db.execute("UPDATE utilisateurs SET photo_profil = NULL, nom_photo_profil = NULL WHERE id_utilisateur = ?", (user_id,))
        db.commit()  
        close_db()
    else:
        flash("Aucune photo de profil trouvée.")
    return redirect(url_for('user.changer_profil'))

@user_bp.route('/chemin_fichier', methods=('GET', 'POST'))
@login_required
def chemin_fichier():
    user_id = session.get('user_id') 
    db = get_db()
    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()

    if request.method == 'POST':
        if 'upload' not in request.files:
            error= "Aucun fichier envoyé."
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
            filepath = os.path.join('app/static/upload' , str(user_id), filename)
            
            base_name, extension = os.path.splitext(filename)
            count = 1
            while os.path.exists(filepath): 
                filename = f"{base_name}_{count}{extension}"
                filepath = os.path.join('app/static/upload' , str(user_id), filename)
                count += 1

            
            user_dir = os.path.join('app/static/upload', str(user_id))
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)

            try:
                file.save(filepath)
            except Exception as e:
                error ="Erreur lors de la sauvegarde du fichier"
                flash(error)
                return redirect(url_for("user.chemin_fichier"))

            #image_url = url_for('static', filename=f'upload/{user_id}/{filename}', _external=True)
            image_url = "static/upload/{user_id}/{filename}"
            user_id = session.get('user_id') 

            if image_url and user_id: 
                db = get_db()
                try:
                    db.execute("INSERT INTO oeuvres (chemin_fichier, utilisateur, nom) VALUES (?, ?, ?)", (image_url, user_id, filename))
                    db.commit()
                except Exception as e:
                    db.rollback()
                    error ="Erreur lors de l'enregistrement"
                    flash(error)
                    return redirect(url_for("user.chemin_fichier"))
                finally:
                    oeuvres = db.execute("SELECT nom, id_oeuvre, chemin_fichier, utilisateur FROM oeuvres WHERE chemin_fichier = ?", (image_url ,)).fetchone()
                    close_db()
                page_type= "upload"
                return render_template('user/upload.html',image_url=image_url, oeuvres=oeuvres, categories=categories,  page_type= page_type)
    page_type= "upload"
    return render_template('user/upload.html', categories=categories,  page_type= page_type)

@user_bp.route('/change_categorie', methods=['POST'])
@login_required
def change_categorie():
    clicked_categories = request.form.getlist('categories')
    oeuvre_id = request.args.get('oeuvre_id')
    
    description = request.form.get('description', '').strip()
        
    if description:
        try:
            db = get_db()
            db.execute('UPDATE oeuvres SET description_oeuvre = ? WHERE id_oeuvre = ?', (description, oeuvre_id))
            db.commit()
        except db.IntegrityError:
            error = "Oups, la bio est trop longue ou une erreur est survenue."
            flash(error)
        finally:
            close_db()

    if not oeuvre_id:
        error = "L'identifiant de l'œuvre est manquant."
        flash(error)
        return redirect(url_for("user.chemin_fichier"))


    if clicked_categories :
        

        try:
            db = get_db()
            for category_id in clicked_categories:
                db.execute("INSERT INTO categorisations (oeuvre, categorie) VALUES (?, ?)", (oeuvre_id , category_id))
            db.commit()
            close_db()
            
        except Exception as e:
            db.rollback()
            flash(f"Une erreur est survenue : {str(e)}", "error")
            return redirect(url_for("user.chemin_fichier"))

    return redirect(url_for('user.show_profile'))


@user_bp.route('/supprimer_utilisateur', methods=['GET', 'POST'])
@login_required
def supprimer_utilisateur():
    
    password = request.form.get('password')
    user_id = session.get('user_id') 
    db = get_db()
    if password:
        try:
            user = db.execute('SELECT * FROM utilisateurs WHERE id_utilisateur = ?', (user_id,)).fetchone()
            if not user:
                flash("Utilisateur introuvable.", "error")
                return redirect(url_for("user.show_profile"))

            if not password:
                flash("Le mot de passe est requis pour supprimer votre compte.", "error")
                return redirect(url_for("user.supprimer_utilisateur"))

            if not check_password_hash(user['mot_passe'], password):
                flash("Le mot de passe est incorrect.", "error")
                return redirect(url_for("user.supprimer_utilisateur"))
            

            user_dir = os.path.join('app/static/upload', str(user_id))
            if os.path.exists(user_dir) and os.path.isdir(user_dir):
                
                os.chmod(user_dir, 0o777)
                shutil.rmtree(user_dir)
                print(f"Le dossier {user_dir} a été supprimé avec succès.")
                
            db.execute("DELETE FROM oeuvres WHERE utilisateur = ?", (user_id,))
            db.execute("DELETE FROM utilisateurs WHERE id_utilisateur = ?", (user_id,))
            db.execute("DELETE FROM contacter WHERE emetteur = ?", (user_id,))
            db.execute("DELETE FROM contacter WHERE recepteur = ?", (user_id,))
            db.execute("DELETE FROM bloque WHERE empecheur = ?", (user_id,))
            db.execute("DELETE FROM bloque WHERE bloqué = ?", (user_id,))
            db.execute("DELETE FROM suivre WHERE suiveur = ?", (user_id,))
            db.execute("DELETE FROM suivre WHERE suivi = ?", (user_id,))
            db.commit()

            flash("Votre compte a été supprimé avec succès.", "success")
        
            session.clear()
            return redirect(url_for("home.landing_page"))

        except Exception as e:
            db.rollback() 
            flash(f"Une erreur est survenue lors de la suppression de votre compte: {e}", "error")
            print(f"Erreur: {e}")
            return redirect(url_for("user.show_profile"))

        finally:
            close_db()
    page_type= "upload"
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE NOT utilisateur = ?",(user_id,)).fetchall() 
    random.shuffle(photo)
    close_db()
    return render_template('user/supprimer_profil.html', user=g.user, page_type= page_type, photo=photo)

@user_bp.route('/chercher', methods=['GET', 'POST'])
@login_required
def chercher():
    chercher = request.form.get('chercher', '').strip() 
    utilisateurs = []
    user_id = session.get('user_id') 

    if chercher:  
        db = get_db()
        
        db = get_db()
        exclusions = db.execute("SELECT empecheur FROM bloque WHERE bloqué = ?", (user_id,)).fetchall()
        exclusion_ids = [row[0] for row in exclusions]
        exclusion_ids.append(user_id)

        if exclusion_ids:
            utilisateurs = db.execute(
                "SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE nom_utilisateur LIKE ? AND id_utilisateur NOT IN ({})".format(', '.join('?' for _ in exclusion_ids)),
                tuple(['%' + chercher + '%'] + exclusion_ids)
            ).fetchall()
        
        else :
            utilisateurs = db.execute("SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE nom_utilisateur LIKE ? AND id_utilisateur != ?",('%' + chercher + '%', user_id)).fetchall()
        
        close_db()
        if not utilisateurs: 
            flash("Aucun utilisateur trouvé pour le terme recherché.")
            return redirect(url_for("home.landing_page"))

        return render_template('user/afficher.html', utilisateurs=utilisateurs)

    else: 
        flash("Le champ de recherche est vide. Veuillez entrer un terme.")
        return redirect(url_for("home.landing_page"))

@user_bp.route('/bloquer', methods=('GET', 'POST'))
@login_required
def bloquer():
    bloque =  request.args.get('user')
    user = session.get('user_id') 
    db = get_db()
    db.execute("INSERT INTO bloque (bloqué, empecheur) VALUES (?, ?)", (bloque , user))
    db.execute("DELETE FROM suivre WHERE suiveur = ? and suivi = ?", (user, bloque))
    db.execute("DELETE FROM suivre WHERE suivi = ? and suiveur = ?", (user, bloque))
    db.commit()
    close_db()
    return redirect(url_for("user.show_autreprofile", user=bloque))

@user_bp.route('/debloquer', methods=('GET', 'POST'))
@login_required
def debloquer():
    bloque = request.args.get('user')
    bloque = int(bloque) 
    db = get_db()
    user = session.get('user_id')
    db.execute("DELETE FROM bloque WHERE empecheur = ? AND bloqué = ?",(user, bloque))
    db.commit()
    close_db()
    return redirect(url_for("user.show_autreprofile", user=bloque))
    
@user_bp.route('/suivre', methods=('GET', 'POST'))
@login_required
def suivre():
    suivi =  request.args.get('user')
    user = session.get('user_id') 
    db = get_db()
    db.execute("INSERT INTO suivre (suivi, suiveur) VALUES (?, ?)", (suivi , user))
    db.commit()
    close_db()
    return redirect(url_for("user.show_autreprofile", user=suivi))

@user_bp.route('/plus_suivre', methods=('GET', 'POST'))
@login_required
def plus_suivre():
    suivi =  request.args.get('user')
    suivi = int(suivi) 
    db = get_db()
    user = session.get('user_id') 
    db.execute("DELETE FROM suivre WHERE suiveur = ? AND suivi = ?", (user, suivi))
    db.commit()
    close_db()
    return redirect(url_for("user.show_autreprofile", user=suivi))

@user_bp.route('/afficher_bloquer', methods=['GET', 'POST'])
@login_required
def afficher_bloquer():
    user_id = session.get('user_id')
    db = get_db()
    
    bloque = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ?", (user_id,)).fetchall()
    bloque_ids = [b['bloqué'] for b in bloque]
    
    if bloque_ids:
        placeholders = ', '.join('?' for _ in bloque_ids)
        query = f"SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE id_utilisateur IN ({placeholders})"
        utilisateurs = db.execute(query, tuple(bloque_ids)).fetchall()
    else:
        utilisateurs = []

    db.close()

    if not utilisateurs:
        flash("Aucun utilisateur bloqué trouvé.")
        return redirect(url_for("user.show_profile"))

    return render_template('user/afficher.html', utilisateurs=utilisateurs)

@user_bp.route('/afficher_suiveur', methods=['GET', 'POST'])
@login_required
def afficher_suiveur():
    user_id = session.get('user_id')
    db = get_db()
    
    suiveurs = db.execute("SELECT suiveur FROM suivre WHERE suivi = ?", (user_id,)).fetchall()
    suivi_ids = [suiveur['suiveur'] for suiveur in suiveurs]
    
    if  suivi_ids:
        placeholders = ', '.join('?' for _ in  suivi_ids)
        query = f"SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE id_utilisateur IN ({placeholders})"
        utilisateurs = db.execute(query, tuple( suivi_ids)).fetchall()
    else:
        utilisateurs = []
        
    db.close()

    if not utilisateurs:
        flash("Aucun utilisateur abonné trouvé.")
        return redirect(url_for("user.show_profile"))

    return render_template('user/afficher.html', utilisateurs=utilisateurs)

@user_bp.route('/afficher_suiveur_autre', methods=['GET', 'POST'])
@login_required
def afficher_suiveur_autre():
    user_id = request.args.get('user_id')
    db = get_db()
    
    suiveurs = db.execute("SELECT suiveur FROM suivre WHERE suivi = ?", (user_id,)).fetchall()
    suivi_ids = [suiveur['suiveur'] for suiveur in suiveurs]
    
    if  suivi_ids:
        placeholders = ', '.join('?' for _ in  suivi_ids)
        query = f"SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE id_utilisateur IN ({placeholders})"
        utilisateurs = db.execute(query, tuple( suivi_ids)).fetchall()
    else:
        utilisateurs = []
        
    db.close()

    if not utilisateurs:
        flash("Aucun utilisateur abonné trouvé.")
        return redirect(url_for('user.show_autreprofile', user=user_id))

    return render_template('user/afficher.html', utilisateurs=utilisateurs, retour=user_id)

@user_bp.route('/afficher_suivi', methods=['GET', 'POST'])
@login_required
def afficher_suivi():
    user_id = session.get('user_id')
    db = get_db()
    
    suivis = db.execute("SELECT suivi FROM suivre WHERE suiveur = ?", (user_id,)).fetchall()
    suivi_ids = [suivi['suivi'] for suivi in suivis]
    
    if  suivi_ids:
        placeholders = ', '.join('?' for _ in  suivi_ids)
        query = f"SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE id_utilisateur IN ({placeholders})"
        utilisateurs = db.execute(query, tuple( suivi_ids)).fetchall()
    else:
        utilisateurs = []
        
    db.close()

    if not utilisateurs:
        flash("Aucun utilisateur suivi trouvé.")
        return redirect(url_for("user.show_profile"))

    return render_template('user/afficher.html', utilisateurs=utilisateurs)

@user_bp.route('/afficher_suivi_autre', methods=['GET', 'POST'])
@login_required
def afficher_suivi_autre():
    user_id = request.args.get('user_id')
    db = get_db()
    
    suivis = db.execute("SELECT suivi FROM suivre WHERE suiveur = ?", (user_id,)).fetchall()
    suivi_ids = [suivi['suivi'] for suivi in suivis]
    
    if  suivi_ids:
        placeholders = ', '.join('?' for _ in  suivi_ids)
        query = f"SELECT photo_profil, id_utilisateur, nom_utilisateur FROM utilisateurs WHERE id_utilisateur IN ({placeholders})"
        utilisateurs = db.execute(query, tuple( suivi_ids)).fetchall()
    else:
        utilisateurs = []
        
    db.close()

    if not utilisateurs:
        flash("Aucun utilisateur suivi trouvé.")
        return redirect(url_for('user.show_autreprofile', user=user_id))


    return render_template('user/afficher.html', utilisateurs=utilisateurs, retour=user_id)

@user_bp.route('/modifier_oeuvre', methods=['POST'])
@login_required
def modifier_oeuvre():
    clicked_categories = request.form.getlist('categories')
    oeuvre_id = request.args.get('oeuvre_id')
    description = request.form.get('description', '').strip()

    if not oeuvre_id:
        flash("L'identifiant de l'œuvre est manquant.", "error")
        return redirect(url_for("user.show_profile"))

    db = get_db()

    try:
        db.execute("DELETE FROM categorisations WHERE oeuvre = ?", (oeuvre_id,))
        db.commit()

        if clicked_categories:
            for category_id in clicked_categories:
                db.execute("INSERT INTO categorisations (oeuvre, categorie) VALUES (?, ?)", (oeuvre_id , category_id))
            db.commit()

        db.execute("UPDATE oeuvres SET description_oeuvre = ? WHERE id_oeuvre = ?", (description, oeuvre_id))
        db.commit()
        flash("L'œuvre a été modifiée avec succès.", "success")
        return redirect(url_for('user.show_profile'))

    except Exception as e:
        db.rollback()
        close_db()
        flash(f"Une erreur est survenue", "error")
        return redirect(url_for('user.modifier_fichier'))

    finally:
        close_db()
        return redirect(url_for("user.show_profile"))

@user_bp.route('/modifier_fichier', methods=('GET', 'POST'))
@login_required
def modifier_fichier():
    db = get_db()
    oeuvre_id = request.args.get('oeuvre_id')

    if not oeuvre_id:
        flash("L'identifiant de l'œuvre est manquant.", "error")
        return redirect(url_for("user.show_profile"))

    oeuvre = db.execute("SELECT id_oeuvre, chemin_fichier, utilisateur, description_oeuvre FROM oeuvres WHERE id_oeuvre = ?",(oeuvre_id,)).fetchone()

    if not oeuvre:
        flash("L'œuvre demandée est introuvable.", "error")
        return redirect(url_for("user.show_profile"))

    categories = db.execute("SELECT id_categorie, nom FROM categories_oeuvres").fetchall()
    page_type= "upload"
    return render_template('user/modifier.html', oeuvre=oeuvre, categories=categories,  page_type= page_type)

@user_bp.route('/supprimer_oeuvre', methods=('GET', 'POST'))
@login_required
def supprimer_oeuvre():
    user_id = session.get('user_id')  
    photoeuvre_id = request.args.get('photogrand_id')
    filename = request.args.get('filename')
    filepath = os.path.join('app/static/upload', str(user_id), filename)
    
    
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

@user_bp.route('/changer_profil', methods=('GET', 'POST'))
@login_required
def changer_profil():
    page_type= "upload"
    user_id = session.get('user_id')
    if user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE NOT utilisateur = ?",(user_id,)).fetchall() 
        close_db()
    
    if not user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
        close_db()
    random.shuffle(photo)
    return render_template('user/changer_profil.html', user=g.user, page_type= page_type, photo=photo)

@user_bp.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    user = session.get('user_id') 

    emetteur_ids = [] 
    recepteur_ids = [] 
    bloque_ids = [] 
    empecheur_ids = [] 
    combined_ids = []
    stop_ids = []
    conversation_ids =[]
    conv = []

    db = get_db()

    emetteurs = db.execute("SELECT emetteur FROM contacter WHERE recepteur= ?", (user,)).fetchall()
    recepteurs = db.execute("SELECT recepteur FROM contacter WHERE emetteur = ?", (user,)).fetchall()
    bloques = db.execute("SELECT bloqué FROM bloque WHERE empecheur = ?", (user,)).fetchall()
    empecheurs = db.execute("SELECT empecheur FROM bloque WHERE bloqué = ?", (user,)).fetchall()

    emetteur_ids = [row[0] for row in emetteurs if row[0]]
    recepteur_ids = [row[0] for row in recepteurs if row[0]]
    bloque_ids = [row[0] for row in bloques if row[0]]
    empecheur_ids = [row[0] for row in empecheurs if row[0]]

    combined_ids = list(set(emetteur_ids) | set(recepteur_ids))
    stop_ids = list(set(bloque_ids) | set(empecheur_ids) )
    
    
    conversation_ids = [id for id in combined_ids if id not in stop_ids]

    user_id = request.args.get('user_id')
    if not user_id :
        if conversation_ids:
            placeholders = ', '.join('?' for _ in stop_ids)
            query = f"SELECT MAX(message_id) AS id_max, recepteur, emetteur FROM contacter WHERE ((recepteur = ? AND emetteur NOT IN ({placeholders}))OR (emetteur = ? AND recepteur NOT IN ({placeholders})))"
            params = (user,) + tuple(stop_ids) + (user,) + tuple(stop_ids)
            max_row = db.execute(query, params).fetchone()

            
            if max_row:
                user_id = max_row['recepteur'] if max_row['recepteur'] != user else max_row['emetteur']

    messages = db.execute("SELECT message, emetteur FROM contacter WHERE (recepteur = ? AND emetteur = ?) OR (recepteur = ? AND emetteur = ?)", (user_id, user, user, user_id)).fetchall(); 
    autre = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
      
    placeholders = ', '.join('?' for _ in conversation_ids)
    query = f"SELECT * FROM utilisateurs WHERE id_utilisateur IN ({placeholders}) AND id_utilisateur != ?"
    conv = db.execute(query, tuple(conversation_ids) + (user_id,)).fetchall()
    
    db.close()
    if not autre :
        flash("Aucune conversation", "error")
        return redirect(url_for("user.show_profile"))

    return render_template('user/messages.html', messages=messages, user=autre, user_id=user_id, conv=conv)

@user_bp.route('/envoyer', methods=['POST'])
@login_required
def envoyer_message():
    db = get_db()
    user_id = session.get('user_id')  
    destinataire_id = request.args.get('user_id')  
    contenu = request.form.get('message', '').strip()

    if not destinataire_id or not contenu:
        flash("Le destinataire et le message sont requis.", "error")
        return redirect(url_for('user.messages', user_id=destinataire_id))

    db.execute("INSERT INTO contacter (emetteur, recepteur, message) VALUES (?, ?, ?)", (user_id, destinataire_id, contenu))

    db.commit()
    db.close()

    return redirect(url_for('user.messages', user_id=destinataire_id))
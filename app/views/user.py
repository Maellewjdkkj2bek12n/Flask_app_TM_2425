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
    user = session.get('user_id')
    
    bloquer= db.execute("SELECT bloqué FROM bloque WHERE empecheur = ? AND bloqué = ?", (user, user_id)).fetchone()
    if bloquer :  
        bloque = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
        user = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        close_db()
        return render_template('user/profil autre.html',photo_user=photo_user, user=user, bloque=bloque)
    
    suivre= db.execute("SELECT suivi FROM suivre WHERE suiveur = ? AND suivi = ?", (user, user_id)).fetchone()
    if suivre : 
        suivi = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
        user = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
        close_db()
        return render_template('user/profil autre.html',photo_user=photo_user, user=user, suivi=suivi)
    else :
        photo_user = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE utilisateur = ?",(user_id,)).fetchall()  
        user = db.execute("SELECT id_utilisateur, nom_utilisateur, bio, photo_profil  FROM utilisateurs WHERE id_utilisateur = ?",(user_id,)).fetchone()
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
                return redirect(url_for("user.changer_profil"))
            
            finally:
                close_db()
                return redirect(url_for("user.changer_profil"))
    return redirect(url_for("user.changer_profil"))

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
                error = "Oups, le nom d'utilisateur est déjà utilisé."
                flash(error)
                return redirect(url_for("user.changer_profil"))
            
            finally:
                close_db()
                return redirect(url_for('user.changer_profil'))
    return redirect(url_for("user.changer_profil"))
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
        nom_fichier = request.args.get('nom_fichier')
        if nom_fichier :
            chemin = os.path.join(current_app.config['IMAGE_FOLDER'], nom_fichier)
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
            filepath = os.path.join(current_app.config['IMAGE_FOLDER'], filename)
            
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
        chemin = os.path.join(current_app.config['IMAGE_FOLDER'], nom_fichier)
        if os.path.exists(chemin):  
            os.remove(chemin)
        db = get_db() 
        db.execute("UPDATE utilisateurs SET photo_profil = NULL, nom_photo_profil = NULL WHERE id_utilisateur = ?", (user_id,))
        db.commit()  
        close_db()
    else:
        flash("Aucune photo de profil trouvée.")
    return redirect(url_for('user.changer_profil'))
    
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


# pour selectionner les catégories 
@user_bp.route('/change_categorie', methods=['POST'])
@login_required
def change_categorie():
    clicked_categories = request.form.getlist('categories')
    oeuvre_id = request.args.get('oeuvre_id')
    
    description = request.form.get('description', '').strip()
        
    if description:
        db = get_db()
        try:
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
        
        db = get_db()

        try:
            for category_id in clicked_categories:
                db.execute("INSERT INTO categorisations (oeuvre, categorie) VALUES (?, ?)", (oeuvre_id , category_id))
            db.commit()
            

            return redirect(url_for('user.show_profile'))

        except Exception as e:
            db.rollback()
            flash(f"Une erreur est survenue : {str(e)}", "error")
            return redirect(url_for("user.chemin_fichier"))

        finally:
            close_db()

    return redirect(url_for('user.chemin_fichier'))

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

            nom_fichier = user['nom_photo_profil']
            if nom_fichier:
                chemin = os.path.join(current_app.config['IMAGE_FOLDER'], nom_fichier)
                if os.path.exists(chemin):  
                    print(f"Suppression de la photo de profil: {chemin}")
                    os.remove(chemin)
                else:
                    print(f"Fichier de la photo de profil non trouvé: {chemin}")

            oeuvres = db.execute('SELECT * FROM oeuvres WHERE utilisateur = ?', (user_id,)).fetchall()
            for oeuvre in oeuvres:
                nom_fichier_oeuvre = oeuvre['nom'] 
                if nom_fichier_oeuvre:
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], nom_fichier_oeuvre)
                    if os.path.exists(filepath):  
                        print(f"Suppression de l'œuvre: {filepath}")
                        os.remove(filepath)
                    else:
                        print(f"Fichier de l'œuvre non trouvé: {filepath}")

            print("Suppression des œuvres de la base de données...")
            db.execute("DELETE FROM oeuvres WHERE utilisateur = ?", (user_id,))
            print("Suppression de l'utilisateur de la base de données...")
            db.execute("DELETE FROM utilisateurs WHERE id_utilisateur = ?", (user_id,))
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


@user_bp.route('/afficher_suivre', methods=['GET', 'POST'])
@login_required
def afficher_suivre():
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
    return render_template('user/changer_profil.html', user=g.user, page_type= page_type, photo=photo)
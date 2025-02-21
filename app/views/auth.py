from enum import auto
from mailbox import Message
import random
import string
from flask import (Blueprint, current_app, flash, g, jsonify, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db.db import get_db, close_db
import os

# Création d'un blueprint contenant les routes ayant le préfixe /auth/...
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Route /auth/register
@auth_bp.route('/register', methods=('GET', 'POST'))
def register():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    
    # Si des données de formulaire sont envoyées vers la route /register (ce qui est le cas lorsque le formulaire d'inscription est envoyé) c'est une requete post
    if request.method == 'POST':

        # On récupère les champs 'nom_utilisateur' et 'password' de la requête HTTP
        
        mail = request.form['mail'] 
        #code = request.form['code'] 
        username = request.form['username'] 
        password = request.form['password'] 
        confirm_password = request.form['confirm_password']

        # On récupère la base de donnée
        db = get_db()

        # Si le nom d'utilisateur et le mot de passe ont bien une valeur
        # on essaie d'insérer l'utilisateur dans la base de données
        if username and password and mail and confirm_password :
            
            #il faut que les deux mots de passes soient les mêmes 
            if password != confirm_password: 
                error = "Les mots de passe ne correspondent pas." 
                flash(error) 
                return redirect(url_for("auth.register"))
            
            #il faut que le code de confirmations soit le bon cote de confirmation 
            #if code != session.get('confirmation_code'): 
            #    flash('Code de confirmation incorrect.') 
            #    return redirect(url_for("auth.register"))
            
            #on met les valeurs dans la base de donnée 
            try:
                db.execute("INSERT INTO utilisateurs (adresse_mail, nom_utilisateur, mot_passe) VALUES (?, ?, ?)",(mail, username, generate_password_hash(password)))
                # db.commit() permet de valider une modification de la base de données
                db.commit()
                # On ferme la connexion à la base de données pour éviter les fuites de mémoire
                close_db()
             
            #si l'utilisateur existe déjà   
            except db.IntegrityError:
                # La fonction flash dans Flask est utilisée pour stocker un message dans la session de l'utilisateur
                # dans le but de l'afficher ultérieurement, généralement sur la page suivante après une redirection
                error = "Oups, l'utilisateur {username} déjà enregistré."
                flash(error)
                return redirect(url_for("auth.register"))
            
            return redirect(url_for("auth.login"))
         
        else:
            error = "Remplir tout les champs"
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        # Si aucune donnée de formulaire n'est envoyée, on affiche le formulaire d'inscription (on a fait une requete get)
        return render_template('home/index.html', photo=photo)

# Route /auth/login
@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    db = get_db()  
    photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
    close_db()
    # Si des données de formulaire sont envoyées vers la route /login (ce qui est le cas lorsque le formulaire de login est envoyé)
    if request.method == 'POST':

        # On récupère les champs 'nom_utilisateur' et 'password' de la requête HTTP
        username = request.form['username']
        password = request.form['password']

        # On récupère la base de données
        db = get_db()
        
        # On récupère l'utilisateur avec le username spécifié (une contrainte dans la db indique que le nom d'utilisateur est unique)
        # La virgule après username est utilisée pour créer un tuple contenant une valeur unique
        user = db.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = ?', (username,)).fetchone()

        # On ferme la connexion à la base de données pour éviter les fuites de mémoire
        close_db()

        # Si aucun utilisateur n'est trouve ou si le mot de passe est incorrect
        # on crée une variable error 
        error = None
        if user is None:
            error = "Le nom d'utilisateur est incorrect."
        elif not check_password_hash(user['mot_passe'], password):
            error = "Le mot de passe est incorrect."

        # S'il n'y pas d'erreur, on ajoute l'id de l'utilisateur dans une variable de session
        # De cette manière, à chaque requête de l'utilisateur, on pourra récupérer l'id dans le cookie session
        if error is None:
            session.clear()
            session['user_id'] = user['id_utilisateur']
            # On redirige l'utilisateur vers la page principale une fois qu'il s'est connecté
            return redirect("/")
        
        else:
            # En cas d'erreur, on ajoute l'erreur dans la session et on redirige l'utilisateur vers le formulaire de login
            flash(error)
            return redirect(url_for("auth.login"))
    else:
        return render_template('home/index.html', photo=photo)

# Route /auth/logout
@auth_bp.route('/logout')
def logout():
    # Se déconnecter consiste simplement à supprimer le cookie session
    session.clear()

    # On redirige l'utilisateur vers la page principale une fois qu'il s'est déconnecté
    return redirect("/")


# Fonction automatiquement appelée à chaque requête (avant d'entrer dans la route) sur une route appartenant au blueprint 'auth_bp'
# La fonction permet d'ajouter un attribut 'user' représentant l'utilisateur connecté dans l'objet 'g' 


@auth_bp.before_app_request
def load_logged_in_user():

    # On récupère l'id de l'utilisateur stocké dans le cookie session
    user_id = session.get('user_id')

    # Si l'id de l'utilisateur dans le cookie session est nul, cela signifie que l'utilisateur n'est pas connecté
    # On met donc l'attribut 'user' de l'objet 'g' à None
    if user_id is None:
        g.user = None

    # Si l'id de l'utilisateur dans le cookie session n'est pas nul, on récupère l'utilisateur correspondant et on stocke
    # l'utilisateur comme un attribut de l'objet 'g'
    else:
         # On récupère la base de données et on récupère l'utilisateur correspondant à l'id stocké dans le cookie session
        db = get_db()
        g.user = db.execute('SELECT * FROM utilisateurs WHERE id_utilisateur = ?', (user_id,)).fetchone()
        # On ferme la connexion à la base de données pour éviter les fuites de mémoire
        close_db()
        
        
@auth_bp.route('/MDP', methods=['GET', 'POST'])
def MDP():
    user_id = session.get('user_id')
    if user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres WHERE NOT utilisateur = ?",(user_id,)).fetchall() 
        close_db()
    
    if not user_id:
        db = get_db()  
        photo = db.execute("SELECT id_oeuvre, chemin_fichier FROM oeuvres").fetchall()  
        close_db()
    
    if request.method == 'POST':
        nom = request.form['nom']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Vérifier si l'e-mail, le mot de passe et la confirmation sont remplis 
        if not nom or not password or not confirm_password:
            flash("Veuillez remplir tous les champs.")
            return redirect(url_for('auth.MDP'))

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.")
            return redirect(url_for('auth.MDP'))

        # Connexion à la base de données
        db = get_db()

        # Vérifier si l'utilisateur existe avec cet e-mail
        user = db.execute('SELECT * FROM utilisateurs WHERE nom_utilisateur = ?', (nom,)).fetchone()
        if user_id :
            if user_id != user['id_utilisateur'] :
                flash("Cette adresse mail n'est pas reliée à ce compte")
                return redirect(url_for('auth.MDP'))

        if user:
            # Hacher le nouveau mot de passe
            hashed_password = generate_password_hash(password)

            # Mettre à jour le mot de passe dans la base de données
            try:
                db.execute('UPDATE utilisateurs SET mot_passe = ? WHERE nom_utilisateur = ?', (hashed_password, nom))
                db.commit()
                return redirect(url_for('auth.logout'))  # Rediriger vers la page de connexion après le changement de mot de passe
            except Exception as e:
                db.rollback()  # Annuler toute modification en cas d'erreur
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
        # Affichage du formulaire quand la requête est GET
        page_type= "MDP"
        random.shuffle(photo)
        return render_template('auth/MDP.html', photo=photo, page_type=page_type)
    

@auth_bp.route('/send_confirmation_code', methods=['POST'])
def send_confirmation_code():
    email = request.json.get('mail')
    if not email:
        return jsonify({"error": "L'email est requis"}), 400
    code = ''.join(random.choices(string.digits, k=6))

    try:
        subject="Votre code de confirmation"
        to_address=[email]
        message = f"Votre code de confirmation est : {code}"
        email.send_email(to_address, subject, message, cc_addresses=None)
        flash({"message": "Code envoyé avec succès", "code": code}), 200

    except Exception as e:
        flash(f"Erreur lors de l'envoi de l'email : {e}")
        return jsonify({"error": "Une erreur est survenue lors de l'envoi de l'e-mail"}), 500

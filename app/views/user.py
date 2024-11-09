from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from app.utils import *
from flask import Flask, request, redirect, url_for, flash, render_template
import sqlite3

# Routes /user/...
user_bp = Blueprint('user', __name__, url_prefix='/user')

# Route /user/profile accessible uniquement à un utilisateur connecté grâce au décorateur @login_required
@user_bp.route('/profil', methods=('GET', 'POST'))
@login_required 
def show_profile():
    page_type = 'profil'
    # Affichage de la page principale de l'application
    return render_template('user/profil.html', page_type=page_type)

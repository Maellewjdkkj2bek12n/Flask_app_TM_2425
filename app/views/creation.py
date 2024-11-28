from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

# Routes /...
creation_bp = Blueprint('creation', __name__)

# Route /affichage
@creation_bp.route('/affichage', methods=('GET', 'POST'))
def affichage():
    # Affichage de limage en grand écran 
    return render_template('creation/affichage.html')

# Route /uploade
@creation_bp.route('/upload', methods=('GET', 'POST'))
def upload():
    # mettre image dans site 
    page_type='profil_setting'
    return render_template('creation/upload.html', page_type=page_type)

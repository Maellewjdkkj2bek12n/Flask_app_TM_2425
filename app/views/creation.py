from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

# Routes /...
creation_bp = Blueprint('creation', __name__)

# Route /auth/register
@creation_bp.route('/affichage', methods=('GET', 'POST'))
def affichage():
    # Affichage de limage en grand écran 
    return render_template('creation/affichage.html')



document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Bloquer et parler à d'autres utilisateurs
    const menuToggle2 = document.getElementById('menu-toggle2');
    const menu2 = document.getElementById('menu2');

    if (menuToggle2 && menu2) {
        menuToggle2.addEventListener('click', () => {
            menu2.classList.toggle('hidden');
            menuToggle2.src = menu2.classList.contains('hidden')
                ? '/static/imgs/Settings.png'
                : '/static/imgs/SettingsA.png';
        });
    }

    // Filtrer les œuvres
    const menuToggle3 = document.getElementById('menu-toggle3');
    const menu3 = document.getElementById('menu3');

    if (menuToggle3 && menu3) {
        menuToggle3.addEventListener('click', () => {
            menu3.classList.toggle('hidden');
            menuToggle3.src = menu3.classList.contains('hidden')
                ? '/static/imgs/Filtre.png'
                : '/static/imgs/FiltreA.png';
        });
    }

    // Gestion connexion et inscription
    const loginButton = document.getElementById('toggle-login');
    const registerButton = document.getElementById('toggle-register');
    const loginMenu = document.getElementById('login-menu');
    const registerMenu = document.getElementById('register-menu');

    if (loginButton && registerButton && loginMenu && registerMenu) {
        loginButton.addEventListener('click', () => {
            if (loginMenu.style.display === 'block') {
                loginMenu.style.display = 'none';
                loginButton.removeAttribute('id');
            } else {
                loginMenu.style.display = 'block';
                registerMenu.style.display = 'none';
                loginButton.setAttribute('id', 'active-login');
                registerButton.removeAttribute('id');
            }
        });

        registerButton.addEventListener('click', () => {
            if (registerMenu.style.display === 'block') {
                registerMenu.style.display = 'none';
                registerButton.removeAttribute('id');
            } else {
                registerMenu.style.display = 'block';
                loginMenu.style.display = 'none';
                registerButton.setAttribute('id', 'active-register');
                loginButton.removeAttribute('id');
            }
        });
    }

    // Barre de recherche
    const menuToggle4 = document.getElementById('menu-toggle4');
    const menu4 = document.getElementById('menu4');

    if (menuToggle4 && menu4) {
        menuToggle4.addEventListener('click', () => {
            menu4.classList.toggle('hidden');
            menuToggle4.src = menu4.classList.contains('hidden')
                ? '/static/imgs/chercher.png'
                : '/static/imgs/chercherA.png';
        });
    }

    // Pour des messages d'erreurs qui disparaissent
    const flashes = document.querySelectorAll('.flash');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(msg => msg.classList.add('hide'));
        }, 2000);
    }



    document.getElementById('mail').addEventListener('blur', function () {
        const email = this.value;
        if (email) {
            fetch('{{ url_for("auth.send_confirmation_code") }}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert('Code de confirmation envoyé !');
                }
            })
            .catch(error => {
                console.error('Erreur :', error);
                alert("Erreur lors de l'envoi du code.");
            });
        }
    });

    // Renvoyer le code quand on clique sur le bouton
    document.getElementById('resend-code-btn').addEventListener('click', function () {
        const email = document.getElementById('mail').value;
        if (email) {
            fetch('{{ url_for("auth.send_confirmation_code") }}', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email: email })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    alert('Code de confirmation renvoyé !');
                }
            })
            .catch(error => {
                console.error('Erreur :', error);
                alert("Erreur lors de l'envoi du code.");
            });
        } else {
            alert("Veuillez entrer une adresse e-mail avant de renvoyer le code.");
        }
    });
    
});



document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Modifier profil perso
    const menuToggle1 = document.getElementById('menu-toggle1');
    const switchToMenu11 = document.getElementById('switchToMenu11');
    const switchToMenu12 = document.getElementById('switchToMenu12');
    const switchToMenu13 = document.getElementById('switchToMenu13');
    const switchToMenu14 = document.getElementById('switchToMenu14');

    const menu1 = document.getElementById('menu1');
    const menu11 = document.getElementById('menu11');
    const menu12 = document.getElementById('menu12');
    const menu13 = document.getElementById('menu13');
    const menu14 = document.getElementById('menu14');

    // Ajouter un événement de clic à logo
    menuToggle1.addEventListener('click', () => {
        // Basculer la classe "hidden" sur le menu
        menu1.classList.toggle('hidden');
        menu11.classList.add('hidden');
        menu12.classList.add('hidden');
        menu13.classList.add('hidden');
        menu14.classList.add('hidden');

        if (!menu1.classList.contains('hidden')) {
            menuToggle1.src = '/static/imgs/SettingsA.png';
        } else if (!menu11.classList.contains('hidden')) {
            menuToggle1.src = '/static/imgs/SettingsA.png';
        } else if (!menu12.classList.contains('hidden')) {
            menuToggle1.src = '/static/imgs/SettingsA.png';
        } else if (!menu13.classList.contains('hidden')) {
            menuToggle1.src = '/static/imgs/SettingsA.png';
        } else if (!menu14.classList.contains('hidden')) {
            menuToggle1.src = '/static/imgs/SettingsA.png';
        } else {
            menuToggle1.src = '/static/imgs/Settings.png';
        }
    });

    switchToMenu11.addEventListener('click', () => {
        menu1.classList.add('hidden');
        menu12.classList.add('hidden');
        menu13.classList.add('hidden');
        menu14.classList.add('hidden');
        menu11.classList.remove('hidden');
    });

    switchToMenu12.addEventListener('click', () => {
        menu1.classList.add('hidden');
        menu11.classList.add('hidden');
        menu13.classList.add('hidden');
        menu14.classList.add('hidden');
        menu12.classList.remove('hidden');
    });

    switchToMenu13.addEventListener('click', () => {
        menu1.classList.add('hidden');
        menu11.classList.add('hidden');
        menu12.classList.add('hidden');
        menu14.classList.add('hidden');
        menu13.classList.remove('hidden');
    });

    switchToMenu14.addEventListener('click', () => {
        menu1.classList.add('hidden');
        menu11.classList.add('hidden');
        menu12.classList.add('hidden');
        menu13.classList.add('hidden');
        menu14.classList.remove('hidden');
    });
});
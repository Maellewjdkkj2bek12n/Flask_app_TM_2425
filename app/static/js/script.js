document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Modifier profil perso
    const menuToggle1 = document.getElementById('menu-toggle1');
    const menuItems1 = ['menu1', 'menu11', 'menu12', 'menu13', 'menu14'];
    const switches1 = ['switchToMenu11', 'switchToMenu12', 'switchToMenu13', 'switchToMenu14'];

    if (menuToggle1) {
        const menus = menuItems1.map(id => document.getElementById(id));
        const switches = switches1.map(id => document.getElementById(id));

        menuToggle1.addEventListener('click', () => {
            menus.forEach(menu => menu.classList.add('hidden'));
            menus[0].classList.toggle('hidden');
            menuToggle1.src = menus.some(menu => !menu.classList.contains('hidden'))
                ? '/static/imgs/SettingsA.png'
                : '/static/imgs/Settings.png';
        });

        switches.forEach((switchElement, index) => {
            if (switchElement) {
                switchElement.addEventListener('click', () => {
                    menus.forEach(menu => menu.classList.add('hidden'));
                    menus[index + 1].classList.remove('hidden');
                });
            }
        });
    }

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

    const uploadButtons = document.querySelectorAll('.uploadgrandsboutons');
    uploadButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('clicked');
        });
    });

    const categoryForm = document.getElementById('categorie_form');
    if (categoryForm) {
        categoryForm.addEventListener('submit', function () {
            const clickedCategories = Array.from(document.querySelectorAll('.uploadgrandsboutons.clicked'))
                .map(button => button.getAttribute('data-id'));
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'clicked_categories';
            input.value = JSON.stringify(clickedCategories);
            this.appendChild(input);
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

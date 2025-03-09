document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    //parametres profil
    const menuToggle1 = document.getElementById('menu-toggle1');
    const menu1 = document.getElementById('menu1');

    if (menuToggle1 && menu1) {
        menuToggle1.addEventListener('click', () => {
            menu1.classList.toggle('hidden');
            menuToggle1.src = menu1.classList.contains('hidden')
                ? '/static/imgs/Settings.png'
                : '/static/imgs/SettingsA.png';
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
});

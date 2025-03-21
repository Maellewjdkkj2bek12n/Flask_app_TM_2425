document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    //parametres profil
    const menuToggle1 = document.getElementById('menu-toggle1');
    const menu1 = document.getElementById('menu1');
    var activeImg1 = '/static/imgs/SettingsA.png';
    var inactiveImg1 = '/static/imgs/Settings.png';

    if (menuToggle1 && menu1 && inactiveImg1 && activeImg1) {
        menuToggle1.addEventListener('click', () => {
            if (menu1.classList.contains('hidden')) {
                menu1.classList.remove('hidden');
                menuToggle1.src = activeImg1; 
            } else {
                menu1.classList.add('hidden'); 
                menuToggle1.src = inactiveImg1; 
            }
        });
    }

    // Bloquer et parler à d'autres utilisateurs
    const menuToggle2 = document.getElementById('menu-toggle2');
    const menu2 = document.getElementById('menu2');
    var activeImg2 = '/static/imgs/SettingsA.png'; 
    var inactiveImg2 = '/static/imgs/Settings.png'; 

    if (menuToggle2 && menu2 && inactiveImg2 && activeImg2) {
        menuToggle2.addEventListener('click', () => {
            if (menu2.classList.contains('hidden')) {
                menu2.classList.remove('hidden'); 
                menuToggle2.src = activeImg2; 
            } else {
                menu2.classList.remove('visible'); 
                menu2.classList.add('hidden'); 
                menuToggle2.src = inactiveImg2; 
            }
        });
    }

    // Filtrer les œuvres
    const menuToggle3 = document.getElementById('menu-toggle3');
    const menu3 = document.getElementById('menu3');
    var activeImg3 = '/static/imgs/FiltreA.png'; 
    var inactiveImg3 = '/static/imgs/Filtre.png'; 

    if (menuToggle3 && menu3 && inactiveImg3 && activeImg3) {
        menuToggle3.addEventListener('click', () => {
            if (menu3.classList.contains('hidden')) {
                menu3.classList.remove('hidden'); 
                menuToggle3.src = activeImg3; 
            } else {
                menu3.classList.remove('visible'); 
                menu3.classList.add('hidden'); 
                menuToggle3.src = inactiveImg3; 
            }
        });
    }

    // Gestion connexion
    const loginButton = document.getElementById('toggle-login');
    const loginMenu = document.getElementById('login-menu');

    if (loginButton && loginMenu) {
        loginButton.addEventListener('click', () => {
            if (loginMenu.classList.contains('hidden')) {
                loginMenu.classList.remove('hidden'); 
                loginButton.classList.add('active'); 
            } else {
                loginMenu.classList.remove('visible'); 
                loginMenu.classList.add('hidden'); 
                loginButton.classList.remove('active'); 
            }
        });

    }

    //gestion inscription
    const registerButton = document.getElementById('toggle-register');
    const registerMenu = document.getElementById('register-menu');

    if (registerButton && registerMenu) {
        registerButton.addEventListener('click', () => {
            if (registerMenu.classList.contains('hidden')) {
                registerMenu.classList.remove('hidden'); 
                registerButton.classList.add('active'); 
            } else {
                registerMenu.classList.remove('visible'); 
                registerMenu.classList.add('hidden'); 
                registerButton.classList.remove('active'); 
            }
        });
    }

    // Barre de recherche
    const menuToggle4 = document.getElementById('menu-toggle4');
    const menu4 = document.getElementById('menu4');
    var activeImg4 = '/static/imgs/chercherA.png'; 
    var inactiveImg4 = '/static/imgs/chercher.png'; 

    if (menuToggle4 && menu4 && inactiveImg4 && activeImg4) {
        menuToggle4.addEventListener('click', () => {
            if (menu4.classList.contains('hidden')) {
                menu4.classList.remove('hidden'); 
                menuToggle4.src = activeImg4; 
            } else {
                menu4.classList.remove('visible'); 
                menu4.classList.add('hidden'); 
                menuToggle4.src = inactiveImg4; 
            }
        });
    }

    // Pour des messages d'erreurs qui disparaissent
    const duration = 3000;
    const flashMessage = document.getElementById('flash-message');

    if (flashMessage) {
        setTimeout(() => {
            flashMessage.style.display = 'none';
        }, duration);
    }

});

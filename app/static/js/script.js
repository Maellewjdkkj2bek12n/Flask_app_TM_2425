console.log("Script bien chargé")

//pour menu déroulant en appuyant sur logo

//pour modifer profil perso
document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner logo et menu
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

//pour bloquer et parler à autre utilisateurs
document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner logo et menu
        const menuToggle2 = document.getElementById('menu-toggle2');
        const menu2 = document.getElementById('menu2');

        // Ajouter un événement de clic à logo
        menuToggle2.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu2.classList.toggle('hidden');

        if (menu2.classList.contains('hidden'))  {
            menuToggle2.src = '/static/imgs/Settings.png'; 
        } else {
            menuToggle2.src = '/static/imgs/SettingsA.png';
        }
        });
});

//pour filtrer les oeuvres
document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Gestion du menu de filtrage des œuvres
    const menuToggle3 = document.getElementById('menu-toggle3');
    const menu3 = document.getElementById('menu3');
    if (menuToggle3 && menu3) {
        menuToggle3.addEventListener('click', () => {
            menu3.classList.toggle('hidden');
            menuToggle3.src = menu3.classList.contains('hidden') ? '/static/imgs/Filtre.png' : '/static/imgs/FiltreA.png';
        });
    }

    // Gestion des boutons cliquables dans la partie upload
    const uploadButtons = document.querySelectorAll('.uploadgrandsboutons');
    uploadButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('clicked');
        });
    });

    // Soumission du formulaire avec les catégories sélectionnées
    const categoryForm = document.getElementById('categorie_form');
    if (categoryForm) {
        categoryForm.addEventListener('submit', function (event) {
            const clickedCategories = Array.from(document.querySelectorAll('.uploadgrandsboutons.clicked'))
                .map(button => button.getAttribute('data-id'));

            // Ajouter les catégories sélectionnées au formulaire
            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'clicked_categories';
            input.value = JSON.stringify(clickedCategories);
            this.appendChild(input);
        });
    }


    // Pour des messages d'erreurs qui disparraissent
    const flashes = document.querySelectorAll('.flash');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(msg => msg.classList.add('hide'));
        }, 2000);
    }

    
});

//pour filtrer les catégories
document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Gestion des boutons cliquables dans la partie filtrer
    const filterButtons = document.querySelectorAll('.Filtrerboutons');
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('clicked');
        });
    });

    // Interception de la soumission du formulaire
    const filterForm = document.getElementById('Filtrer_form');
    if (filterForm) {
        filterForm.addEventListener('submit', function (event) {
            const selectedCategories = Array.from(document.querySelectorAll('.Filtrerboutons.clicked'))
                .map(button => button.getAttribute('data-id'));

            const input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'categories_filtrer';  // Le nom à utiliser côté serveur
            input.value = JSON.stringify(selectedCategories);  // Convertir en chaîne JSON
            this.appendChild(input);
        });
    }
});



//pour afficher menu register et login
document.addEventListener('DOMContentLoaded', function () {
    const loginButton = document.getElementById('toggle-login');
    const registerButton = document.getElementById('toggle-register');
    const loginMenu = document.getElementById('login-menu');
    const registerMenu = document.getElementById('register-menu');
    
    // Gestion du clic sur "Connexion"
    loginButton.addEventListener('click', function () {
      // Si le menu Connexion est visible, on le masque
      if (loginMenu.style.display === 'block') {
        loginMenu.style.display = 'none';
        loginButton.removeAttribute('id'); // Retire l'ID actif
      } else {
        // Sinon, on affiche le menu Connexion
        loginMenu.style.display = 'block';
        registerMenu.style.display = 'none';
        loginButton.setAttribute('id', 'active-login'); // Ajoute l'ID actif à Connexion
        registerButton.removeAttribute('id'); // Retire l'ID actif de l'Inscription
      }
    });
  
    // Gestion du clic sur "Inscription"
    registerButton.addEventListener('click', function () {
      // Si le menu Register est visible, on le masque
      if (registerMenu.style.display === 'block') {
        registerMenu.style.display = 'none';
        registerButton.removeAttribute('id'); // Retire l'ID actif
      } else {
        // Sinon, on affiche le menu Register
        registerMenu.style.display = 'block';
        loginMenu.style.display = 'none';
        registerButton.setAttribute('id', 'active-register'); // Ajoute l'ID actif à Register
        loginButton.removeAttribute('id'); // Retire l'ID actif de Connexion
      }
    });
  });

//pour dérouler la barre de recherche
document.addEventListener('DOMContentLoaded', () => {
    console.log("Script bien chargé");

    // Gestion du menu de filtrage des œuvres
    const menuToggle4 = document.getElementById('menu-toggle4');
    const menu4 = document.getElementById('menu4');
    if (menuToggle4 && menu4) {
        menuToggle4.addEventListener('click', () => {
            menu4.classList.toggle('hidden');
            menuToggle4.src = menu4.classList.contains('hidden') ? '/static/imgs/chercher.png' : '/static/imgs/chercherA.png';
        });
    }
 });
  
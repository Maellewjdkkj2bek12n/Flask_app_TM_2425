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

    

    // Gestion des boutons cliquables pour les types d'art
    const typeArtButtons = document.querySelectorAll('.typeartboutons');
    typeArtButtons.forEach(button => {
        button.addEventListener('click', () => {
            button.classList.toggle('clicked');
        });
    });

    // Gestion des flash messages pour un effet de disparition
    const flashes = document.querySelectorAll('.flash');
    if (flashes.length > 0) {
        setTimeout(() => {
            flashes.forEach(msg => msg.classList.add('hide'));
        }, 2000);
    }

    
});
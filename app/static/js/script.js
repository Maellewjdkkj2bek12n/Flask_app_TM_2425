console.log("Script bien chargé")

//pour menu déroulant en appuyant sur logo

//pour modifer profil perso
document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner logo et menu
        const menuToggle1 = document.getElementById('menu-toggle1');
        const menu1 = document.getElementById('menu1');

        // Ajouter un événement de clic à logo
        menuToggle1.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu1.classList.toggle('hidden');

            if (menu1.classList.contains('hidden'))  {
                menuToggle1.src = '/static/imgs/Settings.png' ; 
            } else {
                menuToggle1.src = '/static/imgs/SettingsA.png' ;
            }
        });

        window.showMenu = (menu4) => {
            document.querySelectorAll('.menu').forEach(menu => {
                menu.classList.add('hidden'); // Cacher tous les menus
                
            });
            document.getElementById(menu4).classList.remove('hidden'); // Afficher le menu sélectionné
        };
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

        document.addEventListener('click', () => {
            if (!menu2.classList.contains('hidden')) {
                menu2.classList.add('hidden');
                menuToggle2.src = '/static/imgs/Settings.png'; // Remettre l'icône initiale
            }
        });

        menu2.addEventListener('click', (event) => {
            event.stopPropagation();
        });
});

//pour filtrer les oeuvres
document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner logo et menu
        const menuToggle3 = document.getElementById('menu-toggle3');
        const menu3 = document.getElementById('menu3');

        // Ajouter un événement de clic à logo
        menuToggle3.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu3.classList.toggle('hidden');

        if (menu3.classList.contains('hidden'))  {
            menuToggle3.src = '/static/imgs/Filtre.png'; 
        } else {
            menuToggle3.src = '/static/imgs/FiltreA.png';
        }
        });
});





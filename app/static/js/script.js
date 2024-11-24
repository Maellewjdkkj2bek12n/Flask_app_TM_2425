console.log("Script bien chargé")

document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner l'image et le menu
        const menuToggle1 = document.getElementById('menu-toggle1');
        const menu1 = document.getElementById('menu1');

        // Ajouter un événement de clic à l'image
        menuToggle1.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu1.classList.toggle('hidden');

            if (menu1.classList.contains('hidden'))  {
                menuToggle1.src = 'http://localhost:5000/static/imgs/Settings.png' ; 
            } else {
                menuToggle1.src = 'http://localhost:5000/static/imgs/SettingsA.png' ;
            }
        });
});

document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner l'image et le menu
        const menuToggle2 = document.getElementById('menu-toggle2');
        const menu2 = document.getElementById('menu2');

        // Ajouter un événement de clic à l'image
        menuToggle2.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu2.classList.toggle('hidden');

        if (menu2.classList.contains('hidden'))  {
            menuToggle2.src = 'http://localhost:5000/static/imgs/Settings.png'; 
        } else {
            menuToggle2.src = 'http://localhost:5000/static/imgs/SettingsA.png';
        }
        });
});

document.addEventListener('DOMContentLoaded', () => {
        // Sélectionner l'image et le menu
        const menuToggle3 = document.getElementById('menu-toggle3');
        const menu3 = document.getElementById('menu3');

        // Ajouter un événement de clic à l'image
        menuToggle3.addEventListener('click', () => {
            // Basculer la classe "hidden" sur le menu
            menu3.classList.toggle('hidden');

        if (menu3.classList.contains('hidden'))  {
            menuToggle3.src = 'http://localhost:5000/static/imgs/Filtre.png'; 
        } else {
            menuToggle3.src = 'http://localhost:5000/static/imgs/FiltreA.png';
        }
        });
});
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

//pour changer les boutons quand on séléctionne une classe la partie uploade 
const uploadgrandsboutons = document.querySelectorAll('.uploadgrandsboutons');
    uploadgrandsboutons.forEach(button => {
      button.addEventListener('click', () => {
        button.classList.toggle('clicked');  // Ajoute ou enlève la classe "clicked"
      });
    });

//pour changer les boutons quand on séléctionne un type d'art à filtrer
const typeartboutons = document.querySelectorAll('.typeartboutons');
typeartboutons.forEach(button => {
  button.addEventListener('click', () => {
    button.classList.toggle('clicked');  // Ajoute ou enlève la classe "clicked"
  });
});

//pour les flash message plus beau
window.onload = function() {
    // Sélectionner tous les messages flash
    var flash = document.querySelectorAll('.flash');

    // Définir un délai de disparition en millisecondes (par exemple, 5 secondes)
    setTimeout(function() {
        flash.forEach(function(msg) {
            msg.style.display = 'none';  // Masquer le message
        });
    }, 2000); 
};


//pour enter la bio sans avior de bouton commit
document.getElementById("bio").addEventListener("keydown", function(event) {
    if (event.key === "Enter") {  
        event.preventDefault();   
        document.getElementById("bio").submit();  // Soumet le formulaire
    }
});
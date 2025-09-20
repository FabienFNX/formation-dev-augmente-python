// Gestion de la navigation entre les interfaces

function showNavigation() {
    document.getElementById('navigationMenu').style.display = 'block';
    document.getElementById('clientInterface').style.display = 'none';

    // Réinitialiser le formulaire et cacher les résultats
    const form = document.getElementById('loanForm');
    if (form) {
        form.reset();
    }

    const result = document.getElementById('result');
    const error = document.getElementById('error');
    if (result) result.style.display = 'none';
    if (error) error.style.display = 'none';
}

function showClientInterface() {
    document.getElementById('navigationMenu').style.display = 'none';
    document.getElementById('clientInterface').style.display = 'block';
}

function goToEmployeeInterface() {
    window.location.href = '/employee.html';
}

// Afficher la navigation au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    // Vérifier si on est sur la page principale
    if (window.location.pathname === '/' || window.location.pathname === '/index.html') {
        showNavigation();
    }
});
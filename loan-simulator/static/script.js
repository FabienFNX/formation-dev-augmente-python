document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('loanForm');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        hideMessages();

        const formData = new FormData(form);
        const loanRequest = {
            amount: parseFloat(formData.get('amount')),
            durationYears: parseInt(formData.get('duration')),
            annualInterestRate: parseFloat(formData.get('rate'))
        };

        const validation = validateInput(loanRequest);
        if (!validation.isValid) {
            const errorMessage = 'Erreurs de saisie :\n• ' + validation.errors.join('\n• ');
            showError(errorMessage);
            return;
        }

        try {
            const response = await fetch('/api/calculate-loan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(loanRequest)
            });

            if (!response.ok) {
                throw new Error('Erreur lors du calcul');
            }

            const result = await response.json();
            displayResult(result);
        } catch (error) {
            showError('Une erreur est survenue lors du calcul. Veuillez réessayer.');
            console.error('Error:', error);
        }
    });

    function validateInput(data) {
        const errors = [];

        if (!data.amount || data.amount <= 0) {
            errors.push('Le montant du prêt doit être supérieur à 0€');
        }

        if (!data.durationYears || data.durationYears <= 0) {
            errors.push('La durée du prêt doit être supérieure à 0 année');
        }

        if (data.annualInterestRate === null || data.annualInterestRate === undefined || data.annualInterestRate < 0) {
            errors.push('Le taux d\'intérêt doit être positif ou nul');
        }

        return {
            isValid: errors.length === 0,
            errors: errors
        };
    }

    function displayResult(result) {
        document.getElementById('loanAmount').textContent = formatCurrency(result.loanAmount);
        document.getElementById('monthlyPayment').textContent = formatCurrency(result.monthlyPayment);
        document.getElementById('totalInterest').textContent = formatCurrency(result.totalInterest);
        document.getElementById('totalCost').textContent = formatCurrency(result.totalCost);

        resultDiv.style.display = 'block';
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function showError(message) {
        // Convertir les \n en <br> pour l'affichage HTML
        errorDiv.innerHTML = message.replace(/\n/g, '<br>');
        errorDiv.style.display = 'block';
        errorDiv.scrollIntoView({ behavior: 'smooth' });
    }

    function hideMessages() {
        resultDiv.style.display = 'none';
        errorDiv.style.display = 'none';
    }

    function formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR'
        }).format(amount);
    }
});
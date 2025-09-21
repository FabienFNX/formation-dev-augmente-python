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

        if (!validateInput(loanRequest)) {
            showError('Veuillez vérifier vos données. Tous les champs sont obligatoires et doivent être positifs.');
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
        return data.amount > 0 &&
               data.durationYears > 0 &&
               data.annualInterestRate >= 0;
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
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
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
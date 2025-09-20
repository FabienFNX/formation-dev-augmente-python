# Formation Dev Augmenté - Python FastAPI

A comprehensive loan simulation and interest rate calculation system built with Python FastAPI.

## Architecture

This system consists of **two separate applications** working together:

1. **loan-simulator** (Port 8080) - Frontend application with loan calculation
2. **interest-rate-api** (Port 8081) - Interest rate calculation API

## Features

### Loan Simulator (Port 8080)
- **Web Frontend**: Interactive HTML/CSS/JavaScript interface for loan simulation
- **Loan Calculation**: Calculate monthly payments, total interest, and total cost
- **Real-time Results**: Instant calculation results with formatted currency display
- **API Documentation**: Available at `/docs`

### Interest Rate API (Port 8081)
- **Interest Rate Calculation**: Calculate personalized rates based on demographic and financial criteria
- **Category Management**: Comprehensive age and professional category definitions
- **Flexible Configuration**: Configurable rate modifiers and income thresholds
- **RESTful API**: Clean, well-documented REST endpoints
- **API Documentation**: Available at `/swagger-ui.html`

## Project Structure

```
formation-dev-augmente-python/
├── loan-simulator/                    # Frontend application (Port 8080)
│   ├── app/
│   │   ├── models.py                  # Loan calculation models
│   │   ├── routers/
│   │   │   └── loan.py                # Loan calculation endpoints
│   │   └── services/
│   │       └── loan_service.py        # Loan calculation logic
│   ├── main.py                        # Loan simulator app entry point
│   └── requirements.txt               # Dependencies
├── interest-rate-api/                 # API application (Port 8081)
│   ├── app/
│   │   ├── config.py                  # Configuration
│   │   ├── models.py                  # Interest rate models and enums
│   │   ├── routers/
│   │   │   └── interest_rate.py       # Interest rate endpoints
│   │   └── services/
│   │       └── interest_rate_service.py # Interest rate calculation logic
│   ├── main.py                        # Interest rate API entry point
│   └── requirements.txt               # Dependencies
├── start-loan-simulator.py            # Start script for loan simulator
├── start-interest-rate-api.py         # Start script for interest rate API
├── start-both.py                      # Start both applications
├── .env                               # Environment configuration
└── README.md                          # This file
```

## Installation

1. Install dependencies for both applications:
```bash
cd loan-simulator && pip install -r requirements.txt
cd ../interest-rate-api && pip install -r requirements.txt
```

2. Ensure static files are available in the `loan-simulator/static` directory for the frontend interface.

## Running the Applications

### Option 1: Start both applications at once
```bash
python start-both.py
```

### Option 2: Start applications separately

**Loan Simulator (Port 8080):**
```bash
python start-loan-simulator.py
```

**Interest Rate API (Port 8081):**
```bash
python start-interest-rate-api.py
```

### Option 3: Start from individual directories

**Loan Simulator:**
```bash
cd loan-simulator
python main.py
```

**Interest Rate API:**
```bash
cd interest-rate-api
python main.py
```

## Application URLs

- **Frontend**: http://localhost:8080
- **Loan API Docs**: http://localhost:8080/docs
- **Interest Rate API**: http://localhost:8081
- **Interest Rate API Docs**: http://localhost:8081/swagger-ui.html

## API Endpoints

### Loan Simulator (Port 8080)
- `GET /` - Frontend application (HTML/CSS/JS)
- `POST /api/calculate-loan` - Calculate loan details
- `GET /docs` - API documentation

### Interest Rate API (Port 8081)
- `POST /api/interest-rate/calculate` - Calculate interest rate
- `GET /api/interest-rate/categories/age` - Get age categories
- `GET /api/interest-rate/categories/professional` - Get professional categories
- `GET /api/interest-rate/config` - Get current configuration
- `GET /swagger-ui.html` - API documentation

## Configuration

The Interest Rate API uses a sophisticated rate calculation system:

### Base Configuration
- **Base Rate**: 1.5% (configurable foundation rate)

### Age-Based Modifiers
- **Young Adult (18-30 years)**: +0.2% (higher risk profile)
- **Adult (31-45 years)**: +0.0% (reference category)
- **Middle Aged (46-60 years)**: -0.1% (stable profile)
- **Senior (61+ years)**: +0.3% (higher risk considerations)

### Professional Category Modifiers
- **Employee (CDI)**: +0.0% (reference category)
- **Executive**: -0.2% (preferential rate)
- **Civil Servant**: -0.3% (most preferential rate)
- **Freelancer**: +0.4% (increased risk)
- **Retired**: +0.1% (slight increase)
- **Student**: +0.5% (higher risk profile)
- **Unemployed**: +0.8% (highest risk category)

### Income-Based Modifiers
- **Low Income (<2,000€)**: +0.3% (additional risk factor)
- **Medium Income (2,000-4,000€)**: +0.0% (reference)
- **High Income (4,000-8,000€)**: -0.1% (preferential)
- **Very High Income (>8,000€)**: -0.2% (most preferential)

## Technical Features

This FastAPI implementation provides:
- **Microservices Architecture**: Two independent, scalable applications
- **Modern Python Stack**: FastAPI, Pydantic, Uvicorn
- **Automatic Documentation**: OpenAPI/Swagger integration
- **Type Safety**: Full Pydantic model validation
- **CORS Support**: Cross-origin resource sharing enabled
- **Production Ready**: Structured for deployment and scaling

# Hands-on

## Hands-on #1

L'application Web doit permettre à un utilisateur de saisir des informations pour simuler le montant d'un prêt immobilier :
- La durée du prêt
- Le montant du prêt souhaité
- Le taux d'intérêt annuel du prêt

La partie IHM est déjà implémentée, vous devez développer l'api REST qui permettra de traiter les informations fournies par l'utilisateur et de lui retourner le coût de son prêt.

Exemple :
Pour un prêt présentant les caractéristiques suivantes :
- 15 ans
- 300 000€
- 5%
Le coût total du prêt est de 427 028€

## Hands-on #2

L'application web intègre un écran dédié pour un employé d'une agence bancaire,
Il doit pouvoir saisir une nouvelle simulation de crédit immobilier avec les éléments suivants : 
- Nom
- Prénom
- Catégorie d'âge
- Catégorie socio-professionnelle
- Revenu mensuel net
- La durée du prêt
- Le montant du prêt souhaité
Lorsqu'il clique sur calculer le taux va être déterminé à partir des informations obtenues depuis l'API REST qui est disponible dans le projet *interest-rate-api* et dont la description est disponible ici : http://localhost:8081/swagger-ui.html

## Hands-on #3

Réalisez les tests unitaires associés au loan-simulator en dépassant 80% de couverture de tests.

Utilisez les instructions/rules pour rédiger ces tests

## Hands-on #4

L'employé d'agence doit également pouvoir sauvegarder les éléments en base de données afin de pouvoir consulter la liste des dossiers de simulation de prêts qu'il a effectué. 

Pour cela vous pouvez vous appuyer sur le fichier de base de données SQL Lite *loan_simulator.db* et l'exemple de script SQL pour insérer les données *sample_data.sql*
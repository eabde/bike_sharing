# Test Suite per Bike Sharing App

Questa cartella contiene tutti i test per l'applicazione di bike sharing.

## Struttura dei Test

```
tests/
├── __init__.py                 # Package marker
├── conftest.py                 # Fixture condivise per tutti i test
├── test_auth.py               # Test autenticazione (login/register)
├── test_models.py             # Test modelli SQLAlchemy
├── test_biciclette.py         # Test API biciclette
├── test_stazioni.py           # Test API stazioni
├── test_services.py           # Test servizi business logic
├── test_api_integration.py    # Test di integrazione end-to-end
└── README.md                  # Questa documentazione
```

## Installazione Dipendenze

```bash
pip install -r requirements-test.txt
```

## Esecuzione Test

### Eseguire tutti i test
```bash
pytest tests/ -v
```

### Eseguire test specifici
```bash
# Test solo autenticazione
pytest tests/test_auth.py -v

# Test solo modelli
pytest tests/test_models.py -v

# Test solo API biciclette
pytest tests/test_biciclette.py -v
```

### Eseguire test con coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

### Eseguire test in modalità quiet
```bash
pytest tests/ -q
```

## Fixture Disponibili

Le fixture sono definite in `conftest.py` e disponibili per tutti i test:

- `test_app`: Applicazione Flask configurata per test con database SQLite in-memory
- `client`: Client di test Flask per chiamare le API
- `session`: Sessione database per test diretti sui modelli
- `sample_admin`: Admin di test pre-creato
- `sample_user`: Utente di test pre-creato
- `sample_bike`: Bicicletta di test pre-creata
- `sample_station`: Stazione di test pre-creata
- `sample_operation`: Operazione di test pre-creata

## Tipi di Test

### Test Unitari
- **test_models.py**: Testa i modelli SQLAlchemy in isolamento
- **test_services.py**: Testa la business logic dei servizi

### Test di Integrazione
- **test_auth.py**: Testa i flussi di autenticazione completi
- **test_biciclette.py**: Testa le API REST delle biciclette
- **test_stazioni.py**: Testa le API REST delle stazioni
- **test_api_integration.py**: Testa flussi end-to-end completi

## Configurazione Database Test

I test utilizzano un database SQLite in-memory che viene:
- Creato all'inizio di ogni test
- Popolato con le fixture necessarie
- Distrutto alla fine del test

Questo garantisce che ogni test sia isolato e non influenzi gli altri.

## Esempi di Utilizzo

### Test di una singola funzione
```python
def test_login_success(client, sample_user):
    response = client.post("/api/auth/login", 
                          json={"email": "mario@test.com", "password": "password123"})
    assert response.status_code == 200
```

### Test con setup personalizzato
```python
def test_multiple_bikes(client, session):
    from models import Bicicletta
    
    # Crea test data
    for i in range(3):
        bike = Bicicletta()
        session.add(bike)
    session.commit()
    
    # Test
    response = client.get("/api/biciclette")
    assert len(response.json["data"]) == 3
```

## Debugging Test

Per debug dettagliato:
```bash
pytest tests/test_auth.py::TestAuth::test_login_admin_success -v -s
```

Per fermarsi al primo errore:
```bash
pytest tests/ -x
```

## Contribuire

Quando aggiungi nuove funzionalità:
1. Scrivi i test per la nuova funzionalità
2. Assicurati che tutti i test esistenti passino
3. Mantieni una copertura del codice alta
4. Usa nomi descrittivi per i test
5. Documenta fixture complesse 
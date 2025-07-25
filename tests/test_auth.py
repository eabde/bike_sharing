# test_auth.py - Test per autenticazione (login e registrazione)
import pytest
import json


class TestAuth:
    """Test per le funzionalità di autenticazione"""

    def test_login_admin_success(self, client, sample_admin):
        """Test login admin con credenziali corrette"""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "admin@test.com", "password": "admin123"}),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert data["tipoUtente"] == "admin"
        assert data["message"] == "Login avvenuto con successo"
        assert "data" in data

    def test_login_user_success(self, client, sample_user):
        """Test login utente con credenziali corrette"""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "mario@test.com", "password": "password123"}),
            content_type="application/json"
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert data["tipoUtente"] == "user"
        assert data["message"] == "Login avvenuto con successo"
        assert "data" in data

    def test_login_invalid_credentials(self, client):
        """Test login con credenziali non valide"""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "nonexistent@test.com", "password": "wrongpass"}),
            content_type="application/json"
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Credenziali non valide. Riprova."

    def test_login_missing_data(self, client):
        """Test login con dati mancanti"""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "test@test.com"}),  # manca password
            content_type="application/json"
        )
        
        assert response.status_code == 500

    def test_register_new_user_success(self, client):
        """Test registrazione nuovo utente"""
        user_data = {
            "nome": "Luigi",
            "cognome": "Verdi",
            "email": "luigi@test.com",
            "numTelefono": "9876543210",
            "cartaCredito": "9876543210987654",
            "password": "newpassword123",
            "via": "Via Milano 2",
            "città": "Roma",
            "provincia": "RM",
            "regione": "Lazio"
        }
        
        response = client.post(
            "/api/auth/register",
            data=json.dumps(user_data),
            content_type="application/json"
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["message"] == "Registrazione avvenuta con successo!"
        assert "data" in data
        assert data["data"]["email"] == "luigi@test.com"

    def test_register_existing_user(self, client, sample_user):
        """Test registrazione utente già esistente"""
        user_data = {
            "nome": "Mario",
            "cognome": "Rossi",
            "email": "mario@test.com",  # email già esistente
            "numTelefono": "1234567890",
            "cartaCredito": "1234567890123456",
            "password": "password123",
            "via": "Via Roma 1",
            "città": "Milano",
            "provincia": "MI",
            "regione": "Lombardia"
        }
        
        response = client.post(
            "/api/auth/register",
            data=json.dumps(user_data),
            content_type="application/json"
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Utente già registrato"

    def test_register_missing_fields(self, client):
        """Test registrazione con campi mancanti"""
        incomplete_data = {
            "nome": "Test",
            "email": "test@test.com"
            # mancano molti campi richiesti
        }
        
        response = client.post(
            "/api/auth/register",
            data=json.dumps(incomplete_data),
            content_type="application/json"
        )
        
        assert response.status_code == 500  # Dovrebbe fallire per campi mancanti

    def test_login_wrong_password(self, client, sample_user):
        """Test login con password sbagliata"""
        response = client.post(
            "/api/auth/login",
            data=json.dumps({"email": "mario@test.com", "password": "wrongpassword"}),
            content_type="application/json"
        )
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Credenziali non valide. Riprova." 
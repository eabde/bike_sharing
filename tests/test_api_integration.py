# test_api_integration.py - Test di integrazione per le API
import pytest
import json


class TestAPIIntegration:
    """Test di integrazione per testare flussi completi"""

    def test_complete_user_flow(self, client):
        """Test flusso completo: registrazione -> login -> operazioni"""
        
        # 1. Registrazione utente
        user_data = {
            "nome": "TestUser",
            "cognome": "Integration", 
            "email": "test.integration@test.com",
            "numTelefono": "1234567890",
            "cartaCredito": "1234567890123456",
            "password": "testpass123",
            "via": "Via Test 1",
            "città": "TestCity",
            "provincia": "TC",
            "regione": "TestRegion"
        }
        
        register_response = client.post(
            "/api/auth/register",
            data=json.dumps(user_data),
            content_type="application/json"
        )
        
        assert register_response.status_code == 201
        register_data = json.loads(register_response.data)
        user_id = register_data["data"]["id"]
        
        # 2. Login utente
        login_response = client.post(
            "/api/auth/login",
            data=json.dumps({
                "email": "test.integration@test.com",
                "password": "testpass123"
            }),
            content_type="application/json"
        )
        
        assert login_response.status_code == 200
        login_data = json.loads(login_response.data)
        assert login_data["tipoUtente"] == "user"
        
        # 3. Verifica profilo utente
        profile_response = client.get(f"/api/utenti/{user_id}/profilo")
        assert profile_response.status_code == 200
        profile_data = json.loads(profile_response.data)
        assert profile_data["data"]["nome"] == "TestUser"

    def test_bike_and_station_workflow(self, client):
        """Test flusso biciclette e stazioni"""
        
        # 1. Crea una stazione
        station_data = {
            "numSlot": 10,
            "numBiciclette": 0,
            "via": "Via Test Station",
            "città": "TestCity",
            "provincia": "TC",
            "regione": "TestRegion"
        }
        
        station_response = client.post(
            "/api/stazioni",
            data=json.dumps(station_data),
            content_type="application/json"
        )
        
        assert station_response.status_code == 201
        station_data_response = json.loads(station_response.data)
        station_id = station_data_response["data"]["ID"]
        
        # 2. Crea alcune biciclette
        bike_ids = []
        for i in range(3):
            bike_response = client.post("/api/biciclette")
            assert bike_response.status_code == 201
            bike_data = json.loads(bike_response.data)
            bike_ids.append(bike_data["data"]["ID"])
        
        # 3. Verifica che tutte le biciclette siano presenti
        bikes_response = client.get("/api/biciclette")
        assert bikes_response.status_code == 200
        bikes_data = json.loads(bikes_response.data)
        assert len(bikes_data["data"]) == 3
        
        # 4. Verifica stato di una bicicletta
        bike_status_response = client.get(f"/api/biciclette/{bike_ids[0]}/status")
        assert bike_status_response.status_code == 200
        bike_status_data = json.loads(bike_status_response.data)
        assert bike_status_data["data"]["ID"] == bike_ids[0]

    def test_api_info_endpoint(self, client):
        """Test endpoint informativo API"""
        response = client.get("/api/info")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data["status"] == "success"
        assert "endpoints" in data
        assert "autenticazione" in data["endpoints"]
        assert "biciclette" in data["endpoints"]
        assert "stazioni" in data["endpoints"]

    def test_get_all_users_endpoint(self, client, sample_user):
        """Test endpoint per ottenere tutti gli utenti"""
        response = client.get("/api/utenti")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data["status"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["email"] == "mario@test.com"

    def test_user_operations_through_api(self, client, sample_user):
        """Test API operazioni utente"""
        user_id = sample_user.id
        
        response = client.get(f"/api/operazioni/utente/{user_id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"] == []  # Nessuna operazione inizialmente

    def test_error_handling_consistency(self, client):
        """Test che tutti gli endpoint gestiscano gli errori in modo consistente"""
        
        # Test endpoint inesistenti
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        
        # Test ID inesistenti
        endpoints_to_test = [
            "/api/biciclette/999/status",
            "/api/utenti/999/profilo",
            "/api/operazioni/utente/999"
        ]
        
        for endpoint in endpoints_to_test:
            response = client.get(endpoint)
            # Tutti dovrebbero gestire l'errore (status 400 o 404)
            assert response.status_code in [400, 404]
            
            data = json.loads(response.data)
            assert data["status"] == "error"
            assert "message" in data 
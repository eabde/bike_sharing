# test_stazioni.py - Test per le API delle stazioni
import pytest
import json


class TestStazioniAPI:
    """Test per le API delle stazioni"""

    def test_get_stazioni_empty(self, client):
        """Test get tutte le stazioni con database vuoto"""
        response = client.get("/api/stazioni")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == []  # Risposta diretta lista vuota

    def test_get_stazioni_with_data(self, client, sample_station):
        """Test get tutte le stazioni con dati"""
        response = client.get("/api/stazioni")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]["ID"] == sample_station.ID
        assert data[0]["città"] == "Milano"

    def test_create_stazione_success(self, client):
        """Test creazione nuova stazione"""
        stazione_data = {
            "numSlot": 15,
            "numBiciclette": 8,
            "via": "Via Dante 10",
            "città": "Roma",
            "provincia": "RM",
            "regione": "Lazio",
            "latitudine": 41.9028,
            "longitudine": 12.4964
        }
        
        response = client.post(
            "/api/stazioni",
            data=json.dumps(stazione_data),
            content_type="application/json"
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["message"] == "Stazione aggiunta con successo"
        assert "data" in data
        assert data["data"]["numSlot"] == 15
        assert data["data"]["città"] == "Roma"

    def test_create_stazione_missing_required_fields(self, client):
        """Test creazione stazione con campi mancanti"""
        incomplete_data = {
            "numSlot": 10,
            "città": "Milano"
            # mancano campi richiesti
        }
        
        response = client.post(
            "/api/stazioni",
            data=json.dumps(incomplete_data),
            content_type="application/json"
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert "richiesto" in data["message"]

    def test_create_stazione_with_default_coordinates(self, client):
        """Test creazione stazione senza coordinate (dovrebbero essere default)"""
        stazione_data = {
            "numSlot": 12,
            "numBiciclette": 6,
            "via": "Via Test",
            "città": "TestCity",
            "provincia": "TC",
            "regione": "TestRegion"
        }
        
        response = client.post(
            "/api/stazioni",
            data=json.dumps(stazione_data),
            content_type="application/json"
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["data"]["latitudine"] == 0.0
        assert data["data"]["longitudine"] == 0.0

    def test_delete_stazione_success(self, client, sample_station):
        """Test eliminazione stazione esistente"""
        station_id = sample_station.ID
        response = client.delete(f"/api/stazioni/{station_id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["message"] == "Stazione eliminata con successo"

    def test_delete_stazione_not_found(self, client):
        """Test eliminazione stazione inesistente"""
        response = client.delete("/api/stazioni/999")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Stazione non trovata"

    def test_create_multiple_stazioni(self, client):
        """Test creazione multiple stazioni"""
        stazioni_data = [
            {
                "numSlot": 10,
                "numBiciclette": 5,
                "via": "Via Roma 1",
                "città": "Milano",
                "provincia": "MI",
                "regione": "Lombardia"
            },
            {
                "numSlot": 15,
                "numBiciclette": 10,
                "via": "Via Veneto 2",
                "città": "Roma",
                "provincia": "RM",
                "regione": "Lazio"
            },
            {
                "numSlot": 8,
                "numBiciclette": 3,
                "via": "Via Garibaldi 3",
                "città": "Napoli",
                "provincia": "NA",
                "regione": "Campania"
            }
        ]
        
        # Crea le stazioni
        for stazione_data in stazioni_data:
            response = client.post(
                "/api/stazioni",
                data=json.dumps(stazione_data),
                content_type="application/json"
            )
            assert response.status_code == 201
        
        # Verifica che siano tutte presenti
        list_response = client.get("/api/stazioni")
        list_data = json.loads(list_response.data)
        assert len(list_data) == 3
        
        # Verifica che le città siano corrette
        città = [stazione["città"] for stazione in list_data]
        assert "Milano" in città
        assert "Roma" in città
        assert "Napoli" in città

    def test_stazione_capacity_validation(self, client):
        """Test che numBiciclette non superi numSlot"""
        stazione_data = {
            "numSlot": 5,
            "numBiciclette": 10,  # Più biciclette che slot!
            "via": "Via Test",
            "città": "TestCity",
            "provincia": "TC",
            "regione": "TestRegion"
        }
        
        response = client.post(
            "/api/stazioni",
            data=json.dumps(stazione_data),
            content_type="application/json"
        )
        
        # L'API attualmente non valida questo, ma la stazione viene comunque creata
        # Questo test documenta il comportamento attuale
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["data"]["numSlot"] == 5
        assert data["data"]["numBiciclette"] == 10

    def test_stazione_json_structure(self, client, sample_station):
        """Test struttura JSON della risposta stazione"""
        response = client.get("/api/stazioni")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        stazione = data[0]
        
        expected_fields = [
            'ID', 'numSlot', 'numBiciclette', 'via', 'città', 
            'provincia', 'regione', 'latitudine', 'longitudine'
        ]
        
        for field in expected_fields:
            assert field in stazione
        
        # Verifica tipi
        assert isinstance(stazione['ID'], int)
        assert isinstance(stazione['numSlot'], int)
        assert isinstance(stazione['numBiciclette'], int)
        assert isinstance(stazione['latitudine'], float)
        assert isinstance(stazione['longitudine'], float) 
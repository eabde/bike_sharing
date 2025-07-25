# test_biciclette.py - Test per le API delle biciclette
import pytest
import json


class TestBicicletteAPI:
    """Test per le API delle biciclette"""

    def test_get_biciclette_empty(self, client):
        """Test get tutte le biciclette con database vuoto"""
        response = client.get("/api/biciclette")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["data"] == []

    def test_get_biciclette_with_data(self, client, sample_bike):
        """Test get tutte le biciclette con dati"""
        response = client.get("/api/biciclette")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert len(data["data"]) == 1
        assert data["data"][0]["ID"] == sample_bike.ID

    def test_create_bicicletta_success(self, client):
        """Test creazione nuova bicicletta"""
        response = client.post("/api/biciclette")
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["status"] == "ok"
        assert data["message"] == "Bicicletta aggiunta con successo"
        assert "data" in data
        assert "ID" in data["data"]
        assert "codiceTag" in data["data"]

    def test_delete_bicicletta_success(self, client, sample_bike):
        """Test eliminazione bicicletta esistente"""
        bike_id = sample_bike.ID
        response = client.delete(f"/api/biciclette/{bike_id}")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert data["message"] == "Bicicletta eliminata con successo"

    def test_delete_bicicletta_not_found(self, client):
        """Test eliminazione bicicletta inesistente"""
        response = client.delete("/api/biciclette/999")
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Bicicletta non trovata"

    def test_get_bike_status_success(self, client, sample_bike):
        """Test get stato bicicletta esistente"""
        bike_id = sample_bike.ID
        response = client.get(f"/api/biciclette/{bike_id}/status")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "success"
        assert "data" in data
        assert data["data"]["ID"] == bike_id

    def test_get_bike_status_not_found(self, client):
        """Test get stato bicicletta inesistente"""
        response = client.get("/api/biciclette/999/status")
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data["status"] == "error"
        assert data["message"] == "Bicicletta non trovata"

    def test_biciclette_ordered_by_distance(self, client, session):
        """Test che le biciclette siano ordinate per distanza percorsa"""
        from models import Bicicletta
        
        # Crea biciclette con distanze diverse
        bici1 = Bicicletta()
        bici1.distanzaPercorsa = 10.0
        
        bici2 = Bicicletta()
        bici2.distanzaPercorsa = 25.0
        
        bici3 = Bicicletta()
        bici3.distanzaPercorsa = 5.0
        
        session.add_all([bici1, bici2, bici3])
        session.commit()
        
        response = client.get("/api/biciclette")
        
        assert response.status_code == 200
        data = json.loads(response.data)
        biciclette = data["data"]
        
        # Verifica che siano ordinate per distanza decrescente
        assert len(biciclette) == 3
        assert biciclette[0]["distanzaPercorsa"] == 25.0
        assert biciclette[1]["distanzaPercorsa"] == 10.0
        assert biciclette[2]["distanzaPercorsa"] == 5.0

    def test_create_multiple_biciclette(self, client):
        """Test creazione multiple biciclette"""
        responses = []
        for i in range(3):
            response = client.post("/api/biciclette")
            responses.append(response)
        
        # Verifica che tutte le creazioni siano riuscite
        for response in responses:
            assert response.status_code == 201
            data = json.loads(response.data)
            assert data["status"] == "ok"
        
        # Verifica che ci siano 3 biciclette nel database
        list_response = client.get("/api/biciclette")
        list_data = json.loads(list_response.data)
        assert len(list_data["data"]) == 3
        
        # Verifica che abbiano codiciTag diversi
        codici_tag = [bici["codiceTag"] for bici in list_data["data"]]
        assert len(set(codici_tag)) == 3  # tutti diversi 
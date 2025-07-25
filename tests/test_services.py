# test_services.py - Test per i servizi di business logic
import pytest
import json
from services import BikeRentalService, UserService


class TestBikeRentalService:
    """Test per BikeRentalService"""

    def test_get_user_operations_empty(self, session, sample_user):
        """Test get operazioni utente senza operazioni"""
        result = BikeRentalService.get_user_operations(sample_user.id)
        
        assert result["status"] == "success"
        assert result["data"] == []

    def test_get_user_operations_with_data(self, session, sample_operation):
        """Test get operazioni utente con dati"""
        user_id = sample_operation.idUtente
        result = BikeRentalService.get_user_operations(user_id)
        
        assert result["status"] == "success"
        assert len(result["data"]) == 1
        assert result["data"][0]["ID"] == sample_operation.ID
        assert result["data"][0]["tipo"] == "noleggio"

    def test_get_user_operations_nonexistent_user(self, session):
        """Test get operazioni utente inesistente"""
        result = BikeRentalService.get_user_operations(999)
        
        assert result["status"] == "success"
        assert result["data"] == []  # Nessuna operazione trovata

    def test_get_user_operations_multiple(self, session, sample_user, sample_bike, sample_station):
        """Test get operazioni multiple per stesso utente"""
        from models import Operazione
        
        # Crea multiple operazioni per lo stesso utente
        op1 = Operazione(
            tipo="noleggio",
            idUtente=sample_user.id,
            idBicicletta=sample_bike.ID,
            idStazione=sample_station.ID
        )
        
        op2 = Operazione(
            tipo="riconsegna",
            idUtente=sample_user.id,
            idBicicletta=sample_bike.ID,
            idStazione=sample_station.ID,
            distanzaPercorsa=10
        )
        
        session.add_all([op1, op2])
        session.commit()
        
        result = BikeRentalService.get_user_operations(sample_user.id)
        
        assert result["status"] == "success"
        assert len(result["data"]) == 2
        
        # Verifica che siano ordinate per ID decrescente (più recenti prima)
        assert result["data"][0]["ID"] > result["data"][1]["ID"]

    def test_get_bike_status_success(self, session, sample_bike):
        """Test get stato bicicletta esistente"""
        result = BikeRentalService.get_bike_status(sample_bike.ID)
        
        assert result["status"] == "success"
        assert result["data"]["ID"] == sample_bike.ID
        assert result["data"]["codiceTag"] == sample_bike.codiceTag

    def test_get_bike_status_not_found(self, session):
        """Test get stato bicicletta inesistente"""
        result = BikeRentalService.get_bike_status(999)
        
        assert result["status"] == "error"
        assert result["message"] == "Bicicletta non trovata"

    def test_get_bike_status_with_updated_position(self, session, sample_bike):
        """Test get stato bicicletta con posizione aggiornata"""
        # Aggiorna posizione bicicletta
        sample_bike.update_position(45.4642, 9.1900)
        sample_bike.add_distance(15.5)
        session.commit()
        
        result = BikeRentalService.get_bike_status(sample_bike.ID)
        
        assert result["status"] == "success"
        assert result["data"]["latitudine"] == "45.4642"
        assert result["data"]["longitudine"] == "9.1900"
        assert result["data"]["distanzaPercorsa"] == 15.5


class TestUserService:
    """Test per UserService"""

    def test_get_user_profile_success(self, session, sample_user):
        """Test get profilo utente esistente"""
        result = UserService.get_user_profile(sample_user.id)
        
        assert result["status"] == "success"
        assert result["data"]["id"] == sample_user.id
        assert result["data"]["nome"] == "Mario"
        assert result["data"]["email"] == "mario@test.com"

    def test_get_user_profile_not_found(self, session):
        """Test get profilo utente inesistente"""
        result = UserService.get_user_profile(999)
        
        assert result["status"] == "error"
        assert result["message"] == "Utente non trovato"

    def test_update_user_profile_success(self, session, sample_user):
        """Test aggiornamento profilo utente"""
        update_data = {
            "nome": "MarioAggiornato",
            "numTelefono": "9999999999",
            "via": "Via Nuova 123"
        }
        
        result = UserService.update_user_profile(sample_user.id, update_data)
        
        assert result["status"] == "success"
        assert result["message"] == "Profilo aggiornato con successo"
        assert result["data"]["nome"] == "MarioAggiornato"
        assert result["data"]["numTelefono"] == "9999999999"
        assert result["data"]["via"] == "Via Nuova 123"
        
        # Verifica che i campi non modificati rimangano uguali
        assert result["data"]["cognome"] == "Rossi"
        assert result["data"]["email"] == "mario@test.com"

    def test_update_user_profile_not_found(self, session):
        """Test aggiornamento profilo utente inesistente"""
        update_data = {"nome": "Test"}
        
        result = UserService.update_user_profile(999, update_data)
        
        assert result["status"] == "error"
        assert result["message"] == "Utente non trovato"

    def test_update_user_profile_partial_update(self, session, sample_user):
        """Test aggiornamento parziale profilo utente"""
        original_nome = sample_user.nome
        original_telefono = sample_user.numTelefono
        
        update_data = {
            "città": "Roma",  # Solo aggiorna città
        }
        
        result = UserService.update_user_profile(sample_user.id, update_data)
        
        assert result["status"] == "success"
        assert result["data"]["città"] == "Roma"
        
        # Verifica che gli altri campi non siano cambiati
        assert result["data"]["nome"] == original_nome
        assert result["data"]["numTelefono"] == original_telefono

    def test_update_user_profile_invalid_fields(self, session, sample_user):
        """Test aggiornamento con campi non aggiornabili"""
        update_data = {
            "nome": "Nuovo Nome",
            "email": "nuova@email.com",  # email non dovrebbe essere aggiornabile
            "password": "nuova_password",  # password non dovrebbe essere aggiornabile
            "invalid_field": "valore"  # campo inesistente
        }
        
        result = UserService.update_user_profile(sample_user.id, update_data)
        
        assert result["status"] == "success"
        assert result["data"]["nome"] == "Nuovo Nome"
        
        # Verifica che email e password non siano cambiati
        assert result["data"]["email"] == "mario@test.com"  # email originale
        
        # Il campo invalid_field dovrebbe essere ignorato silenziosamente

    def test_update_user_profile_all_updateable_fields(self, session, sample_user):
        """Test aggiornamento di tutti i campi aggiornabili"""
        update_data = {
            "nome": "NuovoNome",
            "cognome": "NuovoCognome",
            "numTelefono": "1111111111",
            "cartaCredito": "9999999999999999",
            "via": "Via Nuova",
            "città": "Nuova Città",
            "provincia": "NC",
            "regione": "Nuova Regione"
        }
        
        result = UserService.update_user_profile(sample_user.id, update_data)
        
        assert result["status"] == "success"
        
        # Verifica che tutti i campi siano stati aggiornati
        for field, value in update_data.items():
            assert result["data"][field] == value 
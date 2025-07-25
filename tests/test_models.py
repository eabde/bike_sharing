# test_models.py - Test per i modelli SQLAlchemy
import pytest
from models import Admin, Utente, Bicicletta, Stazione, Operazione


class TestAdmin:
    """Test per il modello Admin"""

    def test_admin_creation(self, session):
        """Test creazione admin"""
        admin = Admin(email="test@admin.com", password="testpass")
        session.add(admin)
        session.commit()
        
        assert admin.ID is not None
        assert admin.email == "test@admin.com"
        assert admin.password != "testpass"  # deve essere hashata

    def test_admin_check_password(self, session):
        """Test verifica password admin"""
        admin = Admin(email="test@admin.com", password="testpass")
        session.add(admin)
        session.commit()
        
        assert admin.check_password("testpass") is True
        assert admin.check_password("wrongpass") is False

    def test_admin_to_dict(self, sample_admin):
        """Test conversione admin a dizionario"""
        data = sample_admin.to_dict()
        
        assert "ID" in data
        assert "email" in data
        assert "password" not in data  # non deve esporre la password


class TestUtente:
    """Test per il modello Utente"""

    def test_utente_creation(self, session):
        """Test creazione utente"""
        utente = Utente(
            nome="Test",
            cognome="User",
            email="test@user.com",
            numTelefono="1234567890",
            cartaCredito="1234567890123456",
            password="testpass",
            via="Via Test",
            città="TestCity",
            provincia="TC",
            regione="TestRegion"
        )
        session.add(utente)
        session.commit()
        
        assert utente.id is not None
        assert utente.nome == "Test"
        assert utente.smartCard is not None
        assert len(utente.smartCard) == 8

    def test_utente_check_password(self, sample_user):
        """Test verifica password utente"""
        assert sample_user.check_password("password123") is True
        assert sample_user.check_password("wrongpass") is False

    def test_utente_generate_smart_card(self, session):
        """Test generazione smart card"""
        utente = Utente(
            nome="Test",
            cognome="User",
            email="test2@user.com",
            numTelefono="1234567890",
            cartaCredito="1234567890123456",
            password="testpass",
            via="Via Test",
            città="TestCity",
            provincia="TC",
            regione="TestRegion"
        )
        
        assert utente.smartCard is not None
        assert len(utente.smartCard) == 8
        assert utente.smartCard.isalnum()

    def test_utente_to_dict(self, sample_user):
        """Test conversione utente a dizionario"""
        data = sample_user.to_dict()
        
        expected_fields = [
            'id', 'nome', 'cognome', 'email', 'numTelefono', 
            'cartaCredito', 'smartCard', 'via', 'città', 'provincia', 'regione'
        ]
        
        for field in expected_fields:
            assert field in data
        
        assert "password" not in data  # non deve esporre la password


class TestBicicletta:
    """Test per il modello Bicicletta"""

    def test_bicicletta_creation(self, session):
        """Test creazione bicicletta"""
        bici = Bicicletta()
        session.add(bici)
        session.commit()
        
        assert bici.ID is not None
        assert bici.codiceTag is not None
        assert len(bici.codiceTag) == 6
        assert bici.gps is not None
        assert len(bici.gps) == 6
        assert bici.distanzaPercorsa == 0.0

    def test_bicicletta_update_position(self, sample_bike):
        """Test aggiornamento posizione bicicletta"""
        sample_bike.update_position(45.4642, 9.1900)
        
        assert sample_bike.latitudine == "45.4642"
        assert sample_bike.longitudine == "9.1900"

    def test_bicicletta_add_distance(self, sample_bike):
        """Test aggiunta distanza percorsa"""
        initial_distance = sample_bike.distanzaPercorsa
        sample_bike.add_distance(5.5)
        
        assert sample_bike.distanzaPercorsa == initial_distance + 5.5

    def test_bicicletta_to_dict(self, sample_bike):
        """Test conversione bicicletta a dizionario"""
        data = sample_bike.to_dict()
        
        expected_fields = ['ID', 'codiceTag', 'latitudine', 'longitudine', 'distanzaPercorsa', 'gps']
        
        for field in expected_fields:
            assert field in data


class TestStazione:
    """Test per il modello Stazione"""

    def test_stazione_creation(self, session):
        """Test creazione stazione"""
        stazione = Stazione(
            numSlot=20,
            numBiciclette=10,
            via="Via Test",
            città="TestCity",
            provincia="TC",
            regione="TestRegion",
            latitudine=45.0,
            longitudine=9.0
        )
        session.add(stazione)
        session.commit()
        
        assert stazione.ID is not None
        assert stazione.numSlot == 20
        assert stazione.numBiciclette == 10

    def test_stazione_to_dict(self, sample_station):
        """Test conversione stazione a dizionario"""
        data = sample_station.to_dict()
        
        expected_fields = [
            'ID', 'numSlot', 'numBiciclette', 'via', 'città', 
            'provincia', 'regione', 'latitudine', 'longitudine'
        ]
        
        for field in expected_fields:
            assert field in data


class TestOperazione:
    """Test per il modello Operazione"""

    def test_operazione_creation(self, session, sample_user, sample_bike, sample_station):
        """Test creazione operazione"""
        operazione = Operazione(
            tipo="noleggio",
            idUtente=sample_user.id,
            idBicicletta=sample_bike.ID,
            idStazione=sample_station.ID,
            distanzaPercorsa=0
        )
        session.add(operazione)
        session.commit()
        
        assert operazione.ID is not None
        assert operazione.tipo == "noleggio"
        assert operazione.data is not None
        assert operazione.ora is not None

    def test_operazione_to_dict(self, sample_operation):
        """Test conversione operazione a dizionario"""
        data = sample_operation.to_dict()
        
        expected_fields = [
            'ID', 'tipo', 'data', 'ora', 'distanzaPercorsa',
            'idUtente', 'idBicicletta', 'idStazione', 'tariffa'
        ]
        
        for field in expected_fields:
            assert field in data

    def test_operazione_relationships(self, sample_operation):
        """Test relazioni dell'operazione"""
        assert sample_operation.utente is not None
        assert sample_operation.bicicletta is not None
        assert sample_operation.stazione is not None
        
        assert sample_operation.utente.nome == "Mario"
        assert sample_operation.stazione.città == "Milano" 
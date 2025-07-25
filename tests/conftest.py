# conftest.py - Configurazione fixture per test pytest
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def test_app():
    """
    Restituisce l'istanza di Flask configurata per i test
    e con un database SQLite in-memory isolato.
    """
    # Importiamo qui dentro per non inizializzare subito il DB MySQL
    import app as app_module
    from models import Base

    # Motore di test in-memory
    engine = sa.create_engine("sqlite:///:memory:", future=True)
    TestingSession = sessionmaker(bind=engine)

    # Colleghiamo i metadati alla nuova engine
    Base.metadata.create_all(engine)

    # Monkey-patch: usiamo la nuova Session invece di quella MySQL
    app_module.Session = TestingSession
    
    # Monkey-patch anche nel modulo models e services
    import models
    import services
    models.Session = TestingSession
    services.Session = TestingSession

    # Attiviamo la modalità di test di Flask
    app_module.app.config.update(TESTING=True)

    yield app_module.app     # forniamo l'oggetto Flask ai test


@pytest.fixture()
def client(test_app):
    """Fornisce un test-client pronto all'uso (lifetime: function)."""
    return test_app.test_client()


@pytest.fixture()
def session(test_app):
    """Fornisce una sessione database per i test diretti sui modelli."""
    import models
    with models.Session() as session:
        yield session


@pytest.fixture()
def sample_admin(session):
    """Crea un admin di test nel database."""
    from models import Admin
    admin = Admin(email="admin@test.com", password="admin123")
    session.add(admin)
    session.commit()
    return admin


@pytest.fixture()
def sample_user(session):
    """Crea un utente di test nel database."""
    from models import Utente
    utente = Utente(
        nome="Mario",
        cognome="Rossi",
        email="mario@test.com",
        numTelefono="1234567890",
        cartaCredito="1234567890123456",
        password="password123",
        via="Via Roma 1",
        città="Milano",
        provincia="MI",
        regione="Lombardia"
    )
    session.add(utente)
    session.commit()
    return utente


@pytest.fixture()
def sample_bike(session):
    """Crea una bicicletta di test nel database."""
    from models import Bicicletta
    bici = Bicicletta()
    session.add(bici)
    session.commit()
    return bici


@pytest.fixture()
def sample_station(session):
    """Crea una stazione di test nel database."""
    from models import Stazione
    stazione = Stazione(
        numSlot=10,
        numBiciclette=5,
        via="Piazza Duomo 1",
        città="Milano",
        provincia="MI",
        regione="Lombardia",
        latitudine=45.4642,
        longitudine=9.1900
    )
    session.add(stazione)
    session.commit()
    return stazione


@pytest.fixture()
def sample_operation(session, sample_user, sample_bike, sample_station):
    """Crea un'operazione di test nel database."""
    from models import Operazione
    operazione = Operazione(
        tipo="noleggio",
        idUtente=sample_user.id,
        idBicicletta=sample_bike.ID,
        idStazione=sample_station.ID,
        distanzaPercorsa=0
    )
    session.add(operazione)
    session.commit()
    return operazione 
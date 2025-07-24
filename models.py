import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base, relationship
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import hashlib
import random
import string

# Configurazione database - seguendo l'esempio lista_spesa_orm.py
db = sa.create_engine("mysql+pymysql://root:root@localhost/noleggio_biciclette", echo=False, future=True)
Session = sessionmaker(bind=db)
Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admin'
    
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    password: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    
    def __init__(self, email, password):
        self.email = email
        self.password = hashlib.md5(password.encode()).hexdigest()
    
    def check_password(self, password):
        return self.password == hashlib.md5(password.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'ID': self.ID,
            'email': self.email
        }

class Utente(Base):
    __tablename__ = 'utenti'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    cognome: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    email: Mapped[str] = mapped_column(sa.String(32), nullable=False, unique=True)
    numTelefono: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    cartaCredito: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    smartCard: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    password: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    via: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    città: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    provincia: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    regione: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    
    # Relazioni
    operazioni = relationship('Operazione', back_populates='utente', lazy='select')
    
    def __init__(self, nome, cognome, email, numTelefono, cartaCredito, password, via, città, provincia, regione, smartCard=None):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.numTelefono = numTelefono
        self.cartaCredito = cartaCredito
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.via = via
        self.città = città
        self.provincia = provincia
        self.regione = regione
        self.smartCard = smartCard or self.generate_smart_card()
    
    def generate_smart_card(self):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    
    def check_password(self, password):
        return self.password == hashlib.md5(password.encode()).hexdigest()
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'cognome': self.cognome,
            'email': self.email,
            'numTelefono': self.numTelefono,
            'cartaCredito': self.cartaCredito,
            'smartCard': self.smartCard,
            'via': self.via,
            'città': self.città,
            'provincia': self.provincia,
            'regione': self.regione
        }

class Bicicletta(Base):
    __tablename__ = 'biciclette'
    
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codiceTag: Mapped[str] = mapped_column(sa.String(32), nullable=False, unique=True)
    latitudine: Mapped[str] = mapped_column(sa.String(32), default='0')
    longitudine: Mapped[str] = mapped_column(sa.String(32), default='0')
    distanzaPercorsa: Mapped[float] = mapped_column(sa.Float, default=0.0)
    gps: Mapped[str] = mapped_column(sa.String(16), nullable=False)
    
    # Relazioni
    operazioni = relationship('Operazione', back_populates='bicicletta', lazy='select')
    
    def __init__(self, codiceTag=None, gps=None):
        self.codiceTag = codiceTag or self.generate_random_string(6)
        self.gps = gps or self.generate_random_string(6)
        self.latitudine = '0'
        self.longitudine = '0'
        self.distanzaPercorsa = 0.0
    
    def generate_random_string(self, length):
        characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return ''.join(random.choices(characters, k=length))
    
    def update_position(self, latitudine, longitudine):
        self.latitudine = str(latitudine)
        self.longitudine = str(longitudine)
    
    def add_distance(self, distance):
        self.distanzaPercorsa += distance
    
    def to_dict(self):
        return {
            'ID': self.ID,
            'codiceTag': self.codiceTag,
            'latitudine': self.latitudine,
            'longitudine': self.longitudine,
            'distanzaPercorsa': self.distanzaPercorsa,
            'gps': self.gps
        }

class Stazione(Base):
    __tablename__ = 'stazioni'
    
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    numSlot: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    numBiciclette: Mapped[int] = mapped_column(sa.Integer, nullable=False)
    via: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    città: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    provincia: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    regione: Mapped[str] = mapped_column(sa.String(32), nullable=False)
    latitudine: Mapped[float] = mapped_column(sa.Float, nullable=False)
    longitudine: Mapped[float] = mapped_column(sa.Float, nullable=False)
    
    # Relazioni
    operazioni = relationship('Operazione', back_populates='stazione', lazy='select')
    
    def __init__(self, numSlot, numBiciclette, via, città, provincia, regione, latitudine=0.0, longitudine=0.0):
        self.numSlot = numSlot
        self.numBiciclette = numBiciclette
        self.via = via
        self.città = città
        self.provincia = provincia
        self.regione = regione
        self.latitudine = latitudine
        self.longitudine = longitudine
    
    def to_dict(self):
        return {
            'ID': self.ID,
            'numSlot': self.numSlot,
            'numBiciclette': self.numBiciclette,
            'via': self.via,
            'città': self.città,
            'provincia': self.provincia,
            'regione': self.regione,
            'latitudine': self.latitudine,
            'longitudine': self.longitudine
        }

class Operazione(Base):
    __tablename__ = 'operazioni'
    
    ID: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(sa.Enum('noleggio', 'riconsegna', name='tipo_operazione'), nullable=False)
    data: Mapped[datetime] = mapped_column(sa.Date, nullable=False, default=datetime.utcnow)
    ora: Mapped[datetime] = mapped_column(sa.Time, nullable=False, default=datetime.utcnow)
    distanzaPercorsa: Mapped[int] = mapped_column(sa.Integer, nullable=False, default=0)
    idUtente: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('utenti.id'), nullable=False)
    idBicicletta: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('biciclette.ID'), nullable=False)
    idStazione: Mapped[int] = mapped_column(sa.Integer, sa.ForeignKey('stazioni.ID'), nullable=False)
    tariffa: Mapped[int] = mapped_column(sa.Integer, nullable=True)
    
    # Relazioni
    utente = relationship('Utente', back_populates='operazioni')
    bicicletta = relationship('Bicicletta', back_populates='operazioni')
    stazione = relationship('Stazione', back_populates='operazioni')
    
    def __init__(self, tipo, idUtente, idBicicletta, idStazione, distanzaPercorsa=0, tariffa=None):
        self.tipo = tipo
        self.idUtente = idUtente
        self.idBicicletta = idBicicletta
        self.idStazione = idStazione
        self.distanzaPercorsa = distanzaPercorsa
        self.tariffa = tariffa
        self.data = datetime.utcnow().date()
        self.ora = datetime.utcnow().time()
    
    def to_dict(self):
        return {
            'ID': self.ID,
            'tipo': self.tipo,
            'data': self.data.isoformat() if self.data else None,
            'ora': self.ora.isoformat() if self.ora else None,
            'distanzaPercorsa': self.distanzaPercorsa,
            'idUtente': self.idUtente,
            'idBicicletta': self.idBicicletta,
            'idStazione': self.idStazione,
            'tariffa': self.tariffa
        }

# Crea le tabelle
Base.metadata.create_all(db) 
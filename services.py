from models import Session, Bicicletta, Operazione, Stazione, Utente


class BikeRentalService:
    """Servizio per gestire le operazioni di noleggio e riconsegna"""

    @staticmethod
    def get_user_operations(user_id):
        """Ottieni tutte le operazioni di un utente"""
        try:
            with Session() as session:
                operazioni = (
                    session.query(Operazione)
                    .filter_by(idUtente=user_id)
                    .order_by(Operazione.ID.desc())
                    .all()
                )
                return {
                    "status": "success",
                    "data": [op.to_dict() for op in operazioni],
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def get_bike_status(bike_id):
        """Ottieni lo stato di una bicicletta"""
        try:
            with Session() as session:
                bicicletta = session.query(Bicicletta).filter_by(ID=bike_id).first()
                if not bicicletta:
                    return {"status": "error", "message": "Bicicletta non trovata"}

                return {"status": "success", "data": bicicletta.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}


class UserService:
    """Servizio per gestire le operazioni degli utenti"""

    @staticmethod
    def get_user_profile(user_id):
        """Ottieni il profilo di un utente"""
        try:
            with Session() as session:
                utente = session.query(Utente).filter_by(id=user_id).first()
                if not utente:
                    return {"status": "error", "message": "Utente non trovato"}

                return {"status": "success", "data": utente.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    @staticmethod
    def update_user_profile(user_id, data):
        """Aggiorna il profilo di un utente"""
        try:
            with Session() as session:
                utente = session.query(Utente).filter_by(id=user_id).first()
                if not utente:
                    return {"status": "error", "message": "Utente non trovato"}

                # Aggiorna i campi forniti
                updateable_fields = [
                    "nome",
                    "cognome",
                    "numTelefono",
                    "cartaCredito",
                    "via",
                    "città",
                    "provincia",
                    "regione",
                ]

                for field in updateable_fields:
                    if field in data:
                        setattr(utente, field, data[field])

                session.commit()

                return {
                    "status": "success",
                    "message": "Profilo aggiornato con successo",
                    "data": utente.to_dict(),
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

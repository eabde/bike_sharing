from flask import Flask, request, jsonify
from models import Session, Admin, Utente, Bicicletta, Stazione, Operazione
from services import BikeRentalService, UserService
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, declarative_base
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

# ==================== API AUTENTICAZIONE ====================


@app.route("/api/auth/login", methods=["POST"])
def login():
    """Endpoint per il login di admin e utenti"""
    try:
        data = request.get_json()

        email = data["email"]
        password = data["password"]

        with Session() as session:
            # Controlla prima se è un admin
            admin = session.query(Admin).filter_by(email=email).first()
            if admin and admin.check_password(password):
                return (
                    jsonify(
                        {
                            "status": "ok",
                            "tipoUtente": "admin",
                            "message": "Login avvenuto con successo",
                            "data": admin.to_dict(),
                        }
                    ),
                    200,
                )

            # Controlla se è un utente normale
            utente = session.query(Utente).filter_by(email=email).first()
            if utente and utente.check_password(password):
                return (
                    jsonify(
                        {
                            "status": "ok",
                            "tipoUtente": "user",
                            "message": "Login avvenuto con successo",
                            "data": utente.to_dict(),
                        }
                    ),
                    200,
                )

        return (
            jsonify({"status": "error", "message": "Credenziali non valide. Riprova."}),
            401,
        )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/auth/register", methods=["POST"])
def register():
    """Endpoint per la registrazione di nuovi utenti"""
    try:
        data = request.get_json()

        required_fields = [
            "nome",
            "cognome",
            "email",
            "numTelefono",
            "cartaCredito",
            "password",
            "via",
            "città",
            "provincia",
            "regione",
        ]

        with Session() as session:
            # Controlla se l'utente esiste già
            existing_user = session.query(Utente).filter_by(email=data["email"]).first()
            if existing_user:
                return (
                    jsonify({"status": "error", "message": "Utente già registrato"}),
                    409,
                )

            # Crea nuovo utente
            nuovo_utente = Utente(
                nome=data["nome"],
                cognome=data["cognome"],
                email=data["email"],
                numTelefono=data["numTelefono"],
                cartaCredito=data["cartaCredito"],
                password=data["password"],
                via=data["via"],
                città=data["città"],
                provincia=data["provincia"],
                regione=data["regione"],
            )

            session.add(nuovo_utente)
            session.commit()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Registrazione avvenuta con successo!",
                        "data": nuovo_utente.to_dict(),
                    }
                ),
                201,
            )

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== API BICICLETTE ====================

@app.route("/api/biciclette", methods=["GET"])
def get_biciclette():
    """Ottieni tutte le biciclette"""
    try:
        with Session() as session:
            biciclette = (
                session.query(Bicicletta)
                .order_by(Bicicletta.distanzaPercorsa.desc())
                .all()
            )
            return (
                jsonify(
                    {
                        "status": "success",
                        "data": [bici.to_dict() for bici in biciclette],
                    }
                ),
                200,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/biciclette", methods=["POST"])
def create_bicicletta():
    """Crea una nuova bicicletta"""
    try:
        with Session() as session:
            nuova_bici = Bicicletta()
            session.add(nuova_bici)
            session.commit()

            return (
                jsonify(
                    {
                        "status": "ok",
                        "message": "Bicicletta aggiunta con successo",
                        "data": nuova_bici.to_dict(),
                    }
                ),
                201,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/biciclette/<int:bici_id>", methods=["PUT"])
def update_bicicletta(bici_id):
    """Aggiorna una bicicletta in base al movimento"""
    raise NotImplemented


@app.route("/api/biciclette/<int:bici_id>", methods=["DELETE"])
def delete_bicicletta(bici_id):
    """Elimina una bicicletta"""
    try:
        with Session() as session:
            bici = session.query(Bicicletta).filter_by(ID=bici_id).first()
            if not bici:
                return (
                    jsonify({"status": "error", "message": "Bicicletta non trovata"}),
                    404,
                )

            session.delete(bici)
            session.commit()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Bicicletta eliminata con successo",
                    }
                ),
                200,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== API STAZIONI ====================


@app.route("/api/stazioni", methods=["GET"])
def get_stazioni():
    """Ottieni tutte le stazioni"""
    try:
        with Session() as session:
            stazioni = session.query(Stazione).all()
            return jsonify([stazione.to_dict() for stazione in stazioni]), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/stazioni", methods=["POST"])
def create_stazione():
    """Crea una nuova stazione"""
    try:
        data = request.get_json()
        required_fields = [
            "numSlot",
            "numBiciclette",
            "via",
            "città",
            "provincia",
            "regione",
        ]

        for field in required_fields:
            if field not in data:
                return (
                    jsonify({"status": "error", "message": f"Campo {field} richiesto"}),
                    400,
                )

        with Session() as session:
            nuova_stazione = Stazione(
                numSlot=data["numSlot"],
                numBiciclette=data["numBiciclette"],
                via=data["via"],
                città=data["città"],
                provincia=data["provincia"],
                regione=data["regione"],
                latitudine=data.get("latitudine", 0.0),
                longitudine=data.get("longitudine", 0.0),
            )

            session.add(nuova_stazione)
            session.commit()

            return (
                jsonify(
                    {
                        "status": "success",
                        "message": "Stazione aggiunta con successo",
                        "data": nuova_stazione.to_dict(),
                    }
                ),
                201,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/stazioni/<int:stazione_id>", methods=["PUT"])
def update_stazione(stazione_id):
    """Aggiorna una stazione"""
    raise NotImplemented


@app.route("/api/stazioni/<int:stazione_id>", methods=["DELETE"])
def delete_stazione(stazione_id):
    """Elimina una stazione"""
    try:
        with Session() as session:
            stazione = session.query(Stazione).filter_by(ID=stazione_id).first()
            if not stazione:
                return (
                    jsonify({"status": "error", "message": "Stazione non trovata"}),
                    404,
                )

            session.delete(stazione)
            session.commit()

            return (
                jsonify(
                    {"status": "success", "message": "Stazione eliminata con successo"}
                ),
                200,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== API OPERAZIONI ====================


@app.route("/api/operazioni", methods=["POST"])
def create_operazione():
    """Crea una nuova operazione (noleggio o riconsegna)"""
    raise NotImplemented


@app.route("/api/operazioni/utente/<int:user_id>", methods=["GET"])
def get_user_operations(user_id):
    """Ottieni tutte le operazioni di un utente"""
    try:
        result = BikeRentalService.get_user_operations(user_id)

        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/biciclette/<int:bike_id>/status", methods=["GET"])
def get_bike_status(bike_id):
    """Ottieni lo stato di una bicicletta"""
    try:
        result = BikeRentalService.get_bike_status(bike_id)

        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== API UTENTI ====================


@app.route("/api/utenti/<int:user_id>/profilo", methods=["GET"])
def get_user_profile(user_id):
    """Ottieni il profilo di un utente"""
    try:
        result = UserService.get_user_profile(user_id)

        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/utenti/<int:user_id>/profilo", methods=["PUT"])
def update_user_profile(user_id):
    """Aggiorna il profilo di un utente"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "Dati richiesti"}), 400

        result = UserService.update_user_profile(user_id, data)

        if result["status"] == "success":
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/api/utenti", methods=["GET"])
def get_all_users():
    """Ottieni tutti gli utenti (solo per admin)"""
    try:
        with Session() as session:
            utenti = session.query(Utente).all()
            return (
                jsonify(
                    {
                        "status": "success",
                        "data": [utente.to_dict() for utente in utenti],
                    }
                ),
                200,
            )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ==================== ENDPOINT INFORMAZIONI ====================


@app.route("/api/info", methods=["GET"])
def get_api_info():
    """Endpoint informativo con tutte le API disponibili"""
    api_endpoints = {
        "status": "success",
        "message": "API Noleggio Biciclette - Backend Flask",
        "endpoints": {
            "autenticazione": {
                "POST /api/auth/login": "Login utente/admin",
                "POST /api/auth/register": "Registrazione nuovo utente",
            },
            "biciclette": {
                "GET /api/biciclette": "Lista tutte le biciclette",
                "POST /api/biciclette": "Crea nuova bicicletta",
                "DELETE /api/biciclette/<id>": "Elimina bicicletta",
                "GET /api/biciclette/<id>/status": "Stato bicicletta",
            },
            "stazioni": {
                "GET /api/stazioni": "Lista tutte le stazioni",
                "POST /api/stazioni": "Crea nuova stazione",
                "PUT /api/stazioni/<id>": "Aggiorna stazione",
                "DELETE /api/stazioni/<id>": "Elimina stazione",
            },
            "operazioni": {
                "POST /api/operazioni": "Crea operazione (noleggio/riconsegna)",
                "GET /api/operazioni": "Lista tutte le operazioni",
                "GET /api/operazioni/utente/<id>": "Operazioni di un utente",
            },
            "utenti": {
                "GET /api/utenti": "Lista tutti gli utenti",
                "GET /api/utenti/<id>/profilo": "Profilo utente",
                "PUT /api/utenti/<id>/profilo": "Aggiorna profilo utente",
            },
            "simulazione": {
                "POST /api/simulazione/<bike_id>": "Simula movimento GPS manuale"
            },
            "info": {"GET /api/info": "Informazioni API"},
        },
    }
    return jsonify(api_endpoints), 200


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5000)
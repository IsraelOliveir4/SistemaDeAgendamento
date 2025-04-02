import pytest
from app import app, db, Agendamento

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_homepage(client):
    response = client.get("/")
    assert response.status_code == 200

def test_criar_agendamento(client):
    response = client.post("/novo", data={
        "cliente": "João",
        "servico": "Corte de cabelo",
        "data": "2025-04-05",
        "horario": "14:00"
    }, follow_redirects=True)
    assert b"João" in response.data

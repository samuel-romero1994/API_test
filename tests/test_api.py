import sys
import os
import pytest
from app import create_app, db
from app.models import Item

# Añade el directorio raíz del proyecto al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    # Configuración para pruebas: base de datos en memoria
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_get_items_empty(client):
    response = client.get('/items/')
    assert response.status_code == 200
    assert response.json == []  # Espera una lista vacía

def test_create_item(client):
    response = client.post('/items/', json={'name': 'Item1', 'description': 'Description1'})
    assert response.status_code == 201
    assert response.json['name'] == 'Item1'

def test_get_items(client):
    client.post('/items/', json={'name': 'Item1', 'description': 'Description1'})
    response = client.get('/items/')
    assert response.status_code == 200
    assert len(response.json) == 1  # Accede directamente a la lista
    assert response.json[0]['name'] == 'Item1'

def test_update_item(client):
    post_response = client.post('/items/', json={'name': 'Item1', 'description': 'Description1'})
    item_id = post_response.json['id']
    put_response = client.put(f'/items/{item_id}', json={'name': 'Item1 Updated', 'description': 'Description1 Updated'})
    assert put_response.status_code == 200
    assert put_response.json['name'] == 'Item1 Updated'

def test_delete_item(client):
    post_response = client.post('/items/', json={'name': 'Item1', 'description': 'Description1'})
    item_id = post_response.json['id']
    delete_response = client.delete(f'/items/{item_id}')
    assert delete_response.status_code == 200
    assert delete_response.json['message'] == 'Item eliminado'  # Espera el mensaje en español

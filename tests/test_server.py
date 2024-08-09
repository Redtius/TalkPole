# import pytest
# from flask.testing import FlaskClient
# from main import app

# @pytest.fixture()
# def client() -> FlaskClient:
#   app.config['TESTING'] = True
#   with app.test_client() as client:
#       yield client

# def test_healthcheck(client):
#   response = client.get('/health')
#   assert response.status_code == 200
#   assert response.json == {'status': 'ok'}
  
# def test_index_get(client):
#   response = client.get('/')
#   assert response.status_code == 200
#   assert b'<!DOCTYPE html>' in response.data

# def test_index_post(client):
#   response = client.post('/', data={'textInput': 'je teste mon requete post'})
#   assert response.status_code == 200
#   assert b'<!DOCTYPE html>' in response.data
#   assert b'<div class="model-pred">' in response.data
  
# def test_docs(client):
#   response = client.get('/docs')
#   assert response.status_code == 200
#   assert b'<!DOCTYPE html>' in response.data
  
  
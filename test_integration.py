from fastapi.testclient import TestClient
from main import app
from database import create_db_and_tables
import os

# Configuração para usar um banco de dados em memória para o teste
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
create_db_and_tables()

client = TestClient(app)

def test_crud_flow():
    print("--- Teste de Fluxo CRUD de Usuários (TestClient) ---")
    
    # 1. POST - Criar Usuário (Sucesso)
    print("\n1. POST - Criar Usuário (Sucesso)")
    user_data = {
        "nome_usuario": "teste_user",
        "email": "teste@email.com",
        "senha": "Senha123" # Atende à validação (letra e número)
    }
    response = client.post("/usuarios", json=user_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 201
    created_user = response.json()
    assert created_user["email"] == user_data["email"]
    user_id = created_user["id"]
    print(f"Usuário criado com ID: {user_id}")

    # 2. POST - Criar Usuário (Falha - E-mail Duplicado)
    print("\n2. POST - Criar Usuário (Falha - E-mail Duplicado)")
    duplicate_data = {
        "nome_usuario": "outro_user",
        "email": "teste@email.com",
        "senha": "OutraSenha123"
    }
    response = client.post("/usuarios", json=duplicate_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 409 # CONFLICT
    assert "Já existe um usuário cadastrado com este email." in response.json()["detail"]

    # 3. POST - Criar Usuário (Falha - Validação de Senha)
    print("\n3. POST - Criar Usuário (Falha - Validação de Senha)")
    invalid_password_data = {
        "nome_usuario": "invalido",
        "email": "invalido@email.com",
        "senha": "apenasletras" # Falha na validação
    }
    response = client.post("/usuarios", json=invalid_password_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 422 # UNPROCESSABLE ENTITY (Pydantic Validation)
    
    # 4. GET - Buscar Usuário por ID (Sucesso)
    print(f"\n4. GET - Buscar Usuário por ID {user_id} (Sucesso)")
    response = client.get(f"/usuarios/{user_id}")
    print(f"Status: {response.status_code}")
    assert response.status_code == 200
    fetched_user = response.json()
    assert fetched_user["id"] == user_id
    
    # 5. PUT - Atualizar Usuário (Sucesso)
    print(f"\n5. PUT - Atualizar Usuário {user_id} (Sucesso)")
    updated_data = {
        "nome_usuario": "teste_user_updated",
        "email": "teste_updated@email.com",
        "senha": "NovaSenha123"
    }
    response = client.put(f"/usuarios/{user_id}", json=updated_data)
    print(f"Status: {response.status_code}")
    assert response.status_code == 200
    updated_user = response.json()
    assert updated_user["email"] == updated_data["email"]
    assert updated_user["nome_usuario"] == updated_data["nome_usuario"]
    
    # 6. DELETE - Deletar Usuário (Sucesso)
    print(f"\n6. DELETE - Deletar Usuário {user_id} (Sucesso)")
    response = client.delete(f"/usuarios/{user_id}")
    print(f"Status: {response.status_code}")
    assert response.status_code == 200
    deleted_user = response.json()
    assert deleted_user["id"] == user_id
    
    # 7. GET - Buscar Usuário por ID (Falha - Não Encontrado)
    print(f"\n7. GET - Buscar Usuário por ID {user_id} (Falha - Não Encontrado)")
    response = client.get(f"/usuarios/{user_id}")
    print(f"Status: {response.status_code}")
    assert response.status_code == 404 # NOT FOUND
    
    print("\n--- Teste CRUD de Usuários Concluído com Sucesso! ---")

if __name__ == "__main__":
    test_crud_flow()

# 1 - bibliotecas
import pytest       #engine / framework de teste de unidade
import requests     # framework de teste de API
import json         # leitor e escritor de arquivos json

# 2 - Classe (opcional no Python, em muitos casos)

# 2.1 - atributos ou variáveis

# consulta de resultado esperado
pet_id = 145063901              # código do animal
pet_name = "Snoopy"             # nome do animal
pet_category_id = 1             # código da categoria do animal
pet_category_name = "dog"       # título da categoria
pet_tag = 1                     # código do rótulo
pet_tag_name = "vacinado"       # título do rótulo

# informações em comum
url='https://petstore.swagger.io/v2/pet'
headers={ 'Content-Type':'application/json' }

# 2.2 - funções / métodos

def test_post_pet():
    # configura
    # dados de entrada estão no arquivo json
    pet=open('./fixtures/json/pet1.json')       # abre o arquivo json
    data=json.loads(pet.read())                 # ler o conteúdo e carrega como json em uma variável data
    # dados de saída / resultado esperado estão nos atributos acima das funções

    # executa
    response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data),
        timeout=5
    )

    # valida

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name

def test_get_pet():
    # Configura
    pet_status = "available"        # status do animal
    # Executa
    response = requests.get(
        url=f'{url}/{pet_id}',      # chama o endereço do get passando o código do animal
        headers=headers
        # não tem body
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['name'] == pet_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag
    assert response_body['status'] == pet_status

def test_put_pet():
    # Configura
    pet_status = "sold"        # stauts do animal

    # dados de entrada vem de um arquivo json
    pet=open('./fixtures/json/pet2.json')
    data = json.loads(pet.read())


    # Executa
    response = requests.put(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )

    # Valida
    response_body = response.json()

    assert response.status_code == 200
    assert response_body['id'] == pet_id
    assert response_body['name'] == pet_name
    assert response_body['category']['name'] == pet_category_name
    assert response_body['tags'][0]['name'] == pet_tag_name
    assert response_body['category']['id'] == pet_category_id
    assert response_body['tags'][0]['id'] == pet_tag
    assert response_body['status'] == pet_status

def test_delete_pet():
    # Configura

    #Executa
    response = requests.delete(
        url=f'{url}/{pet_id}',
        headers=headers,

    )

    # Valida

    response_body = response.json()

    assert response.status_code == 200
    assert response_body['code'] == 200
    assert response_body['type'] == 'unknown'
    assert response_body['message'] == str(pet_id)
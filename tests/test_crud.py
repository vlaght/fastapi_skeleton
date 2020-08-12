import math

common_values = {
    'name': 'Test Item',
    'price': 9.99,
    'is_offer': True,
}


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create(client):
    with client:
        response = client.post('/foo', json=common_values).json()

    assert response['name'] == common_values['name']
    assert response['price'] == common_values['price']
    assert response['is_offer'] == common_values['is_offer']


def test_read(client):
    bad_ids = [None, 'xxx', 5.5, 0, -1, []]
    with client:
        response = client.post('/foo', json=common_values).json()
        response = client.get('/foo/{}'.format(response['id'])).json()

        assert response['name'] == common_values['name']
        assert response['price'] == common_values['price']
        assert response['is_offer'] == common_values['is_offer']

        for id_ in bad_ids:
            response = client.get('/foo/{}'.format(id_))
            assert response.status_code == 422


def test_read_page(client):
    items_to_create = 26
    limit = 5
    initial_page = 1
    with client:
        for _ in range(items_to_create):
            response = client.post('/foo', json=common_values)

        response = client.get(
            f"/foo?page={initial_page}&limit={limit}"
        ).json()
        assert response['page'] == initial_page
        last_page = response['last_page']
        assert last_page == math.ceil(response['total']/limit)
        assert response['limit'] == limit
        assert len(response['items']) == limit

        response = client.get(
            f"/foo?page={last_page+1}&limit={limit}"
        )
        assert response.status_code == 404


def test_update(client):
    updated_values = {
        'name': 'change',
        'price': 1234.12,
        'is_offer': False,
    }
    with client:
        response = client.post('/foo', json=common_values).json()
        response = client.put(
            '/foo/{}'.format(response['id']),
            json=updated_values,
        ).json()

    assert response['name'] == updated_values['name']
    assert response['price'] == updated_values['price']
    assert response['is_offer'] == updated_values['is_offer']


def test_delete(client):
    with client:
        response = client.post('/foo', json=common_values).json()
        id_ = response['id']
        response = client.delete('/foo/{}'.format(id_),)
        assert response.status_code == 200

        response = client.get('/foo/{}'.format(id_))
        assert response.status_code == 404

from mscratch.httpclient import HttpClient, HttpClientParams
import pytest
import requests

@pytest.fixture
def client():
    params = HttpClientParams(headers=HttpClientParams.DEFAULT_UA)
    return HttpClient(params)

def test_httpclient_get_empty_url(client):
    with pytest.raises(requests.exceptions.MissingSchema):
        client.get(None)

def test_httpclient_get_invalid_url(client):
    with pytest.raises(requests.exceptions.MissingSchema):
        client.get('a.b.c')

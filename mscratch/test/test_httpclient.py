from mscratch.httpclient import HttpClient, HttpClientParams
from unittest.mock import Mock
import pytest
import requests

class ResponseMock:

    def __init__(self):
        self.content = 'mock_content'

        
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

        
def test_httpclient_post():
    params = HttpClientParams(headers={'foo': 'bar'}, timeout=10)
    client = HttpClient(params)
    requests.post = Mock(return_value=ResponseMock())

    response_content = client.post('http://example.org')
    requests.post.assert_called_with('http://example.org',
                                     headers={'foo': 'bar'},
                                     timeout=10,
                                     data=None)
    
    assert response_content == 'mock_content'

def test_httpclient_post_with_post_data(client):
    requests.post = Mock()
    
    client.post('http://example.org', data='payload')
    requests.post.assert_called_with('http://example.org',
                                     headers=HttpClientParams.DEFAULT_UA,
                                     timeout=HttpClientParams.DEFAULT_TIMEOUT,
                                     data='payload')


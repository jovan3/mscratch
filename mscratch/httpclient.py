import requests

class HttpClient:

    def __init__(self, http_params):
        ''' Wrapper class arount requests.get '''
        self.params = http_params

    def get(self, url):
        ''' Sends HTTP GET request.

        Parameters:
            url - <string> the URL where the HTTP GET request is sent

        Returns <string> containing the response content data.
        '''
        resp = requests.get(url, headers=self.params.headers, timeout=self.params.timeout)
        return resp.content

class HttpClientParams:
    ''' Class holding parameter values used by requests http clients. '''

    DEFAULT_UA = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 45.0) Gecko/20100101 Firefox/45.0'}

    def __init__(self, headers=None, timeout=40):
        '''
        Parameters:
            headers - <dict> HTTP request headers
            timeout - <int> timeout in seconds
        '''
        self.headers = headers
        self.timeout = timeout

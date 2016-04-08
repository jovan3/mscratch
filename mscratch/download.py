import requests
import hashlib
import os

from abc import ABCMeta, abstractmethod

class PageDownloader:
    ''' Uses HTTP client to request web page contents and save it to a file. '''

    def __init__(self, ddir):
        ''' Initialize PageDownloader.

        Parameters:
            dir - directory in which the downloaded page content is saved.
        '''
        self.dir = ddir
        self.create_dir()

    def save_file(self, contents, url):
        file_path = self.dir + '/' + hashlib.md5(url.encode('utf-8')).hexdigest()
        with open(file_path, 'w') as outfile:
            outfile.write(contents.decode('utf-8'))

    def download(self, url_gen, http_params, stop_on_exception=False):
        ''' Iterates the generate_url generator function of url_gen and downloads the
        contents of the pages of the generated URLs.

        Parameters:
            url_gen - <UrlGeneratorBase> URL generator used to generate download URLs.
        '''
        for url in url_gen.generate_url():
            resp = requests.get(url, headers=http_params.headers, timeout=http_params.timeout)
            self.save_file(resp.content, url)

    def create_dir(self):
        if not os.path.isdir(self.dir):
            os.makedirs(self.dir)

class HttpClientParams:
    ''' Class holding parameter values used by requests http clients. '''

    def __init__(self, headers=None, timeout=40):
        '''
        Parameters:
            headers - <dict> HTTP request headers
            timeout - <int> timeout in seconds
        '''
        self.headers = headers
        self.timeout = timeout

class UrlGeneratorBase(metaclass=ABCMeta):

    def __init__(self, url_str):
        self.url = url_str

    @abstractmethod
    def generate_url(self):
        ''' Implemented as generator method, yielding a string formatted with a tuple of parameters.
        The cardinality of the tuple depends on the implementation.
        '''
        pass

    @abstractmethod
    def get_current_value(self):
        ''' Returns string implementation of the current tuple used to format the URL sring.'''
        pass

class RangeUrlGenerator(UrlGeneratorBase):
    ''' URL generator class which uses a range to generate urls. '''
    def __init__(self, url, start, end, step=1):
        '''
        Parameters:
            start - <int> starting value of the range.
            end - <int> end value.

        Optional keyword parameters:
            step - <int>

        Raises ValueError if start >= end. Raises ValueError if step < 1.
        '''
        if start >= end:
            raise ValueError('start should be >= end.')
        if step < 1:
            raise ValueError('step should be > 0')

        self.start = start
        self.end = end
        self.step = step
        self.current = start
        super(RangeUrlGenerator, self).__init__(url)


    def generate_url(self):
        while self.current < self.end:
            yield self.url.format(str(self.current))
            self.current += self.step

    def get_current_value(self):
        return self.current

'''
if __name__ == '__main__':
    url = 'https://dubai.dubizzle.com/community/car-lift/?page={:s}&is_basic_search_widget=0&is_search=1&added__gte=1&car_lift_from=&car_lift_to=&ot=asc&o=2'
    r = RangeUrlGenerator(url, 1, 5)
    p = PageDownloader('zo')
    htp = HttpClientParams(headers={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv: 45.0) Gecko/20100101 Firefox/45.0'})
    p.download(r, htp)
'''

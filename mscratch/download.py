import hashlib
import os

from abc import ABCMeta, abstractmethod

class PageDownloader:
    ''' Uses HTTP client to request web page contents and save it to a file. '''

    def __init__(self, ddir, httpclient):
        ''' Initialize PageDownloader.

        Parameters:
            dir - directory in which the downloaded page content is saved.
            httpclient - mscratch.download.HttpClient object (requests.get wrapper)
        '''
        self.dir = ddir
        self.client = httpclient
        self.create_dir()

    def save_file(self, contents, url):
        file_path = self.dir + '/' + hashlib.md5(url.encode('utf-8')).hexdigest()
        with open(file_path, 'w') as outfile:
            outfile.write(contents.decode('utf-8'))

    def download(self, url_gen, stop_on_exception=False):
        ''' Iterates the generate_url generator function of url_gen and downloads the
        contents of the pages of the generated URLs.

        Parameters:
            url_gen - <UrlGeneratorBase> URL generator used to generate download URLs.
        '''
        for url in url_gen.generate_url():
            resp_data = self.client.get(url)
            self.save_file(resp_data, url)

    def create_dir(self):
        if not os.path.isdir(self.dir):
            if os.path.isabs(self.dir):
                os.makedirs(self.dir)
            else:
                os.makedirs(os.getcwd() + '/' + self.dir)



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

class ListUrlGenerator(UrlGeneratorBase):

    def __init__(self, url_list):
        self.url_list = url_list
        super(ListUrlGenerator, self).__init__(None)

    def generate_url(self):
        while len(self.url_list):
            yield self.url_list.pop()

    def get_current_value(self):
        return self.url_list[-1]

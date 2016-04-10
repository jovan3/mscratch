from unittest.mock import MagicMock
from mscratch.httpclient import HttpClient, HttpClientParams
from mscratch.download import PageDownloader, UrlGeneratorBase
import pytest
import os
import shutil
import hashlib

class TestUrlGenerator(UrlGeneratorBase):

    def generate_url(self):
        yield 'http://example.org'

    def get_current_value(self):
        return 'example'

TEST_DIR = 'testout'

@pytest.fixture
def pdown(request):
    httpparams = HttpClientParams(headers=HttpClientParams.DEFAULT_UA)
    httpclient = HttpClient(httpparams)
    httpclient.get = MagicMock(return_value='test value'.encode('utf-8'))
    def fin():
        shutil.rmtree(TEST_DIR)
    request.addfinalizer(fin)
    return PageDownloader(TEST_DIR, httpclient)

def test_page_download(pdown):
    url_gen = TestUrlGenerator('test')
    pdown.download(url_gen)
    test_dir_files = os.listdir(TEST_DIR)
    assert(len(test_dir_files)==1)
    # 'dab521de65f9250b4cca7383feef67dc' is md5 value of 'example'
    assert(test_dir_files[0] == 'dab521de65f9250b4cca7383feef67dc')

def test_create_dir():
    p = PageDownloader(TEST_DIR, None)
    assert(os.path.isdir(TEST_DIR))
    shutil.rmtree(TEST_DIR)

    p.dir = 'test1'
    p.create_dir()
    assert(os.path.isdir('test1'))
    shutil.rmtree('test1')

    abs_dir = os.getcwd() + '/test2'
    p.dir = abs_dir
    p.create_dir()
    assert(os.path.isdir(abs_dir))
    shutil.rmtree(abs_dir)

def test_save_file(pdown):
    url = 'testurl'
    url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
    pdown.save_file('test'.encode('utf-8'), url)

    assert(os.path.isfile(TEST_DIR + '/' + url_hash))

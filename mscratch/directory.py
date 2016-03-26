import requests
from lxml import html

class DirectoryLinkExtractor:
    ''' Extracts links of pages that contain data content. '''

    def __init__(self, url):
        self.url = url

    def get_page_tree(self):
        html_page = requests.get(self.url)
        return html.fromstring(html_page.content)

    def extract_links(self, xpath, base_url_append=True):
        ''' Returns list of href attribute values of elements described with an XPath. '''

        tree = self.get_page_tree()
        links = tree.xpath(xpath)

        if base_url_append:
            return [(self.url + link.attrib['href']) for link in links]

        return [link.attrib['href'] for link in links]

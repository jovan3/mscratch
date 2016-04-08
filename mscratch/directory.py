import requests
from lxml import html

class DirectoryLinkExtractor:
    ''' Extracts links of pages that contain data content. '''

    @staticmethod
    def request_page(url):
        return requests.get(url).content

    def get_page_tree(self, page_string):
        return html.fromstring(page_string)

    def extract_links(self, xpath, base_url_append=True, url=None, content=None):
        ''' Returns list of href attribute values of elements described with an XPath. '''
        if not url and not content:
            raise ValueError("Both url and content are None. At least one should have value other than None.")

        if content:
            tree = self.get_page_tree(content)
        else:
            page_string = DirectoryLinkExtractor.request_page(url)
            tree = self.get_page_tree(page_string)

        links = tree.xpath(xpath)

        if base_url_append:
            return [(url + link.attrib['href']) for link in links]

        return [link.attrib['href'] for link in links]

import re
import requests


def download_page_body(url):
    try:
        response = requests.get(url)
    except Exception as e:
        print('Something went wrong:', e)
        return
    return response.text


class Manager:
    def __init__(self, site_proto, site_dn):
        self.site_proto = site_proto
        self.site_dn - site_dn


class Page:
    LINK_PATTERN = re.compile(r'href="([%.\w/-]+)"')

    def __init__(self, site_addr, path):
        self.site_addr = site_addr
        self.path = path
        self.page_url = f'{site_addr}/{path}'
        self.is_visited = False
        self.links = []
        self.title = ''
        self.body = ''

    def __str__(self):
        return f'<class Page instance> {self.path}'

    def get_page_links(self):
        result = re.findall(self.LINK_PATTERN, self.body)
        if not result:
            print(f'No links found on page{self.path}')
        else:
            print(f'Found {len(result)} links on page {self.path}')
            self.links = result

    def get_page_body(self):
        self.body = download_page_body(self.page_url)

    def get_page_title(self):
        result = re.findall(self.LINK_PATTERN, self.body)
        if result:
            self.title = result[0]





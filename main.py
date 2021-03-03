import re
import requests

from config import USER_AGENT

HEADERS = {
    'User-Agent': USER_AGENT
}


def download_page_body(url):
    try:
        response = requests.get(url, HEADERS)
    except Exception as e:
        print('Something went wrong:', e)
        return
    return response.text


class Manager:
    def __init__(self):
        ...

    def add_site_to_be_parsed(self, site_root_addr):
        ...


class Task:
    def __init__(self, site_url):
        self.site_url = site_url

    def process_site(self):
        root_page = Page(self.site_url)
        root_page.process()
        root_page_links = root_page.links
        root_page_links_urls = root_page.get_links_urls()
        print(root_page_links_urls)

        root_page_links_to_be_followed = [link for link in root_page_links if link.should_follow()]
        root_page_links_urls_to_be_followed = set(link.url for link in root_page_links_to_be_followed)
        print(root_page_links_urls_to_be_followed)

class Page:
    LINK_PATTERN = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    TITLE_PATTERN = re.compile(r'<title>([\w\s-]+)</title>')

    def __init__(self, page_url):
        self.__body = ''
        self.page_url = page_url
        self.is_visited = False
        self.links = []
        self.title = ''


    def __str__(self):
        return f'<class Page instance> {self.__path}'

    def __get_page_links(self):
        if not self.body:
            print(f'Body of page {self.__path} is empty.')
            return

        result = re.findall(self.LINK_PATTERN, self.body)
        if not result:
            print(f'No links found on page{self.__path}')
        else:
            print(f'Found {len(result)} links on page {self.__path}')
            self.links = [Link(i) for i in result]

    def __get_page_body(self):
        self.body = download_page_body(self.page_url)

    def __get_page_title(self):
        if not self.body:
            print(f'Body of page {self.__path} is empty.')
            return

        result = re.findall(self.TITLE_PATTERN, self.body)
        if result:
            self.title = result[0]

    def process(self):
        self.__get_page_body()
        self.__get_page_title()
        self.__get_page_links()

    def get_links_urls(self):
        return tuple(link.url for link in self.links)


class Link:
    def __init__(self, url):
        self.url = url
        self.is_followed = False

    def __is_page(self):
        for ext in {'.css', '.js', '.jpg', '.jpeg', '.svg'}:
            if self.url.endswith(ext):
                return False

        if '/' not in self.url:
            return False

        return True

    def __is_internal_page(self):
        return 'dev.by' in self.url

    def should_follow(self):
        if self.is_followed or not self.__is_page():
            return False
        if not self.__is_internal_page():
            return False
        return True


manager = Manager()

task = Task('http', 'dev.by')
task.process_site()

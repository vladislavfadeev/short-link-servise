from bs4 import BeautifulSoup
from faker import Faker
from urllib.parse import urlparse
import requests


class Requester():
    faker = Faker()

    @staticmethod
    def extract_domain(url):
        parsed_url = urlparse(url)
        return parsed_url.netloc

    def __call__(self, url: str):
        headers = {'user-agent': self.faker.user_agent()}
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            return False, (
                'Сервер по указанному вами URL не отвечает. '
                'Убедитесь в правильности введенного адреса'
            )
        except requests.exceptions.HTTPError as e:
            return False, (
                f'Сервер по указанному вами URL ответил "{str(e)}". '
                'Убедитесь в правильности введенного адреса.'
            )
        else:
            page = BeautifulSoup(response.text, 'html.parser')
            if page.title:
                return True, page.title.string
            page_json = response.json()
            if page_json.get('title'):
                return True, page_json.get('title').capitalize()
            # domain = url.replace('//', '/').split('/')[1].capitalize()
            domain = self.extract_domain(url)
            return True, domain
        

requester = Requester()

# print(requester('https://github.com/jonra1993/fastapi-alembic-sqlmodel-async/blob/main/backend/app/app/deps/user_deps.py'))
import string
from typing import Dict, Optional
from random import randrange
import requests
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import os


class Extractor:
    def __init__(self, iterations: int):
        self.characters: str = string.ascii_lowercase + string.digits
        self.headers: Dict[str, str] = {
            'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        self.iterations = int(iterations)
        self.base_url: str = "https://prnt.sc/"
        self.assets_path: str = "assets"
        self.base_photo_name: str = 'photo'
        self.create_directory()

    def create_directory(self):
        if not os.path.isdir(self.assets_path):
            os.mkdir(self.assets_path)

    def generate_url(self, random_string: str) -> str:
        return self.base_url + random_string

    def generate_string(self) -> str:
        return f'{"".join([self.characters[randrange(len(self.characters))] for _ in range(6)])}'

    def get_image_url(self, url: str) -> Optional[str]:
        r = requests.request("GET", url, headers=self.headers)
        html_data = BeautifulSoup(r.text, 'html.parser')
        try:
            image = html_data.find_all('img', class_="no-click screenshot-image", src=True)[0]['src']
            return image
        except IndexError as e:
            pass

    def save_image(self, image_url: str, value: int):
        try:
            r = Request(image_url, headers=self.headers)
            webpage = urlopen(r).read()
            file_name = f"{self.base_photo_name}{value}.png"
            output = open(f"./{self.assets_path}/{file_name}", "wb")
            output.write(webpage)
            output.close()
        except FileExistsError as e:
            print("File already exists")
        except ValueError:
            pass
        except HTTPError:
            pass

    def run_loop(self):
        for value in range(1, self.iterations + 1):
            random_string = self.generate_string()
            print(random_string)
            url = self.generate_url(random_string)
            print(url)
            image_url = self.get_image_url(url)
            if image_url is not None:
                self.save_image(image_url, value)


if __name__ == '__main__':
    e = Extractor(100)
    e.run_loop()

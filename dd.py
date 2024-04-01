import re
from bs4 import BeautifulSoup
import requests

class Search_About_News:

    def get_links_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            links = file.readlines()
        return [link.strip() for link in links]

    def get_response(self, words, links):
        found_links = []
        for word in words:
            for link in links:
                url = f'{link}search?q={word}'
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    # تحديد النص بواسطة تعبير منتظم
                    target_pattern = re.compile(r'د\.العيسى يُعلن الإطلاق "التجريبي" للمتحف الدولي للسيرة النبويّة بأبراج الساعة')
                    for line in soup.stripped_strings:
                        if target_pattern.search(line):
                            parent_a = soup.find('a', string=line)
                            if parent_a and 'href' in parent_a.attrs:
                                found_links.append(parent_a['href'])
                                break

                else:
                    print(f"Failed to fetch {link}")
        return found_links

    def main(self):
        links = self.get_links_from_file('links.txt')
        found_links = self.get_response(words=[], links=links)
        print(f'The links were found in the following links:')
        print(found_links)

if __name__ == '__main__':
    bot = Search_About_News()
    bot.main()
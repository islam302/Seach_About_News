import chardet
import re
import requests
import pycountry
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import urlparse


class Search_About_News:

    def get_links_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            links = file.readlines()
        return [link.strip() for link in links]

    def get_words_from_file(self, words_file_path):
        with open(words_file_path, 'r', encoding='utf-8') as file:
            words = file.readlines()
        return [word.strip() for word in words]

    def get_response(self, words, links):
        found_in_links = []
        for word in words:
            for link in links:
                if link.startswith('https://'):
                    url = f'{link}search?q={word}'
                else:
                    url = f'https://{link}search?q={word}'
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    target_pattern = re.compile(
                        r'د\.العيسى يُعلن الإطلاق “التجريبي” للمتحف الدولي للسيرة النبويّة بأبراج الساعة')
                    for a_tag in soup.find_all('a', href=True):
                        if target_pattern.search(a_tag.get_text()):
                            found_in_links.append(a_tag['href'])
                            break
                else:
                    print(f"Failed to fetch {link}")
        return found_in_links

    def main(self):
        links = self.get_links_from_file('links.txt')
        words = self.get_words_from_file('news.txt')
        found_in_links = self.get_response(words, links)
        print(f'The words were found in the following links:')
        print(found_in_links)



if __name__ == '__main__':
    bot = Search_About_News()
    bot.main()


# #
# #     #
# #     #
# #     #
# #     #
# #     # # def search_for_word_in_google(self, word, arab_countries_google_urls):
# #     # #     for url in arab_countries_google_urls:
# #     # #         search_url = f'{url}search?q={word}'
# #     # #         try:
# #     # #             response = requests.get(search_url)
# #     # #             if response.status_code == 200:
# #     # #                 encoding = chardet.detect(response.content)['encoding']
# #     # #                 soup = BeautifulSoup(response.content.decode(encoding), 'html.parser')
# #     # #                 results = soup.find_all('a', href=True)
# #     # #                 for result in results:
# #     # #                     if 'url?q=' in result['href']:
# #     # #                         link = result['href'].split('url?q=')[1].split('&sa=')[0]
# #     # #                         if word in result.get_text():
# #     # #                             print(f'The word "{word}" was found in the following link:')
# #     # #                             print(link)
# #     # #                             break
# #     # #             else:
# #     # #                 print(f'Failed to fetch search results from {url}')
# #     # #         except:
# #     # #             print(f"Failed to fetch search results from {search_url}. Skipping...")
# #     # #             continue
# #     #
# #     # def main(self):
# #     #
# #     #     def get_countries_from_file(countries_file_path):
# #     #         with open(countries_file_path, 'r') as file:
# #     #             countries = file.readlines()
# #     #         return [country.strip() for country in countries]
# #     #
# #     #     def get_words_from_file(words_file_path):
# #     #         with open(words_file_path, 'r') as file:
# #     #             words = file.readlines()
# #     #         return [word.strip() for word in words]
# #     #
# #     #     def create_google_search_links(countries):
# #     #         google_links = []
# #     #         for country in countries:
# #     #             try:
# #     #                 country_obj = pycountry.countries.lookup(country)
# #     #                 zip_code = country_obj.alpha_2
# #     #                 google_links.append(f"https://www.google.com.{zip_code}/")
# #     #             except LookupError:
# #     #                 print(f"Country '{country}' not found. Skipping...")
# #     #                 continue
# #     #         return google_links
# #     #
# #     #     countries_file_path = 'countries.txt'
# #     #     words_file_path = 'news.txt'
# #     #     countries = get_countries_from_file(countries_file_path)
# #     #     words_to_check = get_words_from_file(words_file_path)
# #     #     # arab_countries_google_urls = create_google_search_links(countries)
# #     #
# #     #     self.list_of_links = self.get_links_from_file('links.txt')
# #     #     responses = self.get_response(self.list_of_links)
# #     #
# #     #
# #     #     # self.search_for_word_in_google('د.العيسى يُعلن الإطلاق “التجريبي” للمتحف الدولي للسيرة النبويّة بأبراج الساعة', arab_countries_google_urls)
#
#
# import requests
# from bs4 import BeautifulSoup
#
# class Search_About_News:
#
#     def get_links_from_file(self, file_path):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             links = file.readlines()
#         return [link.strip() for link in links]
#
#     def get_response(self, links):
#         found_links = []
#         for link in links:
#             response = requests.get(link)
#             if response.status_code == 200:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#                 # تقسيم النص إلى أسطر
#                 lines = soup.get_text().splitlines()
#                 target_text = 'د.العيسى يُعلن الإطلاق “التجريبي” للمتحف الدولي للسيرة النبويّة بأبراج الساعة'
#                 for line in lines:
#                     if target_text in line:
#                         parent_a = soup.find('a', string=line)
#                         if parent_a and 'href' in parent_a.attrs:
#                             found_links.append(parent_a['href'])
#                             break
#             else:
#                 print(f"Failed to fetch {link}")
#         return found_links
#
#     def main(self):
#         links = self.get_links_from_file('links.txt')
#         found_links = self.get_response(links)
#
# if __name__ == '__main__':
#     bot = Search_About_News()
#     bot.main()
#




# import re
# from bs4 import BeautifulSoup
# import requests
#
# class Search_About_News:
#
#     def get_links_from_file(self, file_path):
#         with open(file_path, 'r', encoding='utf-8') as file:
#             links = file.readlines()
#         return [link.strip() for link in links]
#
    # def get_response(self, words, links):
    #     found_links = []
    #     for link in links:
    #         response = requests.get(link)
    #         if response.status_code == 200:
    #             soup = BeautifulSoup(response.text, 'html.parser')
    #             # تحديد النص بواسطة تعبير منتظم
    #             target_pattern = re.compile(r'د\.العيسى يُعلن الإطلاق "التجريبي" للمتحف الدولي للسيرة النبويّة بأبراج الساعة')
    #             for line in soup.stripped_strings:
    #                 if target_pattern.search(line):
    #                     parent_a = soup.find('a', string=line)
    #                     if parent_a and 'href' in parent_a.attrs:
    #                         found_links.append(parent_a['href'])
    #                         break
    #
    #         else:
    #             print(f"Failed to fetch {link}")
    #     return found_links
#
#     def main(self):
#         links = self.get_links_from_file('links.txt')
#         found_links = self.get_response(words=[], links=links)
#         print(f'The links were found in the following links:')
#         print(found_links)
#
# if __name__ == '__main__':
#     bot = Search_About_News()
#     bot.main()




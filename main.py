import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import difflib
import pycountry
import chardet


class Search_About_News:

    def get_links_from_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            links = file.readlines()
        return [link.strip() for link in links if link.strip()]

    def get_words_from_file(self, words_file_path):
        with open(words_file_path, 'r', encoding='utf-8') as file:
            words = file.readlines()
        return list(set([word.strip() for word in words if word.strip()]))

    def get_response(self, words, links):
        found_links = {}
        for word in words:
            found_links[word] = []
            for link in links:
                response = requests.get(url)
                if response.status_code == 200:
                    print(link)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    target_pattern = re.compile(word)
                    for line in soup.stripped_strings:
                        if target_pattern.search(line):
                            parent_a = soup.find('a', string=line)
                            if parent_a and 'href' in parent_a.attrs:
                                found_links[word].append(parent_a['href'])
                                break
                    break
                else:
                    with open('links_need_to_done_manually.txt', 'a', encoding='utf-8') as file:
                        file.write(f'{link}\n')
        return found_links

    def get_countries_from_file(self, countries_file_path):
        with open(countries_file_path, 'r', encoding='utf-8') as file:
            return [country.strip() for country in file if country.strip()]

    def create_google_search_links(self, countries):
        google_links = []
        for country in countries:
            try:
                country_obj = pycountry.countries.lookup(country)
                zip_code = country_obj.alpha_2.lower()
                google_links.append(f"https://www.google.com.{zip_code}/")
            except LookupError:
                print(f"Country '{country}' not found. Skipping...")
        return google_links

    def search_and_get_links(self, query, num_results=10):
        try:
            search_results = search(query, num_results=num_results, lang='en')
            return list(search_results)
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def search_for_word_in_google(self, words, arab_countries_google_urls):
        result_links = {}
        for word in words:
            result_links[word] = []
            links_found = 0
            for url in arab_countries_google_urls:
                search_url = f'{url}search?q={word}'
                try:
                    response = requests.get(search_url)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        links = soup.find_all("a")
                        for link in links:
                            href = link.get("href")
                            if href.startswith("/url?q="):
                                result_links[word].append(href.replace("/url?q=", "").split("&sa=")[0])
                                links_found += 1
                                if links_found >= 10:
                                    break
                except requests.exceptions.RequestException as e:
                    print(f"An error occurred: {e}")
                    continue

        return result_links



    def main(self):
        words = self.get_words_from_file('news.txt')
        x = input('Start Task From Domains enter 1\nFrom Google enter 2\n')
        if x == '1':

            links = self.get_links_from_file('links.txt')
            found_links = self.get_response(words, links)
            df = pd.DataFrame.from_dict(found_links, orient='index').transpose()
            for col in df.columns:
                max_len = max([len(str(cell)) for cell in df[col]])
                width = max(50, max_len)
                df[col] = df[col].astype(str).str.pad(width, side='right')
            df.to_excel('found_links_From_Domains.xlsx', index=False)
            print(f'The links were found and saved in "found_links.xlsx".')

        else:
            countries = self.get_countries_from_file('countries.txt')
            searching_urls = self.create_google_search_links(countries)
            found = self.search_for_word_in_google(words, searching_urls)
            df = pd.DataFrame.from_dict(found, orient='index').transpose()
            if not df.empty:
                max_len = max([len(str(cell)) for col in df.columns for cell in df[col]])
                for col in df.columns:
                    max_len = max([len(str(cell)) for cell in df[col]])
                    width = max(50, max_len)
                    df[col] = df[col].astype(str).str.pad(width, side='right')
                df.to_excel('found_links_From_Google.xlsx', index=False)
                print(f'The links were found and saved in "found_links.xlsx".')
            else:
                print("No results found. No links were saved.")


if __name__ == '__main__':
    bot = Search_About_News()
    bot.main()


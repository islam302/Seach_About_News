from requests.packages.urllib3.exceptions import InsecureRequestWarning
from urllib.parse import quote, urlparse, urljoin, unquote
from ChromeDriver import WebDriver
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
import xlsxwriter
import requests
import chardet
import psutil
import urllib
import time
import sys
import re
import os



class Search_About_News:

    def __init__(self):
        self.driver = None
        self.current_dir = os.path.dirname(sys.argv[0])

    def start_driver(self):
        self.driver = WebDriver.start_driver(self)
        return self.driver

    def killDriverZombies(self, driver_pid):
        try:
            parent_process = psutil.Process(driver_pid)
            children = parent_process.children(recursive=True)
            for process in [parent_process] + children:
                process.terminate()
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    def get_words_from_file(self, words_file_path):
        try:
            with open(words_file_path, 'r', encoding='utf-8') as file:
                words = file.readlines()
            return list(set([word.strip() for word in words if word.strip()]))
        except:
            print(f'check file words.txt, domains.txt, search.txt not found')
            time.sleep(10)
            exit()

    def get_publish_date(self, link):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        try:
            response = requests.get(link)
            if response.status_code == 200:
                encoding = chardet.detect(response.content)['encoding']
                response.encoding = encoding
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')

                link_text = soup.get_text()
                date_match = re.search(r'\b\d{1,2}\s+\w+\s+\d{4}\b', link_text, re.IGNORECASE | re.UNICODE)
                if date_match:
                    link_date = date_match.group()
                    return link_date.strip()

                date_patterns = [
                    r'\b(\d{1,2}/\d{1,2}/\d{2,4})\b',
                    r'\b(\d{1,2}\s+\w+\s+\d{2,4})\b',
                    r'\b(\d{4}-\d{2}-\d{2})\b',
                    r'\b(\d{1,2}\s+\w+\s+\d{4})\b',
                    r'\b(\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{2,4})\b',
                    r'\b(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2})\b',
                    r'\b(\d{1,2}\s+\w+\s+/\s+\w+\s+\d{2,4})\b',
                    r'\b(\d{1,2}\s+\w+\s+\d{4}\s+\d{1,2}:\d{2})\b',
                    r'\b(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\b',
                    r'\b(\d{1,2}/\d{1,2}/\d{2,4}\s+\d{1,2}:\d{2}:\d{2})\b',
                    r'\b(\d{1,2}\s+\w+\s+\d{4}\s+\d{1,2}:\d{2}:\d{2})\b',
                    r'\b(\d{1,2}\s+[?-?]+\s+\d{4})\b',
                    r'\b(\d{1,2}/\d{1,2}/\d{2,4})\s+[?-?]+\s+\d{1,2}:\d{2}\b',
                    r'\b(\d{1,2}\s+[\u0623-\u064a]+\s+\d{4})\b',
                    r'\b(\d{1,2}\s+[\u0623-\u064a]+\s+/\s+[\u0623-\u064a]+\s+\d{2,4})\b',
                ]

                for pattern in date_patterns:
                    date_match = re.search(pattern, html_content, re.IGNORECASE | re.UNICODE)
                    if date_match:
                        link_date = date_match.group()
                        return link_date.strip()

                time_tags = soup.find_all('time', class_=re.compile(r'.*'))
                for time_tag in time_tags:
                    datetime_attr = time_tag.get('datetime')
                    if datetime_attr:
                        arabic_date = time_tag.text.strip()
                        return arabic_date

                link_date_match = re.search(r'(\d{4}-\d{2}-\d{2})', link)
                if link_date_match:
                    return link_date_match.group()

            return None
        except:
            return None

    def get_title(self, link):
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            response = requests.get(link)
            if response.status_code == 200:
                encoding = chardet.detect(response.content)['encoding']
                response.encoding = encoding
                html_content = response.text
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.title.string.strip()
                return title
        except:
            return None

    def get_searching_links(self, words, links, folder_path):
        found_links = {}
        not_working_links = []

        for word in words:
            found_links[word] = []
            links_found = 0
            for base_url in links:
                try:
                    encoded_word = quote(word)
                    response = requests.get(base_url + encoded_word)
                    response.raise_for_status()

                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, "html.parser")
                        search_results = soup.find_all(
                            "a") if base_url != 'https://search.yahoo.com/search?p=' else soup.find_all("div",
                                                                                                        class_="algo-sr")

                        for result in search_results:
                            if links_found >= 10:
                                break
                            link = result.find("a") if base_url == 'https://search.yahoo.com/search?p=' else result
                            if link:
                                href = link.get("href")
                                if href and (href.startswith("/url?q=") or href.startswith("http")):
                                    href = href.replace("/url?q=", "").split("&sa=")[0]
                                    if not href.startswith(('data:image', 'javascript', '#', 'https://maps.google')):
                                        found_links[word].append({'link': unquote(href)})
                                        links_found += 1

                except requests.exceptions.RequestException as e:
                    not_working_links.append(base_url)
                except AttributeError as e:
                    not_working_links.append(base_url)
        for word, links_info in found_links.items():
            for link_info in links_info:
                link = link_info['link']
                try:
                    date = self.get_publish_date(link)
                    link_info['date'] = date if date else 'not found'

                    title = self.get_title(link)
                    link_info['title'] = title if title else 'not found'
                except Exception as e:
                    print(f"Error processing link {link}: {e}")

        not_working_links_file = os.path.join(folder_path, 'not_working_links.txt')
        with open(not_working_links_file, 'w') as f:
            for link in not_working_links:
                f.write(f"{link}\n")

        return found_links

    def get_response(self, words, links, folder_path):
        found_links = {}
        not_working_links = []
        for word in words:
            found_links[word] = []
            screenshot_counter = 1
            for link in links:
                try:
                    match_link = False
                    quoted_word = quote(word)
                    URL = f'{link}{quoted_word}'
                    response = requests.get(URL)
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        all_links = soup.find_all('a', href=True)
                        search_url_parsed = urlparse(link)
                        domain = f'{search_url_parsed.scheme}://{search_url_parsed.netloc}'
                        for a_tag in all_links:
                            href = a_tag.get('href')
                            if href:
                                full_link = urljoin(domain, href)
                                if word.lower() in a_tag.get_text().lower():
                                    date = self.get_publish_date(full_link)
                                    found_links[word].append({'link': full_link, 'date': date})
                                    match_link = True
                                    break
                        if not match_link:
                            not_working_links.append(link)
                    else:
                        not_working_links.append(link)
                except:
                    not_working_links.append(link)
                    pass

            word_folder_path = os.path.join(folder_path, 'screenshots')
            os.makedirs(word_folder_path, exist_ok=True)

            self.start_driver()

            for link_data in found_links[word]:
                try:
                    screenshot_name = f'screenshot{str(screenshot_counter)}.png'
                    screenshot_path = os.path.join(word_folder_path, screenshot_name)
                    self.driver.get(link_data['link'])
                    time.sleep(1)
                    self.driver.save_screenshot(screenshot_path)
                    screenshot_counter += 1
                except:
                    pass

        not_working_links_file = os.path.join(folder_path, 'not_working_links.txt')
        try:
            with open(not_working_links_file, 'w') as f:
                for link in not_working_links:
                    f.write(f"{link}\n")
        except Exception as e:
            pass
        driver_pid = self.driver.service.process.pid
        self.killDriverZombies(driver_pid)

        return found_links

    def main1(self):
        words = self.get_words_from_file('words.txt')
        links = self.get_words_from_file('domains.txt')
        for word in tqdm(words, desc='Processing words', unit='word'):
            folder_name = f'{word}Task1'.replace(':', '-').replace('"', '')
            folder_path = os.path.join(self.current_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            found_links = self.get_response(words, links, folder_path)
            data = []
            for link_data_list in found_links.get(word, []):
                if not link_data_list:
                    data.append({'Link': link, 'Date': 'not found'})
                else:
                    if isinstance(link_data_list, dict):
                        link_data_list = [link_data_list]

                    for link_data in link_data_list:
                        data.append(
                            {'Link': f'=HYPERLINK("{link_data.get('link', 'not found')}")',
                             'Date': link_data.get('date', 'not found')})

            excel_path = os.path.join(folder_path, f'links_and_dates.xlsx')
            df = pd.DataFrame(data)
            writer = pd.ExcelWriter(excel_path, engine='xlsxwriter')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            cell_format = workbook.add_format({'font_color': 'blue', 'underline': True})
            worksheet.set_column('A:A', 10, cell_format)
            writer._save()

    def main2(self):
        links = self.get_words_from_file('search.txt')
        words = self.get_words_from_file('words.txt')
        for word in tqdm(words, desc='Processing words', unit='word'):
            folder_name = f'{word}Task2'.replace(':', '-').replace('"', '').encode('utf-8').decode('utf-8')
            folder_path = os.path.join(self.current_dir, folder_name)
            os.makedirs(folder_path, exist_ok=True)

            self.start_driver()
            found_links = self.get_searching_links(words, links, folder_path)
            driver_pid = self.driver.service.process.pid
            self.killDriverZombies(driver_pid)

            data = []
            for link_data_list in found_links.get(word, []):
                if not link_data_list:
                    data.append({'Link': 'not found', 'Date': 'not found', 'Title': 'not found'})
                else:
                    if isinstance(link_data_list, dict):
                        link_data_list = [link_data_list]

                    for link_data in link_data_list:
                        link = link_data.get('link', 'not found')
                        date = link_data.get('date', 'not found')
                        title = link_data.get('title', 'not found')
                        if date is None:
                            date = 'not found'
                        if title is None:
                            title = 'not found'
                        data.append({'Link': link, 'Date': date, 'Title': title})

            excel_path = os.path.join(folder_path, f'links_and_dates.xlsx')
            df = pd.DataFrame(data)
            df.to_excel(excel_path, index=False)


if __name__ == '__main__':
    bot = Search_About_News()
    run = input('Task1 or Task2 : ')
    if run == '1':
        try:
            bot.main1()
            print('mission complete')
            time.sleep(5)
        except:
            print('There is somthing wrong please try again')
            time.sleep(5)
    else:
        try:
            bot.main2()
            print('mission complete')
            time.sleep(5)
        except:
            print('There is somthing wrong please try again')
            time.sleep(5)









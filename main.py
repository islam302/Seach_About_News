# import requests
# from bs4 import BeautifulSoup
# from urllib.parse import urlparse
#
# def get_links_from_file(file_path):
#     with open(file_path, 'r') as file:
#         links = file.readlines()
#     return [link.strip() for link in links]
#
# list_of_links = get_links_from_file('links.txt')
#
# def get_response(links):
#     responses = []
#     for link in links:
#         url = f'{link}search/?q=حريق'
#         response = requests.get(url)
#         if response.status_code == 200:
#             responses.append(response.text)
#         else:
#             print(f"Failed to fetch {link}")
#     return responses
#
# def check_word(responses, word):
#     found_in = []
#     for idx, response in enumerate(responses):
#         lines = response.split('\n')
#         for line in lines:
#             if word in line:
#                 found_in.append(list_of_links[idx])
#                 break
#     return found_in
#
# responses = get_response(list_of_links)
# word_to_check = "حريق"
# found_in_links = check_word(responses, word_to_check)
#
# if found_in_links:
#     print(f'The word "{word_to_check}" was found in the following links:')
#     for link in found_in_links:
#         parsed_url = urlparse(link)
#         print(parsed_url.netloc)
#
# else:
#     print(f'The word "{word_to_check}" was not found in any of the links.')


import requests
from bs4 import BeautifulSoup

# List of Google search URLs for all 23 Arab countries
arab_countries_google_urls = [
    'https://www.google.dz/',   # Algeria
    'https://www.google.com.bh/',  # Bahrain
    'https://www.google.com.eg/',  # Egypt
    'https://www.google.iq/',   # Iraq
    'https://www.google.jo/',   # Jordan
    'https://www.google.co.ke/',  # Kenya
    'https://www.google.com.kw/',  # Kuwait
    'https://www.google.com.lb/',  # Lebanon
    'https://www.google.com.ly/',  # Libya
    'https://www.google.co.ma/',  # Morocco
    'https://www.google.com.ng/',  # Nigeria
    'https://www.google.com.om/',  # Oman
    'https://www.google.ps/',   # Palestine
    'https://www.google.com.qa/',  # Qatar
    'https://www.google.com.sa/',  # Saudi Arabia
    'https://www.google.co.za/',  # South Africa
    'https://www.google.co.tz/',  # Tanzania
    'https://www.google.tn/',   # Tunisia
    'https://www.google.ae/',   # United Arab Emirates
    'https://www.google.co.ug/',  # Uganda
    'https://www.google.co.zm/'   # Zambia
]

def search_for_word_in_google(word):
    for url in arab_countries_google_urls:
        search_url = f'{url}search?q={word}'
        response = requests.get(search_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('a', href=True)
            for result in results:
                if 'url?q=' in result['href']:
                    link = result['href'].split('url?q=')[1].split('&sa=')[0]
                    if word in result.get_text():
                        print(f'The word "{word}" was found in the following link:')
                        print(link)
                        break
        else:
            print(f'Failed to fetch search results from {url}')

search_for_word_in_google('حصار مستشفى الشفاء')



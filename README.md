# Seach_About_News

Your project, "News Attack," is a Python application with a graphical user interface (GUI) built using Tkinter and PyQt5. It aims to extract news-related information from search results for specific words and domains, saving the results in Excel files. Here's a breakdown of the key features and functionalities of your project:

GUI: The GUI allows users to select tasks (Task 1 and Task 2) to execute. It displays an image ("una.jpeg") at the top and two buttons for running Task 1 and Task 2.
Task Execution:
Task 1: Extracts news-related information based on words from a file and domains from another file. It saves the extracted links, dates, and titles in Excel files.
Task 2: Extracts news-related information based on words from a file and specific search URLs. It saves the extracted links, dates, and titles in Excel files.
Web Scraping: Uses BeautifulSoup and requests libraries to scrape web pages for news-related information. It extracts links, dates, and titles from the search results.
Data Processing: Processes the extracted data to ensure it meets specific criteria (e.g., checking for duplicate links, formatting dates).
Error Handling: Includes error handling for various scenarios, such as failed requests, to ensure the program continues running smoothly.
Driver Management: Manages the ChromeDriver for Selenium, allowing the program to interact with web pages and extract data using Selenium.
File Management: Creates folders and files to organize the extracted data, including a folder for screenshots of the extracted links.
Excel Export: Uses the pandas library to export the extracted data (links, dates, and titles) to Excel files, providing a structured format for further analysis.
Overall, "News Attack" provides a convenient way to extract and analyze news-related information from search results, automating the process and saving the results for further use.

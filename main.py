import requests
from bs4 import BeautifulSoup
from time import sleep
import csv

current_page = 0
BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BEngineer&location=Netherlands&geoId=102890719&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3681016782&position=3&pageNum=0&start={}".format(current_page)
page = requests.get(BASE_URL)
job_fields = {'role': None, 'company': None, 'posted': None, 'applicants': None, 'description': None}
roles_lines = []

def dict_to_csv(content):
    # Nome do arquivo CSV
    file_name = 'jobs_info.csv'

    # Open the CSV file for writing
    with open(file_name, 'w', newline='') as csv_file:
        # Set the CSV headers based on the keys of the first dictionary
        fields = content[0].keys()

        # Create a CSV writer
        writer = csv.DictWriter(csv_file, fieldnames=fields)

        # Write the header to the file
        writer.writeheader()

        # Write the data from the dictionaries in the list to the CSV file
        writer.writerows(content)


#while page.status_code == 200:
while current_page < 25:
    page = requests.get(BASE_URL)
    soup = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup.prettify(), "html.parser") 

    li_elements = soup2.find_all("li")
    jobs_urls = []

    for li_element in li_elements:
        a_element = li_element.find_all("a")
        if a_element:
            for a in a_element:
                href = a['href']
                if "/jobs/view/" in href:
                    jobs_urls.append(href)

    for job_url in jobs_urls:
        current_page = 0
        job_page = requests.get(job_url)
        soup_job_page = BeautifulSoup(job_page.content, "html.parser")
        soup_job_page2 = BeautifulSoup(soup_job_page.prettify(), "html.parser")     
        job_fields = {}    
        job_fields['role'] = soup_job_page2.find(class_='top-card-layout__title').get_text().strip()
        job_fields['company'] = soup_job_page2.find(class_='topcard__flavor').get_text().strip()
        job_fields['posted'] = soup_job_page2.find(class_='posted-time-ago__text').get_text().strip()
        job_fields['applicants'] = soup_job_page2.find(class_='num-applicants__caption').get_text().strip()
        description = soup_job_page2.find(class_='show-more-less-html__markup').get_text()
        description2 = ' '.join(description.split())
        job_fields['description'] = description2.strip()
        roles_lines.append(job_fields)
        sleep(1)
    current_page += 25
    BASE_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=Data%2BEngineer&location=Netherlands&geoId=102890719&trk=public_jobs_jobs-search-bar_search-submit&currentJobId=3681016782&position=3&pageNum=0&start={}".format(current_page)
    page = requests.get(BASE_URL)


dict_to_csv(roles_lines)
print("fim do programa.")



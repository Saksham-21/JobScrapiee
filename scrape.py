import requests
import csv
from bs4 import BeautifulSoup
import json



def fetch_job_data(job, place):
    job_data = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    url_template = 'https://internshala.com/jobs/{job}-jobs-in-{place}/page-{page}/'
    
    with requests.Session() as session:
        for page in range(1, 6):
            url = url_template.format(job=job, place=place, page=page)
            response = session.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            for item, itemm, items, itemi in zip(soup.find_all('div', class_='company'),
                                                      soup.find_all('div', class_='individual_internship_details'),
                                                      soup.find_all('div', class_='status'),
                                                      soup.find_all('div', class_='cta_container')):
                    linki = itemi.find('a')
                    href_value = linki.get('href')
                    f_link = f"https://internshala.com{href_value}"
                    anchors = item.find_all('a')
                    title = item.find('h3').text.strip()
                    company = item.find('p').text.strip()
                    spans = itemm.find_all('span')
                    location = spans[0].text.strip()
                    salary = spans[5].text.strip()
                    ies = items.find('i')
                    time_ago = ies.next_sibling.strip() if ies else None
                    job_data.append({'Title': title, 'Company': company, 'Location': location,
                                     'Salary': salary, 'Time_ago': time_ago, 'Link': f_link})
    return job_data   




def save_to_csv(job_data, filename='job_data.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Company', 'Location', 'Salary', 'Time_ago', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for job in job_data:
            writer.writerow(job)    
import requests
import csv
from bs4 import BeautifulSoup
import json



def fetch_job_data(job,place):
    job_data = []
    def extract(page):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        url = f'https://internshala.com/jobs/{job}-jobs-in-{place}/page-{page}/'
        r = requests.get(url, headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    for page in range(1, 6):
        soup = extract(page)
        divs = soup.find_all('div', class_='company')
        divvs = soup.find_all('div',class_='individual_internship_details')
        divss = soup.find_all('div', class_='status')
        linkk = soup.find_all('div', class_='cta_container')

        for item, itemm, items, itemi in zip(divs, divvs, divss,linkk):
            linki=itemi.find('a')
            href_value = linki.get('href')
            f_link="https://internshala.com"+href_value
            anchors = item.find_all('a')
            if len(anchors) >= 2:
                title = anchors[0].text.strip()
                company = anchors[1].text.strip()

                spans = itemm.find_all('span')
                location = spans[0].text.strip()
                salary = spans[4].text.strip()

                ies = items.find('i')
                if ies:
                    time_ago = ies.next_sibling.strip()

                job_data.append({'Title': title, 'Company': company,'Location':location,'Salary':salary,'Time_ago':time_ago,'Link':f_link})
    return job_data    




def save_to_csv(job_data, filename='job_data.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Title', 'Company', 'Location', 'Salary', 'Time_ago', 'Link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for job in job_data:
            writer.writerow(job)    
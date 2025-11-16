import re
from datetime import datetime
import json
import requests
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

def clear_skill(skill) -> list:
    new_skills = []
    separators = '|;/'
    for separator in separators:
        skill = skill.replace(separator, ',')
    for s in skill.split(','):
        new_skills.append(s.strip())
    return new_skills

def extract_with_bs4(job_link, jobid, keyword, jobdata, tools_list, job_title, failed_jobs):
    print("** Scraping job details:", job_link)
    try:
        response = requests.get(job_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # eskirgan jobni aniqlash va o'tkazib yuborish
        if soup.find('p', {'data-qa': 'alert-expired-job'}):
            print("IGNORED: Expired job")
            return


        description = soup.find('div', class_="job-description_jobDescription__26ney").text
        location = soup.find('li',  {'data-qa': 'job-location'}).text
        salary = soup.find('li',  {'data-qa': 'job-salary'}).text.replace("Not specified", "")

        # skills agar mavjud bo'lsa skills_item lardan olinadi
        skills = [skill.text for skill in soup.find_all('li', class_="skills_item__s027g")]
        skill_list = []
        for skill in skills:
            skill_list.extend(clear_skill(skill))

        # aniqlik uchun descriptiondan ham skillar qaraladi
        cleaned_text = re.sub(r'<.*?>', '', description)
        for skill in tools_list:
            if re.search(rf'\b{re.escape(skill)}\b', cleaned_text, re.IGNORECASE) and skill not in skills:
                skill_list.extend(clear_skill(skill))
        skills = ', '.join(skill_list)

        posted_date = soup.find('script', id="__NEXT_DATA__").text
        posted_date_index = posted_date.find('createdDate') + len("createdDate") + 3
        posted_date = posted_date[posted_date_index:posted_date_index+16]
        posted_date = datetime.strptime(posted_date, "%Y-%m-%dT%H:%M").strftime("%m/%d/%Y %I:%M")

        # logoni olish
        logo = soup.find('img', {'data-qa': 'company-logo-image'})
        if logo:
            logo = logo.attrs.get('srcset', False)
            logo = logo.split('1x')[0]
        else:
            logo = "No logo available"
        
        company_name_index = soup.find('div', {"data-qa": "job-posted-by"}).text.find("by") + 3
        company_name = soup.find('div', {"data-qa": "job-posted-by"}).text[company_name_index:]

        job_entry = {
                "Posted_date": posted_date,
                "Job Title from List": keyword,
                "Job Title": job_title,
                "Company": company_name,
                "Company Logo URL": logo,
                "Country": "UK",
                "Location": location,
                "Skills": skills,
                "Salary Info": salary,
                "Source": 'reed.co.uk'
            }
        jobdata.append(job_entry)
    except Exception as e:
        print('BS4 error :', e)
        new_failed_job = {
            "jobid": jobid,
            "job_title_from_list": keyword,
            "job_title": job_title,
            "fail_cause": e
        }
        failed_jobs.append(new_failed_job)
from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import re
from urllib.parse import urlparse, parse_qs 
from scroller import scrolling
import time

def extract_job_id(url):
    match = re.search(r'/(\d+)\?', url)
    if match:
        return match.group(1)
    return None

def getinfo(driver, alldata, keyword):
    time.sleep(5)
    try:
        while True:
            try:
                notfound = driver.find_element(By.XPATH, "//h2[text()='No jobs found']")
                print("** NO JOBS FOUND")
                break
            except NoSuchElementException as e:
                pass
            except Exception as e:
                print(f"** Enother error({keyword}):", e)
            
            try:
                # wait up to 10s for at least one job card to appear
                wait = WebDriverWait(driver, 10)
                
                job_cards = wait.until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.job-card_jobCard__MkcJD'))
                )
                # job_cards = driver.find_elements(By.CLASS_NAME, "job-card_jobCard__MkcJD")
            except Exception as e:
                print("NO JOBS FOUND for this keys:", keyword)
                break
            if not job_cards:
                print("NO JOBS FOUND for this keys:", keyword)
                break

            for job_card in job_cards:
                title_a = job_card.find_element(By.CSS_SELECTOR, "a.job-card_jobTitle__HORxw")
                print("----------------------------------")
                print("Checking job:", title_a.text)
                ignored = False
                for ignoring_selector in [".index-module_label__featured__Eldps", ".index-module_label__promoted__xiAWL"]:
                    try:
                        featured = job_card.find_element(By.CSS_SELECTOR, ignoring_selector)
                        print("IGNORED: Promoted or Featured")
                        ignored = True
                        break
                    except NoSuchElementException as e:
                        pass
                    except Exception as e:
                        print("Error checking for ignore", job_title    )
                if ignored: continue

                try:
                    job_title = title_a.text
                    link = title_a.get_attribute("href")
                    id = extract_job_id(link)
                    if not any(entry['jobid'] == id for entry in alldata):
                        alldata.append({"keyword": keyword, "jobid":id, "job_link": link, "job_title": job_title})
                        print("Job is valid: ", {"keyword": keyword, "jobid":id, "job_link": link, "job_title": job_title})
                    else:
                        print("This job has already taken")
                except Exception as e:
                    print(f"Error extracting link: {e}")
            print("-------------------------------")            
            if not nextpage(driver):
                break 
                

    except Exception as e:
        print(f"An error occurred: {e}")
        
        
def nextpage(driver):
    try:

        next_button_li = driver.find_element(By.XPATH, "//li[contains(@class, 'page-item') and a[@class='page-link next']]")
        if "disabled" in next_button_li.get_attribute("class"):
            print("Next button is disabled. No more pages.")
            return False

        scrolling(driver)

        next_button = next_button_li.find_element(By.TAG_NAME, "a")

        next_page_url = next_button.get_attribute("href")
        next_page_parsed = urlparse(next_page_url)
        next_page_query = parse_qs(next_page_parsed.query)
        next_page_no = next_page_query.get("pageno", [None])[0]

        # click next btn
        driver.execute_script("arguments[0].click();", next_button)

        print(f"Navigated to the next {next_page_no} page.")
        return True
    except Exception as e:
        print("Error navigating to the next page:", e)
        return False
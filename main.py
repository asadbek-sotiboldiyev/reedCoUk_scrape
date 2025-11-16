from dotenv import load_dotenv

from websitefilter import applytimerange, searching
import time
from firstdataextraction import getinfo
from specificdata import extractspecificinfohtml, extractspecificinfo, extract_with_bs4
from aititlefilter import filtercolumns
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from savetodatabase import savetodb, failed_jobs_log
import pyodbc

from dotenv import load_dotenv

import sys
from datetime import datetime

log_file_date = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

# txt faylga Log yozish
# original_std_out = sys.stdout
# sys.stdout = open(log_file_date + "_log.txt", 'w', encoding="utf-8")
# sys.stderr = open(log_file_date + "_log.txt", 'w', encoding="utf-8")


print("App starting..")
load_dotenv()

options = Options()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--ignore-ssl-errors")


tools_list = list({".NET", "Adobe XD", "Airflow", "Alamofire", "Alexa Skills Kit", "Amplify", "Ansible", "Apache", "Apache Kafka",
     "Apache Airflow", "Apache Nifi", "Apache NiFi", "Apache Storm", "AppDynamics", "Argo", "Asana", "Athena", "AWS",
     "AWS SageMaker", "Azure", "Azure DevOps", "Azure ML", "Bash", "BigQuery", "Bizagi", "Bitbucket", "Blender",
     "Bootstrap", "C++", "Caffe", "Cassandra", "Chef", "Cisco ASA", "Cisco Packet Tracer", "CircleCI", "ClickHouse",
     "CloudFormation", "CloudWatch", "Combine", "Confluence", "CoreData", "CSS", "Dagger", "DataRobot", "Databricks",
     "Datadog", "dbt (data build tool)", "Django", "Docker", "Docker Swarm", "Domo", "Draw.io", "Dynatrace", "Eclipse",
     "ElasticSearch", "Excel", "Fargate", "FastAPI", "Firebase", "Figma", "Flask", "GCP", "Git", "GitHub",
     "GitLab CI/CD", "Glide", "Golang", "Google AI Platform", "Google Analytics", "Google Tag Manager", "Gradle",
     "Grafana", "Graylog", "H2O.ai", "Hadoop", "Helm", "Heroku", "HubSpot", "Hugging Face", "IIS", "Informatica",
     "Informatica Cloud", "Insomnia", "IntelliJ IDEA", "iOS SDK", "Jenkins", "Jenkins X", "JIRA", "JMeter", "Jupyter",
     "Jupyter Notebook", "JUnit", "Kali Linux", "Keras", "Kibana", "KNIME", "Kotlin", "Kubernetes", "Lambda", "Linux",
     "Logstash", "Looker", "LookML", "Lucidchart", "MATLAB", "Marketo", "Maven", "Metasploit",
     "Microsoft Cognitive Services", "Microsoft Project", "Minitab", "MongoDB", "MongoDB Atlas", "Mocha", "Mulesoft",
     "Nagios", "Netlify", "New Relic", "Nexus", "Nginx", "Node.js", "Notion", "NumPy", "Objective-C", "OpenCV",
     "OpenShift", "OpenStack", "Oracle", "Oracle Cloud", "Oracle EBS", "Pandas", "Palo Alto Networks", "PeopleSoft",
     "Podman", "PostgreSQL", "Power BI", "Power Automate", "PowerApps", "PowerShell", "Presto", "Prometheus", "Puppet",
     "PyCharm", "Python", "Pytest", "PyTorch", "QlikView", "Qlik Sense", "R", "R Programming", "R Studio", "Rancher",
     "RapidMiner", "React", "Red Hat Enterprise Linux", "Redshift", "Retrofit", "Ruby", "RxJava", "Salesforce", "SAP",
     "SAP Analytics Cloud", "Scala", "Scikit-learn", "SciPy", "Selenium", "Snyk", "Snowflake", "Spark", "Splunk",
     "Spyder", "SQLite", "SSH", "SQL", "SSL", "Stata", "Superset", "Swagger", "Swift", "Tableau", "Tableau Prep",
     "Tailwind CSS", "Talend", "TensorFlow", "Terraform", "Trello", "Travis CI", "Unity", "Unreal Engine", "Vercel",
     "Visual Studio", "VS Code", "Vue.js", "Wireshark", "Windows Server", "Xcode", "C#", "ASP.NET", "Java", "Spring",
     "JavaScript", "Angular", "Ruby on Rails", "PHP", "Laravel", "Gin", "Qt", "SwiftUI", "Kotlin", "Android SDK",
     "TypeScript", "NestJS", "Shiny", "Scala", "Play", "Elixir", "Phoenix", "Clojure", "Compojure", "Rust", "Rocket",
     "Dart", "Flutter", "Haskell", "Yesod", "Julia", "HTTP.jl", "Lua", "LÖVE", "Shell", "PowerShell", "Cocoa",
     "Simulink", "Assembly", "NASM", "COBOL", "OpenCOBOL", "Pascal", "Free Pascal", "F#", "ASP.NET Core", "Blazor",
     "Visual Basic .NET", "Windows Forms", "Delphi", "Lazarus", "ActionScript", "Flex", "Groovy", "Grails", "VBScript",
     "ASP Classic", "Smalltalk", "Pharo", "Scheme", "Racket", "Prolog", "SWI-Prolog", "Ada", "GNAT", "Nim", "Nimble",
     "Crystal", "Lucky", "Solidity", "Truffle", "V", "Vlang", "Hibernate", "Sinatra", "Echo", "Vapor", "Ktor",
     "Symfony", "Actix", "Aqueduct", "Nerves", "Play Framework", "Giraffe", "SSRS", "Google Data Studio",
     "Mode Analytics", "IBM Cognos Analytics", "Azure Data Factory (ADF)", "SSIS", "Matillion", "Kafka Connect",
     "PowerBI", "VBA"})

keywordlist = ['Data engineer', 'Android developer', 'Data scientist',
       'AI engineer', 'Game developer', 'IOS developer',
       'DevOps engineer', 'Cybersecurity Analyst', 
       'Network engineer', 'Cloud Architect', 'Full stack developer',
       'Data analyst', 'Frontend developer','Front end developer', 'Back end developer', 'Backend developer', 'IT project manager']


driver = webdriver.Chrome(options=options)
driver.maximize_window()
driver.get('https://www.reed.co.uk/jobs/data-analyst-jobs-in-united-kingdom')
wait = WebDriverWait(driver, 10)


time.sleep(6)
try:
    acceptbutton = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    acceptbutton.click()
except:
    pass
time.sleep(2)

applytimerange(driver)
time.sleep(2)
alldata = []

for keyword in keywordlist:
    print("##### NEW ROLE", keyword, "searching ######")
    test_roles += 1
    searching(driver, keyword)

    driver.execute_script("document.body.style.zoom='25%'")

    getinfo(driver, alldata, keyword)
    print("Total ", len(alldata), "jobs are scraped")
    time.sleep(2)

# txt faylga Log yozish
# print('==== Link extraction completed =====\n\n')
# sys.stdout = original_std_out
print('==== Link extraction completed =====')
print('**** Data scrape starting **********')
# sys.stdout = open(log_file_date + "_log.txt", 'a', encoding="utf-8")
driver.quit()


job_data = []
failed_jobs = []

processed_rows = 0
all_rows = 0

for job in alldata:
    all_rows += 1
    try:
        keyword = job['keyword']
        if keyword == 'Front end developer':
            keyword = 'Frontend developer'
        elif keyword == 'Back end developer':
            keyword = 'Backend developer'

        jobid = job['jobid']
        job_link = job['job_link']
        id = job['jobid']
        job_title = job['job_title']

        try:
            # malumotlarni BeutifulSoup bilan olish
            extract_with_bs4(job_link, jobid, keyword, job_data, tools_list, job_title, failed_jobs)
        except Exception as e:
            print("ERROR on extract_with_bs4():", e)
        processed_rows += 1
    except Exception as e:
        print("EROR during extraction in main:", e)
        time.sleep(5)

print("===== DATA EXTRACTING COMPLETED =====")
print("Total rows:", all_rows)
print("Completly processed rows:", processed_rows)
print("===== ====== =====")

df=pd.DataFrame(job_data)

df_failed_jobs = pd.DataFrame(failed_jobs)

newdf = filtercolumns(df, keywordlist)
newdf.index = range(1, len(newdf)+1)
newdf.index.name = "ID"
# Excel faylga yozish
newdf.to_excel(log_file_date + "_jobs.xlsx", index=True)

try:
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost\\SQLEXPRESS;"
        "Database=maab_task;"
        "Trusted_Connection=yes;"
    )
    # Database ga yozish
    savetodb(df, conn)
    # muammo bo'lgan joblarni alohida tablega yozish
    # failed_jobs_log(df_failed_jobs, conn)
except Exception as e:
    print(f'ERROR creating connection: {e}')


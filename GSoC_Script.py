from selenium import webdriver
import csv
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

tech = ['react', 'python', 'android', 'compiler', 'javascript', 'postgresql', 'java', 'coq', 'ocaml', 'rust', 'c/c++']
print(tech)
email = input('Enter your email id: ')
password = input('Enter your password: ')
val = ''
user_tech = []
while val != 'exit':
    val = input('Enter what you know from the above tech stack: ')
    user_tech.append(val)

user_tech.remove('exit')


PATH = "C:\Program Files (x86)\chromedriver.exe"
opts=webdriver.ChromeOptions()
opts.headless=True
driver = webdriver.Chrome(PATH,options=opts)
driver.get("https://summerofcode.withgoogle.com/archive/2020/organizations/")
fields = ['Organization Names','Links','Tech Stack']
rows = []
for i in range(199):
    card = driver.find_elements_by_class_name("organization-card__container")[i]
    actions = ActionChains(driver)
    actions.move_to_element(card)
    actions.click()
    actions.perform()
    try:
        tech = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "organization__tag--technology"))
        )
        a = []
        done = False
        for t in tech:
            for u in user_tech:
                if u == t.text:
                    name = driver.find_element_by_class_name("banner__title")
                    url = driver.current_url
                    for w in tech:
                        a.append(w.text)
                    row=[]
                    row.append(name.text)
                    row.append(url)
                    row.append(a)
                    rows.append(row)
                    done = True
                    break
            if done:
                break
        driver.back()
    except:
        print()
with open('GSoCOrganizations.csv', 'w') as csvfile: 
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields) 
    csvwriter.writerows(rows)

msg = MIMEMultipart()
msg['Subject'] = 'List of GSoC Organizations'
msg['From'] = email
msg['To'] = email
body = 'Please find the following attachment containing the list of organizations on the basis of your tech stack'

msg.attach(MIMEText(body,'plain'))

filename = 'GSoCOrganizations.csv'

with open(filename, "rb") as attachment:

    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
  
encoders.encode_base64(part)

part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

msg.attach(part)
with smtplib.SMTP('smtp.gmail.com',587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    
    smtp.login(email,password)

    smtp.sendmail(email, email, msg.as_string())
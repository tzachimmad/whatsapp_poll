#!/usr/bin/python
# -*- coding: utf-8 -*-
from os import listdir, remove
import sys
import datetime
import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from whatsapp_parser import create_csv_file
from whatsapp_poll import csv_to_drive

reload(sys)
sys.setdefaultencoding('utf-8')

FILE_LINK = 'https://docs.google.com/spreadsheets/d/1GU5e-RFYRsYL1-YYL3ooMHE2VOHnz09oE8LZrmQa4I0/edit?usp=sharing'
admin = "צחי לפידות"
group_to_parse = "כדורסל מטומי-שלישי 19:00"
dico = {}

def scorllUp():
    try:
        driver.find_element_by_class_name("icon-refresh").click()
    except:
        pass

def sendMessage(message):
    msgbox = driver.find_element_by_class_name("input-container")
    msgbox.click()
    msgbox.send_keys(message)
    driver.find_element_by_class_name("icon-send").click()

def parser():
    today = time.strftime("%d")
    yesterday_tmp = datetime.date.today() - datetime.timedelta(1)
    yesterday = yesterday_tmp.strftime('%d')
    if (int(today)<10):
        today = today[1]
    if (int(yesterday)<10):
        yesterday = yesterday[1]

    txt = driver.find_element_by_class_name("message-list").get_attribute("innerHTML")
    txt_find= "inverse-text-direction selectable-text"
    txt_other_find = "class=\"emojitext selectable-text\" dir="
    authour_txt = "<span class=\"emojitext\"><!-- react-text: "
    has_author= "-text has-author\"><h3"
    prev_auth = authour = ""
    for elem in txt.split("bubble bubble"):
        ##define if relative msg
        if (elem.find("docs.google.com")>0):
            continue
        tmp_date =  elem[elem.find('['):elem.find('[')+30]
        tmp_date = tmp_date[tmp_date.find('/')+1:]
        date = tmp_date[:tmp_date.find('/')]
        print date
        print tmp_date
        if (date!=today and date!=yesterday):
            continue

        ##get msg
        written_msg = elem[elem.find("selectable-text"):elem.find("message-meta text-clickable")]
        aa = written_msg.find("-->")+3
        bb= written_msg.find("<!-- /react-text -->")
        cur_msg = written_msg[aa:bb]

        ##set author
        if (elem.find("-->+972 54-772-0957<")>0):
            authour = admin
        if (elem.find(has_author)>=0):
            tmp_authour = elem[elem.find(authour_txt):elem.find(authour_txt)+90]
            strt_author = tmp_authour.find("-->")+3
            end_author = tmp_authour.find("<!-- /react-text -->")
            authour = tmp_authour[strt_author:end_author]
            prev_auth = authour
        if (authour==""):
            authour = prev_auth

        ##put message in dico
        arr = dico.get(authour,[])
        final_msg = cur_msg.replace("\n",". ")
        arr.append(final_msg)
        dico[authour]=arr

###load whatsapp web
chrome_driver_path = '/home/redbend/Desktop/training/Hackathon/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=/home/redbend/Desktop/training/python scripts/WhatsApp_poll/tmp") #Path to your chrome profile
driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)
driver.set_window_size(1024,768)
driver.get('https://web.whatsapp.com/')
time.sleep(5)

###find group
msgbox = driver.find_element_by_class_name("input-search")
msgbox.click()
str = "//*[@title='" + group_to_parse + "']"
##msgbox.send_keys("19:00")
driver.find_element_by_xpath(str).click()
time.sleep(1)
scorllUp()
time.sleep(3)
scorllUp()
time.sleep(3)
scorllUp()
time.sleep(3)
scorllUp()
time.sleep(3)

##parse group and finish
parser()
create_csv_file(dico)
csv_to_drive()

if sys.argv[1].find("publish")>=0:
    sendMessage(FILE_LINK)
    time.sleep(1)
driver.quit()

try:
    remove("output.csv")
except OSError:
    pass

#login_holistor_erp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import json
import time
import os
from dotenv import load_dotenv

def login_erp():
    try:
        options = webdriver.ChromeOptions()
        download_directory = r"D:\default_emails"
        options.add_argument('--start-maximized')
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")
        appState = {
            "recentDestinations": [
                    {
                        "id": "Save as PDF",
                        "origin": "local",
                        "account": ""
                    }
                ],
                "selectedDestination": "Save as PDF",
                "version": 2
                }
        prefs = {
            'printing.print_preview_sticky_settings.appState': json.dumps(appState),
            "download.default_directory": download_directory,
            'savefile.default_directory': download_directory
            }

        options.add_experimental_option('prefs', prefs)
        options.add_argument('--kiosk-printing')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
        driver = webdriver.Chrome(options=options)

        driver.get('https://holistorsaas.com.ar/account/login')

        load_dotenv()
        name_work = os.getenv('NAME_WORK')
        email = os.getenv('EMAIL')
        password = os.getenv('PASS_ERP')

        input_name_work = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/app-root/ng-component/div/div/div/div[2]/div[2]/ng-component/div/form/div[1]/input')))
        input_name_work.send_keys(name_work)
        
        input_email = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/app-root/ng-component/div/div/div/div[2]/div[2]/ng-component/div/form/div[2]/input')))
        input_email.send_keys(email)

        input_password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/app-root/ng-component/div/div/div/div[2]/div[2]/ng-component/div/form/div[3]/input')))
        input_password.send_keys(password)

        btn_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/app-root/ng-component/div/div/div/div[2]/div[2]/ng-component/div/form/div[5]/div[2]/button')))
        btn_login.click()

        return driver

    except Exception as e:
        print('Error:', str(e))
        raise

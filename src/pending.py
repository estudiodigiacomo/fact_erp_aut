from login_holistor_erp import login_erp
import time
from read_sheet import get_clients_from_sheets
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import smtplib
import ssl
from email.message import EmailMessage
from google.oauth2 import service_account
from googleapiclient.discovery import build

def send_email_error(client_name, error_message):
    email_sender = 'administracion@estudiodigiacomo.com'
    email_received1 = 'bruno@estudiodigiacomo.com'
    email_received2 = 'nicolas@estudiodigiacomo.com'
    email_password = 'mwch hrap wcea nksy'
    subject = f'Informe de Error - Facturacion - {client_name}'
    body = f"""
    <html>
    <body>
        <p>Error al enviar email de Reporte a {client_name}</p>
        <p>{error_message}</p>
    </body>
    </html>
    """
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = ', '.join([email_received1, email_received2])
    em['Subject'] = subject
    em.set_content(body, subtype='html')

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
        server.login(email_sender, email_password)
        server.send_message(em)

def update_status_in_sheet(sheet_name, row, status):
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    KEY = 'keys.json'
    SPREADSHEET_ID = '1ndcBOcfHY7quetQCo-w4vrlxhU0l56yQWCAWaNQAOME'

    try:
        creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPE)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        value = 'TRUE' if status else 'FALSE'
        range_ = f'{sheet_name}!J{row}'
        body = {'values': [[value]]}
        sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=range_, valueInputOption="RAW", body=body).execute()
    except Exception as e:
        print("Error actualizando estado en Google Sheets:", str(e))

def select_company(driver, company_name):
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012vEMPRESA')))
    select = Select(select_element)
    for option in select.options:
        if company_name in option.text:
            option.click()
            break
    btn_into = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012INGRESAR')))
    btn_into.click()

def change_company(driver):
    user_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vUSERAVATARSMALL_MPAGE"]')))
    user_btn.click()
    change_company_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="CHANGEEMPRESA_MPAGE"]/a')))
    change_company_btn.click()
    time.sleep(5)

def process_client(driver, client):
    try:
        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'vGENERICFILTER_GRID')))
        search_input.clear()
        search_input.send_keys(client['name'])
        time.sleep(3)
        name_client_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'GridContainerRow_0001')))
        name_client_btn.click()
        time.sleep(3)
        btn_access = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'GridContainerRow_0001')))
        btn_access.click()

        row = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tr"))
        )
        time.sleep(3)

        button_fcc = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "B1")))
        button_fcc.click()
        time.sleep(5)

        select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vCV_CODIGO")))
        select = Select(select_element)
        for option in select.options:
            if client['payment_condition'] in option.text:
                option.click()
                break

        time.sleep(3)
        concept_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vING_IFA_CONCOD")))
        concept_input.click()
        time.sleep(2)
        concept_input.send_keys(client['service'])
        time.sleep(2)

        date_actual = datetime.now()
        period = date_actual.strftime("%m/%Y")
        period_text = f' - Periodo {period}'
        desc_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vING_IFA_DESCRIP")))
        desc_input.click()
        time.sleep(2)
        desc_input.send_keys(period_text)
        time.sleep(2)

        cant_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vING_IFA_CANTIDA")))
        cant_input.click()
        time.sleep(2)
        cant_input.clear()
        cant_input.send_keys(client['cant'])
        time.sleep(2)

        honorary_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vING_IFA_UNIPREC")))
        honorary_input.click()
        time.sleep(2)
        honorary_input.clear()
        honorary_input.send_keys(client['honorary'])
        time.sleep(2)

        add_concept = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "AGREGARARTCON")))
        add_concept.click()
        time.sleep(5)
        desc_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "vING_IFA_DESCRIP")))
        desc_input.click()
        time.sleep(5)

        numbers_day = int(client['pay_days'])
        new_date = datetime.now() + timedelta(days=numbers_day)
        date_formatted = new_date.strftime("%d/%m/%Y")

        payment_due_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "vFA_VTOPAG")))
        payment_due_date.click()
        time.sleep(5)
        payment_due_date.send_keys(date_formatted)
        time.sleep(15)

        confirm_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CONFIRMAR")))
        confirm_btn.click()
        time.sleep(2)

        confirm_cae = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "CONFIRMAR_FE")))
        confirm_cae.click()
        time.sleep(2)

        try:
            window_ok = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "gxp0_cls"))
            )
            window_ok.click()
        except TimeoutException:
            print("El elemento 'gxp0_b' no está disponible, continuando con el flujo.")
        try:
            window_ok = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "gxp0_cls"))
            )
            window_ok.click()
        except TimeoutException:
            print("El elemento 'gxp0_b' no está disponible, continuando con el flujo.")
    except Exception as e:
        print(f"Error procesando cliente {client['name']}: {e}")
        send_email_error(client['name'], str(e))
        update_status_in_sheet(client['sheet_name'], client['row'], False)
        
        # Volver al menú hamburguesa en caso de error
        hamburger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BTNTOGGLEMENU_MPAGE')))
        hamburger.click()
        time.sleep(3)
        diary_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/a')))
        diary_dropdown.click()
        time.sleep(3)
        buys_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/ul/li[1]/a')))
        buys_dropdown.click()
        time.sleep(3)
        issued_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/ul/li[1]/ul/li[1]/a')))
        issued_btn.click()
        time.sleep(5)
        
def loop_report():
    try:
        driver = login_erp()

        # Lista de empresas con su hoja de Google Sheets correspondiente
        companys = [
            {"name": "0000000003 - DI GIÁCOMO NICOLAS", "sheet_name": "Facturacion-Nicolas"},
            {"name": "0000000002 - DI GIÁCOMO JUAN EZEQUIEL", "sheet_name": "Facturacion-Juan"},
            {"name": "0000000001 - DI GIACOMO FRANCISCO", "sheet_name": "Facturacion-Francisco"}
        ]

        time.sleep(10)

        # Manejo de posibles alertas
        try:
            window_alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div")))
            time.sleep(5)
            btn_close_alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[3]/button[1]')))
            btn_close_alert.click()

        except TimeoutException:
            print("Alerta no encontrada, continuar")

        time.sleep(5)

        # Seleccionar el ERP
        btn_erp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[3]/ng-component/plataforma-dashboard/div[2]/div/div[1]/div/div[1]/div/img')))
        btn_erp.click()

        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        time.sleep(5)
        driver.switch_to.window(window_to_select[1])
        time.sleep(5)

        for company in companys:
            select_company(driver, company["name"])

            # Manejo del menú hamburguesa y navegación
            hamburger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[1]/div/div/div/div[1]/table/tbody/tr/td[1]/input')))
            hamburger.click()
            time.sleep(3)
            diary_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/a')))
            diary_dropdown.click()
            time.sleep(3)
            buys_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/ul/li[1]/a')))
            buys_dropdown.click()
            time.sleep(3)
            issued_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[1]/ul/li[1]/ul/li[1]/a')))
            issued_btn.click()
            time.sleep(5)

            clients = get_clients_from_sheets(company["sheet_name"])
            if not clients:
                print(f"No se encontraron clientes para {company['name']}. Cambiando de empresa.")
                continue

            for idx, client in enumerate(clients):
                try:
                    process_client(driver, client)
                    update_status_in_sheet(company["sheet_name"], idx + 2, True)
                except Exception as e:
                    print(f"Error procesando cliente {client['name']}: {e}")
                    send_email_error(client['name'], str(e))
                    update_status_in_sheet(company["sheet_name"], idx + 2, False)

            change_company(driver)
    except Exception as e:
        print("Error general:", str(e))
        raise



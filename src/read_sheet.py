#Read Sheets
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from googleapiclient.errors import HttpError
from tkinter import messagebox

def get_clients_from_sheets(sheet_name):
    # Api spreadsheets
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    # Ruta del archivo con las credenciales
    KEY = 'keys.json'
    # ID del documento de Google Sheets
    SPREADSHEET_ID = '1ndcBOcfHY7quetQCo-w4vrlxhU0l56yQWCAWaNQAOME'

    try:
        creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPE)
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()
        # Aquí estamos accediendo a todas las filas dinámicamente sin fijar el número máximo
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=f'{sheet_name}!A2:I').execute()
        values = result.get('values', [])
        
        # Búsqueda de datos
        if values:
            # Almaceno los clientes en una lista
            clients = [{'name': row[0], 'cuit': row[1], 'company': row[2], 'service': row[3], 'honorary': row[4], 'code_receipt': row[5], 'cant': row[6], 'pay_days': row[7], 'payment_condition': row[8]} for row in values if len(row) == 9]
            return clients
        else: 
            messagebox.showerror('Error', f'No se encontraron datos en la hoja {sheet_name}')
            return []
    except GoogleAuthError as auth_error:
        messagebox.showerror('Error de autenticación', str(auth_error))
        return []
    except HttpError as http_error:
        messagebox.showerror('Error HTTP', str(http_error))
        return []
    except Exception as e:
        messagebox.showerror('Error inesperado', str(e))
        return []

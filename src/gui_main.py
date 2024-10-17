import tkinter as tk
import time
from read_sheet import get_clients_from_sheets
from loop_report import loop_report

def main_gui():
    try:
        holistor_window = tk.Tk()
        holistor_window.title('Automatizacion de Facturacion - Holistor ERP')
        holistor_window.geometry('400x200')

        btn_loop = tk.Button(holistor_window, text='Iniciar bucle', command=login_and_open_vouchers)
        btn_loop.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        holistor_window.mainloop()
    
    except Exception as e:
        print('Error:', str(e))

def login_and_open_vouchers():
    loop_report()

main_gui()

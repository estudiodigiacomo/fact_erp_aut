import time
from read_sheet import get_clients_from_sheets
from loop_report import loop_report

def run_automated_process():
    try:
        print("Iniciando proceso de automatización...")
        
        # Si necesitás trabajar con los clientes antes de pasar a loop_report():
        # clients = get_clients_from_sheets()
        # print(f"Clientes encontrados: {clients}")
        
        loop_report()

        print("Proceso completado con éxito.")

    except Exception as e:
        print(f"Error durante la ejecución automática: {e}")
        input("Presione Enter para salir...")

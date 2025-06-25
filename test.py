from datetime import datetime, timedelta

# Obtener fecha actual
date_actual = datetime.now()

# Calcular el primer día del mes actual y restar 1 día para obtener el último día del mes anterior
first_day_current_month = date_actual.replace(day=1)
last_day_previous_month = first_day_current_month - timedelta(days=1)

# Formatear el mes y año anterior
period_previous = last_day_previous_month.strftime("%m/%Y")
period_text = f' - Periodo {period_previous}'

print(period_text)
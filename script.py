import csv
import os
import django
import time

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "h1b.settings")
django.setup()

# Import your Django models
from visas.models import amrika  

def ingest_data_from_csv(file_path):
    print('preop')
    with open(file_path, "r", encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        next(csv_reader)
        print('postop')
        for row in csv_reader:
            if not row['WAGE_UNIT_OF_PAY_1'] or not row['WAGE_RATE_OF_PAY_FROM_1']:
                continue
            
            salary = float(row['WAGE_RATE_OF_PAY_FROM_1'].replace(',','').replace('$',''))
            unit = row['WAGE_UNIT_OF_PAY_1']

            if unit.lower() == 'month':
                salary *= 12
            elif unit.lower() == 'bi-weekly':
                salary *= 24
            elif unit.lower() == 'week':
                salary *= 48
            elif unit.lower() == 'hour':
                salary *= 2080

            print(salary)
            obj = amrika(unit=unit, salary=salary)
            obj.save()

if __name__ == "__main__":

    try:
        st = time.time()
        file_path = "h1b/data.csv" 
        ingest_data_from_csv(file_path)
    except Exception :
        print(f"phat gya!!! {Exception}")
    print(time.time() - st)
    #this took 598 secs


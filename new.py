import csv
import os
import django
import time

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "h1b.settings")
django.setup()

# Import your Django models
from visas.models import amrika  

MIN_BATCH_SIZE = 100  # Minimum batch size
MAX_BATCH_SIZE = 10000  # Maximum batch size
prev_import_time_per_entry = 5

def ingest_data_from_csv(file_path):
    print('preop')
    objs_to_create = []
    total_entries = 0
    total_time = 0.0
    batch_size = MIN_BATCH_SIZE
    global prev_import_time_per_entry  # Ensure we're accessing the global variable

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

            obj = amrika(unit=unit, salary=salary)
            objs_to_create.append(obj)
            total_entries += 1

            if len(objs_to_create) >= batch_size:
                start_time = time.time()
                amrika.objects.bulk_create(objs_to_create)
                end_time = time.time()
                total_time += (end_time - start_time)

                # Calculate import time per entry for this batch
                import_time_per_entry = total_time / total_entries

                # Adjust batch size based on import time per entry
                if import_time_per_entry < prev_import_time_per_entry and batch_size < MAX_BATCH_SIZE:
                    batch_size = min(batch_size * 2, MAX_BATCH_SIZE)
                elif import_time_per_entry > prev_import_time_per_entry and batch_size > MIN_BATCH_SIZE:
                    batch_size = max(batch_size // 2, MIN_BATCH_SIZE)

                # Update prev_import_time_per_entry for the next batch
                prev_import_time_per_entry = import_time_per_entry

                print(f'Batch size: {batch_size}, Import time per entry: {import_time_per_entry}')

                objs_to_create = []
                total_entries = 0
                total_time = 0.0

        # Insert any remaining objects
        if objs_to_create:
            amrika.objects.bulk_create(objs_to_create)

if __name__ == "__main__":
    try:
        st = time.time()
        file_path = "/Users/survagyabali/Desktop/Newproj/h1b/data.csv" 
        ingest_data_from_csv(file_path)
    except Exception as e:
        print(f"phat gya!!! {e}")
    print(time.time() - st)
# This took 75 secs!!
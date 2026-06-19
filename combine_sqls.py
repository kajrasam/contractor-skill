import os

# Run create_new_sql.py to generate employee_data_update.sql with TEXT types
os.system('python create_new_sql.py')

# Read employee_data_update.sql
with open('employee_data_update.sql', 'r', encoding='utf-8') as f:
    schema_sql = f.read()

# Read insert_30_employees.sql
with open('insert_30_employees.sql', 'r', encoding='utf-8') as f:
    inserts_sql = f.read()

# Combine them
final_sql = schema_sql + "\n\n-- Insert 30 simulated employees\n" + inserts_sql

with open('employee_data_update.sql', 'w', encoding='utf-8') as f:
    f.write(final_sql)

print("Combined schema and inserts into employee_data_update.sql")

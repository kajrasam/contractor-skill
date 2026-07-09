import pandas as pd
import numpy as np

def format_val(val):
    if pd.isna(val):
        return "NULL"
    if isinstance(val, (int, float, np.integer, np.floating)):
        return str(val)
    if isinstance(val, pd.Timestamp):
        return f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'"
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

# Load excel
print("Loading Excel...")
df = pd.read_excel(r'd:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\sap_hr.xlsx')
cols = df.columns.tolist()

# Limit to 150 rows as requested
df = df.head(150)

sql_statements = [
    "-- SQL สำหรับสร้างและนำเข้าข้อมูล legacy_employee_data",
    "DROP VIEW IF EXISTS public.all_employee_data;",
    "DROP TABLE IF EXISTS public.legacy_employee_data CASCADE;",
    "CREATE TABLE public.legacy_employee_data (",
    "    id SERIAL PRIMARY KEY,",
    "    user_id TEXT,",
    "    password TEXT,"
]

# Define columns as TEXT
for col in cols:
    sql_statements.append(f'    "{col}" TEXT,')

# Add FullName and extra columns
sql_statements.append('    "FullName" TEXT,')
sql_statements.append('    "JobGroup" TEXT,')
sql_statements.append('    "Certificate" TEXT,')
sql_statements.append('    "Email" TEXT')
sql_statements.append(");")
sql_statements.append("")

# Generate INSERTS
print(f"Generating INSERT statements for {len(df)} rows...")
all_columns = ['user_id', 'password'] + [f'"{c}"' for c in cols] + ['"FullName"', '"JobGroup"', '"Certificate"', '"Email"']
insert_prefix = f"INSERT INTO public.legacy_employee_data ({', '.join(all_columns)}) VALUES "

values_list = []
for _, row in df.iterrows():
    # Extact USER for user_id
    user_id_val = str(row.get('USER', '')).strip()
    if pd.isna(row.get('USER')) or user_id_val == '' or user_id_val == 'nan':
        user_id_val = str(row.get('PersonnelNumber', '')) # fallback
    
    user_vals = [f"'{user_id_val}'", "'Pass@1234'"]
    
    for col in cols:
        user_vals.append(format_val(row[col]))
        
    # FullName
    first_name = str(row.get('FirstNameThai', '')).strip()
    last_name = str(row.get('LastNameThai', '')).strip()
    if first_name == 'nan': first_name = ''
    if last_name == 'nan': last_name = ''
    
    full_name = f"{first_name} {last_name}".strip()
    user_vals.append(f"'{full_name}'")
    
    # Extra columns
    user_vals.append("NULL") # JobGroup
    user_vals.append("NULL") # Certificate
    user_vals.append("NULL") # Email
    
    values_list.append("(" + ", ".join(user_vals) + ")")
    
sql_statements.append(insert_prefix)
sql_statements.append(",\n".join(values_list) + ";\n")

# Create View
columns_for_view = ['id', 'user_id', 'password'] + [f'"{c}"' for c in cols] + ['"FullName"', '"JobGroup"', '"Certificate"', '"Email"']
col_list_str = ", ".join(columns_for_view)

sql_statements.append("-- สร้าง SQL View สำหรับรวมข้อมูล 2 ตาราง")
sql_statements.append("CREATE OR REPLACE VIEW public.all_employee_data AS")
sql_statements.append(f"SELECT {col_list_str} FROM public.legacy_employee_data")
sql_statements.append("UNION ALL")
sql_statements.append(f"SELECT {col_list_str} FROM public.employee_data;")

with open('legacy_employee_data_150.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(sql_statements))

print("Successfully created legacy_employee_data_150.sql")

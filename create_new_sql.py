import pandas as pd
import math
import numpy as np

# Load excel
df = pd.read_excel(r'd:\Work\งานใหม่\อบรม\2026\Vibe Coding Workshop\Project\EMP_DaTa.xlsx')

cols = df.columns.tolist()

# Mapping pandas dtypes to SQL types
sql_types = []
for col in cols:
    sql_types.append('TEXT')

sql_statements = [
    "DROP TABLE IF EXISTS public.employee_data;",
    "CREATE TABLE public.employee_data (",
    "    id SERIAL PRIMARY KEY,",
    "    user_id TEXT UNIQUE,",
    "    password TEXT,"
]

for i, col in enumerate(cols):
    col_name = f'"{col}"'
    sql_statements.append(f"    {col_name} {sql_types[i]},")

# Add FullName column
sql_statements.append('    "FullName" TEXT,')

# Remove last comma
sql_statements[-1] = sql_statements[-1][:-1]
sql_statements.append(");")

sql_statements.append("")

# Generate insert for the first row
first_row = df.iloc[0].to_dict()

# Let's map admin users to be inserted
admin_users = [
    ("admin", "Admin", "Admin"),
    ("somchai.j", "Pass@1234", "หัวหน้างานซ่อม"),
    ("somsri.m", "Pass@1234", "หัวหน้าหมวดซ่อม"),
    ("ratthasart.m", "Pass@1234", "เจ้าหน้าที่บัญชี"),
    ("wichai.r", "Pass@1234", "HR BP Manager"),
    ("mana.c", "Pass@1234", "ช่างซ่อมไฟฟ้า"),
    ("piti.s", "Pass@1234", "ผู้จัดการโรงงาน"),
    ("choojai.b", "Pass@1234", "HR BP Officer"),
    ("weera.n", "Pass@1234", "HR BP Officer"),
    ("arun.p", "Pass@1234", "พนักงานขาย")
]

insert_prefix = f"INSERT INTO public.employee_data (user_id, password, " + ", ".join([f'"{c}"' for c in cols]) + ', "FullName") VALUES '

values_list = []

def format_val(val):
    if pd.isna(val):
        return "NULL"
    if isinstance(val, (int, float, np.integer, np.floating)):
        return str(val)
    if isinstance(val, pd.Timestamp):
        return f"'{val.strftime('%Y-%m-%d %H:%M:%S')}'"
    val_str = str(val).replace("'", "''")
    return f"'{val_str}'"

# First row
first_row_vals = ["'thidas'", "'Pass@1234'"]
for col in cols:
    first_row_vals.append(format_val(first_row[col]))

first_name = str(first_row.get('FirstNameThai', '')).strip()
last_name = str(first_row.get('LastNameThai', '')).strip()
first_row_vals.append(f"'{first_name} {last_name}'")

values_list.append("(" + ", ".join(first_row_vals) + ")")

# Admin users
for uid, pwd, pos in admin_users:
    user_vals = [f"'{uid}'", f"'{pwd}'"]
    for col in cols:
        if col == "PositionNameThai":
            user_vals.append(f"'{pos}'")
        elif col == "NamePrefixThai":
            user_vals.append("'คุณ'")
        elif col == "FirstNameThai":
            user_vals.append(f"'{uid}'")
        elif col == "LastNameThai":
            user_vals.append("'(Admin)'")
        elif col == "EmailAddressBusiness":
            user_vals.append(f"'{uid}@company.com'")
        else:
            user_vals.append("NULL")
    
    user_vals.append(f"'{uid} (Admin)'")
    values_list.append("(" + ", ".join(user_vals) + ")")

sql_statements.append(insert_prefix)
sql_statements.append(",\n".join(values_list) + ";")

with open('employee_data_update.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(sql_statements))

print("Created employee_data_update.sql")

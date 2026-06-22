import os
import random
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def main():
    print("Fetching employee data...")
    res = supabase.table("employee_data").select("*").execute()
    data = res.data
    
    if not data:
        print("No data found!")
        return
        
    print(f"Found {len(data)} employees.")
    
    # Extract list of english names
    english_names = []
    for emp in data:
        # Replicate JS logic for Name (EN)
        name_en = emp.get("name_en")
        if not name_en:
            name_en = emp.get("FullNameENG")
            if not name_en:
                first = emp.get("FirstNameEnglish")
                if first:
                    prefix = emp.get("NamePrefixEnglish", "")
                    last = emp.get("LastNameEnglish", "")
                    name_en = f"{prefix} {first} {last}".strip()
                else:
                    name_en = ""
                    
        if name_en and name_en != "None" and name_en.strip() != "":
            english_names.append(name_en.strip())
            
    print(f"Extracted {len(english_names)} valid English names.")
    if not english_names:
        print("No english names found to use as Report To Name!")
        return
        
    print("Updating ReportToName for all rows...")
    for emp in data:
        # Choose a random english name
        random_manager = random.choice(english_names)
        
        # We need the primary key to update. The PK might be 'id' or 'person_id' or 'PersonID'
        pk_field = None
        pk_value = None
        if "id" in emp:
            pk_field = "id"
            pk_value = emp["id"]
        elif "PersonID" in emp:
            pk_field = "PersonID"
            pk_value = emp["PersonID"]
        elif "person_id" in emp:
            pk_field = "person_id"
            pk_value = emp["person_id"]
            
        if pk_field:
            try:
                # Update ReportToName and report_to_name just in case both exist
                update_payload = {}
                if "ReportToName" in emp:
                    update_payload["ReportToName"] = random_manager
                if "report_to_name" in emp:
                    update_payload["report_to_name"] = random_manager
                
                if update_payload:
                    supabase.table("employee_data").update(update_payload).eq(pk_field, pk_value).execute()
            except Exception as e:
                print(f"Failed to update row with {pk_field}={pk_value}: {e}")
        else:
            print(f"Could not determine primary key for row: {emp}")
            
    print("Successfully updated all rows with random English Report To Names!")

if __name__ == '__main__':
    main()

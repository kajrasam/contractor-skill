import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

try:
    # Attempt to read from users table
    response = supabase.table("users").select("*").limit(1).execute()
    print("Connection successful! Tables exist.")
    print("Response:", response.data)
except Exception as e:
    print("Connection failed or tables do not exist:", str(e))

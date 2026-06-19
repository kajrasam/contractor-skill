import os
from supabase import create_client, Client

url = "https://fgeqhfgjklxsezwducyk.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZnZXFoZmdqa2x4c2V6d2R1Y3lrIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4MTIxNTY0OSwiZXhwIjoyMDk2NzkxNjQ5fQ.6b8R3_MYIMj7Etf4O5p9txIXZgtFqKmIhMKmc_9pgBA"
supabase: Client = create_client(url, key)

uid = "Ratthasp"
pos = "HR BP Officer"
pt_res = supabase.table("position_targets").select("*").eq("position_name", pos).execute()

for pt in pt_res.data:
    idx = pt["competency_idx"]
    tgt = pt["target_level"]
    if tgt > 0:
        supabase.table("user_actuals").update({"actual_level": tgt}).eq("user_id", uid).eq("competency_idx", idx).execute()

print("Fixed user actuals for Ratthasp to match targets")

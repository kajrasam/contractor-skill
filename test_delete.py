import urllib.request, json
url = "https://contractor-skill.onrender.com/api/admin/sync_employees"
req = urllib.request.Request(url, headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla'}, data=json.dumps({"employees": [], "deleted_ids": [1]}).encode('utf-8'))
try:
    response = urllib.request.urlopen(req).read().decode('utf-8')
    print("Response:", response)
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode('utf-8'))

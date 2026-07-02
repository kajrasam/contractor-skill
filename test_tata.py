import urllib.request, json
url = "https://contractor-skill.onrender.com/api/data"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla'})
response = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(response)

employees = data.get('employeeData', [])
print(f"Total employees: {len(employees)}")
for e in employees:
    if "ทาทา" in e.get("FullName", "") or "ทาทา" in e.get("FullNameTH", ""):
        print(f"Found Tata: id={e.get('id')}, user_id={e.get('user_id')}, PersonnelNumber={e.get('PersonnelNumber')}")

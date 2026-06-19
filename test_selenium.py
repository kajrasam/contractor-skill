from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=opts)
try:
    driver.get('https://competency-system-operation-by-kr.onrender.com/')
    time.sleep(3)
    # Login
    driver.execute_script("document.getElementById('login-username').value = 'Admin'; document.getElementById('login-password').value = '0817906628'; handleLogin();")
    time.sleep(3)
    
    for log in driver.get_log('browser'):
        print('CONSOLE:', log)
        
    driver.execute_script("switchTab('training-need')")
    time.sleep(2)
    
    html = driver.execute_script("return document.getElementById('position-filters').innerHTML")
    print('POSITION FILTERS HTML LENGTH:', len(html))
    print('POSITION FILTERS CONTAINS CHECKBOX:', 'checkbox' in html)
    print('POSITION FILTERS CONTAINS SELECT ALL:', 'Select All' in html)
    
    html2 = driver.execute_script("return document.getElementById('job-group-filters').innerHTML")
    print('JOB GROUP FILTERS CONTAINS HR:', 'HR' in html2)
    
    # Check sections
    html3 = driver.execute_script("return document.getElementById('section-filters').innerHTML")
    print('SECTION FILTERS CONTAINS Production:', 'Production' in html3)
except Exception as e:
    print('ERROR:', e)
finally:
    driver.quit()

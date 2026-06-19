from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

opts = Options()
opts.add_argument('--headless')
opts.add_argument('--no-sandbox')
driver = webdriver.Chrome(options=opts)
try:
    print('Testing localhost:3000')
    driver.get('http://127.0.0.1:3000/')
    time.sleep(2)
    # Login
    driver.execute_script("document.getElementById('login-username').value = 'Admin'; document.getElementById('login-password').value = '0817906628'; handleLogin();")
    time.sleep(2)
    
    driver.execute_script("switchTab('training-need')")
    time.sleep(1)
    
    # Try to open Section dropdown
    print('Opening section dropdown...')
    driver.execute_script("toggleFilterMenu('section-dropdown-menu')")
    time.sleep(1)
    
    menu_class = driver.execute_script("return document.getElementById('section-dropdown-menu').className")
    print('MENU CLASSES:', menu_class)
    
    html = driver.execute_script("return document.getElementById('section-filters').innerHTML")
    print('SECTION FILTERS HTML:', html[:200])
    
    logs = driver.get_log('browser')
    for l in logs:
        print('LOG:', l)
        
except Exception as e:
    print('ERROR:', e)
finally:
    driver.quit()

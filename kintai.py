from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select    
import json
import time
import config

def setup_chrome_options():
    """Chrome印刷設定の初期化（PDF保存用）"""
    chrome_options = webdriver.ChromeOptions()
    app_state = {
        "recentDestinations": [{
            "id": "Save as PDF",
            "origin": "local",
            "account": ""
        }],
        "selectedDestinationId": "Save as PDF",
        "version": 2,
        "isLandscapeEnabled": True,
        "pageSize": 'A4',
        "isHeaderFooterEnabled": False,
        "isCssBackgroundEnabled": True,
    }
    
    prefs = {
        'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
        "download.default_directory": "~/Downloads"
    }
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument('--kiosk-printing')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    
    return chrome_options

def setup(driver, userid, pwd):
    """KingOfTimeへのログインとチュートリアルスキップ"""
    print(type(config.URL))
    print(config.URL)
    driver.get(config.URL)
    
    # ログイン処理
    driver.find_element(By.CLASS_NAME, config.USER_ID).send_keys(userid)
    driver.find_element(By.CLASS_NAME, config.PASSWORD).send_keys(pwd)
    driver.find_element(By.ID, config.LOGIN_BUTTON).click()
    
    # チュートリアルのスキップ
    driver.find_element(By.ID, config.TUTORIAL_START).click()
    for _ in range(4):
        driver.find_element(By.CLASS_NAME, config.TUTORIAL_SKIP).click()
    
    # ガイド停止
    for _ in range(10):
        try:
            shadow_root = driver.find_element(By.ID, config.SHADOW_ROOT).shadow_root
            shadow_root.find_element(By.CSS_SELECTOR, config.END_GUIDE).click()
            continue
        except:
            break

def change_date(driver, year, month):
    """出力対象年月の変更"""
    year_elem = driver.find_element(By.ID, 'year')
    month_elem = driver.find_element(By.ID, 'month')
    
    driver.execute_script('arguments[0].value = arguments[1]', year_elem, year)
    driver.execute_script('arguments[0].value = arguments[1]', month_elem, month)

def export_data(driver, home_url, data_type, year, month):
    """データ出力処理"""
    driver.get(home_url)
    driver.find_element(By.CLASS_NAME, config.MENU).click()
    
    match data_type:
        case 'timecard':
            export_timecard(driver, year, month)
        case 'monthly_xls':
            export_monthly_xls(driver, year, month)
        case 'monthly_csv':
            export_monthly_csv(driver, year, month)
        case 'schedule':
            export_schedule(driver, year, month)
        case 'all':
            for dtype in ['timecard', 'monthly_xls', 'monthly_csv', 'schedule']:
                export_data(driver, home_url, dtype, year, month)

def export_timecard(driver, year, month):
    """タイムカードの出力"""
    driver.find_element(By.XPATH, config.EXPORT).click()
    driver.find_element(By.XPATH, config.TIME_CARD).click()
    change_date(driver, year, month)
    for _ in range(2):
        driver.find_element(By.ID, config.RESULT_BUTTON).click()

def export_monthly_xls(driver, year, month):
    """月次データ（Excel）の出力"""
    driver.find_element(By.XPATH, config.MONTHLY_DATA).click()
    change_date(driver, year, month)
    driver.find_element(By.ID, config.DATA_DISPLAY).click()
    
    for _ in range(2):  # 2種類のデータを出力
        WebDriverWait(driver, 180).until(
            lambda d: d.find_element(By.ID, config.MONTHLY_DATA_EXPORT).get_attribute('disabled') is None
        )
        for _ in range(2):
            driver.find_element(By.ID, config.MONTHLY_DATA_EXPORT).click()
            time.sleep(1)
        
        driver.find_element(By.CLASS_NAME, 'htBlock-tab_item--custom').click()

def export_monthly_csv(driver, year, month):
    """月次データ（CSV）の出力"""
    driver.find_element(By.XPATH, config.EXPORT).click()
    driver.find_element(By.ID, config.MONTHLY_DATA_CSV).click()
    change_date(driver, year, month)
    
    layouts = Select(driver.find_element(By.ID, config.SELECT_LAYOUT))
    layout_count = len(layouts.options)
    
    for i in range(layout_count):
        select = Select(driver.find_element(By.ID, config.SELECT_LAYOUT))
        select.select_by_index(i)
        for _ in range(2):
            driver.find_element(By.ID, config.RESULT_BUTTON).click()
        driver.back()
        
def export_schedule(driver, year, month):
    """スケジュールの出力"""
    driver.find_element(By.XPATH, config.SCHEDULE).click()
    change_date(driver, year, month)
    driver.find_element(By.ID, config.DATA_DISPLAY).click()
    driver.find_element(By.ID, config.SCHEDULE_PRINT).click()
    
    driver.switch_to.window(driver.window_handles[1])
    WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)
    driver.execute_script('return window.print()')

def startrpa(userid, pwd, selected_year, selected_month, selected_dataname):
    """RPAメイン処理"""
    chrome_options = setup_chrome_options()
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.implicitly_wait(3)
    
    try:
        setup(driver, userid, pwd)
        home_url = driver.current_url
        export_data(driver, home_url, selected_dataname, selected_year, selected_month)
    finally:
        driver.quit()
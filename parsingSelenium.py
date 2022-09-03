import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, JavascriptException, TimeoutException
from selenium.webdriver.chrome.service import Service as ChromeService
from subprocess import CREATE_NO_WINDOW
import requests
import time

def ones():
    global browser
    prefs = {
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.stylesheets": 2,
    # "profile.managed_default_content_settings.mixed_script": 2,
    # "profile.managed_default_content_settings.media_stream": 2,
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.ignore_zoom_level = True
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("start-maximized")
    # chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    num_error = 0
    serv = ChromeService(chromedriver_autoinstaller.install())
    serv.creationflags = CREATE_NO_WINDOW

    # try:
    #     browser.quit()
    # except NameError:
    #     print("Первый поиск")

    browser = webdriver.Chrome(service=serv, options=chrome_options)
    browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # browser.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent.random})

    try:
        browser.get('https://rp5.ru')
        return 0
    except Exception:
        browser.quit()
        print("ИНТЕРНЕТ ЛЁГ")
        num_error = 1
        return num_error

def search(city):
    global start
    global count_result
    global data_result_canc
    global link_and_result
    start = time.time()

    browser.switch_to.window(browser.window_handles[0])
    try:
        browser.find_element(By.ID, "searchStr").clear()
        browser.find_element(By.ID, "searchStr").send_keys(city)
        num_error = 2
    except NoSuchElementException:
        browser.quit()
        print("Нет элемента searchStr")
        num_error = 0
        return num_error
    
    try:
        browser.find_element(By.ID, "searchButton").click()
        num_error = 2
    except NoSuchElementException:
        browser.quit()
        print("Нет элемента searchButton")
        num_error = 0
        return num_error

    all_result = browser.find_elements(By.CLASS_NAME, "innerTextResult")

    try:
        search_result = browser.find_element(By.CLASS_NAME, "searchResults")
        num_error = 2
    except NoSuchElementException:
        # browser.quit()
        print("По Вашему запросу ничего не найдено")
        num_error = 0
        return num_error

    count_result = browser.find_element(By.CLASS_NAME, "stinfo").text
    all_links = search_result.find_elements(By.TAG_NAME, "a")

    def func_chunks_generators(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    data_result = [result.text for result in all_result]
    data_result_canc = list(func_chunks_generators(data_result, 4))
    data_link = [link for link in all_links]
    link_and_result = dict(zip(data_link, data_result_canc))

    return count_result, data_result_canc, num_error

def result_list(select_city):
    global current_link_city
    global downld_page
    def get_key(data, value):
        for k, v in data.items():
            if v == value:
                return k

    browser.switch_to.window(browser.window_handles[0])
    key_selected_city = get_key(link_and_result, data_result_canc[select_city])
    current_link_city = key_selected_city.get_attribute('href')
    view_city = key_selected_city.text
    print('ВЫБРАН ГОРОД', view_city )
    browser.execute_script(f"window.open('{current_link_city}', 'new_window')")

    browser.switch_to.window(browser.window_handles[1])
    archive = browser.find_elements(By.PARTIAL_LINK_TEXT, "Архив")
    archive[0].click()

    try:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "fsynop")))
    except TimeoutException:
        WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, "fmetar")))

    try:
        start_monitoring = browser.find_element(By.ID, "fsynop")                     # Дата начала наблюдений
        id_station = "fsynop"
    except NoSuchElementException:
        start_monitoring = browser.find_element(By.ID, "fmetar")
        id_station = "fmetar"

    # номер станции
    try:
        num_weather_station = browser.find_element(By.XPATH, f'//*[@id="{id_station}"]/span/input').get_attribute('value')
        print("номер станции", num_weather_station)
    except Exception:
        num_weather_station = "Н/Д" 
         
    strt_monit = start_monitoring.text.partition(',')[2]
    print(strt_monit)
    downld_page = browser.current_url
    return {'view_city': view_city, 'strt_monit': strt_monit, 'num_weather_station': num_weather_station }

def input_date(date_start, date_end):
    global js_code
    global js_code2

    browser.execute_script(f"window.open('{downld_page}', 'new_window')")

    try:
        browser.find_element(By.ID, "tabSynopDLoad")
    except NoSuchElementException:
        browser.find_element(By.ID, "tabMetarDLoad").click()
    else:
        browser.find_element(By.ID, "tabSynopDLoad").click()
                                                                                     # Вставка даты в поля
    js_code = f"document.querySelector('input[name=ArchDate1]').value ='{date_start}'"
    browser.execute_script(js_code)

    js_code2 = f"document.querySelector('input[name=ArchDate2]').value ='{date_end}'"
    browser.execute_script(js_code2)

    try:
        browser.find_element(By.ID, "tabSynopDLoad")
    except NoSuchElementException:
        browser.find_element(By.ID, "tabMetarDLoad").click()
    else:
        browser.find_element(By.ID, "tabSynopDLoad").click()

def download():
    global download_link
    num_error = 0
    WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "download")))

    try:
        buttonGZ = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, "download"))) #клик по кнопке Выбрать архив
        buttonGZ.click()
    except Exception:
        # browser.quit()
        print('Не подгружается с сервера')
        browser.refresh()
        return num_error

    download = browser.find_element(By.ID, "f_result")

    try:
        download_link = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.LINK_TEXT, "Скачать"))) # написать обработчик при false варианте
    except Exception:
        # browser.quit()
        print('Не подгружается с сервера')
        browser.refresh()
        return num_error

    download_href = download_link.get_attribute("href")

    # print("Ссылка получена", download_href)
    num_error += 1

    print('Время парсинга:',time.time()-start)

    print('Скачивание файла...')
    r = requests.get(download_href)
    with open('Data/SP/arhiv.xls.gz', 'wb') as f:
        f.write(r.content)
    print('Файл загружен!')

    return num_error

def input_date_statist(date_start, date_end):
    global js_code
    global js_code2

    browser.execute_script(f"window.open('{downld_page}', 'new_window')")
    try:
        browser.find_element(By.ID, "tabSynopStatist")
    except NoSuchElementException:
        browser.find_element(By.ID, "tabMetarStatist").click()
    else:
        browser.find_element(By.ID, "tabSynopStatist").click()
                                                                                     # Вставка даты в поля
    js_code = f"document.querySelector('input[name=StatDate1]').value ='{date_start}'"
    browser.execute_script(js_code)

    js_code2 = f"document.querySelector('input[name=StatDate2]').value ='{date_end}'"
    browser.execute_script(js_code2)

    try:
        browser.find_element(By.ID, "tabSynopStatist")
    except NoSuchElementException:
        browser.find_element(By.ID, "tabMetarStatist").click()
    else:
        browser.find_element(By.ID, "tabSynopStatist").click()

def load():
    num_error = 0

    try:
        load_btn = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statistMenu"]/form/table/tbody/tr[3]/td/div[2]/div'))) # написать обработчик при false варианте
        load_btn.click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="t_statist_synop_t"]')))
    except Exception:
        print('Не подгружается с сервера')
        browser.refresh()
        return num_error
        
    # температура
    try:
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_t"]'))).click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_t"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[2]/div[1]/span')))
        average_temp = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[2]/div[1]/span'))).text
        min_temp = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[3]/div[1]/span'))).text
        max_temp = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[4]/div[1]/span'))).text
        date_min_temp = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[3]/div[3]'))).text
        date_max_temp = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[4]/div[3]'))).text
        all_range = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[1]'))).text
        number_of_observations = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_1"]/table/tbody/tr[2]/td[5]'))).text
    except Exception:
        print("Температура не подгружена")
        average_temp = "Н/Д"
        max_temp = "Н/Д"
        min_temp = "Н/Д"
        number_of_observations = "Н/Д"
        date_min_temp = "Н/Д"
        date_max_temp = "Н/Д"
        all_range = "Н/Д"

    try:
        # давление
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_p0"]'))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_p0"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_2"]/table/tbody/tr[2]/td[2]/div[1]')))
        average_pressure = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_2"]/table/tbody/tr[2]/td[2]/div[1]'))).text
        
        # влажность воздуха
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_u"]'))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_u"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_4"]/table/tbody/tr[2]/td[2]')))
        average_humidity = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_4"]/table/tbody/tr[2]/td[2]'))).text
        
        # ветер
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_dd"]'))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_dd"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_5"]/table/tbody/tr[2]/td[2]/div[1]')))
        orientations = []
        for orientation in range(2,18):
            wind = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, f'//*[@id="statist_synop_data_5"]/table/tbody/tr[2]/td[{orientation}]/div[1]'))).text
            orientations.append(float(wind[:-2]))
        wind_directions = ['С', 'ССВ', 'СВ', 'ВСВ', 'В', 'ВЮВ', 'ЮВ', 'ЮЮВ', 'Ю', 'ЮЮЗ', 'ЮЗ', 'ЗЮЗ', 'З', 'ЗСЗ', 'СЗ', 'ССЗ']
        winds = dict(zip(wind_directions, orientations))
        main_wind = max(winds, key=winds.get)
        
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_wv"]'))).click()
        WebDriverWait(browser, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_wv"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_6"]/table/tbody/tr[2]/td[2]/div[1]')))
        average_speed_wind = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_6"]/table/tbody/tr[2]/td[2]/div[1]'))).text
        max_speed_wind = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_6"]/table/tbody/tr[2]/td[3]/div[1]/span'))).text
    except Exception:
        print("Данные не подгружены")
        average_pressure = "Н/Д"
        average_humidity = "Н/Д"
        main_wind = "Н/Д"
        average_speed_wind = "Н/Д"
        max_speed_wind  = "Н/Д"
    
    try:
        # осадки
        WebDriverWait(browser, 1).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_pr"]'))).click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_pr"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_14"]/table/tbody/tr[2]/td[3]/div[1]/span')))
        precipitation_on_12_hour = WebDriverWait(browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_14"]/table/tbody/tr[2]/td[3]/div[1]/span'))).text
        # снежный покров
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_sss"]'))).click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="t_statist_synop_sss"]'))).click()
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="statist_synop_data_15"]/table/tbody/tr[2]/td[2]/div[1]')))
        average_height_snow = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_15"]/table/tbody/tr[2]/td[2]/div[1]'))).text
        max_height_snow = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_15"]/table/tbody/tr[2]/td[3]/div[1]/span'))).text
        first_date_snow = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_15"]/table/tbody/tr[2]/td[5]/div[1]'))).text
        last_date_snow = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="statist_synop_data_15"]/table/tbody/tr[2]/td[4]/div[1]'))).text
    except Exception:
        print("Данные о осадках и снежгом покрове отсутствуют")
        precipitation_on_12_hour = "Н/Д"
        average_height_snow = "Н/Д"
        max_height_snow = "Н/Д"
        first_date_snow = "Н/Д"
        last_date_snow = "Н/Д"

    # print("Element is visible? " + str(download_link.is_displayed()))
    # data_link[2].click()
    num_error += 1
    # return num_error, min_temp, date_min_temp, max_temp, date_max_temp, all_range, average_temp
    return {'num_error': num_error, 'min_temp': min_temp, 'date_min_temp': date_min_temp, 
            'max_temp': max_temp, 'date_max_temp': date_max_temp, 'all_range': all_range, 'average_temp': average_temp,
            'number_of_observations': number_of_observations, 'average_pressure': average_pressure, 'average_humidity': average_humidity, 'main_wind': main_wind, 
            'average_speed_wind': average_speed_wind, 'max_speed_wind': max_speed_wind, 'precipitation_on_12_hour': precipitation_on_12_hour,
            'average_height_snow': average_height_snow, 'max_height_snow': max_height_snow, 'first_date_snow': first_date_snow, 'last_date_snow': last_date_snow}

def close_browser():
    try:
        browser.quit()
    except NameError:
        return
    except Exception:
        return

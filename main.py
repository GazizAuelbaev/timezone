from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, wait
import time
from selenium.webdriver.support.select import Select

# Скрипт для автоматического обновления телефонов грандстрим
# Устанавливается поддержка 802.1.х, а также обновление прошивки через tftp
# Перед любыми изменениями рекомендую изучить selenium через сайт https://selenium-python.readthedocs.io/

# Тут вводить айпи адреса
phone_ip_address = ["0.0.0.0"]
# Логин пароль для входа
login = "admin"
passwd = "sssssss"
ntpdomen = "10.1.255.1"


def automate_phone_settings():
    # Тут не трогать, настройка дров для браузера
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    # Цикл по айпи адресам
    for ip in phone_ip_address:

        try:
            # Переход по адресу
            driver.get(f"http://{ip}")

            # В данном этапе происходит поиск HTML элементов для взаимодействия
            # Элементы страницы по классу
            loginTextBox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gwt-TextBox")))
            password = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gwt-PasswordTextBox")))
            submitButton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "gwt-Button")))

            # С элемента убираются данные, и вставляются другие (Логин и пароль)
            loginTextBox.clear()
            loginTextBox.send_keys(login)
            password.clear()
            password.send_keys(passwd)

            # Пауза между этапами для загрузки страниц

            time.sleep(1)

            submitButton.click()

            time.sleep(3)

            # Переход на страницу и смена домена

            driver.get(f"http://{ip}/#page:settings_date_time")

            time.sleep(3)

            Ntpdomen = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "P30")))

            Ntpdomen.clear()
            Ntpdomen.send_keys(ntpdomen)

            time.sleep(1)

            # Изменение даты

            select = Select(driver.find_element(By.NAME, "P64"))
            time.sleep(3)
            select.select_by_value('TZS-5')
            time.sleep(3)
            checkbox_element = driver.find_element(By.NAME, "P143")
            if checkbox_element.is_selected():
                print("Allow DHCP Option 2 to Override Time Zone Setting уже включен")
            else:
                # Если чекбокс не выбран, то кликаем по нему, чтобы включить
                checkbox_element.click()
                print("Allow DHCP Option 2 to Override Time Zone Setting был включен")
            time.sleep(3)

            SaveApply = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="Save and Apply"]')))

            SaveApply.click()

            time.sleep(4)

            rebootButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'reboot')))

            rebootButton.click()
            time.sleep(3)

            okButton = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[text()="OK"]')))
            okButton.click()
            time.sleep(3)

            # Победа, для проверки нужно проверить терминал

            print("Phone settings at" + ip + "updated successfully!")

        except Exception as e:

            print(ip + "An error occurred:", str(e))

    # Закрываем окно браузера
    driver.close()
# Запуск скрипта, для выбора достаточно убрать комменты
if __name__ == "__main__":
    automate_phone_settings()

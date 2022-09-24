import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

driver = webdriver.Chrome("chromedriver.exe")
driver.get("https://weather.com/en-MT/weather/hourbyhour/l/Huddersfield+England+United+Kingdom?canonicalCityId=9d2d451b1f11fcbd3a2cd65d86022f5113788c93903af32b8c77845f8c598d10")
# clear cookie pop up
time.sleep(5)
cookies = driver.find_element(by=By.ID, value="truste-consent-required")
cookies.click()
time.sleep(5)
# 
driver.fullscreen_window()
# make the driver keep trying to click if it's not working as intended
def clickRecurson(current, count):
    count = count+1
    if count == 100:
        raise "not working "
    try:
        current.click()
    except:
        time.sleep(2)
        clickRecurson(current, count)

HOURS = 24
uvs = []
# looks HOURS hours ahead
def findUvs(driver):
    for i in range(HOURS):
        current = driver.find_element(by=By.ID, value="detailIndex" + str(i))
        if current.text[1] == ":":
            currentHour = "0" + current.text[0]
        else:
            currentHour = current.text[0:2]
        clickRecurson(current, 0)
        # uv = current.find_element_by_css_selector('[data-testid="uvIndexSection"]')
        # print(current.text)
        uvHalf = current.text.split("UV Index")[1]
        if uvHalf[2] == " ":
            uv = uvHalf[1]
        else:
            uv = uvHalf[1:2]
        uvs.append((uv, currentHour))
        # time.sleep(5)


time.sleep(4)
driver.quit()
print(len(uvs))
import time
import writeEmail
from selenium import webdriver
from selenium.webdriver.common.by import By



def setup():
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get("https://weather.com/en-MT/weather/hourbyhour/l/Huddersfield+England+United+Kingdom?canonicalCityId=9d2d451b1f11fcbd3a2cd65d86022f5113788c93903af32b8c77845f8c598d10")
    # clear cookie pop up
    time.sleep(5)
    cookies = driver.find_element(by=By.ID, value="truste-consent-required")
    cookies.click()
    time.sleep(5)
    # 
    driver.fullscreen_window()
    return driver

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

# looks HOURS hours ahead
def findUvs(driver):
    HOURS = 24
    uvs = []
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
        print(str(i)+ " of " + str(HOURS) + "hours")
        # time.sleep(5)
    return uvs

def findDanger(uvs):
    dangers = []
    for i in range(len(uvs)):
        if int(uvs[i][0]) >=3:
            dangers.append(uvs[i])
    return dangers

def formatString(dangers):
    string = ""
    for i in dangers:
        string = string + "sun indx " + i[0] + " at "+ i[1]+" "
        string = string + "\n"
    return string

def getInfo():
    li = []
    with open("details.txt", "r") as file:
        for i in file:
            if i[-1] == "\n":
                li.append(i[0:-1])
            else:
                li.append(i)
    return li

def main():
    # pass
    driver = setup()
    uvs = findUvs(driver)
    dangers = findDanger(uvs)
    message = formatString(dangers)
    userDeats = getInfo()
    writeEmail.send_mail(message,"uv index" , userDeats[2], [userDeats[3]], userDeats[0], userDeats[1])
    time.sleep(4)
    driver.quit()
main()
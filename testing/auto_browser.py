import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np


def run_trace(filename):
    data = np.loadtxt(filename)

    driver = webdriver.Chrome()
    driver.get("file:///home/acer/Documents/ttstream/testing/web/index.html")

    IDX_DURATION = 1

    for item in data:
        next_elem = driver.find_elements_by_id("nextbutton")
        progress_elem = driver.find_elements_by_id("progress")
        actions = ActionChains(driver)
        actions.move_to_element(next_elem[0])
        actions.click(next_elem[0])
        actions.perform()

        while float(progress_elem[0].get_attribute("value")) < item[IDX_DURATION] - 0.4:
            print(f"Target duration: {item[IDX_DURATION]} - Actual duration: {float(progress_elem[0].get_attribute('value'))}")
            sleeptime = max(item[IDX_DURATION] - float(progress_elem[0].get_attribute("value")), 0.4)
            time.sleep(sleeptime)

        print(f"Target duration: {item[IDX_DURATION]} - Actual duration: {float(progress_elem[0].get_attribute('value'))}")

    driver.close()


filename = "./dataclean/data/128.237.82.1-0.txt"
run_trace(filename)
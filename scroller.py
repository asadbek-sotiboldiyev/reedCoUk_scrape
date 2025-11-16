
import time


def scrolling (driver):
    driver.execute_script("window.scrollTo(0, 0);")

    time.sleep(2)

    total_height = driver.execute_script("return document.body.scrollHeight")

    scroll_increment = total_height * 0.10

    for i in range(4):
        driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
        time.sleep(.5)

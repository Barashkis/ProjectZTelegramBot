from selenium.webdriver.common.by import By
from selenium import webdriver

from aiogram import Dispatcher

from loader import bot


async def get_screenshot(dp: Dispatcher, driver: webdriver, project_id: int):
    state = dp.current_state()
    data = await state.get_data()
    user_id = data["user_id"]
    all_projects = data["all_projects"]

    try:
        driver.get("https://zvezda.cam-program.ru/category/raschet-trudoemkosti/")

        count = 0
        while True:
            cards = driver.find_elements(By.CLASS_NAME, "category-raschet-trudoemkosti")[1:]
            for card in cards:
                count += 1
                url = card.find_element(By.TAG_NAME, "a").get_attribute("href")

                if count == project_id:
                    driver.get(url)

                    ele = driver.find_element(By.CLASS_NAME, "wp-block-group__inner-container")
                    total_height = ele.size["height"] + 1000

                    driver.set_window_size(1920, total_height)
                    screenshot_path = f"screenshots/{all_projects[project_id]}.png"
                    ele.screenshot(screenshot_path)

                    return screenshot_path
            try:
                previous = driver.find_element(By.XPATH, "//*[@id=\"content\"]/ul/li[1]/a")
            except Exception:
                break
            else:
                previous.click()
    except Exception as _ex:
        bot.send_message(user_id, "Что-то пошло не так... Пожалуйста, повторите попытку позже")


async def get_data(dp: Dispatcher, driver: webdriver):
    state = dp.current_state()
    data = await state.get_data()
    user_id = data["user_id"]

    try:
        driver.get("https://zvezda.cam-program.ru/category/raschet-trudoemkosti/")

        index_dict = {}
        count = 0
        while True:
            cards = driver.find_elements(By.CLASS_NAME, "category-raschet-trudoemkosti")[1:]
            for card in cards:
                count += 1
                title = card.find_element(By.TAG_NAME, "a").get_attribute("title")
                index_dict[count] = title
            try:
                previous = driver.find_element(By.XPATH, "//*[@id=\"content\"]/ul/li[1]/a")
            except Exception:
                break
            else:
                previous.click()

        return index_dict
    except Exception as _ex:
        bot.send_message(user_id, "Что-то пошло не так... Пожалуйста, повторите попытку позже")

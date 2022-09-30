from pathlib import Path

from selenium.webdriver.common.by import By
from selenium import webdriver

from aiogram import Dispatcher


async def get_screenshot(dp: Dispatcher, driver: webdriver.Chrome, project_id: int) -> str:
    state = dp.current_state()
    data = await state.get_data()
    all_projects = data["all_projects"]

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
                screenshot_path = str(Path(Path().resolve(), all_projects[project_id] + ".png"))
                ele.screenshot(screenshot_path)

                return screenshot_path
        try:
            previous = driver.find_element(By.XPATH, "//*[@id=\"content\"]/ul/li[1]/a")
        except Exception:
            break
        else:
            previous.click()


async def get_data(dp: Dispatcher, driver: webdriver.Chrome) -> dict:
    state = dp.current_state()

    driver.get("https://zvezda.cam-program.ru/category/raschet-trudoemkosti/")

    all_projects = {}
    count = 0
    while True:
        cards = driver.find_elements(By.CLASS_NAME, "category-raschet-trudoemkosti")[1:]
        for card in cards:
            count += 1
            title = card.find_element(By.TAG_NAME, "a").get_attribute("title")
            all_projects[count] = title

        try:
            previous = driver.find_element(By.XPATH, "//*[@id=\"content\"]/ul/li[1]/a")
        except Exception:
            break
        else:
            previous.click()

    await state.update_data({
        "all_projects": all_projects
    })

    return all_projects

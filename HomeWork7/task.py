from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import csv


def scroll_to_bottom(driver):
    size_length = driver.execute_script('return document.documentElement.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight);')
        time.sleep(2)
        size_new = driver.execute_script('return document.documentElement.scrollHeight')
        if size_new == size_length:
            break
        size_length = size_new


def get_video_data(driver):
    video_titles = driver.find_elements(By.XPATH, "//*[@id='video-title']")
    time_additions = driver.find_elements(By.XPATH, "//*[@id='metadata-line']/span[1]")
    views = driver.find_elements(By.XPATH, '//*[@id="metadata-line"]/span[2]')
   
    data = []
    for i in range(len(video_titles)):
        video_data = {
            'title': video_titles[i].text,
            'time_addition': time_additions[i].text,
            'views': views[i].text,            
        }
        data.append(video_data)
    return data


def save_to_json(data, filename='video.json'):
    with open(filename, 'w', encoding='U8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def save_to_csv(data, filename='video.csv'):
    with open(filename, 'w', encoding='U8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def main():
    user_agent = (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    )
    url = 'https://www.youtube.com/@varlamov/videos'
    chrome_option = Options()
    chrome_option.add_argument(f'user-agent={user_agent}')
    driver = webdriver.Chrome(options=chrome_option)

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        time.sleep(5)

        scroll_to_bottom(driver)

        data = get_video_data(driver)

        save_to_json(data)
        save_to_csv(data)

    except Exception as er:
        print(f'Error: {er}')
    finally:
        driver.quit()


if __name__ == '__main__':
    main()
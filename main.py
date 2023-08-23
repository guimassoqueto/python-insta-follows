from typing import List
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.webdriver import WebDriver
from app.settings import FOLLOWING_FILE, TOFOLLOW_FILE
from app.terms_to_ignore import check_username
from instagpy import InstaGPy


INSTAGRAM_URL = "https://www.instagram.com/"


def get_account_followers() -> List[dict]:
    user_input = input('type the account id to get followers: ')
    insta = InstaGPy(use_mutiple_account=False, session_ids=None,
                     min_requests=None, max_requests=None)
    followers = insta.get_user_friends(user_input, followers_list=True, followings_list=False, end_cursor=None, total=None)
    return followers


def write_to_follow_file(followers: List[dict]):
    with open(TOFOLLOW_FILE, 'a', encoding='utf-8') as f:
        for follower in followers:
            if follower["is_private"] or follower["is_possible_scammer"]: continue
            f.write(follower['username'] + "\n")


def write_following_file(username: str):
    with open(FOLLOWING_FILE, 'a', encoding='utf-8') as f:
        f.write(f"{username}\n")


def login() -> WebDriver:
    browser = webdriver.Chrome()
    browser.implicitly_wait(1)
    browser.get(INSTAGRAM_URL)
    sleep(5)
    username_input = browser.find_element(by=By.CSS_SELECTOR, value="input[name='username']")
    password_input = browser.find_element(by=By.CSS_SELECTOR, value="input[name='password']")
    username_input.send_keys("guanma.ltd@gmail.com")
    password_input.send_keys("deus te odeia 666")
    login_button = browser.find_element(by=By.XPATH ,value="//button[@type='submit']")
    login_button.click()
    return browser


def follow(browser: WebDriver, users: List[str]) -> None:
    today_follows = 0
    twenty_follows = 0 # no more than 20 at every 30 minutes
    
    for username in users:
        if check_username(username): continue

        if today_follows == 200: browser.close()
        if twenty_follows == 20: 
          sleep(60 * 30)
          twenty_follows = 0

        try:
          browser.get(INSTAGRAM_URL + username)
          sleep(10)
          
          has_stories = browser.find_element(by=By.CLASS_NAME, value="_aarg")
          follow_button = browser.find_element(by=By.TAG_NAME, value="button")

          if has_stories and follow_button and follow_button.text == "Follow": 
            follow_button.click()
            write_following_file(username)
          sleep(5)

        except Exception:
          continue

    browser.close()


def get_users_from_to_follow(filename: str) -> List[str]:
    users = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            users.append(line.strip())
    return users


def init_get_account_followers() -> bool:
    user_input  = input("Do you want to get followers from an Instagran account? [Y or N]")
    
    while user_input.strip().lower() not in ['y', 'n']:
        user_input = input("Invalid option. Do you want to get followers from an Instagran account? [Y or N]")

    if user_input == 'y': return True
    return False


def init_following() -> bool:
    user_input  = input("Users collected. Do you want to starting following now? [Y or N]")
    
    while user_input.strip().lower() not in ['y', 'n']:
        user_input = input("Invalid option. Do you want to starting following now? [Y or N]")

    if user_input == 'y': return True
    print("Following list file was written. ")
    return False

if __name__ == "__main__":
    try:
        if init_get_account_followers():
            followers = get_account_followers()
            write_to_follow_file(followers)
        
        if init_following():
            browser = login()
            users = get_users_from_to_follow(TOFOLLOW_FILE)
            sleep(30)
            follow(browser, users)
        
    except Exception as e:
       print(e)

import time
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException

import requests
from bs4 import BeautifulSoup
import random

test_url = "https://example.com"


# function to get the proxy list
def get_proxies():
    url = "https://free-proxy-list.net/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find(
        "table", attrs={"class": "table table-striped table-bordered"})
    proxies = []
    for row in table.find("tbody").find_all("tr"):
        ip = row.find_all("td")[0].text
        port = row.find_all("td")[1].text
        https = row.find_all("td")[6].text
        if https == "yes":
            proxies.append(f"{ip}:{port}")
    return proxies

# function to create multiple users with different ips from the proxy


def create_users(num_users):
    proxies = get_proxies()
    users = []
    for i in range(num_users):
        proxy = random.choice(proxies)
        print(f"Creating user with proxy: {proxy}")
        PROXY = proxy
        webdriver.DesiredCapabilities.FIREFOX['proxy'] = {
            "httpProxy": PROXY,
            "ftpProxy": PROXY,
            "sslProxy": PROXY,
            "proxyType": "MANUAL",
        }
        user = webdriver.Firefox()
        user.set_window_size(800, 200)
        user.get(test_url)
        users.append(user)
    return users

# function to randomly click on links


def random_click(user, max_iterations=10000, max_time=60000):
    iteration = 0
    start_time = time.time()
    while iteration < max_iterations and (time.time() - start_time) < max_time:
        try:
            # change as needed to match your site
            WebDriverWait(user, 10).until(EC.presence_of_element_located((By.XPATH, "//a[starts-with(@href, '/')]")))
            links = user.find_elements(By.XPATH, "//a[starts-with(@href, '/')]")
            link = random.choice(links)
            link.click()
            time.sleep(random.randint(3, 10))
            iteration += 1
        except (StaleElementReferenceException, NoSuchElementException, TimeoutException) as e:
            print(f"Error clicking link: {e}")
            pass
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    print(f"{iteration} links clicked by user {user} in {time.time() - start_time} seconds")
    # If an error occurs while clicking the link, remove the user from the list and start a new user
    if iteration == 0:
        user.quit()
        new_user = create_users(1)
        new_thread = threading.Thread(target=random_click, args=(new_user[0],))
        threads.append(new_thread)
        new_thread.start()




users = create_users(2)

# create a thread for each user and start the thread
threads = []
for user in users:
    t = threading.Thread(target=random_click, args=(user,))
    threads.append(t)
    t.start()

# wait for all threads to finish
for t in threads:
    t.join()


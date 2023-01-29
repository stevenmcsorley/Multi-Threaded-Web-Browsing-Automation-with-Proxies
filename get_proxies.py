import requests
from bs4 import BeautifulSoup

url = "https://free-proxy-list.net/"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Find the table containing the proxies
table = soup.find("table", attrs={"class": "table table-striped table-bordered"})

# Iterate through each row of the table
proxies = []
for row in table.find("tbody").find_all("tr"):
    # Extract the data from each column
    ip = row.find_all("td")[0].text
    port = row.find_all("td")[1].text
    code = row.find_all("td")[2].text
    country = row.find_all("td")[3].text
    anonymity = row.find_all("td")[4].text
    https = row.find_all("td")[6].text
    
    # Add the data to a list of proxies
    proxies.append(f"{ip}:{port}")

print(proxies)
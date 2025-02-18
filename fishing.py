import requests
from bs4 import BeautifulSoup
import pickle
import sys
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with open("data.pickle", "rb") as file:
    loaded_data = pickle.load(file)

url = "https://dwrapps.utah.gov/fishstocking/Fish?y=2025"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

try:
  response = requests.get(url, headers=headers, timeout=1)
  response.raise_for_status()
except (requests.RequestException, requests.exceptions.Timeout) as e:
  print()
  print("[ERROR] Could not connect to the internet to check UDWR fly fishing data.")
  print()
else:

  soup = BeautifulSoup(response.text, "lxml")
  vivian_new_cnt = str(soup).count("VIVIAN PARK P")
  provo_new_cnt = str(soup).count("PROVO R")

  if len(sys.argv) > 1 and sys.argv[1] == "--update":

      loaded_data["vivian_cnt"] = vivian_new_cnt
      loaded_data["provo_cnt"] = provo_new_cnt
      with open("data.pickle", "wb") as file:
          pickle.dump(loaded_data, file)

  else:

    print()
    found_flag = False

    if loaded_data["vivian_cnt"] != vivian_new_cnt:
        print("Vivian Park Pond has been stocked! (new stock count: " + str(vivian_new_cnt) + ")")
        found_flag = True

    if loaded_data["provo_cnt"] != provo_new_cnt:
        print("The Provo River has been stocked! (new stock count: " + str(provo_new_cnt) + ")")
        found_flag = True

    if not found_flag:
        print("No new UDWR fly fishing data found.")
    else:
        print(url)

    print()

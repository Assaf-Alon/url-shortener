# import unittest
import requests
import os
from termcolor import colored
import subprocess
from time import sleep
import signal
import test_utils

app_process = None
data = [
        {"short_url": "rick", "long_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        {"short_url": "admin_rick", "long_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ", "user_id": "nadav"},
        {"short_url": "flask", "long_url": "https://www.youtube.com/watch?v=GMppyAPbLYk", "user_id": "assaf"},
        {"short_url": "git", "long_url": "https://github.com/Assaf-Alon/url-shortener", "user_id": "nadav"},
        {"short_url": "1", "long_url": "https://www.google.com", "user_id": "user1"},
        {"short_url": "2", "long_url": "https://www.google.com", "user_id": "user2"},
        {"short_url": "3", "long_url": "https://www.google.com", "user_id": "user3"},
        {"short_url": "4", "long_url": "https://www.google.com", "user_id": "user4"},
        {"short_url": "5", "long_url": "https://www.google.com", "user_id": "user5"},
        {"short_url": "6", "long_url": "https://www.google.com", "user_id": "user6"},
        {"short_url": "11", "long_url": "https://www.google.com/maps", "user_id": "user1"},
        {"short_url": "12", "long_url": "https://www.google.com/maps", "user_id": "user2"},
        {"short_url": "13", "long_url": "https://www.google.com/maps", "user_id": "user3"},
        {"short_url": "14", "long_url": "https://www.google.com/maps", "user_id": "user4"},
        {"short_url": "15", "long_url": "https://www.google.com/maps", "user_id": "user5"},
        {"short_url": "16", "long_url": "https://www.google.com/maps", "user_id": "user6"},
        {"short_url": "21", "long_url": "https://www.google.com/photos", "user_id": "user1"},
        {"short_url": "22", "long_url": "https://www.google.com/photos", "user_id": "user2"},
        {"short_url": "23", "long_url": "https://www.google.com/photos", "user_id": "user3"},
        {"short_url": "24", "long_url": "https://www.google.com/photos", "user_id": "user4"},
    ]

def clear_db():
    print("Clearing Database...", end='')
    if os.path.exists("./database.db"):
        try:
            os.remove("./database.db")
            print("Removed DB...", end='')
        except:
            print(colored("Failed to clear DB", "red"))
            print("Try to see if there're any python processes running")
            exit()
    else:
        print("No DB found...", end='')
    print(colored("[OK]", "green"))

def init_db():
    print("Initializing DB...")
    
    for dat in data:
        res = requests.put(test_utils.BASE + "translate/" + dat['short_url'], dat)
        assert res.status_code == 201
        
    print(colored("[OK]", "green"))

def run_app():
    global app_process
    app_process = subprocess.Popen(["python", "./app.py"], shell=True)
    sleep(1)
    print(colored("[OK]", "green"))


def test_get_url_translations1():
    print("Testing GET on added records")
    for dat in data:
        short_url = dat['short_url']
        long_url = dat['long_url']
        user_id  = dat['user_id'] if 'user_id' in dat.keys() else "anonymous"
        test_utils.assert_get_request(short_url, long_url, user_id)
    print(colored("[OK]", "green"))
    
def test_get_url_translations2():
    print("Testing GET on record not added")
    test_utils.assert_get_request("not_added", status_code=404)
    print(colored("[OK]", "green"))
    
    
    

if __name__ == "__main__":
    clear_db()
    run_app()
    sleep(0.4)
    init_db()
    test_get_url_translations1()
    test_get_url_translations2()
    os.kill(app_process.pid, signal.CTRL_C_EVENT) # WORKS ON WINDOWS ONLY [PROBABLY]!!!
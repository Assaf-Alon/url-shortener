# import unittest
import requests
import os
from termcolor import colored
import subprocess
from time import sleep
import signal
import test_utils

TEST_TRANS = True
TEST_USERS = True


app_process = None
trans_data = [
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

user_data = [
    {"user_id": "nadav", "password": "nadav1", "email": "nadav@mail.com"},
    {"user_id": "assaf", "password": "assaf2", "email": "assaf@mail.com"},
    {"user_id": "user1", "password": "Aa123456", "email": "user1@mail.com"},
    {"user_id": "user2", "password": "Aa123456", "email": "user2@mail.com"},
    {"user_id": "user3", "password": "Aa123456", "email": "user3@mail.com"},
    {"user_id": "user4", "password": "Aa123456", "email": "user4@mail.com"},
    {"user_id": "user5", "password": "Aa123456", "email": "user5@mail.com"},
    {"user_id": "user6", "password": "Aa123456", "email": "user6@mail.com"}
    
]

def clear_db():
    print("Clearing Database... ", end='')
    if os.path.exists("./database.db"):
        try:
            os.remove("./database.db")
            print("Removed DB...", end='')
        except:
            print(colored("Failed to clear DB ", "red"))
            print("Try to see if there're any python processes running")
            exit()
    else:
        print("No DB found... ", end='')
    print(colored("[OK]", "green"))

def test_post_url_translations1():
    print("Initializing DB... ", end='')
    
    for dat in trans_data:
        res = requests.post(test_utils.BASE + "translate/" + dat['short_url'], dat)
        assert res.status_code == 201
        
    print(colored("[OK]", "green"))

def run_app():
    print("Running app... ")
    global app_process
    app_process = subprocess.Popen(["python", "./app.py"], shell=True)
    sleep(2.5)
    print(colored("[OK]", "green"))

def test_get_url_translations1():
    print("Testing GET on added records... ", end='')
    for dat in trans_data:
        short_url = dat['short_url']
        long_url = dat['long_url']
        user_id  = dat['user_id'] if 'user_id' in dat.keys() else "anonymous"
        test_utils.assert_get_translate(short_url, long_url, user_id)
    print(colored("[OK]", "green"))
    
def test_get_url_translations2():
    print("Testing GET on record not added... ", end='')
    test_utils.assert_get_translate("not_added", status_code=404)
    print(colored("[OK]", "green"))

def test_delete_url_translations1():
    print("Testing DELETE translation... ", end='')
    test_utils.assert_get_translate(trans_data[1]['short_url'], trans_data[1]['long_url'], trans_data[1]['user_id'])
    res = requests.delete(test_utils.BASE + "translate/" + trans_data[1]['short_url'])
    assert res.status_code == 204
    sleep(0.2)
    test_utils.assert_get_translate(short_url=trans_data[1]['short_url'], status_code=404)
    print(colored("[OK]", "green"))
    

def test_post_user1():
    print("Testing POST on users... ", end='')
    
    for user in user_data:
        res = requests.post(f"{test_utils.BASE}user/{user['user_id']}", user)
        assert res.status_code == 201
    print(colored("[OK]", "green"))
    
def test_get_user1():
    print("Testing GET on added users... ", end='')
    for user in user_data:
        test_utils.assert_get_user(user['user_id'], user)
    print(colored("[OK]", "green"))

def test_get_user2():
    print("Testing GET on user not added... ", end='')
    test_utils.assert_get_user("not_added", dict(), status_code=404)
    test_utils.assert_get_user("user1", dict(), status_code=403)
    
    user_dict = user_data[2]
    user_dict['password'] = "wrong"
    test_utils.assert_get_user("user1", user_dict, status_code=403)
    print(colored("[OK]", "green"))

def test_delete_user1():
    print("Testing DELETE user... ", end='')
    user = user_data[0]
    test_utils.assert_get_user(user['user_id'], user)
    res = requests.delete(f"{test_utils.BASE}user/{user['user_id']}")
    assert res.status_code == 204
    sleep(0.2)
    test_utils.assert_get_user(user['user_id'], dict(), 404)
    print(colored("[OK]", "green"))
    
    
    
# res = requests.get(test_utils.BASE + "translate/1")
# res = requests.delete(test_utils.BASE + "translate/1")
# res = requests.get(test_utils.BASE + "translate/1")


# user_dict = {"user_id": "nadav",
#              "password": "nadav1",
#              "email": "nadav@mail.com"}
# res = requests.get(test_utils.BASE + "user/nadav", user_dict)

# res = requests.post(test_utils.BASE + "user/nadav", user_dict)


engine = None

if __name__ == "__main__":
    clear_db()
    run_app()
    sleep(0.35)
    
    if TEST_TRANS:
        test_post_url_translations1()
        test_get_url_translations1()
        test_get_url_translations2()
        test_delete_url_translations1()
    
    if TEST_USERS:
        test_post_user1()
        test_get_user1()
        test_get_user2()
        test_delete_user1()
    
    os.kill(app_process.pid, signal.CTRL_C_EVENT) # WORKS ON WINDOWS ONLY [PROBABLY]!!!
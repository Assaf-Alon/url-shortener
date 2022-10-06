import requests

BASE = "http://127.0.0.1:5000/"
VERBOSE = False

def assert_get_translate(short_url, long_url="", user_id="", status_code=200):
    get_url = f"{BASE}translate/{short_url}"
    res = requests.get(get_url)
    if VERBOSE:
        print(f"[VERBOSE] requested {get_url}")
        print(f"[VERBOSE] response code: {res.status_code}")
        print(f"[VERBOSE] response: {res.json()}")
        print()
    assert res.status_code == status_code
    if status_code == 404:
        return
    assert res.json()[short_url]['short_url'] == short_url
    assert res.json()[short_url]['long_url']  == long_url
    assert res.json()[short_url]['user_id']   == user_id
    

def assert_get_user(user_id, user_dict, status_code=200):
    get_url = f"{BASE}user/{user_id}"
    res = requests.get(get_url, user_dict)
    if VERBOSE:
        print(f"[VERBOSE] requested {get_url}")
        print(f"[VERBOSE] body: {user_dict}")
        print(f"[VERBOSE] response code: {res.status_code}")
        print(f"[VERBOSE] response: {res.json()}")
        print()
    assert res.status_code == status_code
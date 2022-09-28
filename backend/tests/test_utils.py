import requests

BASE = "http://127.0.0.1:5000/"

def assert_get_request(short_url, long_url="", user_id="", status_code=200):
    res = requests.get(BASE + "translate/" + short_url)
    assert res.status_code == status_code
    if status_code == 404:
        return
    assert res.json()[short_url]['short_url'] == short_url
    assert res.json()[short_url]['long_url']  == long_url
    assert res.json()[short_url]['user_id']   == user_id
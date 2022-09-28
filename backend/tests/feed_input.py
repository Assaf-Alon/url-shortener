import requests

BASE = "http://127.0.0.1:5000/"

def init_db():
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

    for dat in data:
        res = requests.put(BASE + "translate/" + dat['short_url'], dat)
        print(res.json())


init_db()
print()

for i in range(21,25):
    res = requests.get(BASE + "translate/" + str(i))
    print(res.json())
    
    res = requests.delete(BASE + "translate/" + str(i))
    print(res)
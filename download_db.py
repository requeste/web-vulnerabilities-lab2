import requests as rq
from pathlib import Path

url = "http://localhost:8000/backup"

res = rq.get(url, allow_redirects=False, timeout=5)

if res.status_code == 200 and res.content.startswith(b"SQLite format 3\x00"):
    Path("downloaded.db").write_bytes(res.content)
    print("База данных загрузилась без проверки прав доступа")
else:
    print(f"База данных не загрузилась. HTTP {res.status_code}")
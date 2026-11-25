"""queue/ の投稿を X に出す。

- approved が true で、posted_id が空で、when が過ぎたものを、古い順に1件だけ投稿する
- 投稿したら posted_id と posted_at を書き戻す(コミットはワークフロー側)
- `python scripts/post_x.py check` はキーが使えるかだけを確かめる(投稿しない)

キーは環境変数から読む: X_API_KEY / X_API_SECRET / X_ACCESS_TOKEN / X_ACCESS_TOKEN_SECRET
"""
import json, os, sys, glob, datetime
import requests
from requests_oauthlib import OAuth1

API = "https://api.x.com/2"

def auth():
    return OAuth1(os.environ["X_API_KEY"], os.environ["X_API_SECRET"],
                  os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"])

def check():
    r = requests.get(f"{API}/users/me", auth=auth(), timeout=30)
    print("status", r.status_code)
    if r.ok:
        print("account:", r.json()["data"]["username"])
    else:
        print(r.text[:500]); sys.exit(1)

def upload(path):
    with open(path, "rb") as f:
        r = requests.post(f"{API}/media/upload", auth=auth(), timeout=120,
                          files={"media": (os.path.basename(path), f, "image/jpeg")},
                          data={"media_category": "tweet_image"})
    if not r.ok:
        print("upload failed", path, r.status_code, r.text[:500]); sys.exit(1)
    return r.json()["data"]["id"]

def due_items():
    now = datetime.datetime.now(datetime.timezone.utc)
    items = []
    for p in sorted(glob.glob("queue/*.json")):
        it = json.load(open(p, encoding="utf-8"))
        if not it.get("approved") or it.get("posted_id"):
            continue
        when = datetime.datetime.fromisoformat(it["when"])
        if when <= now:
            items.append((when, p, it))
    return sorted(items)

def post():
    items = due_items()
    if not items:
        print("nothing due"); return
    _, path, it = items[0]
    media_ids = [upload(img) for img in it.get("images", [])][:4]
    body = {"text": it["text"]}
    if media_ids:
        body["media"] = {"media_ids": media_ids}
    r = requests.post(f"{API}/tweets", auth=auth(), json=body, timeout=60)
    if not r.ok:
        print("post failed", r.status_code, r.text[:500]); sys.exit(1)
    it["posted_id"] = r.json()["data"]["id"]
    it["posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    json.dump(it, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("posted", path, it["posted_id"])

if __name__ == "__main__":
    check() if (len(sys.argv) > 1 and sys.argv[1] == "check") else post()

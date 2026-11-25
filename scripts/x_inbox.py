"""X の自分あてリプライ・メンションを inbox/x_mentions.jsonl に追記する(読むだけ。返信はしない)。
- 前回の続き(since_id)だけ取るので、読む量は最小限
- 返信を書くのは Claude の毎日の作業。書いた返信は queue/ に reply_to つきで置き、post_x.py が出す
"""
import json, os, sys, requests
from requests_oauthlib import OAuth1
API = "https://api.x.com/2"
STATE = "inbox/state.json"; OUT = "inbox/x_mentions.jsonl"
def auth():
    return OAuth1(os.environ["X_API_KEY"], os.environ["X_API_SECRET"], os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"])
def main():
    st = json.load(open(STATE)) if os.path.exists(STATE) else {}
    if "me" not in st:
        r = requests.get(f"{API}/users/me", auth=auth(), timeout=30); r.raise_for_status(); st["me"] = r.json()["data"]["id"]
    p = {"max_results": 50, "tweet.fields": "author_id,created_at,conversation_id,in_reply_to_user_id,referenced_tweets",
         "expansions": "author_id", "user.fields": "username,name"}
    if st.get("since_id"): p["since_id"] = st["since_id"]
    r = requests.get(f"{API}/users/{st['me']}/mentions", auth=auth(), params=p, timeout=30)
    print("status", r.status_code)
    if not r.ok: print(r.text[:300]); sys.exit(1)
    j = r.json(); users = {u["id"]: u for u in j.get("includes", {}).get("users", [])}
    data = list(reversed(j.get("data", [])))
    with open(OUT, "a", encoding="utf-8") as f:
        for t in data:
            u = users.get(t["author_id"], {})
            t["author"] = {"username": u.get("username"), "name": u.get("name")}
            t["status"] = "new"
            f.write(json.dumps(t, ensure_ascii=False) + "\n")
    if j.get("meta", {}).get("newest_id"): st["since_id"] = j["meta"]["newest_id"]
    json.dump(st, open(STATE, "w"), indent=2)
    print("new mentions:", len(data))
if __name__ == "__main__": main()

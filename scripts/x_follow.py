"""queue/follows/*.json の {"username": ..., "approved": true} を、1回に5件までフォローする。
大量フォローはXのルール違反(凍結の原因)なので、1日の上限は毎日の作業側で5件に抑える。
"""
import json, os, glob, datetime, requests
from requests_oauthlib import OAuth1
API = "https://api.x.com/2"
def auth():
    return OAuth1(os.environ["X_API_KEY"], os.environ["X_API_SECRET"], os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"])
def main():
    st = json.load(open("inbox/state.json")) if os.path.exists("inbox/state.json") else {}
    me = st.get("me") or requests.get(f"{API}/users/me", auth=auth(), timeout=30).json()["data"]["id"]
    n = 0
    for p in sorted(glob.glob("queue/follows/*.json")):
        it = json.load(open(p, encoding="utf-8"))
        if not it.get("approved") or it.get("followed_at") or it.get("error"): continue
        u = requests.get(f"{API}/users/by/username/{it['username']}", auth=auth(), timeout=30)
        if not u.ok or "data" not in u.json():
            it["error"] = f"lookup {u.status_code}"
        else:
            r = requests.post(f"{API}/users/{me}/following", auth=auth(), json={"target_user_id": u.json()["data"]["id"]}, timeout=30)
            if r.ok: it["followed_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            else: it["error"] = f"follow {r.status_code} {r.text[:120]}"
        json.dump(it, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print(p, it.get("followed_at") or it.get("error")); n += 1
        if n >= 5: break
    print("done", n)
if __name__ == "__main__": main()

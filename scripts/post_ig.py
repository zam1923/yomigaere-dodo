"""queue/ の投稿のうち "instagram" を持つものを、Instagramのリールとして出す。
- approved が true、ig_posted_id が空、when が過ぎたものを1件だけ
- 動画は resumable upload で直接送る(公開URLは不要)。Facebookログイン(ビジネス)のアプリが前提
- 環境変数: IG_USER_ID / IG_ACCESS_TOKEN (どちらも GitHub Secrets)
- `python scripts/post_ig.py check` はキーの確認だけ
"""
import json, os, sys, glob, time, datetime, requests
G = "https://graph.facebook.com/v25.0"
def tok(): return os.environ["IG_ACCESS_TOKEN"]
def uid(): return os.environ["IG_USER_ID"]
def check():
    r = requests.get(f"{G}/{uid()}", params={"fields": "username", "access_token": tok()}, timeout=30)
    print("status", r.status_code); print(r.json().get("username", r.text[:300])); r.raise_for_status()
def reel(video, caption):
    r = requests.post(f"{G}/{uid()}/media", data={"media_type": "REELS", "upload_type": "resumable", "caption": caption, "share_to_feed": "true", "access_token": tok()}, timeout=60)
    r.raise_for_status(); cid = r.json()["id"]
    size = os.path.getsize(video)
    with open(video, "rb") as f:
        u = requests.post(f"https://rupload.facebook.com/ig-api-upload/{cid}", headers={"Authorization": f"OAuth {tok()}", "offset": "0", "file_size": str(size)}, data=f, timeout=600)
    u.raise_for_status()
    for _ in range(60):
        s = requests.get(f"{G}/{cid}", params={"fields": "status_code", "access_token": tok()}, timeout=30).json()
        if s.get("status_code") == "FINISHED": break
        if s.get("status_code") == "ERROR": print(s); sys.exit(1)
        time.sleep(10)
    p = requests.post(f"{G}/{uid()}/media_publish", data={"creation_id": cid, "access_token": tok()}, timeout=60)
    p.raise_for_status(); return p.json()["id"]
def post():
    now = datetime.datetime.now(datetime.timezone.utc)
    for path in sorted(glob.glob("queue/*.json")):
        it = json.load(open(path, encoding="utf-8")); ig = it.get("instagram")
        if not ig or not it.get("approved") or it.get("ig_posted_id"): continue
        if datetime.datetime.fromisoformat(it["when"]) > now: continue
        it["ig_posted_id"] = reel(ig["video"], ig["caption"])
        json.dump(it, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("posted", path, it["ig_posted_id"]); return
    print("nothing due")
if __name__ == "__main__":
    if not os.environ.get("IG_ACCESS_TOKEN"): print("Instagram not connected yet"); sys.exit(0)
    check() if (len(sys.argv) > 1 and sys.argv[1] == "check") else post()

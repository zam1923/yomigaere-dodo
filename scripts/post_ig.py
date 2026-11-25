"""queue/ の投稿のうち "instagram" を持つものを、Instagramのリールとして出す。
- approved が true、ig_posted_id が空、when が過ぎたものを1件だけ
- 動画は resumable upload で直接送る(公開URLは不要)。Facebookログイン(ビジネス)のアプリが前提
- 環境変数: IG_USER_ID(workflowに直書き) / IG_ACCESS_TOKEN(GitHub Secrets)
- `python scripts/post_ig.py check` はキーの確認だけ。`inbox` はコメントを取ってくるだけ。ふだん(post)はコメントへの返信とリールの投稿
"""
import json, os, sys, glob, time, datetime, requests
G = "https://graph.facebook.com/v25.0"
def tok(): return os.environ["IG_ACCESS_TOKEN"]
def uid(): return os.environ["IG_USER_ID"]
def check():
    r = requests.get(f"{G}/{uid()}", params={"fields": "username", "access_token": tok()}, timeout=30)
    print("status", r.status_code); print(r.json().get("username", r.text[:300])); r.raise_for_status()
    d = requests.get(f"{G}/debug_token", params={"input_token": tok(), "access_token": tok()}, timeout=30).json().get("data", {})
    print("expires_at", d.get("expires_at"), "(0 = never)")
def reel(video, caption):
    r = requests.post(f"{G}/{uid()}/media", data={"media_type": "REELS", "upload_type": "resumable", "caption": caption, "share_to_feed": "true", "access_token": tok()}, timeout=60)
    if not r.ok: raise RuntimeError(f"container {r.status_code}: {r.text[:300]}")
    cid = r.json()["id"]; up = r.json().get("uri") or f"https://rupload.facebook.com/ig-api-upload/v25.0/{cid}"
    size = os.path.getsize(video)
    with open(video, "rb") as f:
        u = requests.post(up, headers={"Authorization": f"OAuth {tok()}", "offset": "0", "file_size": str(size)}, data=f, timeout=600)
    if not u.ok: raise RuntimeError(f"upload {u.status_code}: {u.text[:300]}")
    for _ in range(60):
        s = requests.get(f"{G}/{cid}", params={"fields": "status_code", "access_token": tok()}, timeout=30).json()
        if s.get("status_code") == "FINISHED": break
        if s.get("status_code") == "ERROR": print(s); sys.exit(1)
        time.sleep(10)
    p = requests.post(f"{G}/{uid()}/media_publish", data={"creation_id": cid, "access_token": tok()}, timeout=60)
    p.raise_for_status(); return p.json()["id"]
def inbox():
    """自分の最近の投稿についたコメントを inbox/ig_comments.jsonl に追記する(読むだけ)"""
    st_path = "inbox/ig_state.json"; out = "inbox/ig_comments.jsonl"
    st = json.load(open(st_path)) if os.path.exists(st_path) else {"seen": []}
    seen = set(st["seen"]); new = 0
    media = requests.get(f"{G}/{uid()}/media", params={"fields": "id,caption,timestamp", "limit": 10, "access_token": tok()}, timeout=30).json().get("data", [])
    with open(out, "a", encoding="utf-8") as f:
        for m in media:
            cs = requests.get(f"{G}/{m['id']}/comments", params={"fields": "id,text,username,timestamp", "limit": 50, "access_token": tok()}, timeout=30)
            if not cs.ok: print("comments failed", cs.status_code, cs.text[:200]); continue
            for c in cs.json().get("data", []):
                if c["id"] in seen or c.get("username") == "yomigaere_dodo": continue
                c["media_id"] = m["id"]; c["status"] = "new"
                f.write(json.dumps(c, ensure_ascii=False) + "\n"); seen.add(c["id"]); new += 1
    st["seen"] = sorted(seen)[-2000:]; json.dump(st, open(st_path, "w"), indent=1)
    print("new comments:", new)
def replies():
    """queue/ig_replies/*.json(ig_reply_to=コメントID)を、時刻が来たものから10件まで返信する"""
    now = datetime.datetime.now(datetime.timezone.utc); n = 0
    for path in sorted(glob.glob("queue/ig_replies/*.json")):
        it = json.load(open(path, encoding="utf-8"))
        if not it.get("approved") or it.get("ig_posted_id") or datetime.datetime.fromisoformat(it["when"]) > now: continue
        r = requests.post(f"{G}/{it['ig_reply_to']}/replies", data={"message": it["text"], "access_token": tok()}, timeout=30)
        if not r.ok: print("reply failed", path, r.status_code, r.text[:200]); continue
        it["ig_posted_id"] = r.json()["id"]; json.dump(it, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("replied", path); n += 1
        if n >= 10: break
def post():
    if os.path.exists("ig_paused"):   # Metaに止められている間は、無理に試さない(ブロックが深くなるのを防ぐ)
        print("instagram paused:", open("ig_paused").read().strip()); return
    now = datetime.datetime.now(datetime.timezone.utc)
    for path in sorted(glob.glob("queue/*.json")):
        it = json.load(open(path, encoding="utf-8")); ig = it.get("instagram")
        if not ig or not it.get("approved") or it.get("ig_posted_id"): continue
        if datetime.datetime.fromisoformat(it["when"]) > now: continue
        if it.get("ig_tries", 0) >= 3: continue   # 3回失敗したら、直すまで止める
        try:
            it["ig_posted_id"] = reel(ig["video"], ig["caption"])
        except Exception as e:
            it["ig_tries"] = it.get("ig_tries", 0) + 1; it["ig_error"] = str(e)[:300]
            json.dump(it, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
            print("ig failed", path, e); return
        json.dump(it, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("posted", path, it["ig_posted_id"]); return
    print("nothing due")
if __name__ == "__main__":
    if not os.environ.get("IG_ACCESS_TOKEN"): print("Instagram not connected yet"); sys.exit(0)
    mode = sys.argv[1] if len(sys.argv) > 1 else "post"
    if mode == "check": check()
    elif mode == "inbox": inbox()
    else:
        replies(); post()

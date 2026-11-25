"""自分の最近の投稿の反応(いいね・リポスト・表示回数など)を reports/YYYY-MM.md にまとめる。月1回。"""
import os, datetime, requests
from requests_oauthlib import OAuth1
A = OAuth1(os.environ["X_API_KEY"], os.environ["X_API_SECRET"], os.environ["X_ACCESS_TOKEN"], os.environ["X_ACCESS_TOKEN_SECRET"])
me = requests.get("https://api.x.com/2/users/me", auth=A, params={"user.fields": "public_metrics"}, timeout=30).json()["data"]
r = requests.get(f"https://api.x.com/2/users/{me['id']}/tweets", auth=A, timeout=30,
                 params={"max_results": 40, "tweet.fields": "created_at,public_metrics,text"}).json()
rows = []
for t in r.get("data", []):
    m = t["public_metrics"]
    rows.append((t["created_at"][:10], t["text"].split("\n")[0][:30], m.get("impression_count", 0), m["like_count"], m["retweet_count"], m["reply_count"], m.get("bookmark_count", 0)))
os.makedirs("reports", exist_ok=True)
name = datetime.date.today().strftime("reports/%Y-%m.md")
with open(name, "w", encoding="utf-8") as f:
    f.write(f"# 反応レポート {datetime.date.today()}\n\nフォロワー: {me['public_metrics']['followers_count']}\n\n| 日付 | 投稿 | 表示 | いいね | リポスト | 返信 | ブックマーク |\n|---|---|---|---|---|---|---|\n")
    for row in sorted(rows, reverse=True): f.write("| " + " | ".join(str(x) for x in row) + " |\n")
print(name)

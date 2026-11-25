# よみがえれ、ドードー 制作リポジトリ

絶滅動物16体の漫画「よみがえれ、ドードー」を作り、Xに投稿するための場所。オーナーはとりお(GitHub: zam1923)。

## 最初に読むもの
1. 設計書(Claude Docs): https://claude.ai/artifact/LYWU4MF8fYHmY2bh2ymi43 — 世界のルール、影の仕掛け、章立て、伏線、運営
2. `canon/settei_note.md` — いまどこまで描いたか、張った伏線、キャラの状態、次の候補

## 守ること
- 16体は人間の言葉を話さない。16体以外の生き物と人間は黒い影でだけ描く。ベッドなど人間の道具は使わない
- かわいい絵のまま、史実の過酷さはごまかさない。ただし血や死体は描かない
- 毎回同じ流れにしない。投稿の型も決めすぎない。日常回・わちゃわちゃ・不穏・山場を混ぜる
- 図鑑メモと年号は、出典を開いて確かめてから書く
- 描いたら必ず `canon/settei_note.md` を更新する(話の記録、伏線、キャラの状態、次の候補)

## 作り方
- 部品は `kit/`。各話は `episodes/epNN.py` に書き、リポジトリの直下から `python3 episodes/epNN.py` で `out/` にPNGができる(Playwright と Zen Maru Gothic を使う)
- 漫画は描いたあと、必ず3周「見直し→描き直し」をする。見るのは絵の出来より、話の因果が伝わるか:
  - コマとコマのあいだで「何が起きたか」が、初めて読む人に分かるか(分からなければ、原因か結果を1コマで見せる)
  - 新しいキャラの初登場や山場は、大ゴマのアップで見せる。ページの最後に置いて、めくった先で効かせる
  - 大事な瞬間を引きの絵で弱くしていないか
  - 毎周、コマごとに問題を書き出し、直してから描き直す。3周目で問題がなくなるまで出さない
- 「つづく」は、その日の投稿の最後の1枚にだけ入れる。途中の枚には入れない
- 出来た絵は、JPEG(5MB未満)にして `episodes/pages/` に置く
- キャラデザの元データは `art/design_canvas/`(Claude Design のキャンバスと同じもの)

## ほかの媒体
- リール動画: 漫画を描いたら `python3 kit/reel.py epNN "第N話　タイトル" "図鑑メモ"` で `reels/epNN.mp4` を作り(音はBGMと効果音を kit/sound.py で一から合成。各話ファイルの REEL に、コマごとの明暗 mood と効果音 sfx を書く。市販の曲や素材は使わない)、その話のキューに `"instagram": {"video": ..., "caption": ...}` を足す。Instagramのキー(IG_USER_ID / IG_ACCESS_TOKEN)が Secrets に入るまでは、自動で飛ばされる
- LINEスタンプ: `stamps/`。第1弾はトト8種(`stamps/set1/`、`python3 stamps/make_set1.py` で申請用 `stamps/set1_line.zip` もできる。文言は `stamps/set1_listing.md`)。8種でキャラの大きさをそろえ、余白10pxで枠いっぱいに描く。申請はとりおがLINE Creators Marketで行う。仲間が増えたら、その子を入れた弾を作って知らせる
- 反応レポート: GitHub Actions `monthly-report` が毎月1日に `reports/YYYY-MM.md` を作る。毎週の制作では最新のレポートを読み、よく見られた種類やキャラを次の週に反映する

## 投稿
- `queue/NNNN_*.json` に1投稿ずつ置く: `when`(ISO時刻、+09:00)、`text`、`images`(最大4枚)、`approved`、`posted_id`
- 新しく置くものは必ず `"approved": false`。とりおがOKを出したものだけ `true` にする
- GitHub Actions の `post-to-x` が毎時、時刻の来た承認済みを1件ずつ投稿して `posted_id` を書き戻す
- Xのキーは GitHub の Secrets にだけある。読まない、書かない、ログに出さない

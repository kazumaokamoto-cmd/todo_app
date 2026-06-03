26/05/30
だいたいうまくいったがtodoをクリックしたときに
Not Found
The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.
が表示される
ルーティングがよくわからない
todoとidは紐づいているはずなのでわざわざcomplete/idなんてしなくてもできそうな気がするが
原因多分引数の名前がミスってた


26/05/31
バグlist index out of range問題
原因forで削除をしていたが削除すると要素数が減る
解決策
最後にまとめて消す
リスト内包表記


ver2.0
デザイン面を改善
チェックボタンをクリックするのではなくタスクをクリックしたら消えるようにしたい
あとは細かいところをやればいいかな
あと、archiveが見れるページも作りたい


todoをクリックして達成できない

06/02
関数の使いまわしについて
load_csvはpathを引数にしておく
こうすることでnormal_csvとweekly_csv両方で使えるようにする
save_csvも同様
save_csvは実質idつけて保存するだけなので

06/03
ver2.1はとりあえず動くようになった
id管理がめんどい（達成したときの処理とか）のでweeky.csvの廃止
weeklytodoも追加されるが再読み込みをしたときに増殖してしまう

date型で比較したらうまくいかんかった
intにしたらできた
# DeepLabCut支援ツール
研究で行う前処理とか解析を行うツール

<img src="https://github.com/alrab223/DeepLabCut_Analyzes/blob/make_GUI/static/readme/gui.png" width="500px">

製作中の画像

<img src="https://github.com/alrab223/DeepLabCut_Analyzes/blob/make_GUI/static/readme/roly.gif">

DLCでラベリングしたダンゴムシ
## Q,これは何ですか

DEEPLABCUTのデータセットを作成する際、データセットの選択を手っ取り早く終わらせ、任意の部位のラベリングをもっと手軽に行えるようにしたかった


よく使うけどツールが分散してるとか、無料版では使えない機能を自分で実装して、寄せ集めたのがこのツールです。

以下の機能を実装しています。

* 動画のクロッピング
* 動画からフレームを抽出
* ランダムでフレームを抽出
* DEEPLABCUTで作成したCSVから動画のラベリング

他、機能追加予定。

今後、どの端末からも利用できるようにウェブアプリにする予定

## 1. pipenvの準備
pipenvが必要です。
```sh
$ pip install pipenv
```
インストール後は同様に、以下のコマンドを実行してください。
```sh
$ pipenv install
$ pipenv shell
```

## 2. Git Large File Storageのインストール
このリポジトリはGit Large File Storageを使用しています。OS別で準備が必要です。
## MacOS
Homebrewで下記のコマンドを実行

```sh
$ brew install git-lfs
```
インストール後、リポジトリで、以下のコマンドを実行すれば完了です。
```sh
$ git lfs install
```

## Windows
Git for WindowsにはGit LFSが含まれているので、インストールは不要です。リポジトリで以下のコマンドを実行してください。
```sh
$ git lfs install
```

## Ubuntu
Ubuntuでは、以下のコマンドでインストールしてください
```sh
$ sudo apt install git-lfs
```
インストール後は同様に、以下のコマンドを実行してください。
```sh
$ git lfs install
```

## 3. 使用方法
起動するにはmain.pyを実行してください
```sh
$ python main.py
```
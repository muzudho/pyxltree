# 第２章：　test.pypi.org に Python パッケージをアップロードし、動作確認する

* [test.pypi.org](https://test.pypi.org/) にアカウントを開設、２要素認証も設定


## 第１節：　test.pypi.org にログイン

アカウントは既に作っているものとします。  
test.pypi.org と pypi.org はアカウントは別管理です。  

📖 [test.pypi.org　＞　ログイン画面](https://test.pypi.org/account/login/?next=%2Fmanage%2Faccount%2F#api-tokens)  

Microsoft Authentication などを使って、二要素認証を行います。  


# 第２節：　README.md について

トップ・ディレクトリーの 📄 `README.md` テキストは pypi.org のパッケージのページの README としても使われるので、それを想定して書くこと。  
画像は相対パスではなくURLを指定すること  


# 第３節：　test.pypi.org へのデプロイについて

とりあえずこれを読め  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

```shell
py -m pip install --upgrade pip
py -m pip install --upgrade build
py -m pip install --upgrade twine
```

👇　ディレクトリー階層は以下のようにする  

```plaintext
📁 {REPOSITORY_NAME}/    # GitHub のリポジトリー名に対応。詳しくはソースコードの現物参照
└─ 📄 src/
    └─ 📄 {PACKATE_NAME}/    # Python パッケージ名に対応。詳しくはソースコードの現物参照
        ├─ 📄 __init__.py
        └─ others...
```


# 第４節：　環境のアップデート

👇　pip をアップデートする  

```shell
py -m pip install --upgrade pip
```

👇　pypi にアップロードできる形式にファイル圧縮してくれるパッケージをインストールする  

```shell
py -m pip install --upgrade build
```

👆 `build` は、 📄 `pyproject.toml` ファイルで指定したビルドツールを使ってくれる  


# 第５節：　環境の確認

例では、ビルドツールに Hatchling を使っているので真似てみる  

* 📖 [Hatchling > Build system](https://hatch.pypa.io/latest/config/build/#build-system)

👇  インストールしておく必要があるパッケージを調べる方法はないが、以下のコマンドが利用できるので調べておくこと。関係ないパッケージ名も出てくるので、手動で選別する必要がある  

```shell
pip freeze
```


# 第６節：　📄［pyproject.toml］ファイルを更新

📄 `pyproject.toml` を書く。トップディレクトリーに置いてある現物を参照  


# 第７節：　build 実行

`build` を**実行する前**に:  

* 📄 `pyproject.toml` のバージョンを設定したか確認しておくこと
* デプロイしたいファイルで、GitHub にプッシュし忘れているファイルが残っていれば、プッシュしてください
* ファイルの保存のし忘れがあれば、ファイルの保存をしてください

👇 pyproject.toml を書き上げたら、 `build` を実行する  

```shell
py -m build
```

`build` を実行すると、 `dist` フォルダーが作成される  

例：  

```plaintext
📁 dist/
├─ 📄 {PACKATE_NAME}-0.0.1-py2.py3-none-any.whl     # Python パッケージ名に対応。詳しくはソースコードの現物参照
└─ 📄 {PACKATE_NAME}-0.0.1.tar.gz
```

これが pypi にアップロードするファイルだ  


# 第８節：　test.pypi.org にログイン

[test.pypi.org](https://test.pypi.org/) に Fire Fox でログインする（Google Chrome や Edge では二要素認証が通らないことがあった）  

https://test.pypi.org/account/login/

**test.pypi.org の［アカウント設定］の［API トークン］の欄から、［APIトークンの追加］ボタンをクリックする。**  
スコープは `アカウント全体` を選ぶ。発行されたAPIトークンは再発行されないので、どこかに記憶しておく  


# 第９節：　twine をインストール

👇 twine をインストールする

```shell
py -m pip install --upgrade twine
```

👇　アップデート

```shell
pip install --upgrade pkginfo
#pip install --upgrade twine
```

👇　書式チェック

```shell
twine check dist/*
```

* エラーがでたら、書式を確認する。
    * 📖 [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)


# 第１０節：　twine を実行する

twine を実行する前に、 📄 `pyproject.toml` のバージョンの数を設定（２回目以降なら上げる）しておくこと  

👇 twine を実行する  

```shell
py -m twine upload --repository testpypi --verbose dist/*
```

APIトークンを尋ねられるので、 `pypi-` プレフィックスを付けたまま入力する  


# 第１１節：　アップロードされたものを確認しにいく

👇 アップロードされたら、test.pypi.org を見に行く  

https://test.pypi.org/project/xltree/0.0.1/  


## デプロイのための参考記事

* 📖 [【Python】PyPIに自作ライブラリを登録する](https://qiita.com/gsy0911/items/702f43100e5abdefd318)
    * 📖 [PyPIパッケージ定義ファイル作成方法 - __init__.py setup.py MANIFEST.in の書き方](https://qiita.com/shinichi-takii/items/6d1063e0aa3f79e599f0)
* 📖 [【GitHub Actions】自作Pythonパッケージを自動ビルドしてPyPIとGitHubリリースまで一気にデプロイする](https://qiita.com/hanaosan/items/83194c4cd6c80fc3c377)

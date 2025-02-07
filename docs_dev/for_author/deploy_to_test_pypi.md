# 第２章：　test.pypi.org に Python パッケージをアップロードし、動作確認する

* [test.pypi.org](https://test.pypi.org/) にアカウントを開設、２要素認証も設定


## 第１節：　設計時の確認

### 第１項：　README.md について

トップ・ディレクトリーの 📄 `README.md` テキストは pypi.org のパッケージのページの README としても使われるので、それを想定して書くこと。  
画像は相対パスではなくURLを指定すること  


### 第２項：　ディレクトリー階層の例

👇　ディレクトリー階層は以下のようにする  

```plaintext
📁 {REPOSITORY_NAME}/    # GitHub のリポジトリー名に対応。詳しくはソースコードの現物参照
└─ 📄 src/
    └─ 📄 {PACKATE_NAME}/    # Python パッケージ名に対応。詳しくはソースコードの現物参照
        ├─ 📄 __init__.py
        └─ others...
```


## 第２節：　build 実行

### 第１項：　事前確認

`build` を**実行する前**に:  

* 📄 `pyproject.toml` のバージョンを設定したか確認しておくこと
* デプロイしたいファイルで、GitHub にプッシュし忘れているファイルが残っていれば、プッシュしてください
* ファイルの保存のし忘れがあれば、ファイルの保存をしてください


### 第２項：　実行

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


## 第３節：　アップロード

### 第１項：　書式チェック

👇　書式チェック。圧縮ファイルに対して行う  

```shell
twine check dist/*
```

* エラーがでたら、書式を確認する。
    * 📖 [Writing your pyproject.toml](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)


### 第２項：　twine を実行する

twine を実行する前に、 📄 `pyproject.toml` のバージョンの数を設定（２回目以降なら上げる）しておくこと  

👇 twine を実行する  

```shell
py -m twine upload --repository testpypi dist/*

# 細かいログが見たいとき
#py -m twine upload --repository testpypi --verbose dist/*
```

APIトークンを尋ねられるので、 `pypi-` プレフィックスを付けたまま入力する  


## 第３節：　アップロードされたものを確認しにいく

### 第１項：　test.pypi.org にログイン

👇 アップロードされたら、test.pypi.org を見に行く  

[test.pypi.org](https://test.pypi.org/) に Fire Fox でログインする（Google Chrome や Edge では二要素認証が通らないことがあった）  

https://test.pypi.org/account/login/

**test.pypi.org の［アカウント設定］の［API トークン］の欄から、［APIトークンの追加］ボタンをクリックする。**  
スコープは `アカウント全体` を選ぶ。発行されたAPIトークンは再発行されないので、どこかに記憶しておく  


## 第４節：　デプロイのための参考記事

* 📖 [【Python】PyPIに自作ライブラリを登録する](https://qiita.com/gsy0911/items/702f43100e5abdefd318)
    * 📖 [PyPIパッケージ定義ファイル作成方法 - __init__.py setup.py MANIFEST.in の書き方](https://qiita.com/shinichi-takii/items/6d1063e0aa3f79e599f0)
* 📖 [【GitHub Actions】自作Pythonパッケージを自動ビルドしてPyPIとGitHubリリースまで一気にデプロイする](https://qiita.com/hanaosan/items/83194c4cd6c80fc3c377)

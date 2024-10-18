# 作者本人向けドキュメント

# README.md について

トップ・ディレクトリーの 📄 `README.md` テキストは pypi.org のパッケージのページの README としても使われるので、それを想定して書くこと  

# pypi へのデプロイについて

とりあえずこれを読め  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

```shell
py -m pip install --upgrade pip
```

ディレクトリー階層は以下のようにする  

```plaintext
📁 pyxltree/    # GitHub のリポジトリー名に対応
└─ 📄 src/
    └─ 📄 xltree/    # Python パッケージ名に対応
        ├─ 📄 __init__.py
        └─ others...
```

例では、ビルドツールに Hatchling を使っているので真似てみる

```shell
py -m pip install --upgrade build
```

* 📖 [Hatchling > Build system](https://hatch.pypa.io/latest/config/build/#build-system)

👇 pyproject.toml を書き上げたら、 `build` を実行する  

```shell
py -m build
```

`build` を実行すると、 `dist` フォルダーが作成される  

例：  

```plaintext
📁 dist/
├─ 📄 xltree-0.0.1-py2.py3-none-any.whl
└─ 📄 xltree-0.0.1.tar.gz
```

これが pypi にアップロードするファイルだ  

[test.pypi.org](https://test.pypi.org/) に Fire Fox でログインする（Google Chrome や Edge では二要素認証が通らないことがあった）  

https://test.pypi.org/account/login/

test.pypi.org にAPIトークンを追加する。スコープは `アカウント全体` を選ぶ。発行されたAPIトークンは再発行されないので、どこかに記憶しておく  

👇 twine をインストールする

```shell
py -m pip install --upgrade twine
```

👇 twine を実行する  

```shell
py -m twine upload --repository testpypi dist/*
```

APIトークンを尋ねられるので、 `pypi-` プレフィックスを付けたまま入力する  

👇 アップロードされたら、test.pypi.org を見に行く  

https://test.pypi.org/project/xltree/0.0.1/  

# デプロイのためのオーバービュー

次の３ステップ

* (Step 1) Python パッケージを作成する
* (Step 2) [test.pypi.org](https://test.pypi.org/) に Python パッケージをアップロードし、動作確認する
* (Step 3) [pypi.org](https://pypi.org/) に Python パッケージをアップロードする

## (Step 1) Python パッケージを作成する

### 📄 `requirements.txt` ファイルを作成する

```shell
pip freeze > requirements.txt
```

👆 関係ないものも含まれているので手動で整理する  

* 📖 [How to install Python packages with pip and requirements.txt](https://note.nkmk.me/en/python-pip-install-requirements/)

📄 `pyproject.toml` ファイルの dependencies の項目に移した方がいいか？

### 📄 `pyproject.toml` ファイルを作成する

* 📖 [pyproject.toml を書く](https://packaging.python.org/ja/latest/guides/writing-pyproject-toml/)
* 📖 [【GitHub Actions】自作Pythonパッケージを自動ビルドしてPyPIとGitHubリリースまで一気にデプロイする](https://qiita.com/hanaosan/items/83194c4cd6c80fc3c377)

## (Step 2) test.pypi.org に Python パッケージをアップロードし、動作確認する

* test.pypi.org にアカウントを開設、２要素認証も設定

# デプロイのための参考記事

* 📖 [【GitHub Actions】自作Pythonパッケージを自動ビルドしてPyPIとGitHubリリースまで一気にデプロイする](https://qiita.com/hanaosan/items/83194c4cd6c80fc3c377)
* 📖 [【Python】PyPIに自作ライブラリを登録する](https://qiita.com/gsy0911/items/702f43100e5abdefd318)
    * 📖 [PyPIパッケージ定義ファイル作成方法 - __init__.py setup.py MANIFEST.in の書き方](https://qiita.com/shinichi-takii/items/6d1063e0aa3f79e599f0)

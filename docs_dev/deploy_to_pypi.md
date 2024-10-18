# pypi にデプロイする

# README.md について

トップ・ディレクトリーの 📄 `README.md` テキストは pypi.org のパッケージのページの README としても使われるので、それを想定して書くこと。  
画像は相対パスではなくURLを指定すること  

# pypi へのデプロイについて

とりあえずこれを読め  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

👇　pip をアップデートする  

```shell
py -m pip install --upgrade pip
```

👇　ディレクトリー階層は以下のようにする  

```plaintext
📁 pyxltree/    # GitHub のリポジトリー名に対応
└─ 📄 src/
    └─ 📄 xltree/    # Python パッケージ名に対応
        ├─ 📄 __init__.py
        └─ others...
```

👇　pypi にアップロードできる形式にファイル圧縮してくれるパッケージをインストールする  

```shell
py -m pip install --upgrade build
```

`build` は、 📄 `pyproject.toml` ファイルで指定したビルドツールを使ってくれる  

例では、ビルドツールに Hatchling を使っているので真似てみる  

* 📖 [Hatchling > Build system](https://hatch.pypa.io/latest/config/build/#build-system)

📄 `pyproject.toml` を書く。トップディレクトリーに置いてある現物を参照  

`build` を実行する前に、 📄 `pyproject.toml` のバージョンを設定したか確認しておくこと  

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

twine を実行する前に、 📄 `pyproject.toml` のバージョンの数を上げておくこと  

👇 twine を実行する  

```shell
py -m twine upload --repository testpypi dist/*
```

APIトークンを尋ねられるので、 `pypi-` プレフィックスを付けたまま入力する  

👇 アップロードされたら、test.pypi.org を見に行く  

https://test.pypi.org/project/xltree/0.0.1/  

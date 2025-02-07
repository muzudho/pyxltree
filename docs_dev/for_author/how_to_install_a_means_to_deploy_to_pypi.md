# PyPI にデプロイする手段をインストールする方法


## 第１節：　詳しくは

とりあえずこれを読め。詳しくは後述する。  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)


## 第２節：　pip パッケージのアップデート

👇　pip をアップデートする  

```shell
py -m pip install --upgrade pip
```


## 第３節：　build パッケージのアップデート

build パッケージは、pypi にアップロードできる形式にファイル圧縮してくれるツール  

```shell
py -m pip install --upgrade build
```

👆 `build` は、 📄 `pyproject.toml` ファイルで指定したビルドツールを使ってくれる  


## 第４節：　📄［pyproject.toml］ファイルの記述

### 第１項：　どのビルドツールを使うか決める

例では、ビルドツールに Hatchling を使っているので真似てみる  

* 📖 [Hatchling > Build system](https://hatch.pypa.io/latest/config/build/#build-system)


### 第２項：　プロジェクトで使用しているパッケージを調べる

👇  インストールしておく必要があるパッケージを調べる方法はないが、以下のコマンドが利用できるので調べておくこと。関係ないパッケージ名も出てくるので、手動で選別する必要がある  

```shell
pip freeze
```


### 第３項：　📄［pyproject.toml］ファイルを書く

📄 `pyproject.toml` を書く。トップディレクトリーに置いてある現物を参照  

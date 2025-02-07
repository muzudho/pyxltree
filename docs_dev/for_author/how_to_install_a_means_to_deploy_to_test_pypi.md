# PyPI にデプロイする手段をインストールする方法


## 第１節：　詳しくは

### 第１項：

とりあえずこれを読め。詳しくは後述する。  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)


### 第２項：　test.pypi.org にログイン

これは確認するだけ。アカウントは既に作っているものとします。  
test.pypi.org と pypi.org はアカウントは別管理です。  

📖 [test.pypi.org　＞　ログイン画面](https://test.pypi.org/account/login/?next=%2Fmanage%2Faccount%2F#api-tokens)  

Microsoft Authentication などを使って、二要素認証を行います。  


## 第２節：　パッケージのインストール、またはアップデート

### 第１項：　pip パッケージ

```shell
py -m pip install --upgrade pip
```


### 第２項：　build パッケージのアップデート

```shell
py -m pip install --upgrade build
```

👆 build パッケージは、pypi にアップロードできる形式にファイル圧縮してくれるツール。  
📄 `pyproject.toml` ファイルで指定したビルドツールを使ってくれる  


### 第３項：　twine パッケージ

```shell
py -m pip install --upgrade twine
```

👆 `twine` は、圧縮されたファイルを pypi ウェブサイトへアップロードする  


### 第４項：　pkginfo パッケージ

```shell
pip install --upgrade pkginfo
```


### 第５項：　packaging パッケージの削除

```shell
pip install -U packaging
```

👆　古いから、アンインストールしてください  


## 第３節：　📄［pyproject.toml］ファイルの記述

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

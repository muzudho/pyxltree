# 作者本人向けドキュメント

とりあえずこれを読め  

* 📖 [Packaging Python Projects](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

```shell
py -m pip install --upgrade pip
```

ディレクトリー階層は以下のようにする  

```
📁 pyxltree/    # GitHub のリポジトリー名に対応
└─ 📄 src/
    └─ 📄 xltree/    # Python パッケージ名に対応
        ├─ 📄 __init__.py
        └─ others...
```


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

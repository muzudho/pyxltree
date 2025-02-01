# 第１章：　Python パッケージを作成する


## 第１節：　📄［`requirements.txt`］ファイルを作成する

```shell
pip freeze > requirements.txt
```

👆 関係ないものも含まれているので手動で整理する  

* 📖 [How to install Python packages with pip and requirements.txt](https://note.nkmk.me/en/python-pip-install-requirements/)

後述の　📄［`pyproject.toml`］ファイルの dependencies の項目に移した方がいいか？


## 第２節：　📄［`pyproject.toml`］ファイルを作成する

プロジェクト・ルートに📄［`pyproject.toml`］ファイルを作成してください。  
既存のリポジトリーを真似るのが早いでしょう。  

* 📖 [pyproject.toml を書く](https://packaging.python.org/ja/latest/guides/writing-pyproject-toml/)
* 📖 [【GitHub Actions】自作Pythonパッケージを自動ビルドしてPyPIとGitHubリリースまで一気にデプロイする](https://qiita.com/hanaosan/items/83194c4cd6c80fc3c377)

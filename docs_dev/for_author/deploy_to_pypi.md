# 第３章：　pypi にデプロイする


## 第１節： pypi.org へのデプロイについて

test.pypi.org と pypi.org は別アカウントなので、ログインし直す。  

https://pypi.org/account/login/


アカウント設定画面から、APIトークンも発行する  

`twine` のコマンド引数が変わる  

```shell
twine upload dist/*
```

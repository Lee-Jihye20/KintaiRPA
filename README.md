# KintaiRPA
KINGOFTIME勤怠出力RPA
ファイル説明:
### app_icon.ico:アイコンファイル
### key:鍵ファイル
### SavedData:ID・パスワード保存ファイル
### security.py:PEM生成・暗号化・復号化ファイル
### itemlist.py:項目リストファイル
**kintai.py:勤怠出力ファイル**
### window.py:ウィンドウ(Tkinter)ファイル
### Pipfile・Pipfile.lock:pyenvの環境ファイル
### build.spec:pyinstallerのビルドファイル

各説明
- プロジェクトのビルド方法:
    - ターミナルを開き、プロジェクトのディレクトリに移動
    - pyinstaller build.spec
    - ビルドが完了したら、distフォルダに実行ファイルが生成される
    - アイコンやファイル名を変えたい場合はbuild.specを変更する(https://qiita.com/kotai2003/items/170900c426db037b5a17)
- 開発環境での実行方法:
    - ターミナルを開き、プロジェクトのディレクトリに移動
    - pipenv sync(初回のみ、pipfile.lockをもとにpipenvの環境を構築)
    - pipenv shell(仮想環境に入る)
    - python window.py(実行)
    > pipのライブラリなどを新たに読み込む場合pipenv install ライブラリ名で実行すること


初めての実践なので読みづらい・効率の悪い部分あると思いますが、ご了承ください。
お仕事頑張ってください、よろしくお願いします。

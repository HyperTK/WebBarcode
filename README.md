# バーコードスキャン + Web

# 環境構築
Raspberry pi上にNginx + uWSGIを稼働させ、FlaskでWebからバーコードを読み取るシステムの環境を準備する方法を記す。

## nginx + Flask + raspberry pi
### デバイス
* Raspberry pi3 Model B+
* microusbメモリ 16GB
* BUFFALO BSW200MBK(Webカメラ)

### pythom modules
sudo pip3 installしたものたち。インストールの詳細は「手順」の項目にて。

* flask(0.12.1)
* pymssql(2.1.4)
* opencv-python(3.4.4.19)
* pyzbar(0.1.8)

### Web
* CSS framework : materialize 1.0.0

### 手順
#### ラズパイセットアップ
  * Wifi接続設定
  * インターフェース設定にてCameraをEnable
  * パッケージマネージャ更新
    * sudo apt update
    * sudo apt upgrade
  * 必ずsudo rpi-update すること

#### モジュールセットアップ
* OpenCVインストール
    
    カメラの制御に使用するモジュール。

    参考 : http://asukiaaa.blogspot.com/2018/07/pythonopencvraspi.html
    
    * OpenCVのビルドに必要なパッケージをインストールする
        ``` shell
        sudo apt install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
        ```

    * pipでOpenCVをインストールする
        ``` shell
        $ sudo pip3 install opencv-python
        ```

    * OpenCV実行時に必要なパッケージをインストールする
        ``` shell
        $ sudo apt install libcblas-dev libatlas3-base libilmbase12 libopenexr22 libgstreamer1.0-0 libqtgui4 libqttest4-perl
        ```

    * インストールの確認
        ``` shell
        コンソールでpython起動
        $ python3
        ```
        ``` python
        # 下記でインストール確認
        import cv2
        cv2.__version__
        ```

* pymssqlインストール

    ラズパイからMicrosoftのSqlserverに接続するモジュール。必要であればインストールする。

    参考 : https://hotch-potch.hatenadiary.jp/entry/2019/02/15/203500

    * pymssqlのコンパイルに必要なライブラリをインストール
        ``` shell
        $ sudo apt-get install freetds-dev -y
        ```
    
    * pymssqlをインストール
        ``` shell
        10分程度時間を要するため、フリーズしたと思って消さないように注意！
        $ sudo pip3 install pymssql
        ```

* pyzbarをインストール
    
    バーコードを認識するためのモジュール
    ```
    $ sudo pip3 install pyzbar
    ```

* flaskをインストール

    PythonでWebサービスを構築するための軽量フレームワーク。インストール済みの場合もあり。

    ```
    $ sudo pip3 install flask
    ※インストール済みの場合は下記のメッセージ
    Requirement already satisfied: flask in /usr/lib/python3/dist-packages
    ```

#### NginxとuWSGIのインストールおよび設定
参考(インストール) : https://qiita.com/kinpira/items/bbccc8e66777a4526b0f
* Nginxインストール
    ```
    $ sudo apt install nginx
    ```

* uWSGIインストール
    ```
    $ sudo pip3 install uwsgi
    ```

インストールが完了したら設定をしていく。

参考(設定) : https://qiita.com/morinokami/items/e0efb2ae2aa04a1b148b

* Nginxの設定
    
    設定ファイルを作成する。
    ``` shell
    $ cd /etc/nginx/conf.d
    $ sudo nano default.conf

    sites-enabled/default の無効化
    $ sudo unlink /etc/nginx/sites-enabled/default
    ```

    テキストエディタに記入
    ```
    ----ここから
    server {
    listen       80;

        location / {
            include uwsgi_params;
            uwsgi_pass unix:///tmp/uwsgi.sock;
        }
    }
    ----ここまで
    ```

* uwsgiの設定
    ``` shell
    $ mkdir flask
    $ sudo nano myapp.ini
    ```

    テキストエディタに記入
    ```
    ----ここから
    [uwsgi]
    module = app
    callable = app
    master = true
    processes = 1
    socket = /tmp/uwsgi.sock
    chmod-socket = 666
    vacuum = true
    die-on-term = true
    wsgi-file = /home/pi/flask/app.py
    chdir = /home/pi/flask/
    ----ここまで


    保存する
    ctrl + x
    ```

#### プログラム
Nginx上にFlaskを設置し、アクセスページの制御を行う。ラズパイ上でのフォルダ構成は以下になる。

```
home
  |-pi
     |-flask
         |-static必要に応じてcssやjsを追加
            |-myapp.js
         |-templates(必要に応じてhtmlを追加)
            |-index.html
            |-scan.html
         |-app.py
         |-myapp.py

```

htmlテンプレート及びpythonスクリプトはgitのとおりである。各ファイルを配置したらuwsgiを起動しページの表示確認を実施する。

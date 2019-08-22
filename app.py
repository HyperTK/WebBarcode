import cv2
from flask import Flask, render_template, redirect, url_for
from pyzbar.pyzbar import decode

app = Flask(__name__)

'''
インデックスを描画する
Scanからのリダイレクトの場合は、バーコードのパラメータを受け取る
'''
@app.route("/")
def index():
    title = "WebBarcode"
    # indexを描画
    return render_template("index.html", title=title)


'''
スキャンのプレビューを表示する
読み取り成功 : コードの内容を返す
タイムアウト : 空の文字を返す
'''
@app.route("/scan", methods=["GET"])
def scan():
    code = ""
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

    while True:
        ret, frame = cap.read()
        cv2.imshow("Preview", frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        data = decode(gray)

        # Code39とQRのみ読み取る
        for symbol in data:
            if symbol.type == "CODE39" or symbol.type == "QRCODE":
                code = data[0][0].decode("utf-8", "ignore")
                print(code)
                break

        # スキャン成功ならリダイレクトする
        if code != "":
            break

        # Escキーで終了(GUIがある場合のみ)
        if cv2.waitKey(1) == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    # リダイレクト
    return redirect(url_for("index", code=code))


if __name__ == '__main__':
    app.run("localhost", port=3000)

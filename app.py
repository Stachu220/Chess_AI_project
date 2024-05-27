from flask import Flask, Response, request, render_template
import time
import traceback
import chess
import chess.svg
from chess_logic import ocen_szachownice, alfa_beta, szachowe_quiesce, wybierz_ruch, ruch_dev_zero
from szachownica import szachownica

app = Flask(__name__)

@app.route("/")
def main(message=""):
    global licznik, szachownica
    if licznik == 1:
        licznik += 1
    status = ""
    if message:
        status = message
    elif szachownica.is_stalemate():
        status = 'Remis'
    elif szachownica.is_checkmate():
        status = 'Szach mat'
    elif szachownica.is_insufficient_material():
        status = 'Remis z powodu niewystarczajacego materialu'
    elif szachownica.is_check():
        status = 'Szach'
    return render_template('index.html', image_url="/szachownica.svg?%f" % time.time(), status=status)

@app.route("/szachownica.svg/")
def szachownica_svg():
    return Response(chess.svg.board(board=szachownica, size=700), mimetype='image/svg+xml')

@app.route("/ruch/")
def ruch():
    message = ""
    try:
        ruch = request.args.get('ruch', default="")
        szachownica.push_san(ruch)
        ruch_dev_zero()
    except Exception:
        traceback.print_exc()
        message = "Nielegalny ruch, spróbuj ponownie"
    return main(message)

@app.route("/silnik/", methods=['POST'])
def silnik():
    message = ""
    try:
        ruch_dev_zero()
    except Exception:
        traceback.print_exc()
        message = "Nielegalny ruch, spróbuj ponownie"
    return main(message)

@app.route("/nowa_gra/", methods=['POST'])
def nowa_gra():
    global szachownica
    message = "Szachownica zresetowana, powodzenia w kolejnej grze."
    szachownica.reset()
    return main(message)

@app.route("/cofnij/", methods=['POST'])
def cofnij():
    global szachownica
    message = ""
    try:
        szachownica.pop()
    except Exception:
        traceback.print_exc()
        message = "Nie ma ruchu do cofnięcia"
    return main(message)

if __name__ == '__main__':
    licznik = 1
    app.run()

import chess
import chess.svg
import chess.polyglot
import chess.engine

# Tabele oceniania pozycji figur na szachownicy
tabela_pionkow = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

tabela_skoczkow = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

tabela_goncow = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

tabela_wiez = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

tabela_hetmanow = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

tabela_krolow = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

# Funkcja oceniająca aktualną sytuację na szachownicy
def ocen_szachownice():
    if szachownica.is_checkmate():
        if szachownica.turn:
            return -9999
        else:
            return 9999
    if szachownica.is_stalemate():
        return 0
    if szachownica.is_insufficient_material():
        return 0

    # Liczenie materiału na szachownicy
    pionki_biale = len(szachownica.pieces(chess.PAWN, chess.WHITE))
    pionki_czarne = len(szachownica.pieces(chess.PAWN, chess.BLACK))
    skoczki_biale = len(szachownica.pieces(chess.KNIGHT, chess.WHITE))
    skoczki_czarne = len(szachownica.pieces(chess.KNIGHT, chess.BLACK))
    goncy_biali = len(szachownica.pieces(chess.BISHOP, chess.WHITE))
    goncy_czarni = len(szachownica.pieces(chess.BISHOP, chess.BLACK))
    wieze_biale = len(szachownica.pieces(chess.ROOK, chess.WHITE))
    wieze_czarne = len(szachownica.pieces(chess.ROOK, chess.BLACK))
    hetmany_biale = len(szachownica.pieces(chess.QUEEN, chess.WHITE))
    hetmany_czarne = len(szachownica.pieces(chess.QUEEN, chess.BLACK))

    # Obliczanie wartości materiału
    material = 100 * (pionki_biale - pionki_czarne) + 320 * (skoczki_biale - skoczki_czarne) + 330 * (goncy_biali - goncy_czarni) + 500 * (wieze_biale - wieze_czarne) + 900 * (hetmany_biale - hetmany_czarne)

    # Obliczanie wartości pozycji na podstawie tablic oceny
    pozycja_pionkow = sum([tabela_pionkow[i] for i in szachownica.pieces(chess.PAWN, chess.WHITE)])
    pozycja_pionkow = pozycja_pionkow + sum([-tabela_pionkow[chess.square_mirror(i)]
                           for i in szachownica.pieces(chess.PAWN, chess.BLACK)])
    pozycja_skoczkow = sum([tabela_skoczkow[i] for i in szachownica.pieces(chess.KNIGHT, chess.WHITE)])
    pozycja_skoczkow = pozycja_skoczkow + sum([-tabela_skoczkow[chess.square_mirror(i)]
                               for i in szachownica.pieces(chess.KNIGHT, chess.BLACK)])
    pozycja_goncow = sum([tabela_goncow[i] for i in szachownica.pieces(chess.BISHOP, chess.WHITE)])
    pozycja_goncow = pozycja_goncow + sum([-tabela_goncow[chess.square_mirror(i)]
                               for i in szachownica.pieces(chess.BISHOP, chess.BLACK)])
    pozycja_wiez = sum([tabela_wiez[i] for i in szachownica.pieces(chess.ROOK, chess.WHITE)])
    pozycja_wiez = pozycja_wiez + sum([-tabela_wiez[chess.square_mirror(i)]
                           for i in szachownica.pieces(chess.ROOK, chess.BLACK)])
    pozycja_hetmanow = sum([tabela_hetmanow[i] for i in szachownica.pieces(chess.QUEEN, chess.WHITE)])
    pozycja_hetmanow = pozycja_hetmanow + sum([-tabela_hetmanow[chess.square_mirror(i)]
                             for i in szachownica.pieces(chess.QUEEN, chess.BLACK)])
    pozycja_krolow = sum([tabela_krolow[i] for i in szachownica.pieces(chess.KING, chess.WHITE)])
    pozycja_krolow = pozycja_krolow + sum([-tabela_krolow[chess.square_mirror(i)]
                           for i in szachownica.pieces(chess.KING, chess.BLACK)])

    # Końcowa ocena szachownicy
    ocena = material + pozycja_pionkow + pozycja_skoczkow + pozycja_goncow + pozycja_wiez + pozycja_hetmanow + pozycja_krolow
    if szachownica.turn:
        return ocena
    else:
        return -ocena


# Wyszukiwanie najlepszego ruchu za pomocą algorytmu minimax z alfą-beta przy użyciu negamax
def alfa_beta(alfa, beta, glebokosc):
    najlepszy_wynik = -9999
    if glebokosc == 0:
        return szachowe_quiesce(alfa, beta)
    for ruch in szachownica.legal_moves:
        szachownica.push(ruch)
        wynik = -alfa_beta(-beta, -alfa, glebokosc - 1)
        szachownica.pop()
        if wynik >= beta:
            return wynik
        if wynik > najlepszy_wynik:
            najlepszy_wynik = wynik
        if wynik > alfa:
            alfa = wynik
    return najlepszy_wynik


# Funkcja "quiescence search" w celu uniknięcia problemu "horizon effect"
def szachowe_quiesce(alfa, beta):
    stan_pat = ocen_szachownice()
    if stan_pat >= beta:
        return beta
    if alfa < stan_pat:
        alfa = stan_pat

    for ruch in szachownica.legal_moves:
        if szachownica.is_capture(ruch):
            szachownica.push(ruch)
            wynik = -szachowe_quiesce(-beta, -alfa)
            szachownica.pop()

            if wynik >= beta:
                return beta
            if wynik > alfa:
                alfa = wynik
    return alfa


# Wybieranie ruchu na podstawie głębokości przeszukiwania
def wybierz_ruch(glebokosc):
    try:
        ruch = chess.polyglot.MemoryMappedReader("/books/human.bin").weighted_choice(szachownica).move
        return ruch
    except:
        najlepszy_ruch = chess.Move.null()
        najlepsza_wartosc = -99999
        alfa = -100000
        beta = 100000
        for ruch in szachownica.legal_moves:
            szachownica.push(ruch)
            wartosc_szachownicy = -alfa_beta(-beta, -alfa, glebokosc - 1)
            if wartosc_szachownicy > najlepsza_wartosc:
                najlepsza_wartosc = wartosc_szachownicy
                najlepszy_ruch = ruch
            if wartosc_szachownicy > alfa:
                alfa = wartosc_szachownicy
            szachownica.pop()
        return najlepszy_ruch


# Wykonanie ruchu Dev-Zero
def ruch_dev_zero():
    ruch = wybierz_ruch(3)
    szachownica.push(ruch)


# Wykonanie ruchu Stockfish
def ruch_stockfish():
    silnik = chess.engine.SimpleEngine.popen_uci(
        "engines/stockfish.exe")
    ruch = silnik.play(szachownica, chess.engine.Limit(time=0.1))
    szachownica.push(ruch.move)
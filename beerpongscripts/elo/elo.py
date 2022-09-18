"""ELO Funktionen zur Berechnung der Elozahl für das BPT


"""

def Ewert_A(elo_A, elo_B, q=1400):
    """
    Parameters
    ----------
    elo_A : int
        Elozahl des Spieler A
    elo_B : int
        Elozahl des Spieler B
    400 : Fixzahl
        Abstufung der Elo-Skala
    """
    if elo_B-elo_A > q:
        x = q
    elif elo_B-elo_A < -q:
        x = -q
    else:
        x = elo_B-elo_A

    RES = 1 / (1 + (10 ** (x / q)))
    print("B:",elo_B, "A:", elo_A, "X:", x, "Chance A:", RES)

    return RES

def k_factor(elo, spiele):
    if spiele<30:
        return 60
    elif spiele>=30 and elo<2500:
        return 40
    else:
        return 15

def new_Elo(elo_Eigen, elo_Gegner, spiele_eigen, punkte):
    k = k_factor(elo_Eigen, spiele_eigen)
    e_wert = Ewert_A(elo_Eigen, elo_Gegner)
    return int(elo_Eigen + k*(punkte - e_wert))
import math as m
"""ELO Funktionen zur Berechnung der Elozahl für das BPT


"""
Q = 500

def Ewert_A(elo_A, elo_B, q=Q):
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
    print("A:", elo_A, "B:",elo_B,  "X:", x, "Chance A:", RES)

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

def elo_for_max_points(elo_Eigen, spiele_eigen):
    k = k_factor(elo_Eigen, spiele_eigen)
    Ewert = 1/(2*k)
    Y = m.log10(abs(1/Ewert-1))
    return int(Q*Y)

if __name__ == '__main__':
    print(new_Elo(1759, 1000, 40, 1))
    print(elo_for_max_points(1000, 40))
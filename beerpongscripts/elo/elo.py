import math as m
"""ELO Funktionen zur Berechnung der Elozahl für das BPT


"""
# CONSTANTS
Q = 700

def Ewert_A(elo_A, elo_B):
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

    RES2 = (10**(elo_A/Q))/((10**(elo_A/Q))+(10**(elo_B/Q)))
    print("A:", elo_A, "B:",elo_B,  "X:", elo_B-elo_A, "Chance A:", RES2)

    return RES2

def k_factor(elo, spiele):
    if spiele<30:
        return 90
    elif spiele >= 30 and elo<2000:
        return 70
    else:
        return 30

def new_Elo(elo_Eigen, elo_Gegner, spiele_eigen, punkte):
    k = k_factor(elo_Eigen, spiele_eigen)
    e_wert = Ewert_A(elo_Eigen, elo_Gegner)
    return int(elo_Eigen + k*(punkte - e_wert))

def elo_for_max_points(elo_Eigen, spiele_eigen):
    k = k_factor(elo_Eigen, spiele_eigen)
    Ewert = 1/(2*k)
    Y = m.log10(abs((1/Ewert)-1))
    return int(Q*Y)

if __name__ == '__main__':
    pass

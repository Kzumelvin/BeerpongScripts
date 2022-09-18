# BPT Elo

<aside>
💡 Das BPT Elo liegt der Elo-Zahl aus dem Schach zugrunde. Im Nachgang wird dies immer als Elo-Zahl bezeichnet.

</aside>

# Inhaltsverzeichnis

# Legende

- $R$ = ELO - Zahl des Spielers
- $R'$ = Neue Elo-Zahl
- $A$ = Alte BPT Spielstärke
- $Q$ = Umrechnungskonstante
- $E$ = Erwartungswert
- $k$ = k-Faktor
- $S$ = Punkte aus Punkteverteilung

# Anfängliche Elo-Schätzung

<aside>
💡 Für die anfängliche Elo-Schätzung wird als Maßstab die alte Spielstärke des Beerpongturniers (Stand: 16.09.2022) herangezogen. Hierbei ist die tatsächliche Spielstärke $A$ zu verwenden, ohne das eine Anteilsberechnung bei weniger als 25 Spielen erfolgt. Die Elo-Zahl selbst bietet mit den verschiedenen Werten des [$k$-Faktor](https://www.notion.so/k-Faktor-9b7a17c9dc5c4c11bdd446377005820f)s einen Variation dieser Anteilsberechnung.

</aside>

### Berechnungsweiße der Umrechnungskonstanten

<aside>
💡 Die Konstante $Q = 33702$ erechnet sich aus dem Verhältnis der Top-Spielstärke $A_{max} = 13,48$ zur Summe aller der Spielstärken aller aktiven Spieler $A_{gesamt} = 168,26$ multipliziert mit der zugewiesenen Top-Elo $R_{top}$.

</aside>

<aside>
💡 $R_{top} = 2700$  ergibt sich aus der [](https://www.notion.so/1ea9ffe3e5f04f979ef0f59d3502a9d8) Abstufung.

</aside>

$$
Q = \frac{A_{gesamt}}{A_{max}}\times R_{top}
$$

$$
= \frac{168,26}{13,48}\times 2700 = 33702
$$

### Berechnungsweiße der geschätzten Elo-Zahl

$$
R = \frac{A}{A_{gesamt}}\times Q
$$

$$
= \frac{A \times A_{gesamt} \times R_{top}}{A_{gesamt}\times A_{max}} =
$$

$$
= \frac{R_{top}}{A_{max}}\times A =
$$

$$
= \frac{2700}{13,48} \times A
$$

<aside>
💡 Damit ergibt sich am Beispiel der Nummer 2 - Moritz Fedeneder - folgende gerundete Elo-Zahl:

</aside>

$$
\frac{12,48}{168,26}\times 33702 \thickapprox 2564
$$

# Berechnung des Erwartungswerts

<aside>
💡 Der Erwartungswert $E$ gibt die Sieg-Wahrscheinlichkeit des jeweiligen Spielers an und ist nötig um die neue Elo-Zahl nach jedem Spiel zu berechnen.

</aside>

$$
E = \{x|0 \leq x \leq 1\}
$$

<aside>
💡 $Y$ stellt den Abstufungsumfang der Elo-Skala von stark zu schwach dar. Diese kann - wenn notwendig - angepasst werden.

Vorerst wird für das BPT Rating die Abstufung $Y = 1400$ festgelegt. Sie ergibt sich aus der Elo-Spanne zwischen stärkstem und schwächstem Spieler. Diese Abstufung kann aber jederzeit angepasst werden. 

</aside>

### Erwartungswert des Spieler A

$$
E_{A} = \frac{1}{1+10^{(R_{A}-R_{B})/Y}}
$$

### Erwartungswert des Spieler B

$$
E_{B} = \frac{1}{1+10^{(R_{B}-R_{A})/Y}}
$$

$$
E_A + E_B = 1
$$

## Neuberechnung der Elo-Zahl

### $k$-Faktor

<aside>
💡 Der $k$-Faktor gibt an, wie viele ELO-Punkte ein Spieler bei einer Partie maximal hinzugewinnen kann.

</aside>

<aside>
⚠️ Wenn $k$-Faktor sehr groß:

- Zufällige Einzelergebnisse wirken sich stark aus
- Elo-Zahl schwankt stark
</aside>

<aside>
⚠️ Wenn $k$-Faktor sehr klein:

- Anpassung sehr “träge”
- Viele Spiele für reale Änderung der Elo-Zahl nötig
</aside>

### Schachmodell

- $k=40$: für neue Spieler mit weniger als 30 Partien
- $k=20$: für alle Spieler mit mind. 30 Partien und einer Elo-Zahl < 2400
    
    ⇒ trifft bei den meisten Spielern zu
    
- $k = 10$: für alle Top-Spieler mit einer Elo-Zahl ≥ 2400

### Schweizer Tischtennis

- $k=10$: für alle Spieler

### Modell des Beerpongturniers

<aside>
💡 Aufgrund der wenigen Spiele pro Jahr wurden die $k$-Faktoren folgendermaßen festgelegt

</aside>

- $k=60$: für neue Spieler mit weniger als 30 Partien
- $k=40$: für alle Spieler mit mind. 30 Partien und $R < 2500$
- $k = 15$: für alle Top-Spieler mit einer $R \geq 2500$

### Punkteverteilung

<aside>

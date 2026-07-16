# Notation Summary

| Symbol | Definition |
| --- | --- |
| $t$ | Current turn (number of peeks revealed) |
| $m$ | Turn on which the player submits a guess (standard game: $m=5$) |
| $n$ | Number of sides on each die (standard game: $n=6$) |
| $g$ | Player's guess |
| $r$ | Actual roll on the guessing turn |
| $X_t$ | The set of all rolls on the first die before turn $t$ |
| $x_t$ | The roll on the first die on turn $t$ |
| $Y_t$ | The set of all rolls on the second die before turn $t$ |
| $y_t$ | The roll on the second die on turn $t$ |
| $p_t$ | Observed sum on turn $t$ |
| $P_t$ | Ordered observation history $(p_1,\ldots,p_t)$ |
| $F_t$ | Ordered future sums $(p_{t+1}, ..., p_{n})$ |
| $D_n$ | Set of faces of an $n$-sided die |
| $A_t$ | Available faces of a depleting die after turn $t$ |
| $A_t^{(1)}$ | Available faces on the first die |
| $A_t^{(2)}$ | Available faces on the second die |
| $\mathcal{D}$ | A depleting die |
| $S_t$ | Complete game state after turn $t$ |
| $p(g,r)$ | Payout function |
| $M(r)$ | Maximum payout function |
| $G(r)$ | Optimum guess function |
| $\Sigma_{P_t}$ | The sum of all observed peeks |
| $\Sigma_{F_t}$ | The sum of all future peeks |
| $\mathcal{T}(S_t)$ | The set of all possible game states after given state $S_t$ |
| $P(S_{t+1} \| S_t)$ | The probaility of the next state of the game |
| $N(p, S)$ | The number of ways a peek $p$ can be made with state $S$ |
| $P(p_{t+1} \| S_t)$ | The probability of the next peek given the state |
| $P(S_t)$ | The probability of getting to any game state |

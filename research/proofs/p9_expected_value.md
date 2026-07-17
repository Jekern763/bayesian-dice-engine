# p9: Expected Value

First, finding the EV for any guess, given the peeks history

$$
EV(g | P_t) = \sum_{r=2}^{12}p(g, r) \cdot P(r | P_t)
$$

Expanding

$$
EV(g | P_t) = \sum_{r=2}^{12}(2-|g-r|)\cdot(|g-7|)\cdot P(r|P_t) \\[1em]
=|g-7|\sum_{r=2}^{12}(2-|g-r|)\cdot P(r|P_t) \\[1em]
=|g-7|\left(\sum_{r=2}^{12}(2P(r|P_t)) - \sum_{r=2}^{12}|g-r| \cdot P(r|P_t)\right) \\[1em]
\text{because the sum of all } P(r|P_t) = 1 \\[1em]
=|g-7| \cdot (2-\sum_{r=2}^{12}|g-r| \cdot P(r|P_t))
$$

But this formula only gives the EV for any one guess, so to find the maximum EV, with best play

$$
\max_g(EV(g | P_t)) = \max(
    |g-7| \cdot (2-\sum_{r=2}^{12}|g-r| \cdot P(r|P_t))
)
$$

Then finding the average max EV for any possible game, theoretically

$$
\sum_{P_t}\max_g(EV(g|P_t)) \cdot P(P_t) \\[1em]
=\sum_{P_t}\max_g(EV(g|P_t)) \cdot \sum_{S_t}\alpha(S_t)
$$

Finding the best guess given $P_t$ is simply

$$
\argmax_g(EV(g|P_t))
$$

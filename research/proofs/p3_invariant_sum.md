# p3: Invariant Sum Formula

See `c4`

Trying to prove

$$
\Sigma_{P_t} + \Sigma_{F_t} = (n+1)(n)
$$

First defining some variables:

Let

$$
\Sigma_{P_t} = \sum_{i=1}^tp_i
$$

Where $m$ is the number of turns after the player guesses and $p_i$ is the $i$th sum observed.

Let

$$
\Sigma_{F_t} = \sum_{i=t+1}^np_i
$$

## p3.1 In General

$$
\Sigma_{P_t} + \Sigma_{F_t} = \sum_{i=1}^tp_i + \sum_{i=t+1}^np_i \\[1em]
= \sum_{i=1}^np_i \\[1em]
= \sum_{i=1}^n(r_i^{(\mathcal{D}_1)}+r_i^{(\mathcal{D}_2)})
$$

Because $r_t$ can only be integers 1 through n, and each one can only be used once, all are used exactly once.

$$
\sum_{i=1}^n(r_i^{(\mathcal{D}_1)}+r_i^{(\mathcal{D}_2)}) =
2\sum_{i=1}^ni\\[1em]
= (n)(n+1) = n^2+n
$$

## p3.2 When $t=m=4$ and $n=6$

Plugging into the formula for $n=6$

$$
\Sigma_{P_t} + \Sigma_{F_t} = (n+1)(n) = 42
$$

Follwing, with $m=4$, and at $t=m$

$$
\Sigma_{P_4} + \Sigma_{F_4} = 42 \\[1em]
\Sigma_{F_4} = 42 - \Sigma_{P_4} \\[1em]
avg(F_4) = \frac{42 - \Sigma_{P_4}}{2}
$$

Thus, after the fourth observed sum, the average value of the four remaining sums is completely determined by the first four observations:

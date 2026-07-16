# p5: Peek Liklihood Given State

See `c7`

Recall
$$
S_t = (A_t^{(1)}, A_t^{(2)})
$$

And

$$
A_t^{(d)} = \set{\text{Sides Remaining on Depleting Dice } \mathcal{D}^{(d)}}
$$

Also recall from `p4`: Game State Transitions
$$
\mathcal{T}(S_t) = \left\{
S_{t+1}:
    \begin{array}{l}
        A_{t+1}^{(1)} = A_t^{(1)} \backslash \set{r^{(1)}} \\[1em]
        A_{t+1}^{(2)} = A_t^{(2)} \backslash \set{r^{(2)}} \\[1em]
        r^{(1)} \in A_t^{(1)}, r^{(2)} \in A_t^{(2)}
    \end{array}
\right\}
$$

&nbsp;

$$
P(S_{t+1} | S_t) =
\begin{cases}
\frac{1}{(6-t)^2}, & S_{t+1}\in \mathcal{T}(S_t) \\[1em]
0, & S_{t+1} \not \in \mathcal{T}(S_t)
\end{cases}
$$

## p5.1: Number of Combinations of $x_t + y_t = p_t$

Let

$$N(p, S) \\
p \in \mathbb{Z}$$

be the number of ways $p$ can be made from the current state $S$

So

$$
N(p, S) = \left|
    \left\{
        \begin{array}{l}
            (x, y) \in A^{(1)} \times A^{(2)} : x+y=S
        \end{array}
    \right\}
\right|  
$$

## p5.2: $P(p_{t+1} | S_t)$ in general

$$
P(p_{t+1} | S_t) = \frac{N(p_{t+1}, S_t)}{|A^{(1)} \times A^{(2)}|}
$$

## p5.3: $P(P_{t+1}| S_t)$ for $t=4$

Because in this specific game the player guesses after seeing $p_4$ at $t=4$, we can simplify the equation

$$
|A^{(1)}| = |A^{(2)}| = 2 \\
|A^{(1)} \times A^{(2)}| = 4 \\[1em]
\therefore \\[1em]
\boxed{
    P(p_{t+1} | S_t) = \frac{N(p_{t+1}, S_t)}{4}
}
$$

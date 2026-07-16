# p8: Next Peek Liklihood
Proving

$$
P(p_{t+1}|P_t)
$$

Recall from previous proofs

$$
P(S_t|P_t) = \frac{
    \alpha_t(S_t)
}{
    \sum_{S_t}\alpha_t(S_t)
} \\[1.5em]

P(p_{t+1}|S_t) = \frac{\mathcal{N}_{p_{t}}(t+1))}{(n-t)^2} \\[1.5em]
$$

Using the law of total probability

$$
P(p_{t+1}|P_t) = \sum_{S_t}P(p_{t+1}|S_t, P_t) \cdot P(S_t|P_t) \\[1em]
$$

and because $p_{t+1}$ is independant of $P_t$ when we know $S_t$

$$
= \sum_{S_t}P(p_{t+1}|S_t) \cdot P(S_t|P_t)\\[1.5em]

= \sum_{S_t} \frac{\mathcal{N}_{p_{t+1}}(t+1)}{(6-t)^2} \cdot P(S_t|P_t) \\[1.5em]

=\sum_{S_t} \frac{\mathcal{N}_{p_{t+1}}(t+1)}{(6-t)^2} \cdot \frac{
    \alpha_t(S_t)
}{
    \sum_{S_t}\alpha_t(S_t)
}
$$

Now expanding everything

$$
= \sum_{S_t}
\frac{
    \left|
    \left\{
        \begin{array}{l}
            (x_{t+1}, y_{t+1}) \in A_t^{(1)} \times A_t^{(2)} : x_{t+1}+y_{t+1}= p_{t+1}
        \end{array}
    \right\}
\right|  
}{
    (6-t)^2
}

\cdot

\frac{
    \sum_{S_{t-1}}P(P_{t-1}, S_{t-1})
\cdot

    \left|\left\{
        (x_{t}, y_{t}) :
        \begin{array}{l}
            x_{t} + y_{t} = p_{t}\\[1em]
            A_{t}^{(1)} = A_{t-1}^{(1)}\backslash\set{x_{t}}\\[1em]
            A_{t}^{(2)} = A_{t-1}^{(2)}\backslash\set{y_{t}}
        \end{array}
    \right\}\right|
}{
    \sum_{S_t}\sum_{S_{t-1}}P(P_{t-1}, S_{t-1})
\cdot

\left|\left\{
        (x_{t}, y_{t}) :
        \begin{array}{l}
            x_{t} + y_{t} = p_{t}\\[1em]
            A_{t}^{(1)} = A_{t-1}^{(1)}\backslash\set{x_{t}}\\[1em]
            A_{t}^{(2)} = A_{t-1}^{(2)}\backslash\set{y_{t}}
        \end{array}
    \right\}\right|
}
$$

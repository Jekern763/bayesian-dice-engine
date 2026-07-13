# p4: Game State Transition

See `c6`

Recall
$$
S_t = (A_t^{(1)}, A_t^{(2)})
$$

And

$$
A_t^{(d)} = \set{\text{Sides Remaining on Depleting Dice } \mathcal{D}^{(d)}}
$$

## p4.1: Successor State Set

Let

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

Such that $S_{t+1}$ is any possible game state after a side has been removed from each die.

## p4.2 Cardinalty of $\mathcal{T}(S_t)$

Let

$$
n = \text{number of sides on an inital dice (usually 6)} \\
k = n-t
$$

such that $k$ is the number of sides left on a dice

$$
k = |A_t^{(d)}| \space \forall \space d
$$

Since one remaining face is selected independently from each die, the number of possible successor states is

$$
|A_t^{(1)}| \cdot |A_t^{(2)}| = k^2
$$

So

$$
|\mathcal{T}(S_t)| = k^2 \\
=(n-t)^2 \\
= (6-t)^2 \text{ For the standard game}
$$

## p4.3: Probability of Transition

Since each remaining face on each die is sampled uniformly and independently, each element in $A_t^{(d)}$ has $\frac{1}{∣A_t^{(d)}|}$ probability of being removed.

Therefore every successor state is equally likely.

Let

$$
P(S_{t+1} | S_t) =
\begin{cases}
\frac{1}{|\mathcal{T}(S_t)|}, & S_{t+1}\in \mathcal{T}(S_t) \\[1em]
0, & S_{t+1} \not \in \mathcal{T}(S_t)
\end{cases}
$$

Substituting in the cardinality function `p4.2`

$$
P(S_{t+1} | S_t) =
\begin{cases}
\frac{1}{(n-t)^2}, & S_{t+1}\in \mathcal{T}(S_t) \\[1em]
0, & S_{t+1} \not \in \mathcal{T}(S_t)
\end{cases}
$$

Or for this game specifically

$$
\boxed{
P(S_{t+1} | S_t) =
\begin{cases}
\frac{1}{(6-t)^2}, & S_{t+1}\in \mathcal{T}(S_t) \\[1em]
0, & S_{t+1} \not \in \mathcal{T}(S_t)
\end{cases}
}
$$

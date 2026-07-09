# Derivations

## Optimum Guess Function

Let $G(r)$ be the best guess given $r$.

$$
G(r)=
\begin{cases}
    r & r \in (-\infty, 5] \cup [9, \infty) \\[1em]
    \frac{r+5}{2}  & r \in [5, 7] \\[1em]
    \frac{r+9}{2}  & r \in [7, 9]
\end{cases}
$$

See `proofs/p1_optimum_guess_function`

## Maximum Payout Function

Let $M(r)$ be the maximum payout for any $r$

$$
M(r) =
\begin{cases}
14-2r & r \le 5 \\[1em]
\frac{(9-r)^2}{4} & 5 \le r \le 7 \\[1em]
\frac{(r-5)^2}{4} & 7 \le r \le 9 \\[1em]
2r-14 & r \ge 9
\end{cases}
$$

See `proofs/p2_maximum_payout_function`

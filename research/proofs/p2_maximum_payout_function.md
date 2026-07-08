# p2: maximum payout function

See `c1`

See `p1` for proof of $G(r)$

Let

$$
M(r) = \max _{g \in \mathbb{R}}(p(g, r))
$$

So that $M(r)$ is the maximum payout for a given roll, for all guesses.

Using

$$
G(r) = \argmax _{g \in \mathbb{(R))}}(p(g, r)) \\[1em]

=

\begin{cases}
    r & r \in (-\infty, 5] \cup [9, \infty) \\[1em]
    \frac{r+5}{2}  & r \in [5, 7] \\[1em]
    \frac{r+9}{2}  & r \in [7, 9]
\end{cases}
$$

To determine $g$, then

$$
M(r) = p(G(r), r)
$$

Where $M(r)$ is now a piecwise function that splits at

$$
r = 5 \\
r= 7 \\
r = 9
$$

## p2.1: symetry about $r=7$

As proven in `p1`, $G(r)$ is symetrical around $r=7$, as is $p(g, r)$. Therefore, $M(r)$ has the same property:

$$
M(r) = M(14-r) \\
\text{or}\\
M(r+7) = M(r-7)
$$

## p2.2: $r \in (-\infin, 5] \cup [9, \infin) \text{ or } r \le 5 \cup r \ge 9$

For this interval

$$
G(r) = r \\[1em]
\therefore \\[1em]
M(r) = p(r,r) \\
= (2-|r-r|)|7-r|
= 2|7-r| \\[1em]
M(r) =
\begin{cases}
14-2r & r \le 5 \\[1em]
2r-14 & r \ge 9
\end{cases}
$$

## p2.3 $r \in [5, 7] \text{ or } 5 \le r \le 7$

For this interval

$$
G(r) = \frac{r+5}{2} \le r \le 7\\[1em]
\therefore \\[1em]
M(r) = p(\frac{r+5}{2}, r) \\[1em]
= (2-|\frac{r+5}{2} - r|)|\frac{r+5}{2}-7|
$$

Becuase $\frac{r+5}{2} \le r \le 7$

$$
= (2-r+\frac{r+5}{2})(7-\frac{r+5}{2}) \\[1em]
= \frac{(9-r)^2}{4}
$$

## p2.4 $r \in [7, 9] \text{ or } 7 \le r \le 9$

Using the reflection property

$$
M(r) \space r \in [7, 9] \\
= \\
M(14 -r) \space r \in [5, 7]
$$

So, for this interval

$$
M(r) = \frac{(9-(14-r))^2}{4} \\[1em]
= \frac{(r-5)^2}{4}
$$

## p2.5 $M(r)$ for all intervals

$$
M(r) =
\begin{cases}
14-2r & r \le 5 \\[1em]
\frac{(9-r)^2}{4} & 5 \le r \le 7 \\[1em]
\frac{(r-5)^2}{4} & 7 \le r \le 9 \\[1em]
2r-14 & r \ge 9
\end{cases}
$$

See `figures/maximum_payout` for graph

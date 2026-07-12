# p1: Optimal Guess Function

See `c2`, `c3`

## p1.1 Reflection Property

The payout function is symmetric about the median roll $r=7$.

For any real number $x$, reflection across $7$ is defined by

$$
x' = 14 - x,
$$

so that

$$
x + x' = 14.
$$

Applying this reflection simultaneously to both the player's guess and the actual roll gives

$$
g' = 14-g,\qquad
r' = 14-r.
$$

Then

$$
|g'-r'| = |(14-g)-(14-r)| = |g-r|
$$

and

$$
|g'-7|
=
|(14-g)-7|
=
|g-7|.
$$

$$
\therefore
$$

$$
p(g,r)=p(14-g,\,14-r)
$$

$$
\forall \space g,r\in\mathbb{R}
$$

Consequently, if $G(r)$ is an optimal guess for roll $r$, then

$$
G(r)=14-G(14-r) \\[1em]
\square \\[2em]
$$

Note, that all future parts of p1 will be solved for $r \le 7$

---

## p1.2 $G(r)$ for $r \le g \le 7$

Recall

$$G(r) = \argmax_{g \in \mathbb{R}}(p(g,r))$$

Because $p(g,r) = (2-|g-r|)|g-7|$ is a piecewise function, first solve for,

$$g \ge r, g \le 7 \therefore r \le g \le 7$$

Where

$$
p(g,r) = (2-g+r)(7-g) \\[1em]
= 14 - 2g - 7g + g^2 + 7r - rg \\[1em]
= g^2 - (9+r)g + 14 + 7r
$$

Because the $g^2$ term is positive, this parabola opens upward. Therefore, the maximum on the closed interval $r \le g \le 7$ must occur at one of the boundaries.

Checking boundaries $g=r$ and $g=7$:

At $g=r$:
$$
p(r,r) = (2-r+r)(7-r) = 14-2r
$$

At $g=7$:
$$
p(7,r) = (2-7+r)(7-7) = 0
$$

Checking Bounds:

For $r \le 5$, the boundary $g=r$ yields $14-2r \ge 4$. Since $14-2r > 0$, the maximum payout occurs at $g=r$.

$$
\therefore \\[1.5em]
\forall \space r \in (-\infty, 5]; \space G(r) = r
$$

## p1.3 $G(r)$ for $g \le r \le 7$

For reference: $p(g, r) = (2-|g-r|)|7-g|$

Solving for

$$
g \le r \le 7 \\[2em]
p(g, r) = (2-r+g)(7-g) \\[1em]
= 14 - 2g -7r + rg +7g -g^2 \\[1em]
= -g^2 +g(r+5) -7r +14
$$

Finding the maximum

$$
\frac{\partial p}{\partial g} = -2g + r+5 \\[1em]
0 = -2g + r + 5 \\[1em]
g = \frac{r+5}{2}
$$

Checking Bounds

$$
\frac{r+5}{2} \le r \\[1em]
5 \le r
$$
and
$$
r \le 7
$$

**Global Maximum Check for $r \in [5, 7]$:**
Evaluating the domain $g \ge 7$ for rolls $r \le 7$ yields a second local maximum at $g = \frac{r+9}{2}$. Checking the payouts for $r \in (5, 7]$:

$$
p\left(\frac{r+5}{2}, r\right) = \left(\frac{9-r}{2}\right)^2 \\[1.5em]
p\left(\frac{r+9}{2}, r\right) = \left(\frac{r-5}{2}\right)^2
$$

Because $r \le 7$, $9-r \ge 2$, meaning the first payout is $\ge 1$. Conversely, $r-5 \le 2$, meaning the second payout is $\le 1$. Therefore, the global maximum remains $g = \frac{r+5}{2}$.

so
$$
\forall \space r \in [5, 7]; G(r) = \frac{r+5}{2}
$$

## p1.4 Applying the reflections

For reference

$$
G(r)=
\begin{cases}
     r & \text{ if } r \le 5 \\
    \frac{r+5}{2}  & \text{if } 5 \le r \le 7
\end{cases}
$$

To reflect the formula for $r \le 5$

$$
G(14-r) = 14-r \\[1em]
G(r) = 14 - G(14-r) \text{ : (p1.1)} \\[1em]
G(r) = 14 - (14-r) \\[1em]
G(r) = r
$$

Similarly for reflecting $5 \le r \le 7$

$$
G(14-r) = \frac{(14-r)+5}{2} \\[1em]
G(r) = 14 - \frac{19-r}{2} \\[1em]
G(r) = \frac{28-19+r}{2} \\[1em]
G(r) = \frac{r+9}{2}
$$

Therefore

$$
\boxed{
G(r)=
\begin{cases}
    r & r \in (-\infty, 5] \cup [9, \infty) \\[1em]
    \frac{r+5}{2}  & r \in [5, 7] \\[1em]
    \frac{r+9}{2}  & r \in [7, 9]
\end{cases}
}
$$

For a graph of this function see `figures/optimum_guess`

## p1.5 Properties

Determing certain properties for this function: funciton validity, continuity, differentiability, injectivity

### p1.5.1 function validity

Does each input produce only on output?

We already know that each of the parts of the piecewise formula are functions themeselves, so we only need to check the hand off points:

$$
r = 5 \\
r= 7 \\
r=9
$$

For $r=5$ and $G(r)$ to be a function
$$
r = \frac{r+5}{2} \\[1em]
5 = \frac{5+5}{2} \\[1em]
5 = 5
$$

For $r=7$

$$
\frac{r+5}{2} = \frac{r+9}{2} \\[1em]
\frac{7+5}{2} = \frac{7+9}{2} \\[1em]
6 \not = 8 \\[1em]
$$

Therefore $G(r)$ is not strictly a function.

### p1.5.2 continuity

For $G(r)$ to be continuous, at every break point $b$

$$
\lim _{r \rightarrow b^+}(G(r)) = \lim _{r \rightarrow b^-}(G(r))
$$

But as shown in `p1.5.1`, that is not true for $b=7$. But also as shown, $G(r)$ is continous $r \not = 7$, by the reflection property of `p1.5.1` at $r=5$.

### p1.5.3 differentiability

Because $G(r)$ is not continuus at $r=7$ it is not differentiable at $r=7$. So instead testing for $r=5$ (and using the reflection property)

For $G(r)$ to be differentiable at $r=5$
$$
G'_-(5) = G'_+(5) \\[1em]
1 = \frac{1}{2} + \frac{3}{2} \\[1em]
1 \not = 2 \\[1em]
$$

Therefore $G(r)$ is not differentiable at any breakpoint:

$$
r=5 \\
r=7 \\
r=9
$$

### p1.5.4 injectivity

For $G(r)$ to be 1-to-1, no inputs must yield the same output, but by the reflection property:

$$
G(r) = G(14-r) \\
r \not = 14-r
$$

Therefore $G(r)$ is not 1-to-1

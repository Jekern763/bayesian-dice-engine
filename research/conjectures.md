# Conjectures

Conjectures will be organized, starting with c1, and for sub conjectures moving down to c1.1. All conjectures will use notation defined in definitions and derivations. Any relevant matierial outside of those will be referenced at the beginning of the conjecture if it uses it.

## c1: Payout Function Maximum

Let

$M(r)$

be the maximum attainable payout for any roll, where

$M(r)=\max_{g\in\mathbb{R}} p(g,r)$

Note that in this case, to find a graphable function, g and r must only be real numbers, not just integers.

### c1: Initial Observations

$M(r)$ will likely be piecwise, because it is defined on $p(g,r)$ which is piecwise.

Graphically, it looks like it will be linear over the interval $(- \infin, 5] \cup [9, \infin)$, which is where the optimal guess $G(r) = r$. (see c2)

## c2: Optimal Guess Function For Any Roll

Let

$G(r) = \argmax _{g\in\mathbb{R}}p(g,r)$

denote the optimal guess for a given roll.

### c2: Initial Observations

It appears that $G(r)=r$ on the interval $(- \infin, 5] \cup [9, \infin)$

Outside of that interval, the guess skews outwards (away from $g=7$, to preserve some riskiness multiplier)

For only integer guesses and rolls, $r=7$ is the only time that $G(r) \not= r$. There are times when $G(r) = r, x$, where x is another integer not equal to r, but only at 7 is r not a solution.

## c3: Properties of payout functions

For the payout function $p(g,r)$ and related functions $G(r)$ and $M(r)$, what properties are true of the follwing?

- Differentiability
- Continuity

Put these in p1 and p2, as an extension. Maybe slope lines up for some jumps in the piecwise function

## c4: Invariant Formula

For the any game state $G_t$:

$$
\sum _{i=1}^{m-1} p_t+ \sum_{i=m}^n p_t
= n(n+1)
$$

So basically, for this game params, it is saying

$$
\text{Sums}_{\text{observed}} + \text{Sums}_\text{remaining} = 42
$$

A useful observation is that if you combine the two sumations, it is really just the basic sum of n integers formula:

$$
\sum_{i=1}^{n} i = \frac{n(n + 1)}{2}
$$

but because each sum is adding up the sum of two die faces, it is essentially multiplied by 2, canceling out the $/2$. The only reason I split it up is to show that you can know exactly what the sum of the remaining faces is after any number of peeks.

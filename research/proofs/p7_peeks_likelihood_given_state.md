# p7: Peeks Likelihood Given Game State

Proving

$$
P(P_t | S_t)
$$

## p7.1: $P(S_t, P_t)$

We can rewrite any $P_t$ such that

$$
P_t = (p_1, p_2, ..., p_3)\\
=(P_{t-1}, p_t)
$$

Then

$$
P(P_t|S_t) = P(P_{t-1}, p_t| S_t)
$$

We can also find the probability of $S_t$ using the equation from `p4`

$$
P(S_t | S_{t-1}) = \frac{1}{(6-(t-1))^2}
$$

Since we know that $S_t$ is possible and $n=6$

Let us also define (using `p5`)

$$
P(p_t | S_{t-1}) = \frac{\mathcal{N}_{p_t}(t)}{(6-t)^2}
$$

Just to combine everything we have

$$
P(P_t|S_t) = P(P_{t-1}, p_t| S_t) \\[1em]
P(S_t | S_{t-1}) = \frac{1}{(6-(t-1))^2} \\[1em]
P(p_t | S_{t-1}) = \frac{\mathcal{N}_{p_t}(t)}{(6-(t-1))^2}
$$

Using these to define $P(S_t, P_t)$

$$
P(P_t, S_t) = P(P_{t-1},p_t, S_t) \\[1em]
= \sum_{S_{t-1}}P(P_{t-1}, p_t, S_t, S_{t-1})
$$

Then using the product rule

$$
P(P_{t-1}, p_t, S_t, S_{t-1}) = P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣P_{t−1​},S_{t−1}​)⋅P(S_t​∣P_{t−1}​,S_{t−1}​,p_t​)
$$

Using the properties of the game:

- The probability of $p_{t}$ depends only on $S_{t-1}$
- The probability of $S_{t}$ depends only on $S_{t-1}$ and $p_{t-1}$

$$
P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣P_{t−1​},S_{t−1}​)⋅P(S_t​∣P_{t−1}​,S_{t−1}​,p_t​)\\ 
=P(P_{t-1}​,S_{t−1}​)⋅P(p_t​∣S_{t−1}​)⋅P(S_t​∣​S_{t−1}, p_{t}​​)\\[1em]
$$
Substituting
$$
=
P(P_{t-1}​,S_{t−1}​)
\cdot
\frac{\mathcal{N}_{p_t}(t)}{(6-(t-1))^2}
\cdot
\frac{\mathcal{N}_{S_t, p_t}(t)}{\mathcal{N}_{p_t}(t)}
$$

So going back into the sum

$$
\sum_{S_{t-1}}P(P_{t-1}​,S_{t−1}​)
\cdot
\frac{\mathcal{N}_{p_t}(t)}{(6-(t-1))^2}
\cdot
\frac{\mathcal{N}_{S_t, p_t}(t)}{\mathcal{N}_{p_t}(t)}
$$

This the recursive step. Defining end points:

$$
S_0 = (\set{1,2,3,4,5,6}, \set{1,2,3,4,5,6}) \\
P_0 = \set{} \\
P(S_0, P_0) = 1
$$

So

$$
P(P_t, S_t) = 
\sum_{S_{t-1}}P(P_{t-1}​,S_{t−1}​)
\cdot
\frac{\mathcal{N}_{p_t}(t)}{(6-(t-1))^2}
\cdot
\frac{\mathcal{N}_{S_t, p_t}(t)}{\mathcal{N}_{p_t}}

\\[1em]
\boxed{
=\sum_{S_{t-1}}P(P_{t-1}, S_{t-1})
\cdot
\frac{
    \mathcal{N}_{S_t,p_t}
}
{
    (7-t)^2
}
}
$$

For ease of use

$$
\alpha_t(S_t) = P(P_t, S_t)
$$

## p7.2: $P(S_t | P_t)$

Using Bayes Theorem

$$
P(S_t | P_t) = \frac{P(S_t, P_t)}{P(P_t)} \\[1em]
=\boxed{
\frac{
    \alpha_t(S_t)
}{
    \sum_{S_t}\alpha_t(S_t)
}
}
$$
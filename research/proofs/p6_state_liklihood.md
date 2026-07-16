# p6: State and Peeks Liklihood

In order to apply Bayes Theorem in later proofs, we must define

$$
P(S_t)
$$

## p6.1 $P(S_t)$

Recall

$$
S_t = (A_t^{(1)}, A_t^{(2)})
$$

Where

$$
A_t^{(d)} = \set{\text{Remaining Faces on Depleting Die }\mathcal{D}_d}
$$

So at time $t$ we have removed $t$ sides.

Since each face of a fair depleting die is selected uniformly from the remaining faces, every ordered sequence of $t$ removed faces has equal probability. Furthermore, every $A_t$ set of size $n−t$ corresponds to exactly $t!$ such sequences. Therefore, every $A_t$ is equally likely

Therefore, because we are choosing $t$ faces to remove from $n=6$ total faces, the number of possible ways to remove is $\binom{6}{t}$

$$
P(A_t^{(1)}) = P(A_t^{(2)}) = \frac{1}{\binom{6}{t}}
$$

And, because $S_t$ contains two $A_t$

$$
P(S_t) = P(A_t^{(1)}) \cdot P(A_t^{(2)}) \\[1em]
\boxed{
P(S_t)=\frac{1}{\binom{6}{t}^2} \\[1em]
}
$$

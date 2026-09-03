# Brainstorming Ideas for Asymptotic Analysis

## Ways to define things

### Using vectors

Previously I had used the notation

$$
P_t = (\text{observed sums } p_t) = (p_1, p_2, ..., p_n)
$$

Now to represent $P_t$ in a more ordered fashion, I will use vectors
Moving to $H$ to represent any given history, where

$$
h_t =
\begin{cases}
S_t & \text{if turn } t \text{ has occurred and yielded an observed sum } S_t \\
0 & \text{if turn } t \text{ has not yet been reached}
\end{cases}
\\
\text{then}
\\[1.5em]
\mathbf{H} = (h_1, h_2, h_n)
\text{ in }
\mathbb{R}^n
\\[2em]
\text{alternatively}
\\[2em]
\mathbf{v}_t = h_t\mathbf{e}_t
$$
where $\mathbf{e}_t$ is the t-th standard basis vector

Then

$$
\mathbf{H} = \sum_{t=1}^n\mathbf{v}_t
$$

What does this mean for operations like magnitude, dot product, direction cosines, etc
**Leaving open for later research**


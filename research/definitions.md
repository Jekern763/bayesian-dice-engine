# Definitions

## Turns

Let $t$ denote the current turn, or equivalently, the number of peeks that have been revealed.

Let $m$ denote the turn on which the player submits a guess.

For the standard game,

$
m = 5
$

Equivalently, the player observes $m-1 = 4$ peeks before making a guess.

## Guess

Let $g$ denote the player's guess, submitted immediately before turn $m$, where

$
g \in \mathbb{Z}, \qquad 2 \le g \le 12.
$

## Roll

Let $r$ denote the actual roll observed on turn $m$, where

$
r \in \mathbb{Z}, \qquad 2 \le r \le 12.
$

## Peeks

Let $p_t$ denote the observed sum revealed on turn $t$, such that $p_1$ is the first observed peek.

Let

$
P_t = (p_1,p_2,\ldots,p_t)
$

denote the ordered observation history.

For the standard game,

$P_{m-1}=(p_1,p_2,\ldots,p_{m-1})$

is the complete observation history available to the player before making a guess.

## Payout Formula

$
p(g,r)=(2-|g-r|)|g-7|
$

### Accuracy Section

The factor

$
2-|g-r|
$

determines the payout based on the accuracy of the player's guess.

### Riskiness Section

The factor

$
|g-7|
$

determines the payout based on the riskiness of the player's guess (its distance from the median roll of 7).

## Depleting Dice

Let

$
D_n=\{1,2,\ldots,n\}
$

denote the set of faces of an $n$-sided die.

A depleting die is an ordered pair

$
\mathcal{D}=(D_n,A_t),
$

where

$
A_t\subseteq D_n
$

is the set of currently available faces after turn $t$.

Initially,

$
A_0=D_n.
$

Whenever the die is rolled, a value

$
r\in A_t
$

is selected uniformly at random, after which

$
A_{t+1}=A_t\setminus\{r\}.
$

Thus every face may be rolled at most once.

For the standard game,

$
n=6.
$

## Game State

Let

$
S_t=(A_t^{(1)},A_t^{(2)},P_t)
$

denote the complete game state after turn $t$, where

- $A_t^{(1)}$ is the set of available faces on the first die,
- $A_t^{(2)}$ is the set of available faces on the second die,
- $P_t$ is the ordered observation history.

Initially,

$
S_0=(D_n,D_n,()).
$

## Observation Function

Let $O$ denote the observation function.

Given a game state $S_t$, the player observes only the ordered sequence of revealed peeks.

$
O(S_t)=P_t.
$

The remaining faces on each die are hidden.

## Belief State

Let $\mathcal{S}$ denote the set of all valid game states.

Let $B_t$ denote the player's belief state after turn $t$.

Then

$
B_t
=
\{\,S\in\mathcal S \mid O(S)=P_t\,\},
$

that is, the set of all game states consistent with the player's observation history.
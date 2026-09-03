# Vector Sum & Asymptotic Connections

## 1. Vector-Sum Collapse ↔ Known Permutation Sequence (A175176)

**What it's counting:** $T(n)$ counts the number of distinct full-length peek-histories $(p_1,\ldots,p_n)$ achievable across every possible way the two depleting dice could be rolled. Formally, it's the size of the image of the map $(\sigma,\tau)\mapsto(\sigma(1)+\tau(1),\ldots,\sigma(n)+\tau(n))$ over all pairs of permutations $\sigma,\tau$ of $\{1,\ldots,n\}$ — i.e. how many distinguishable sum-sequences exist when two decks labeled $1..n$ are each shuffled and dealt one at a time. This is exactly OEIS A175176, "number of vector sums of two permutations of $1,2,\ldots,n$."

**Status:** Already known/cataloged — not a new sequence, but a clean, verified cross-reference your "vector analysis" section can cite directly.

**Big question:** A175176 itself has no known closed form on OEIS (just a table plus a "≤" bound via A362968). So the open problem doesn't go away — it transfers to a real unsolved combinatorics question you could actually attack: is there a closed form or generating function for the number of distinct vector sums of two permutations of $[n]$? If you found one, that's a genuine contribution independent of your game.

## 2. Fixed-$n$, Growing-$k$ Rows Hit Named Figurate Numbers

**What it's counting:** same object as above, generalized from 2 dice to $k$ dice — the number of distinct full-length peek-histories when $k$ permutations of $1,\ldots,n$ are summed component-wise instead of just 2, with $n$ held fixed and $k$ varying. The $n=3$ row ($3k^2+3k+1$) matches the centered hexagonal numbers, which normally count dots arranged in concentric hexagonal rings around a center point. The $n=4$ row apparently matches a centered octahedral sequence, which normally counts lattice points filling out an octahedron shell by shell — per your OEIS lookup.

**Status:** Confirmed for $n=3$ directly (exact polynomial fit); $n=4$ per your OEIS match — worth double-checking that the exact A-number and offset match the row precisely, since "looks like octahedral" and "is literally that OEIS entry, verified term-by-term" are different claims.

**Big question:** is this a genuine "$n$-dimensional figurate number" family — i.e. does the $n$-th row always equal the $(n-1)$-dimensional centered "cross-polytope" or simplex figurate numbers, generalizing hexagonal → octahedral → (4-dim analog) → …? Or do $n=3,4$ just accidentally land on named sequences because those are the two smallest nontrivial cases, and it breaks at $n=5$? You already have the $n=5$ data (leading coefficient 125, degree 4) — worth explicitly checking if the whole degree-4 polynomial matches a known 4D figurate-number formula, not just the leading term.

## 3. Leading Coefficient $= n^{n-2}$ — Cayley's Formula for Labeled Trees

**What it's counting:** the leading coefficient of the degree-$(n-1)$ polynomial from item 2 — i.e. the dominant term governing how fast the number of distinct vector sums grows as $k\to\infty$ with $n$ fixed. Numerically it equals $n^{n-2}$, which is Cayley's formula for the number of labeled trees on $n$ vertices — normally this counts the number of distinct spanning trees of the complete graph $K_n$.

**Status:** Empirical, four data points ($n=2,3,4,5$ giving $1,3,16,125$), no derivation yet.

**Big question:** is there an actual bijection between some natural leading-order structure in the $k\to\infty$ collapse of vector-sums and labeled trees on $n$ vertices? That's the difference between "cute numerical coincidence" and "real theorem." Cayley's formula shows up via Prüfer sequences, the Matrix-Tree theorem, and parking functions — any of those machineries might be the right lens here, since the underlying process (removing/depleting labeled values one at a time across parallel structures) is parking-function-adjacent.

## 4. Vectors + Asymptotics Unified

**What it's counting:** the same underlying quantity, $T(n,k)$ — the number of distinct vector sums of $k$ permutations of $1,\ldots,n$ — but tracked as a function of *both* parameters at once instead of fixing one and scaling the other. Sending $n\to\infty$ with $k$ fixed gives near-$(n!)^2$-scale growth (the original $T(n)$ direction); sending $k\to\infty$ with $n$ fixed gives merely polynomial growth of degree $n-1$ (items 2–3). Same object, two wildly different growth regimes depending on which parameter is scaled.

**Status:** Both regimes now have concrete, verified data; neither has a unifying derivation yet.

**Big question:** can one generating function or one piece of asymptotic machinery produce both limits as special cases — i.e., a genuine two-variable asymptotic analysis of $T(n,k)$ as $n,k\to\infty$ jointly (fixing a ratio, or one then the other) that recovers the Vandermonde/Franel-style behavior in one direction and the $n^{n-2}k^{n-1}$-type polynomial behavior in the other? That's exactly the kind of result that would let "vector analysis" and "asymptotic analysis" become one section instead of two.
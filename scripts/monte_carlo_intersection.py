#!/usr/bin/env python3
"""
BC-MFA Reproducibility Artifact
-------------------------------
Verifies all analytical formulas, worked example (Fig. 3), response divergence
(Eq. 3), and the 500-trial rational-adversary Monte Carlo intersection analysis
(Table III) for:

  "Blind Cognitive Multi-Factor Authentication Architecture for Untrusted Web
   and Mobile Endpoints under OpenID Connect"
  Carlos André Sousa, ISPGAYA (2026/2027)

Requires only the Python 3 standard library.
Fixed PRNG seed: 2026
"""

import itertools
import math
import random
import statistics

SEED = 2026
TRIALS = 500
DIVERGENCE_PAIRS = 200_000

QUADS = [
    [(0, 0), (0, 1), (1, 0), (1, 1)],  # Q1
    [(0, 2), (0, 3), (1, 2), (1, 3)],  # Q2
    [(2, 0), (2, 1), (3, 0), (3, 1)],  # Q3
    [(2, 2), (2, 3), (3, 2), (3, 3)],  # Q4
]
HALVES = [
    [(r, c) for r in range(2) for c in range(4)],
    [(r, c) for r in range(2, 4) for c in range(4)],
]
OFFSETS_NO_ZERO = [(r, c) for r in range(4) for c in range(4) if (r, c) != (0, 0)]
ALL_PATHS = list(itertools.permutations(OFFSETS_NO_ZERO, 4))


def verify_entropies() -> None:
    """Verify Eq. (1) challenge matrix Shannon entropies (Section IV-B)."""
    h_full = 16 * math.log2(36)
    h_d4_unconstrained = math.log2(math.comb(36, 4)) + math.log2(
        math.factorial(16) / (math.factorial(4) ** 4)
    )
    h_d4_quad = math.log2(math.comb(36, 4)) + 4 * math.log2(math.factorial(4))
    h_d2_half = math.log2(math.comb(36, 8)) + 2 * math.log2(math.factorial(8))

    print("=== 1. Challenge Matrix Entropies (Eq. 1) ===")
    print(f"BC-MFA quadrant-balanced (d=L=4): {h_d4_quad:.2f} bits")
    print(f"Half-balanced (d=L=2):            {h_d2_half:.2f} bits")
    print(f"Unconstrained multiset (d=4):     {h_d4_unconstrained:.2f} bits")
    print(f"Unconstrained i.i.d. (36^16):     {h_full:.2f} bits")
    print(f"Valid non-zero paths Omega:       {len(ALL_PATHS):,} (15!/11!)")
    print(f"Full secret space L*Omega (L=4):  {4 * len(ALL_PATHS):,}\n")


def verify_worked_example() -> None:
    """Verify Fig. 3 worked 4x4 toroidal matrix example (Section IV-B)."""
    grid = [
        ["M", "7", "3", "K"],
        ["K", "3", "7", "M"],
        ["7", "K", "M", "3"],
        ["3", "M", "K", "7"],
    ]
    for idx, q in enumerate(QUADS, 1):
        assert sorted(grid[r][c] for r, c in q) == ["3", "7", "K", "M"], f"Q{idx} unbalanced"

    r0, c0 = 0, 3  # Anchor N_ch = 'K' inside Q2
    assert grid[r0][c0] == "K"
    offsets = [(0, 1), (1, 2), (2, 1), (3, 3)]
    response = "".join(grid[(r0 + dr) % 4][(c0 + dc) % 4] for dr, dc in offsets)
    assert response == "M37K", f"Unexpected response: {response}"
    print("=== 2. Worked Example (Fig. 3) ===")
    print(f"Anchor K in Q2 -> (0,3); offsets {offsets} -> R_t = '{response}' [VERIFIED]\n")


def gen_grid_quad(syms):
    grid = [[0] * 4 for _ in range(4)]
    anchors = []
    for q in QUADS:
        s = list(syms)
        random.shuffle(s)
        for (r, c), ch in zip(q, s):
            grid[r][c] = ch
            if ch == syms[0]:
                anchors.append((r, c))
    return grid, anchors


def gen_grid_half(syms):
    grid = [[0] * 4 for _ in range(4)]
    anchors = []
    for h in HALVES:
        s = list(syms)
        random.shuffle(s)
        for (r, c), ch in zip(h, s):
            grid[r][c] = ch
            if ch == syms[0]:
                anchors.append((r, c))
    return grid, anchors


def gen_grid_d1(syms):
    grid = [[0] * 4 for _ in range(4)]
    s = list(syms)
    random.shuffle(s)
    anchor = None
    for idx, ch in enumerate(s):
        r, c = divmod(idx, 4)
        grid[r][c] = ch
        if ch == syms[0]:
            anchor = [(r, c)]
    return grid, anchor


def eval_path(grid, r0, c0, path):
    return tuple(grid[(r0 + dr) % 4][(c0 + dc) % 4] for dr, dc in path)


def run_mc_regime(label, gen_fn, L, n_syms):
    """Simulate a rational consistent adversary tracking (q, path) across k=1..4."""
    random.seed(SEED)
    syms = list(range(n_syms))
    results = {k: [] for k in range(1, 5)}

    for _ in range(TRIALS):
        true_q = random.randrange(L)
        true_p = random.choice(ALL_PATHS)
        surviving = None
        for k in range(1, 5):
            grid, anchors = gen_fn(syms)
            r0, c0 = anchors[true_q]
            resp = eval_path(grid, r0, c0, true_p)
            if k == 1:
                surviving = []
                for q in range(L):
                    ar, ac = anchors[q]
                    pos = {s: [] for s in range(n_syms)}
                    for dr, dc in OFFSETS_NO_ZERO:
                        pos[grid[(ar + dr) % 4][(ac + dc) % 4]].append((dr, dc))
                    p0, p1, p2, p3 = pos[resp[0]], pos[resp[1]], pos[resp[2]], pos[resp[3]]
                    for o0 in p0:
                        for o1 in p1:
                            if o1 == o0:
                                continue
                            for o2 in p2:
                                if o2 == o0 or o2 == o1:
                                    continue
                                for o3 in p3:
                                    if o3 == o0 or o3 == o1 or o3 == o2:
                                        continue
                                    surviving.append((q, (o0, o1, o2, o3)))
            else:
                surviving = [
                    (q, p)
                    for (q, p) in surviving
                    if eval_path(grid, anchors[q][0], anchors[q][1], p) == resp
                ]
            results[k].append(len(surviving))

    print(f"Regime: {label} (trials={TRIALS}, seed={SEED})")
    for k in range(1, 5):
        vals = sorted(results[k])
        mean = statistics.mean(vals)
        sd = statistics.stdev(vals)
        med = statistics.median(vals)
        p05 = vals[int(0.05 * len(vals))]
        p95 = vals[int(0.95 * len(vals))]
        exact = sum(1 for v in vals if v == 1) / len(vals) * 100.0
        print(
            f"  k={k}: mean={mean:6.2f} +/- {sd:6.2f} | median={med:5.1f} | "
            f"P5={p05:3d} | P95={p95:3d} | Pr(|C_k|=1)={exact:5.1f}%"
        )
    print()


def verify_divergence() -> None:
    """Verify Eq. (3) consecutive response divergence probability."""
    random.seed(SEED)
    same_fixed = 0
    same_fresh = 0
    alphabet = list(range(36))
    for _ in range(DIVERGENCE_PAIRS):
        tq = random.randrange(4)
        tp = random.choice(ALL_PATHS)
        g1, a1 = gen_grid_quad([0, 1, 2, 3])
        g2, a2 = gen_grid_quad([0, 1, 2, 3])
        if eval_path(g1, a1[tq][0], a1[tq][1], tp) == eval_path(g2, a2[tq][0], a2[tq][1], tp):
            same_fixed += 1
        s1 = random.sample(alphabet, 4)
        s2 = random.sample(alphabet, 4)
        g1, a1 = gen_grid_quad(s1)
        g2, a2 = gen_grid_quad(s2)
        if eval_path(g1, a1[tq][0], a1[tq][1], tp) == eval_path(g2, a2[tq][0], a2[tq][1], tp):
            same_fresh += 1

    print(f"=== 4. Consecutive Response Divergence (Eq. 3, {DIVERGENCE_PAIRS:,} pairs) ===")
    print(f"Fixed Sigma_sub (worst-case finite grid): {(1 - same_fixed / DIVERGENCE_PAIRS) * 100:.2f}%")
    print(f"Fresh Sigma_sub (|Sigma|=36):             {(1 - same_fresh / DIVERGENCE_PAIRS) * 100:.3f}%")


def main() -> None:
    verify_entropies()
    verify_worked_example()
    print("=== 3. Rational-Adversary Monte Carlo Intersection Analysis (Table III) ===")
    run_mc_regime("Naive (d=1, L=1)", gen_grid_d1, 1, 16)
    run_mc_regime("Half-Balanced (d=2, L=2)", gen_grid_half, 2, 8)
    run_mc_regime("BC-MFA Quadrant-Balanced (d=4, L=4)", gen_grid_quad, 4, 4)
    verify_divergence()


if __name__ == "__main__":
    main()

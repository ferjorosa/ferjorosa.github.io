# Analysis of Qwen 3 Thinking Reasoning vs. Variable Elimination

## Algorithm Comparison

**Ground Truth (Variable Elimination):**
1.  **Formalism:** Factors ($\phi$), Product, Marginalization.
2.  **Process:** Systematic factor operations.

**Qwen Approach:**
1.  **Formalism:** **Direct Probabilistic Expansion** (Chain Rule / Law of Total Probability).
2.  **Process:**
    *   **Goal Definition:** States $P(Q|E) = \frac{P(Q,E)}{P(E)}$.
    *   **Denominator:** Computes the marginal $P(V_1=s_0)$ by summing over $V_0$.
    *   **Numerator:** Derives the joint probability formula by considering the dependencies (parents of $V_3$ are $V_0, V_1$).
    *   **Execution:** Calculates terms independently and sums them.

**Key Differences:**
*   **Methodology:** Like the others, it relies on probability theory basics rather than the specific VE algorithm.
*   **Structure:** It breaks the problem strictly into "Denominator Calculation" and "Numerator Calculation", treating them as separate sub-problems.

## Arithmetic & Verification

1.  **Approximation vs. Precision:** Qwen shows a mix of approximation and precise calculation.
    *   It starts with approximations ("approx 0.1555") but then corrects itself ("but exact calculation...").
    *   It uses a "decomposition" method for multiplication (e.g., $0.311 = 0.3 + 0.011$) to verify its mental arithmetic.
2.  **Iterative Refinement:**
    *   It computes a rough value, then refines it.
    *   It uses a "difference method" to estimate division: "How much less than 0.79? Difference is ... so subtract ...". This is a clever way to avoid full long division while maintaining high precision.
3.  **Self-Correction:** It frequently pauses to check consistency ("Wait, wait...", "That seems conflicting..."). It explicitly cross-checks results against earlier steps (e.g., verifying the term `0.03469312` matches a previous calculation).

## Conclusion

*   **Algorithmic Fidelity:** It **does not** use Variable Elimination. It uses a **Law of Total Probability** approach.
*   **Efficiency:**
    *   **Logical:** High. It correctly identifies the structure and dependencies.
    *   **Computational:** Moderate. It spends a fair amount of tokens on arithmetic verification (decomposition, difference estimation), but it is less obsessive than Kimi's digit-by-digit long division. It finds a balance between estimation and exactness.


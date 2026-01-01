## Proposal: “Variable elimination algorithm” section

### Goal of the section
Explain **variable elimination (VE)** as an *exact* inference procedure that computes \(P(\mathbf{Q}\mid \mathbf{E}=\mathbf{e})\) by operating on **local factors** (CPTs) instead of expanding the full joint. The reader should finish with:
- a clear mental model (“eliminate one hidden variable at a time by multiplying the factors that mention it, then summing it out”),
- a crisp algorithm they could implement,
- an understanding of what determines runtime (intermediate factor size / elimination order),
- and how evidence is incorporated (factor restriction + normalization).

### Section structure (recommended headings + content beats)

#### 1) One-paragraph intuition (what VE is doing)
Open with the core idea: inference queries look like “sum of a product,” and VE is just a **reordering of computation** that avoids building the full product table.

Suggested beats:
- Start from an unnormalized quantity \(\tilde{P}(\mathbf{q})\) and normalize at the end.
- Emphasize locality: we only ever touch the CPTs involving a variable and the intermediate factors created so far.

#### 2) Ingredients: factors and the two operations
Define *exactly* what objects VE manipulates.

- **Factors**: functions over subsets of variables. Each CPT becomes a factor:
  \[
  \phi_i(x_i, \mathrm{pa}_i) \equiv P(x_i \mid \mathrm{pa}_i).
  \]
- **Evidence absorption (restriction)**: if \(E=e\), any factor containing \(E\) becomes \(\phi(\cdot)\big|_{E=e}\). This reduces the factor’s effective dimensionality.
- **Factor product**: if \(f(A)\) and \(g(B)\), then \((f\cdot g)(A\cup B)\).
- **Sum-out (marginalization)**: for hidden \(Z\),
  \[
  (\sum_Z f)(\text{scope}(f)\setminus\{Z\}) \;=\; \sum_z f(z,\ldots).
  \]

Short note: keep this framed as “table operations” for discrete BNs, but defined abstractly so it reads cleanly.

#### 3) Problem statement in the VE-friendly form
State VE’s target as “compute an unnormalized factor over \(\mathbf{Q}\) then normalize.”

- Let \(\mathbf{Z}=X\setminus(\mathbf{Q}\cup\mathbf{E})\).
- After conditioning on evidence, we want:
  \[
  \tilde{P}(\mathbf{q}) \;=\; \sum_{\mathbf{z}} \prod_{i=1}^n \phi_i(\cdot)\big|_{\mathbf{E}=\mathbf{e}}.
  \]
- Then:
  \[
  P(\mathbf{Q}=\mathbf{q}\mid \mathbf{E}=\mathbf{e})
  \;=\;
  \frac{\tilde{P}(\mathbf{q})}{\sum_{\mathbf{q}}\tilde{P}(\mathbf{q})}.
  \]

This keeps normalization conceptually separate and makes the algorithm read naturally.

#### 4) The algorithm (core loop)
Present as a compact numbered recipe or pseudo-code-style prose.

**Inputs**:
- factors \(\{\phi_i\}\) from CPTs,
- query variables \(\mathbf{Q}\),
- evidence assignment \(\mathbf{E}=\mathbf{e}\),
- an elimination order \(\pi\) over \(\mathbf{Z}\).

**Procedure**:
1. **Condition on evidence**: for each factor \(\phi\) containing any \(E\in\mathbf{E}\), restrict it to \(E=e\).
2. For each \(Z\) in the elimination order \(\pi\):
   - Collect all factors that mention \(Z\): \(\mathcal{F}_Z=\{f\in\mathcal{F}: Z\in\mathrm{scope}(f)\}\).
   - Multiply them into a single factor:
     \[
     g \;=\; \prod_{f\in \mathcal{F}_Z} f.
     \]
   - Eliminate \(Z\) by summing it out:
     \[
     h \;=\; \sum_Z g.
     \]
   - Replace \(\mathcal{F}_Z\) in the factor set with \(h\).
3. Multiply the remaining factors to obtain a factor over \(\mathbf{Q}\):
   \[
   \tilde{P}(\mathbf{Q}) \;=\; \prod_{f\in\mathcal{F}} f.
   \]
4. **Normalize** \(\tilde{P}(\mathbf{Q})\) to get \(P(\mathbf{Q}\mid\mathbf{e})\).

Optional micro-clarifications:
- If the query is a single number \(P(\mathbf{Q}=\mathbf{q}\mid\mathbf{e})\), compute the full \(\tilde{P}(\mathbf{Q})\) and then read off \(\mathbf{q}\) after normalization.
- Deterministic evidence can be seen as “zeroing out” inconsistent rows in factor tables.

#### 5) Why elimination order matters (one focused paragraph)
Explain cost at a high level without diving into graph theory.

Key points:
- The size of intermediate factor \(g\) grows with the number of variables in its scope and their cardinalities.
- The elimination order controls these scopes; poor orders create large intermediate factors early.
- A clean statement like: “VE is exponential in the size of the largest intermediate factor (often summarized by treewidth).”

Optionally name heuristics in one sentence (no details): min-fill / min-degree.

#### 6) (Optional) Two simplifications worth mentioning briefly
Only include if it helps your later narrative; keep it short.

- **Pruning irrelevant variables**: variables that cannot influence \(\mathbf{Q}\) once \(\mathbf{E}\) is fixed can be dropped before running VE (conceptually via conditional independence / d-separation).
- **Barren nodes**: variables that do not affect the query (after evidence) can be removed, shrinking the factor set.

#### 7) One-sentence wrap that bridges to the rest of the post
End with a line that sets up your LLM/probabilistic reasoning angle:
- VE is exact and principled, but worst-case expensive; practical success depends on exploiting structure (good orders, sparsity, conditional independencies) and motivates approximations/heuristics.

### Tone notes (to match your blog)
- Keep the prose **math-forward but intuitive**: each equation should be paired with a “what this means operationally” sentence.
- Avoid references to other posts; keep it self-contained.
- Prefer consistent notation with your earlier section: \(\mathbf{Q},\mathbf{E},\mathbf{Z}\), and “CPT \(\rightarrow\) factor.”


## Probabilistic inference on Bayesian networks

Given the Bayesian network defined above (variables, DAG structure, and CPTs), we are often interested in answering probabilistic queries of the form
\begin{equation}
P(\mathbf{Q}=\mathbf{q}\mid \mathbf{E}=\mathbf{e}),
\end{equation}
where \(\mathbf{Q}\subseteq X\) is the set of query variables, \(\mathbf{E}\subseteq X\) is the set of evidence variables observed to take values \(\mathbf{e}\), and \(\mathbf{Z}=X\setminus(\mathbf{Q}\cup \mathbf{E})\) is the set of latent (unobserved) variables.

Using the BN factorization, this conditional can be written in the standard “sum of a product” form:
\begin{equation}
P(\mathbf{Q}=\mathbf{q}\mid \mathbf{E}=\mathbf{e})
\;=\;
\frac{\sum_{\mathbf{z}} \prod_{i=1}^n P(x_i \mid \mathbf{Pa}_i)\big|_{\mathbf{E}=\mathbf{e}}}
{\sum_{\mathbf{q}} \sum_{\mathbf{z}} \prod_{i=1}^n P(x_i \mid \mathbf{Pa}_i)\big|_{\mathbf{E}=\mathbf{e}}}.
\end{equation}
The denominator is a normalization constant ensuring the result sums to 1 over \(\mathbf{q}\).

Computing these quantities exactly is, in the worst case, computationally intractable, but the BN factorization offers structure we can exploit. In discrete BNs, exact inference ultimately reduces to three kinds of operations:
1. multiplying local tables (CPTs) and intermediate tables,
2. incorporating evidence by fixing observed variables to their values,
3. summing out latent variables \(\mathbf{Z}\).

The **variable elimination** algorithm is a systematic way to do this without ever forming the full joint table.


## Variable elimination algorithm

Variable elimination (VE) is an exact inference algorithm that computes \(P(\mathbf{Q}\mid \mathbf{E}=\mathbf{e})\) by manipulating **factors**—local functions over small subsets of variables—rather than expanding the joint distribution explicitly.

### Factors

A factor \(\phi(\mathbf{S})\) is a function from assignments of a set of variables \(\mathbf{S}\) (the *scope* of the factor) to a nonnegative real number. In a BN, each CPT is a factor:
\begin{equation}
\phi_i(X_i,\mathbf{Pa}_i) \;\equiv\; P(X_i\mid \mathbf{Pa}_i).
\end{equation}

During inference, VE creates intermediate factors that are typically **unnormalized**. This is convenient: we can compute an unnormalized quantity and normalize once at the end.

### Evidence as factor restriction

If an evidence variable \(E\in \mathbf{E}\) is observed to be \(e\), any factor \(\phi(\mathbf{S})\) that includes \(E\) can be restricted to that value, producing a smaller factor:
\begin{equation}
\phi'(\mathbf{S}\setminus \{E\}) \;=\; \phi(\mathbf{S})\big|_{E=e}.
\end{equation}
Operationally, this corresponds to selecting the slice of the table consistent with the observation.

### Two atomic operations

VE relies on two simple operations on factors.

1. **Product (pointwise multiplication).**  
If \(f(\mathbf{A})\) and \(g(\mathbf{B})\) are factors, their product is a factor over \(\mathbf{A}\cup \mathbf{B}\):
\begin{equation}
(f\cdot g)(\mathbf{A}\cup \mathbf{B}) \;=\; f(\mathbf{A})\, g(\mathbf{B}),
\end{equation}
where both sides are evaluated on a consistent joint assignment.

2. **Sum-out (marginalization).**  
If \(Z\in \mathbf{S}\) and \(\phi(\mathbf{S})\) is a factor, summing out \(Z\) produces a new factor over \(\mathbf{S}\setminus\{Z\}\):
\begin{equation}
\left(\sum_Z \phi\right)(\mathbf{S}\setminus\{Z\}) \;=\; \sum_{z} \phi(\mathbf{S}).
\end{equation}

### The VE objective: compute an unnormalized \(\tilde{P}(\mathbf{Q})\), then normalize

After restricting all CPT factors to the evidence \(\mathbf{E}=\mathbf{e}\), define
\begin{equation}
\tilde{P}(\mathbf{q})
\;=\;
\sum_{\mathbf{z}} \prod_{i=1}^n \phi_i(\cdot)\big|_{\mathbf{E}=\mathbf{e}}.
\end{equation}
VE computes \(\tilde{P}(\mathbf{Q})\) as a factor over \(\mathbf{Q}\). The conditional distribution is then obtained by normalization:
\begin{equation}
P(\mathbf{Q}=\mathbf{q}\mid \mathbf{E}=\mathbf{e}) \;=\; \frac{\tilde{P}(\mathbf{q})}{\sum_{\mathbf{q}} \tilde{P}(\mathbf{q})}.
\end{equation}

### The algorithm

**Input:** CPT factors \(\{\phi_i\}\), query variables \(\mathbf{Q}\), evidence \(\mathbf{E}=\mathbf{e}\), elimination order \(\pi\) over \(\mathbf{Z}=X\setminus(\mathbf{Q}\cup\mathbf{E})\).  
**Output:** \(P(\mathbf{Q}\mid \mathbf{E}=\mathbf{e})\).

1. **Initialize the factor set.**  
Start with \(\mathcal{F} \leftarrow \{\phi_1,\dots,\phi_n\}\) and restrict each factor to the evidence \(\mathbf{E}=\mathbf{e}\) (dropping fixed variables from its scope).

2. **Eliminate latent variables one at a time.**  
For each variable \(Z\) in the elimination order \(\pi\):
   - **Collect** all factors that mention \(Z\):
     \[
     \mathcal{F}_Z \;=\; \{f\in \mathcal{F} : Z\in \mathrm{scope}(f)\}.
     \]
   - **Multiply** them into a single factor:
     \[
     g \;=\; \prod_{f\in \mathcal{F}_Z} f.
     \]
   - **Sum out** the variable:
     \[
     h \;=\; \sum_Z g.
     \]
   - **Update** the factor set:
     \[
     \mathcal{F} \leftarrow (\mathcal{F}\setminus \mathcal{F}_Z)\cup \{h\}.
     \]

3. **Finish and normalize.**  
After all \(Z\in\mathbf{Z}\) have been eliminated, multiply the remaining factors to obtain an unnormalized factor over \(\mathbf{Q}\):
\begin{equation}
\tilde{P}(\mathbf{Q}) \;=\; \prod_{f\in\mathcal{F}} f.
\end{equation}
Normalize \(\tilde{P}(\mathbf{Q})\) to obtain \(P(\mathbf{Q}\mid \mathbf{E}=\mathbf{e})\).

### Why the elimination order matters

VE’s runtime and memory are dominated by the largest intermediate factor created during elimination. When we collect and multiply the factors containing \(Z\), the resulting factor \(g\) may involve many variables; summing out \(Z\) removes one variable, but the intermediate table can still be large. Different elimination orders \(\pi\) can therefore change the cost by orders of magnitude. In practice, good orders aim to keep intermediate scopes small (often discussed in terms of induced width / treewidth), and simple heuristics such as *min-fill* or *min-degree* are commonly used to choose \(\pi\).

### Practical simplifications (optional, but often useful)

Before (or during) VE, the factor set can often be reduced:
- **Prune irrelevant variables.** If parts of the network cannot influence \(\mathbf{Q}\) once \(\mathbf{E}\) is fixed (intuitively: they are conditionally independent of \(\mathbf{Q}\) given \(\mathbf{E}\)), they can be dropped.
- **Remove barren nodes.** Variables that do not affect the query (after evidence is incorporated) can be eliminated early, reducing computation \citep{druzdzel1993}.



---
layout: post
title: "How capable are language models at probabilistic reasoning?"
date: 2026-01-02
categories: blog
description: "Exploring how frontier LLMs approach probabilistic inference on Bayesian networks, comparing their reasoning strategies against the Variable Elimination algorithm."
tags: [Probabilistic Reasoning]
---

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">Table of Contents</summary>

<ul style="margin-top: 0.5em;">
  <li style="margin-bottom: 0.5em;"><a href="#can-large-language-models-think-rationally">Can language models think "probabilistically"?</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#bayesian-networks">Bayesian networks</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#probabilistic-inference-on-bayesian-networks">Probabilistic inference on Bayesian networks</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#variable-elimination-algorithm">Variable Elimination algorithm</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#operations-on-factors">Operations on factors</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#the-algorithm">The algorithm</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#example">Example</a>
        <ul style="margin-top: 0.3em;">
          <li style="margin-bottom: 0.3em;"><a href="#step-1-restrict-factors">Step 1: Restrict factors based on evidence</a></li>
          <li style="margin-bottom: 0.3em;"><a href="#step-2-eliminate-v2">Step 2: Eliminate V2</a></li>
          <li style="margin-bottom: 0.3em;"><a href="#step-3-eliminate-v0">Step 3: Eliminate V0</a></li>
          <li style="margin-bottom: 0.3em;"><a href="#step-4-normalize">Step 4: Normalize</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#how-llms-do-it">How LLMs do it</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#experimental-setup">Experimental setup</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#raw-reasoning-results">Raw reasoning results</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#code-generation-results">Code generation results</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#conclusion">Conclusion</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#references">References</a></li>
</ul>

</details>

<h2 id="can-large-language-models-think-rationally">Can language models think "probabilistically"?</h2>

This question has been on my mind for a while. It motivated me to revisit probabilistic graphical models, write my [blog series on Decision Theory](https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html), and explore how large language models (LLMs) solved [a few hand-crafted decision problems](https://github.com/ferjorosa/decision-theory-llms/blob/main/notebooks/how_good_are_llms_decision_problems.ipynb).

Early experiments were promising: models like O3 and Gemini-2.5-Pro reached correct solutions on small decision problems. But I observed they were solving them using decision trees, which [have theoretical limitations](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html). I wondered: were LLMs using decision trees because it was "easier", or because they didn't know how to apply influence diagrams?

To answer that, I started running more extensive experiments. But midway through, I realized I was getting ahead of myself. If I wanted to evaluate LLMs on influence diagrams, I should probably start with Bayesian networks, since influence diagrams are essentially Bayesian networks augmented with decisions and utilities. If LLMs struggle with probabilistic inference on Bayesian networks, expecting them to solve full decision problems could be premature.

So that's what this post explores: **how do current frontier LLMs handle probabilistic inference on a Bayesian network?** I'll walk through the Variable Elimination algorithm since it is one of the easiest to understand and implement, solve an example by hand with it, and then compare how seven reasoning LLMs approach the same query, analyzing not just whether they get the right answer, but *how* they reason through the problem.

<h2 id="bayesian-networks">Bayesian networks</h2>

A Bayesian network (BN) is a directed acyclic graph (DAG) in which nodes represent random variables. Arcs encode conditional dependencies between variables in a way that allows us to factorize the joint probability distribution into a product of conditional probability distributions (CPDs),

$$
\begin{equation}
P(\mathbf{\textcolor{purple}{V}}) = P(\textcolor{purple}{V_1}, \ldots, \textcolor{purple}{V_n}) = \prod_{i=1}^{n} P(\textcolor{purple}{V_i} | \mathbf{Pa}_{\textcolor{purple}{V_i}})
\end{equation}
$$

where $$\mathbf{Pa}_{\textcolor{purple}{V_i}}$$ denotes the parents of variable $$\textcolor{purple}{V_i}$$ in the DAG. This property is often called the **chain rule for Bayesian networks**.


As an example, consider a Bayesian network with 4 binary variables ($$\textcolor{purple}{V_0}, \textcolor{purple}{V_1}, \textcolor{purple}{V_2}, \textcolor{purple}{V_3}$$). The structure is a simple diamond-like shape where $$\textcolor{purple}{V_0}$$ is the root, $$\textcolor{purple}{V_1}$$ and $$\textcolor{purple}{V_2}$$ depend on $$\textcolor{purple}{V_0}$$, and $$\textcolor{purple}{V_3}$$ depends on both $$\textcolor{purple}{V_0}$$ and $$\textcolor{purple}{V_1}$$.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-12-14-llms-bn-inference/bn_example.png" alt="Bayesian network example" 
      height="300">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Bayesian network example with 4 variables</i>
    </td>
  </tr>
</table>
</center>

<table>
  <tr>
    <th colspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_0})$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.5072</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.4928</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_1} \mid \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.3110</td>
    <td>0.0704</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.6890</td>
    <td>0.9296</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_2} \mid \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.8950</td>
    <td>0.0562</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.1050</td>
    <td>0.9438</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_3} \mid \textcolor{purple}{V_0},\, \textcolor{purple}{V_1})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0 = s_0}$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0 = s_1}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_1}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.0607</td>
    <td>0.8173</td>
    <td>0.8890</td>
    <td>0.2251</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.9393</td>
    <td>0.1827</td>
    <td>0.1110</td>
    <td>0.7749</td>
  </tr>
</table>

<h2 id="probabilistic-inference-on-bayesian-networks">Probabilistic inference on Bayesian networks</h2>

Once we have a BN, we can use it to reason by performing probabilistic inference. This task involves computing the probability of query variables $$\mathbf{\textcolor{purple}{Q}}$$ given some observed evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$.

Theoretically, this is straightforward. The Bayesian network defines the full joint distribution, so we could sum over all unobserved "nuisance" variables $$\mathbf{\textcolor{purple}{Z}}$$:

$$
\begin{equation}
P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}} \mid \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}) = \frac{\sum_{\mathbf{\textcolor{purple}{z}}} P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}, \mathbf{\textcolor{purple}{Z}} = \mathbf{\textcolor{purple}{z}})}{\sum_{\mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{z}}} P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}, \mathbf{\textcolor{purple}{Z}} = \mathbf{\textcolor{purple}{z}})}
\end{equation}
$$

However, this naive approach is computationally infeasible. For a network with $$n$$ binary variables, storing the full joint distribution would require a table with $$2^n$$ entries.

Instead of storing that massive table, we can use the **BN factorization** (Equation 1) to compute only the specific joint probabilities we need on-the-fly. By substituting the factorization into Equation (2), we get:

$$
\begin{equation}
P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}} \mid \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}) = \frac{\sum_{\mathbf{\textcolor{purple}{z}}} \prod_{i=1}^{n} P(\textcolor{purple}{V_i} \mid \mathbf{Pa}_{\textcolor{purple}{V_i}})}{\sum_{\mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{z}}} \prod_{i=1}^{n} P(\textcolor{purple}{V_i} \mid \mathbf{Pa}_{\textcolor{purple}{V_i}})}
\end{equation}
$$

While this saves us from storing the full table, we still face the problem of summing over it. We still need to enumerate all combinations of hidden variables $$\mathbf{\textcolor{purple}{z}}$$. For 30 binary variables, that's over a billion terms to sum. This approach, often called **inference by enumeration** or simply applying the **chain rule** naively, is conceptually simple but does not scale.

Efficient inference algorithms avoid this exponential blowup by exploiting the factorized representation more cleverly. Rather than enumerating all combinations, they manipulate the individual CPDs (which are much smaller) and perform marginalization locally, pushing sums inside products where conditional independence allows. Well-known examples include Variable Elimination, Junction Tree algorithm, and Belief Propagation (<a href="http://mcb111.org/w06/KollerFriedman.pdf">Koller & Friedman, 2009</a>). We'll focus on Variable Elimination since it's the easiest to explain and commonly used when teaching BN inference.

<h2 id="variable-elimination-algorithm">Variable Elimination algorithm</h2>

As the name suggests, the **Variable Elimination** (VE) algorithm works by eliminating the variables of the network until it yields the answer to a specific query. This algorithm is
typically defined in terms of factors.

A **factor** $$\phi(\mathbf{\textcolor{purple}{X}})$$ is a function that maps a set of variables $$\mathbf{\textcolor{purple}{X}}$$ to a real positive value. CPDs are an example of factors. In fact, the initial set of factors corresponds exactly to the CPDs of the network.

During inference, new factors are created by multiplying and marginalizing existing ones. These **intermediate factors** are generally **unnormalized**, meaning their values do not sum to one. This is not a problem, since normalization is only required for the final result. Working with unnormalized factors simplifies computation and allows inference algorithms to focus on local operations.

<h3 id="operations-on-factors">Operations on factors</h3>

VE relies on three operations:

1. **Factor Product:** Combine two factors $$\phi_1(\textcolor{purple}{V_1})$$ and $$\phi_2(\textcolor{purple}{V_2})$$ into a new factor $$\phi_{new}$$ over $$\textcolor{purple}{V_1} \cup \textcolor{purple}{V_2}$$ by multiplying their values for every consistent assignment:

$$
\phi_{new}(\textcolor{purple}{V_1}, \textcolor{purple}{V_2}) = \phi_1(\textcolor{purple}{V_1}) \cdot \phi_2(\textcolor{purple}{V_2})
$$

2. **Marginalization:** Eliminate a variable $$\textcolor{purple}{Z}$$ from factor $$\phi(\textcolor{purple}{V}, \textcolor{purple}{Z})$$ by summing over all its values to produce a new factor $$\phi_{new}$$:

   $$\phi_{new}(\textcolor{purple}{V}) = \sum_{\textcolor{purple}{z}} \phi(\textcolor{purple}{V}, \textcolor{purple}{Z} =\textcolor{purple}{z})$$

3. **Evidence restriction:** If variable $$\textcolor{purple}{E}$$ is observed to be $$\textcolor{purple}{e}$$, restrict any factor containing $$\textcolor{purple}{E}$$ to that value, essentially selecting the slice of the table consistent with the observation.

<h3 id="the-algorithm">The algorithm</h3>

Given a Bayesian network, query variables $$\mathbf{\textcolor{purple}{Q}}$$, and evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$:

1. **Initialize:** Treat each CPD as a factor. Restrict all factors to be consistent with the evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$.

2. **Choose elimination order:** Pick an ordering for the hidden variables $$\mathbf{\textcolor{purple}{Z}}$$ (neither query nor evidence). The choice of ordering affects efficiency because **bad orders create large intermediate factors**.

<!-- Here we should later put a comment with a reference or something explaining different heuristics for elimination order -->

3. **Eliminate variables:** For each variable $$\textcolor{purple}{Z_i}$$ in order:
   - **Collect** all factors containing $$\textcolor{purple}{Z_i}$$
   - **Multiply** them into a single factor $$\phi_{new}'$$
   - **Sum out** $$\textcolor{purple}{Z_i}$$ to get a new factor $$\phi_{new}''$$
   - **Replace** the collected factors with $$\phi_{new}''$$

4. **Normalize:** Multiply remaining factors (now only over $$\mathbf{\textcolor{purple}{Q}}$$) and normalize to obtain $$P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}} \mid \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}})$$.

<h3 id="example">Example</h3>

As an example we are going to use the BN we defined in Figure 1 and compute the probability of $$\textcolor{purple}{V_3}$$ being $$\textcolor{purple}{s_1}$$ given that $$\textcolor{purple}{V_1}$$ is observed to be $$\textcolor{purple}{s_0}$$:

$$P(\textcolor{purple}{V_3} = \textcolor{purple}{s_1} \mid \textcolor{purple}{V_1} = \textcolor{purple}{s_0})$$

The evidence is $$\mathbf{\textcolor{purple}{E}} = \{\textcolor{purple}{V_1} = \textcolor{purple}{s_0}\}$$. The query variable is $$\mathbf{\textcolor{purple}{Q}} = \{\textcolor{purple}{V_3}\}$$. The hidden variables to eliminate are $$\mathbf{\textcolor{purple}{Z}} = \{\textcolor{purple}{V_0}, \textcolor{purple}{V_2}\}$$.

We start with the initial factors (the CPDs):

$$
\begin{aligned}
\phi_0(\textcolor{purple}{V_0}) &= P(\textcolor{purple}{V_0}) \\
\phi_1(\textcolor{purple}{V_1}, \textcolor{purple}{V_0}) &= P(\textcolor{purple}{V_1} \mid \textcolor{purple}{V_0}) \\
\phi_2(\textcolor{purple}{V_2}, \textcolor{purple}{V_0}) &= P(\textcolor{purple}{V_2} \mid \textcolor{purple}{V_0}) \\
\phi_3(\textcolor{purple}{V_3}, \textcolor{purple}{V_0}, \textcolor{purple}{V_1}) &= P(\textcolor{purple}{V_3} \mid \textcolor{purple}{V_0}, \textcolor{purple}{V_1})
\end{aligned}
$$

For the elimination order, we have randomly selected to start with $$\textcolor{purple}{V_2}$$ and then $$\textcolor{purple}{V_0}$$.

<h4 id="step-1-restrict-factors">Step 1: Restrict factors based on evidence</h4>

Since we observe $$\textcolor{purple}{V_1} = \textcolor{purple}{s_0}$$, we restrict any factor containing $$\textcolor{purple}{V_1}$$ to this value.

For $$\phi_1(\textcolor{purple}{V_1}, \textcolor{purple}{V_0})$$, we fix $$\textcolor{purple}{V_1} = \textcolor{purple}{s_0}$$. Since $$\textcolor{purple}{V_1}$$ is now a constant, the resulting factor depends only on $$\textcolor{purple}{V_0}$$. We call this new factor $$\phi_1'(\textcolor{purple}{V_0})$$:

<center>
<table>
  <tr>
    <th colspan="2" style="text-align: center;">$$\phi_1'(\textcolor{purple}{V_0})$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.3110</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.0704</td>
  </tr>
</table>
</center>

For $$\phi_3(\textcolor{purple}{V_3}, \textcolor{purple}{V_0}, \textcolor{purple}{V_1})$$, we similarly select the entries consistent with $$\textcolor{purple}{V_1} = \textcolor{purple}{s_0}$$. The new factor depends only on $$\textcolor{purple}{V_3}$$ and $$\textcolor{purple}{V_0}$$:

<center>
<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$\phi_3'(\textcolor{purple}{V_3}, \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.0607</td>
    <td>0.8890</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.9393</td>
    <td>0.1110</td>
  </tr>
</table>
</center>

<h4 id="step-2-eliminate-v2">Step 2: Eliminate V2</h4>

The only factor containing $$\textcolor{purple}{V_2}$$ is $$\phi_2(\textcolor{purple}{V_2}, \textcolor{purple}{V_0})$$. Summing over $$\textcolor{purple}{V_2}$$:

$$
\phi_4(\textcolor{purple}{V_0}) = \sum_{\textcolor{purple}{V_2}} \phi_2(\textcolor{purple}{V_2}, \textcolor{purple}{V_0}) = \sum_{\textcolor{purple}{V_2}} P(\textcolor{purple}{V_2} \mid \textcolor{purple}{V_0}) = 1
$$

Since $$\textcolor{purple}{V_2}$$ is a leaf node and not part of the query or evidence, it sums to 1 and effectively disappears (it is a "barren node").

<h4 id="step-3-eliminate-v0">Step 3: Eliminate V0</h4>

We collect all factors containing $$\textcolor{purple}{V_0}$$: $$\phi_0(\textcolor{purple}{V_0})$$, $$\phi_1'(\textcolor{purple}{V_0})$$, and $$\phi_3'(\textcolor{purple}{V_3}, \textcolor{purple}{V_0})$$.
We multiply them to form $$\phi_{prod}(\textcolor{purple}{V_3}, \textcolor{purple}{V_0})$$:

For $$\textcolor{purple}{V_0} = \textcolor{purple}{s_{0}}$$:

$$
\begin{aligned}
\phi_{0}(\textcolor{purple}{V_0} = \textcolor{purple}{s_0}) \cdot \phi_{1}'(\textcolor{purple}{V_0} = \textcolor{purple}{s_0}) &= 0.5072 \cdot 0.3110 = 0.1577 \\[0.5em]
\phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) &= 0.1577 \cdot \phi_{3}'(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) \\[0.5em] &= 0.1577 \cdot 0.0607 = 0.0096 \\
\phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) &= 0.1577 \cdot \phi_{3}'(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) \\[0.5em] &= 0.1577 \cdot 0.9393 = 0.1481
\end{aligned}
$$

For $$\textcolor{purple}{V_0} = \textcolor{purple}{s_{1}}$$:

$$
\begin{aligned}
\phi_{0}(\textcolor{purple}{V_0} = \textcolor{purple}{s_1}) \cdot \phi_{1}'(\textcolor{purple}{V_0} = \textcolor{purple}{s_1}) &= 0.4928 \cdot 0.0704 = 0.0347 \\[0.5em]
\phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) &= 0.0347 \cdot \phi_{3}'(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) \\[0.5em] &= 0.0347 \cdot 0.8890 = 0.0308 \\
\phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) &= 0.0347 \cdot \phi_{3}'(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) \\[0.5em] &= 0.0347 \cdot 0.1110 = 0.0039
\end{aligned}
$$

<center>
<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$\phi_{prod}(\textcolor{purple}{V_3}, \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.0096</td>
    <td>0.0308</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.1481</td>
    <td>0.0039</td>
  </tr>
</table>
</center>

Then we sum out $$\textcolor{purple}{V_0}$$ to get $$\phi_5(\textcolor{purple}{V_3})$$:

$$
\phi_5(\textcolor{purple}{V_3}) = \sum_{\textcolor{purple}{V_0}} \phi_{prod}(\textcolor{purple}{V_3}, \textcolor{purple}{V_0})
$$


$$
\begin{aligned}
\phi_5(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}) &= \phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) + \phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_0}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) \\
&= 0.0096 + 0.0308 = 0.0404 \\[1em]
\phi_5(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}) &= \phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_0}) + \phi_{prod}(\textcolor{purple}{V_3} = \textcolor{purple}{s_1}, \textcolor{purple}{V_0} = \textcolor{purple}{s_1}) \\
&= 0.1481 + 0.0039 = 0.1520
\end{aligned}
$$

<center>
<table>
  <tr>
    <th colspan="2" style="text-align: center;">$$\phi_5(\textcolor{purple}{V_3})$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.0404</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.1520</td>
  </tr>
</table>
</center>

<h4 id="step-4-normalize">Step 4: Normalize</h4>

Finally, we normalize $$\phi_5(\textcolor{purple}{V_3})$$ to get the probability distribution.

$$
Z = 0.0404 + 0.1520 = 0.1924
$$

$$
\begin{aligned}
P(\textcolor{purple}{V_3} = \textcolor{purple}{s_0} \mid \textcolor{purple}{V_1} = \textcolor{purple}{s_0}) &= \frac{0.0404}{0.1924} = 0.2100 \\
P(\textcolor{purple}{V_3} = \textcolor{purple}{s_1} \mid \textcolor{purple}{V_1} = \textcolor{purple}{s_0}) &= \frac{0.1520}{0.1924} = 0.7900
\end{aligned}
$$

<h2 id="how-llms-do-it">How LLMs do it</h2>

Now that we have solved the problem manually, let's see how LLMs approach the task. To evaluate this comprehensively, I have prepared two complementary experiments:

1. **Raw reasoning**: Provide the network definition with CPDs in the prompt and ask for the answer without any tools. This tests whether LLMs can apply inference algorithms (Variable Elimination, Junction Tree, brute force, etc.) and perform arithmetic operations correctly. It's essentially a test of what I did above but without a calculator (which I used).

2. **Code generation**: Provide the network definition with CPDs in the prompt and ask LLMs to write Python code to solve the problem. Given that current reasoning models have demonstrated excellent coding capabilities, this tests their ability to translate the problem into code and solve it. This is a "one-shot" test. I want to see what kind of code they would generate and how many output tokens are required compared to the raw reasoning approach.

<h3 id="experimental-setup">Experimental setup</h3>

I have selected seven state-of-the-art language models, including both open-source and closed-source reasoning models. The experiments have been conducted using [OpenRouter](https://openrouter.ai/).

**Models evaluated:** 


<table>
<thead>
<tr>
<th>Model</th>
<th>Context Length</th>
<th>Max Output Tokens</th>
<th>Cost Input ($/1M tokens)</th>
<th>Cost Output ($/1M tokens)</th>
</tr>
</thead>
<tbody>
<tr>
<td colspan="5" style="background-color: #f0f0f0; font-weight: bold;">Open-source</td>
</tr>
<tr>
<td>DeepSeek-R1-0528</td>
<td>163,840</td>
<td>163,800</td>
<td>0.40</td>
<td>1.75</td>
</tr>
<tr>
<td>Kimi-K2-thinking</td>
<td>262,144</td>
<td>262,000</td>
<td>0.40</td>
<td>1.75</td>
</tr>
<tr>
<td>Qwen3-235B-A22B-thinking-2507</td>
<td>262,144</td>
<td>262,000</td>
<td>0.30</td>
<td>1.20</td>
</tr>
<tr>
<td>GLM-4.7</td>
<td>202,752</td>
<td>131,800</td>
<td>0.40</td>
<td>1.50</td>
</tr>
<tr>
<td colspan="5" style="background-color: #f0f0f0; font-weight: bold;">Closed-source</td>
</tr>
<tr>
<td>Claude Sonnet-4.5</td>
<td>1,000,000</td>
<td>64,000</td>
<td>3.00</td>
<td>15.00</td>
</tr>
<tr>
<td>Gemini-3-Pro</td>
<td>1,048,576</td>
<td>65,500</td>
<td>2.00</td>
<td>12.00</td>
</tr>
<tr>
<td>GPT-5.2-high</td>
<td>400,000</td>
<td>128,000</td>
<td>1.75</td>
<td>14.00</td>
</tr>
</tbody>
</table>

The complete experimental code is available in the [`code/llms-probabilistic-reasoning/`](https://github.com/ferjorosa/ferjorosa.github.io/tree/main/code/llms-probabilistic-reasoning) directory. Running the experiments requires only a few OpenRouter credits, and I've shared all results as JSON files for analysis under the [`results`](https://github.com/ferjorosa/ferjorosa.github.io/tree/main/code/llms-probabilistic-reasoning/results) sub-directory.

Each experiment uses a different prompt, both defined in the [`prompts.yaml`](https://github.com/ferjorosa/ferjorosa.github.io/tree/main/code/llms-probabilistic-reasoning/prompts.yaml) file. The raw reasoning template is <code>prompt_base</code> and the code generation template is <code>prompt_base_code</code>.

<h3 id="raw-reasoning-results">Raw reasoning results</h3>

<table>
<thead>
<tr>
<th>Model</th>
<th>Response</th>
<th>Input tokens</th>
<th>Completion tokens</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ground truth</td>
<td>0.7900</td>
<td>1018 <sup>(1)</sup></td>
<td>3275 <sup>(1)</sup></td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold;">Open-source</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/deepseek_deepseek-r1-0528_20251226_164351.md">DeepSeek-R1-0528</a></td>
<td>0.789967</td>
<td>1031</td>
<td>14786</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/moonshotai_kimi-k2-thinking_20251213_171713.md">Kimi-K2-thinking</a></td>
<td>0.78996796</td>
<td>987</td>
<td>39224</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/qwen_qwen3-235b-a22b-thinking-2507_20251226_172229.md">Qwen3-235B-A22B-thinking-2507</a></td>
<td>0.7900</td>
<td>1079</td>
<td>7623</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/z-ai_glm-4.7_20251226_170612.md">GLM-4.7</a></td>
<td>0.78997</td>
<td>1044</td>
<td>12432</td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold;">Closed-source</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/anthropic_claude-sonnet-4.5_20251226_173811.md">Claude Sonnet-4.5</a></td>
<td>0.7899686793</td>
<td>1188</td>
<td>18721</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/google_gemini-3-pro-preview_20251226_175749.md">Gemini-3-Pro</a></td>
<td>0.7900</td>
<td>1155</td>
<td>7576</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_md/openai_gpt-5.2_20251226_180834.md">GPT-5.2-high</a></td>
<td>0.789967957981</td>
<td>1029</td>
<td>10004</td>
</tr>
</tbody>
<tfoot>
<tr>
<td colspan="4" style="font-size: 0.9em; font-style: italic; padding-top: 10px;">
<sup>(1)</sup> <a href="https://platform.openai.com/tokenizer">Ground truth token values were approximated using OpenAI's GPT-4o tokenizer.</a>
</td>
</tr>
</tfoot>
</table>

All models successfully computed the correct probability. However, to be honest, that was not especially surprising. Reasoning models have shown great performance [on math benchmarks](https://livebench.ai/#/?Mathematics=as&sort=Mathematics+Average) in recent years, and the example query is not especially complicated given the size of the network. What is particularly interesting to me is **how each model approached the task**. 

To analyze their approaches, I reviewed the traces and used Gemini-3-Pro to compare them against the VE algorithm I manually applied above. Note that for Gemini-3 and GPT-5.2 we only have access to reasoning "summaries" rather than the full thinking trace, so the analysis of these models is not as accurate.

As a summary, **none of the models used the VE algorithm.** Instead, all models except GPT-5.2 essentially wrote out the formula for the full joint distribution and then summed it up. 

DeepSeek-R1, Kimi-K2, Sonnet-4.5, and Gemini-3 wrote the full joint distribution using the chain rule and brute-forced the summation. This forced them to re-calculate the same sub-problems multiple times (e.g., computing the probability of the parents for both the numerator and denominator separately). This redundancy is a major driver of token bloat.

GLM-4.7 and Qwen-3 also summed over the full joint distribution, but they realized that the numerator and denominator shared common terms, like $$P(\textcolor{purple}{V_0})P(\textcolor{purple}{V_1} \mid \textcolor{purple}{V_0})$$, so they explicitly calculated these "blocks" once and reused them, naming them for example `term1` and `term2`. However, while they avoid re-multiplying the same numbers, they are still committed to a formula that grows **exponentially with the network size**.

Finally, GPT-5.2 is the only one that truly changed the structure of the problem. It seems to me that it has applied <a href="https://www.doc.ic.ac.uk/~dfg/ProbabilisticInference/IDAPILecture09.pdf"><b>Cutset conditioning</b></a>. The idea is to find the minimal set of nodes whose instantiation will make the remainder of the network "singly connected" (i.e., a polytree). Once we have a tree, inference is easy and efficient. In this case, GPT-5.2 correctly identified that $$\textcolor{purple}{V_0}$$ acts as a cutset (of size 1). Instantiating $$V_0$$ breaks the connection between the "left" path ($$\textcolor{purple}{V_1}$$) and "right" path ($$\textcolor{purple}{V_2}$$). After it solved a small problem (finding $$\textcolor{purple}{V_0}$$'s posterior), it then used that answer to solve the next small problem (finding $$\textcolor{purple}{V_3}$$). To be honest, I was impressed by this. This is what I was hoping to see: **LLMs using their reasoning capabilities to find "heuristics" to simplify the inference problem**. 
<br>

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<b>The "arithmetic anxiety" phenomenon</b>
<br><br>
It seems the choice of strategy had a direct impact on the model's "arithmetic confidence". Basically, some of the models, usually those that approached the problem from a "brute-force" perspective, suffered from severe verification loops. 
<br><br>
For instance, DeepSeek-R1 recalculated simple products dozens of times using different formats (decimals, fractions, scientific notation) to "be sure". Sonnet-4.5 constantly interrupted itself to double-check divisions, catching and correcting its own precision errors. Kimi-K2 was the most extreme case, performing manual long division to <b>over 100 decimal places</b> for a problem that only needed 4. Finally, Gemini-3 seems to have done some verification steps, but given the lack of full reasoning trace, we cannot be sure. It is probably not very anxious given the amount of tokens it generated.
<br><br>
<b>Note:</b> In the prompt I instruct to "Use at least 4 decimal places for precision", so I am sure that also influenced, but it seems more prominent in those that had to do more arithmetic operations.
</div>
<div style="height: 1.1em;"></div>

<h3 id="code-generation-results">Code generation results</h3>

<table>
<thead>
<tr>
<th>Model</th>
<th>Response</th>
<th>Input tokens</th>
<th>Completion tokens</th>
</tr>
</thead>
<tbody>
<tr>
<td>Ground truth</td>
<td>0.7900</td>
<td>1039 <sup>(1)</sup></td>
<td>636 <sup>(1)</sup></td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold;">Open-source</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/deepseek_deepseek-r1-0528_20251227_193907.md">DeepSeek-R1-0528</a></td>
<td>0.789968</td>
<td>1048</td>
<td>2793</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/moonshotai_kimi-k2-thinking_20251227_194650.md">Kimi-K2-thinking</a></td>
<td>0.789967957981</td>
<td>963</td>
<td>27339</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/qwen_qwen3-235b-a22b-thinking-2507_20251227_200602.md">Qwen3-235B-A22B-thinking-2507</a></td>
<td>0.7900</td>
<td>1097</td>
<td>13353</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/z-ai_glm-4.7_20251227_195156.md">GLM-4.7</a></td>
<td>0.7899679579812788</td>
<td>1064</td>
<td>5663</td>
</tr>
<tr>
<td colspan="4" style="background-color: #f0f0f0; font-weight: bold;">Closed-source</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/anthropic_claude-sonnet-4.5_20251227_193625.md">Claude Sonnet-4.5</a></td>
<td>0.7899679579812788</td>
<td>1205</td>
<td>19864</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/google_gemini-3-pro-preview_20251227_163622.md">Gemini-3-Pro</a></td>
<td>0.7899679579812788</td>
<td>1167</td>
<td>5885</td>
</tr>
<tr>
<td><a href="https://github.com/ferjorosa/ferjorosa.github.io/blob/main/code/llms-probabilistic-reasoning/results_code_md/openai_gpt-5.2_20251227_193226.md">GPT-5.2-high</a></td>
<td>0.7899679580</td>
<td>1049</td>
<td>11799</td>
</tr>
</tbody>
<tfoot>
<tr>
<td colspan="4" style="font-size: 0.9em; font-style: italic; padding-top: 10px;">
<sup>(1)</sup> <a href="https://platform.openai.com/tokenizer">Ground truth token values were approximated using OpenAI's GPT-4o tokenizer.</a>
</td>
</tr>
</tfoot>
</table>

All models achieved the correct numerical answer. However, despite the prompt explicitly mentioning the possibility to write code for `pgmpy` and `pyAgrum`, **none of the models used these established BN libraries**. Instead, they all followed the same pattern: they derived the **chain rule** formula and implemented it using vanilla Python.

Looking at the traces, most models actually computed the answer (or at least verified their approach) manually before writing any code. Kimi-K2 and GPT-5.2 were the most extreme examples. They performed the full calculation by hand, including manual long division to many decimal places. Their code then used high-precision arithmetic (`fractions.Fraction` for Kimi-K2, `decimal.Decimal` with 50-digit precision for GPT-5.2), essentially double-checking their mental work rather than delegating the computation. On the other side of the spectrum, DeepSeek-R1 also computed the numerator and denominator but not the final result, which is why it was far more token efficient.

From my personal tests, I know these models are aware of `pgmpy` and `pyAgrum` and can write code using them. However, they seem to prefer direct calculations. Perhaps they find them more explainable or maybe they didn't see it necessary for a small network like this one.

As an example, here is the resulting Python code from Sonnet-4.5 (all of them are quite similar):

```python
# Calculate P(V3=s1 | V1=s0)

# P(V0)
P_V0_s0 = 0.5072
P_V0_s1 = 0.4928

# P(V1 | V0)
P_V1_s0_given_V0_s0 = 0.3110
P_V1_s0_given_V0_s1 = 0.0704

# P(V3 | V0, V1)
P_V3_s1_given_V0_s0_V1_s0 = 0.9393
P_V3_s1_given_V0_s1_V1_s0 = 0.1110

# Calculate P(V3=s1, V1=s0) using law of total probability
P_V3_s1_V1_s0 = (P_V3_s1_given_V0_s0_V1_s0 * P_V1_s0_given_V0_s0 * P_V0_s0 + 
                 P_V3_s1_given_V0_s1_V1_s0 * P_V1_s0_given_V0_s1 * P_V0_s1)

# Calculate P(V1=s0)
P_V1_s0 = P_V1_s0_given_V0_s0 * P_V0_s0 + P_V1_s0_given_V0_s1 * P_V0_s1

# Calculate P(V3=s1 | V1=s0)
result = P_V3_s1_V1_s0 / P_V1_s0

print(result)
```

For comparison's sake, here's how the problem could be solved using `pgmpy`. This is what I have considered ground truth for this experiment:

```python
from pgmpy.inference import VariableElimination
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD

# Create the Bayesian network structure
bn = DiscreteBayesianNetwork([('V0', 'V1'), ('V0', 'V2'), ('V0', 'V3'), ('V1', 'V3')])

# Define CPDs based on the provided tables

# CPD for V0 (root node)
cpd_v0 = TabularCPD(
    variable='V0',
    variable_card=2,
    values=[[0.5072], [0.4928]],
    state_names={'V0': ['s0', 's1']}
)

# CPD for V1 (depends on V0)
cpd_v1 = TabularCPD(
    variable='V1',
    variable_card=2,
    values=[[0.3110, 0.0704],
            [0.6890, 0.9296]],
    evidence=['V0'],
    evidence_card=[2],
    state_names={'V1': ['s0', 's1'], 'V0': ['s0', 's1']}
)

# CPD for V2 (depends on V0)
cpd_v2 = TabularCPD(
    variable='V2',
    variable_card=2,
    values=[[0.8950, 0.0562],
            [0.1050, 0.9438]],
    evidence=['V0'],
    evidence_card=[2],
    state_names={'V2': ['s0', 's1'], 'V0': ['s0', 's1']}
)

# CPD for V3 (depends on V0 and V1)
cpd_v3 = TabularCPD(
    variable='V3',
    variable_card=2,
    values=[[0.0607, 0.8173, 0.8890, 0.2251],
            [0.9393, 0.1827, 0.1110, 0.7749]],
    evidence=['V0', 'V1'],
    evidence_card=[2, 2],
    state_names={'V3': ['s0', 's1'], 'V0': ['s0', 's1'], 'V1': ['s0', 's1']}
)

# Add CPDs to the bn
bn.add_cpds(cpd_v0, cpd_v1, cpd_v2, cpd_v3)

# Validate the bn
assert bn.check_model()

# Create inference object
inference = VariableElimination(bn)

# Compute P(V3=s1 | V1=s0)
query_result = inference.query(variables=['V3'], evidence={'V1': 's0'})
prob_v3_s1_given_v1_s0 = query_result.values[1]  # Index 1 corresponds to V3=s1

print(prob_v3_s1_given_v1_s0)
```

Writing code using the chain rule for a small network is not "bad" per se, but it may suggest that these models are not accustomed to using BN libraries. This could be an issue for more complex queries, where translating the problem manually becomes error-prone or even infeasible.

A more significant observation is that all models manually solved the problem before writing the code. This redundancy, combined with the verbose chain rule approach, generates a substantial number of tokens. Since reasoning LLMs have limited context windows and generation speeds (often 50-100 tokens/s), reducing this manual verification would make the process far more efficient.

Now, I don't want to be all "doom and gloom". First, this is based on a single example, and **more experiments are needed**. Second, I think these results are very interesting and hint at notable opportunities for optimization (e.g., **training LLMs to use these BN libraries more often**), especially as we move from pure LLMs to agents with iterative reasoning processes and tools.

<h2 id="conclusion">Conclusion</h2>

The key takeaway from this exploration is that **LLMs can solve probabilistic inference problems, but they do so inefficiently**. Rather than applying BN algorithms like VE, they seem to prefer to write the chain rule formula and brute-force the arithmetic. This works for small networks but does not scale.

**Limitations.** This was a small-scale exploration with a single query on a 4-node network. A systematic evaluation would require varying network sizes, query complexities, and prompting strategies. I also did not test function calling, which would enable a more agentic approach.

**Related work.** While I have not found many papers on the topic, two recent papers are relevant: <a href="https://arxiv.org/abs/2406.12830">Paruchuri et al. (2024)</a> evaluated LLMs on probabilistic reasoning over univariate distributions. <a href="https://arxiv.org/abs/2402.09614">Nafar et al. (2025)</a> is closer to my experiments, testing how LLMs translate text-based probabilistic queries into symbolic representations.

**Looking ahead.** More experiments are needed: testing different network structures, varying sizes, and exploring alternative prompting strategies. I would also like to evaluate tool-augmented approaches via function calling, which could reveal whether LLMs perform better when they can delegate computation rather than doing it "in their heads."

More broadly, understanding how LLMs reason "under the hood" about structured mathematical problems like probabilistic inference is valuable in itself. It helps us identify where current architectures struggle and what kinds of reasoning they handle well. This connects to a fascinating discussion on the <a href="https://www.youtube.com/@MachineLearningStreetTalk">Machine Learning Street Talk</a> channel that I watched the other day, where researchers explore why LLMs still fail at arithmetic that a second-grader could do, and whether mathematical frameworks like Category Theory could help us understand these limitations more rigorously. It is a bit dense, but I recommend watching it if you are interested in the topic.

<center>
<iframe width="560" height="315" src="https://www.youtube.com/embed/AWqvBdqCAAE" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>
</center>

<h2 id="references">References</h2>

1. Rodriguez, F. (2025, July 4). <a href="https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html"><u>Introduction to decision theory: Part II</u></a>.
<br><br>
2. Rodriguez, F. (2025, August 7). <a href="https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html"><u>Introduction to decision theory: Part III</u></a>.
<br><br>
4. Koller, D., & Friedman, N. (2009). <a href="http://mcb111.org/w06/KollerFriedman.pdf"><u>Probabilistic Graphical Models: Principles and Techniques</u></a>. MIT Press.
<br><br>
5. Cutset conditioning lecture notes from Imperial College London. <a href="https://www.doc.ic.ac.uk/~dfg/ProbabilisticInference/IDAPILecture09.pdf"><u>PDF link</u></a>.
<br><br>
6. Nafar, A., Venable, K. B., & Kordjamshidi, P. (2025). <a href="https://arxiv.org/abs/2402.09614"><u>Reasoning over uncertain text by generative large language models</u></a>. In Proceedings of the AAAI Conference on Artificial Intelligence (Vol. 39, No. 23, pp. 24911-24920).
<br><br>
7. Paruchuri, A., Garrison, J., Liao, S., et al. (2024). <a href="https://arxiv.org/abs/2406.12830"><u>What are the odds? Language models are capable of probabilistic reasoning</u></a>. In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing (pp. 11712-11733).
<br><br>
8. pgmpy documentation: <a href="https://pgmpy.org/"><u>https://pgmpy.org/</u></a>.

---
layout: post
title: "How Capable Are Language Models At Probabilistic Reasoning?"
date: 2025-12-13
categories: blog
description: "Evaluating LLMs on probabilistic reasoning: from univariate distributions to Bayesian networks."
tags: [Probabilistic Reasoning, LLMs, Bayesian Networks, Decision Theory]
math: true
---

<h2 id="introduction">Can large language models think "rationally"?</h2>

This question has been on my mind for a while. It motivated me to revise probabilistic graphical models and write my [blog series on Decision Theory](https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html) this past summer. In the [final post of that series](https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html), I outlined a vision of combining large language models (LLMs) with influence diagrams to solve complex decision problems.

The truth is, I had already started exploring that idea even before writing the first blog post. Back in May 2025, I put together a [notebook](https://github.com/ferjorosa/decision-theory-llms/blob/main/notebooks/how_good_are_llms_decision_problems.ipynb) testing how well LLMs could solve decision problems. The results were promising—models like O3 and Gemini 2.5 Pro reached correct solutions on small problems. But there was a catch: they were solving them using **decision trees**.

As I explained in [Part II](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html), decision trees have theoretical limitations. They scale poorly and hide the causal structure of the problem. If we want LLMs to tackle real-world ambiguity, they need to "think" in terms of **Influence Diagrams** (or Bayesian Networks). But crafting these problems requires a solid grasp of probability.

This made me realize I might be skipping a step. Since influence diagrams are essentially Bayesian networks augmented with decisions and utilities, I first need to answer a more fundamental question: **How well do LLMs handle basic probabilistic inference?**

If they struggle with calculating probabilities on a static Bayesian network, expecting them to solve dynamic decision problems is premature. This post documents my investigation into that question, starting from simple distributions and moving to the "curse of dimensionality" in multivariate systems.

<h2 id="recap">What is Probabilistic Inference?</h2>

At its core, probabilistic inference is about answering questions under uncertainty. Given a model of the world and some observed evidence (what we know), we want to compute the probability of a query variable (what we don't know).

Mathematically, if we have a set of random variables $\mathbf{X}$ and we observe that some of them take specific values ($\mathbf{E} = \mathbf{e}$), we want to compute:

$$ P(Q \mid \mathbf{E} = \mathbf{e}) = \frac{P(Q, \mathbf{e})}{P(\mathbf{e})} $$

This looks simple, but the complexity depends entirely on how the probability distribution $P(\mathbf{X})$ is represented.

<h2 id="level-1">Level 1: Univariate Distributions</h2>

Let's start with the simplest scenario: a single random variable. Imagine we're modeling the height of adults. We might represent this with a Gaussian (normal) distribution, $X \sim \mathcal{N}(\mu, \sigma)$.

Inference here is straightforward. If I ask, *"What is the probability that a randomly selected person is taller than 180cm?"*, the task is to integrate the Probability Density Function (PDF) from 180 to infinity. In practice, humans (and computers) solve this by calculating a Z-score and looking up the value in a standard normal table or using an error function:

$$ Z = \frac{x - \mu}{\sigma} $$

### Research on LLMs and Univariate Distributions

Recently, a team from Google published an interesting paper titled ["What Are the Odds? Language Models Are Capable of Probabilistic Reasoning"](https://arxiv.org/pdf/2406.12830). They systematically evaluated how well LLMs can estimate percentiles, draw samples, and calculate probabilities for various 1D distributions (Normal, Log-Normal, Bernoulli, etc.).

Their findings were nuanced. LLMs don't "integrate" functions in the mathematical sense. Instead, they seem to rely on:
1.  **Pattern Matching**: Recognizing standard questions (e.g., "probability of heads in a fair coin flip").
2.  **Anchoring**: Using memorized heuristics (like the 68-95-99.7 rule for normal distributions) to interpolate answers.

The paper shows that while models struggle with raw numerical reasoning, providing **context** (e.g., "this data represents human heights") or **anchors** (examples from the distribution) significantly improves performance. However, for a Gaussian distribution, getting the *exact* number requires precise arithmetic and knowledge of the CDF—two things LLMs are notoriously shaky at without tools.

<h2 id="level-2">Level 2: The Multivariate Cliff</h2>

Real-world problems rarely involve just one variable. We don't just care about height; we care about height, weight, diet, exercise, and heart disease risk simultaneously.

If we have two variables, say Height ($H$) and Weight ($W$), we can model them with a Bivariate Gaussian. Visually, this looks like a 3D mountain.

<center>
<!-- Placeholder for Bivariate Gaussian Plot -->
[TODO: Insert Bivariate Plot]
</center>

But what happens when we move to discrete variables? Suppose we have $N$ binary variables (True/False). To fully specify the joint distribution $P(X_1, \ldots, X_n)$, we would need a table with $2^N$ entries.

*   With 3 variables: $2^3 = 8$ parameters. Easy.
*   With 20 variables: $2^{20} \approx 1,000,000$ parameters.
*   With 50 variables: $2^{50} \approx 10^{15}$ parameters.

This is the **curse of dimensionality**. We cannot even store the probability table, let alone perform inference on it by summing rows. This effectively kills the "naive" approach.

### Enter Bayesian Networks

This is where **Bayesian Networks (BNs)** come in. They allow us to represent the joint distribution compactly by exploiting **conditional independence**. Instead of one giant table, we factor the distribution into smaller pieces:

$$ P(X_1, \ldots, X_n) = \prod_{i=1}^{n} P(X_i \mid \text{Parents}(X_i)) $$

If a variable only has a few parents, the tables remain small, and the representation becomes tractable. But here's the catch: **inference** on a Bayesian Network isn't just a formula lookup anymore. It requires an **algorithm**.

In the next section, I want to explore whether LLMs can execute one of these algorithms—**Variable Elimination**—step by step.

<h2 id="variable-elimination">The Challenge: Variable Elimination</h2>

To test if LLMs can handle this, I set up a synthetic Bayesian Network with 4 binary nodes ($V0, V1, V2, V3$). The structure is a simple diamond-like shape:

*   **V0** is the root.
*   **V1** and **V2** depend on $V0$.
*   **V3** depends on $V0$ and $V1$.

<center>
<pre class="mermaid">
graph TD
    V0 --> V1
    V0 --> V2
    V0 --> V3
    V1 --> V3
</pre>
</center>

The task is to compute the conditional probability $P(V3=s1 \mid V1=s0)$.

### The Logical Test
There is a "trap" in this query. Notice that **V2** is a child of $V0$ but has no connection to $V3$ or $V1$. In probabilistic terms, $V2$ is a **barren node** for this query. It provides no information about $V0$ (since we are summing over $V0$) and doesn't influence $V3$.

A smart human (or algorithm) would immediately delete $V2$ from the graph before starting any calculation. If the LLM tries to sum over $V2$, it's doing unnecessary work.

### The Numerical Test
The exact calculation requires summing over the hidden variable $V0$:

$$ P(V3 \mid V1) = \alpha \sum_{V0} P(V0) \cdot P(V1 \mid V0) \cdot P(V3 \mid V0, V1) $$

This involves multiplying probabilities (e.g., $0.5072 \times 0.3110$) and summing the results. It's not advanced calculus, but it requires high-precision arithmetic.

<h2 id="experiment">The Experiment: "Raw" Reasoning vs. Calculators</h2>

I prompted a reasoning model, **Moonshot AI's Kimi k1.5**, with the CPT definitions and the query. I explicitly removed access to code execution tools to see how it would handle the problem "mentally."

The result was fascinating—and slightly terrifying.

### 1. Logical Reasoning: Pass
The model correctly identified the barren node structure immediately:

> "The network is V0 -> V1, V0 -> V2, ... So V2 is not a parent of V3... Since V2 is a child of V0 and not connected to V3, conditional independence holds... So we can ignore V2 for this query."

It successfully navigated the graph structure and simplified the equation.

### 2. Numerical Reasoning: Brute Force
Then came the math. Instead of hallucinating a number (as GPT-3 might have done) or giving up, the model proceeded to implement **long division manually** in the chat window.

It generated a **39,224 token response** (costing ~$0.10). It didn't just multiply the numbers; it wrote out the digit-by-digit operations for high-precision division, iterating through dozens of decimal places to ensure accuracy.

> "Digit 92: remainder*10 = 5,392,540,000. q92 = floor(4.483... ) = 4... Remainder = 581,732,000."

It literally acted as a biological CPU, simulating a floating-point unit token by token.

### The Verdict
The final answer derived by the model was `0.78996796`.
The ground truth calculated by `pgmpy` is `0.789968`.

The model was correct to 6 decimal places. But it took ~40,000 tokens of compute to do what a Python script does in microseconds. This highlights a critical lesson for building AI decision systems: **LLMs are excellent at formulating the problem (reasoning), but we should never ask them to solve it (computation) directly.**

<h2 id="level-3">Level 3: The "Neuro-Symbolic" Solution</h2>

The experiment above proves that LLMs *can* do probabilistic inference "in their heads" (or rather, in their context windows), but it's the wrong way to use them. The optimal approach is **neuro-symbolic**:

1.  **The "Neuro" part (LLM)**: Handles the qualitative reasoning. It reads the messy real-world description ("The ground is wet"), translates it into a structured Bayesian Network (Nodes, Edges, CPTs), and decides *what* to calculate.
2.  **The "Symbolic" part (Solver)**: Handles the quantitative reasoning. It takes the structured query and runs an exact algorithm (like Variable Elimination) using a library like `pgmpy`.

If I had given the model access to a Python interpreter, it likely would have written a 10-line script to define the CPTs and run the query, returning the answer in seconds with zero arithmetic errors.

<h2 id="future-work">The Frontier: Measuring the Limits</h2>

This investigation is just the start. I am currently collaborating with colleagues to build a comprehensive benchmark for probabilistic reasoning in LLMs. We are designing a dataset that goes beyond simple textbook examples, inspired by recent work like [Generalized Probabilistic Reasoning](https://arxiv.org/abs/2402.09614).

Our goal is to test:
1.  **Modeling**: Can LLMs correctly structure a messy word problem into a valid Bayesian Network?
2.  **Heuristics**: Can they find efficient **elimination orders** for Variable Elimination? (This is a graph theory problem, not an arithmetic one).
3.  **Approximate Inference**: When the network is too massive for exact inference (e.g., medical diagnosis with hundreds of variables), can LLMs propose reasonable **sampling strategies** (like MCMC) or provide good heuristic estimates?

<h2 id="conclusion">Conclusion</h2>

Large Language Models are not naturally "rational" in the Bayesian sense—they don't maintain a consistent internal probability distribution. However, they are remarkably capable of **simulating** rational reasoning processes.

They can understand conditional independence, identify irrelevant variables, and even execute complex algorithms step-by-step. The bottleneck is simple arithmetic. By pairing their reasoning capabilities with symbolic solvers, we might finally be able to build the decision-making agents I envisioned at the start of this journey.

Stay tuned for the results of our larger benchmark!

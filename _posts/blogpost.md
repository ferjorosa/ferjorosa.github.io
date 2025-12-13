---
layout: post
title: "Are Language Models Capable of Probabilistic Reasoning?"
date: 2025-08-07
categories: blog
description: "TODO"
tags: [Probabilistic Reasoning]
---

<h2 id="the-challenge-of-decision-making">Can large language models think "rationally"?</h2>

This question has been on my mind for a while. It has motivated me to revise probabilistic graphical models and write my blog series on Decision Theory during summer. [In my last post of that series](https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html), I outlined a vision of combining large language models (LLMs) with influence diagrams.

The truth is, I had already started exploring that idea even before writing the first blog post. Back in May 2025, I put together a [notebook](https://github.com/ferjorosa/decision-theory-llms/blob/main/notebooks/how_good_are_llms_decision_problems.ipynb) testing how well LLMs could solve decision problems. The results were interesting. LLMs like O3 and Gemini 2.5 Pro reached correct solutions on the three small problems I tested. But there was a catch: they were solving them using decision trees, which [as I later ended up explaining](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html) have theoretical limitations. Now, these limitations combined with LLMs' constrained output token budgets made me intuit a sort of "reasoning ceiling" unless they used a different approach (like influence diagrams).

So I set out to run more extensive experiments and for that I needed a dataset of synthetic decision problems. And that's where I hit a wall: crafting meaningful decision scenarios, ones with realistic utilities, plausible probabilities, and coherent narratives, is still an inherently human process. There is probably a way of doing this, but I was finding it a bit of a "hybrid" process, with me thinking of problems, defining influence diagrams manually and then doing back-and-forth iterations with LLMs to define a good story around it.

This made me think I may be "skipping a step". Since influence diagrams are essentially Bayesian networks augmented with decisions and utilities, I should first understand how LLMs handle basic probabilistic inference. If they struggle with probability calculations on Bayesian networks, expecting them to solve complex decision problems could be premature.

This post documents that investigation. I'll start with a brief primer on probabilistic inference, then examine recent research on univariate distributions (including a Google paper that caught my attention), and finally share what I've been working on: extending that evaluation to multivariate distributions using Bayesian networks—building on my PhD work in this area.

## Brief recap on probabilistic inference

<!-- Aqui podemos empezar comentando sobre el caso mas simple como es una Gaussiana univariante y luego damos pie a las distribuciones multivariantes y de ahi damos pie a las redes bayesianas, las cuales tienen sentido especialmente en el caso discreto ya que representar una distribucion multivariante categorica en forma de tabla nos llevaria a una explosion combinatoria rapidamente (similar a lo que ocurre con arboles de decision)
-->

## Brief recap on probabilistic inference

Probabilistic inference is, at its core, about using probability theory to answering questions under uncertainty. Given what we know (or observe), what can we conclude about what we don't know?

### The univariate case

Let's start with the simplest scenario: a single random variable. Imagine we're modeling the height of adults in a population. We might represent this with a Gaussian (normal) distribution:

$$X \sim \mathcal{N}(\mu = 170, \sigma = 10)$$

Probabilistic inference here means answering questions like: *What's the probability that a randomly selected person is taller than 180cm?* With a univariate distribution, this is straightforward—we integrate (or look up) the relevant area under the curve.

The same logic applies to discrete distributions. If we model a coin flip as a Bernoulli distribution with \\(P(\text{heads}) = 0.6\\), inference is trivial: we just read off the probability.

### The multivariate challenge

Real-world problems rarely involve just one variable. Consider a medical diagnosis scenario with three binary symptoms and one disease. To fully specify this joint distribution, we'd need a table with \\(2^4 = 16\\) entries. Manageable, right?

Now scale up. With 20 binary variables, we need \\(2^{20} \approx 1\\) million entries. With 50 variables, we're looking at \\(2^{50} \approx 10^{15}\\) entries—more than we could ever store or estimate from data.

This is the **curse of dimensionality** for probability distributions, and it mirrors the exact problem I discussed with decision trees in my [earlier post](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html): naive enumeration simply doesn't scale.

### Bayesian networks: structured representations

Bayesian networks offer an elegant solution. Instead of storing the full joint distribution, they exploit **conditional independence** to factor it into smaller, manageable pieces.

A Bayesian network represents the joint distribution as:

$$P(X_1, X_2, \ldots, X_n) = \prod_{i=1}^{n} P(X_i \mid \text{Parents}(X_i))$$

Each variable only depends on its parents in the graph, not on all other variables. This dramatically reduces the number of parameters we need to specify.

For example, in a network where each variable has at most 2 parents, we go from \\(2^n\\) parameters to roughly \\(n \cdot 2^3\\)—a massive reduction that makes inference tractable.

This is why Bayesian networks became my natural starting point for evaluating LLMs on probabilistic reasoning: they're the standard tool for representing and reasoning about multivariate distributions in a structured way.


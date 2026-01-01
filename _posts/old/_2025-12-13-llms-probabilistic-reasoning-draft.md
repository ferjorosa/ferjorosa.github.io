---
layout: post
title: "Can Language Models Reason About Probability? Testing the Limits"
date: 2025-12-13
categories: blog
description: "Investigating whether LLMs can handle probabilistic inference—from simple distributions to complex Bayesian networks"
tags: [Probabilistic Reasoning, LLMs, Bayesian Networks]
---

## The Question That Made Me Step Back

Can large language models reason about uncertainty? This question has been driving my work for months. It motivated me to revisit probabilistic graphical models and write a [blog series on Decision Theory](https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html) over the summer, where I explored combining LLMs with influence diagrams for decision-making under uncertainty.

But somewhere along the way, I realized I might be getting ahead of myself.

Back in May, I built a [notebook](https://github.com/ferjorosa/decision-theory-llms/blob/main/notebooks/how_good_are_llms_decision_problems.ipynb) testing how well models like O3 and Gemini 2.5 Pro could solve decision problems. The results were promising—they reached correct solutions on the small problems I tested. But they were doing it through decision trees, which [as I later explained](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html), have fundamental scalability limitations. Combined with LLMs' finite context windows and token budgets, I sensed a hard ceiling on their reasoning capabilities unless they could leverage more structured approaches like influence diagrams.

I wanted to run more extensive experiments. I needed a dataset of synthetic decision problems. And that's where I hit a wall: creating meaningful decision scenarios—with realistic utilities, plausible probabilities, and coherent narratives—turned out to be surprisingly difficult to automate. Even with LLM assistance, it required substantial human iteration and judgment.

Then it hit me: **I was skipping a fundamental step.**

Influence diagrams are essentially Bayesian networks augmented with decisions and utilities. If LLMs struggle with basic probabilistic inference on Bayesian networks, expecting them to solve complex decision problems is like expecting someone to run before they can walk.

This post documents what I found when I took that step back. I'll examine how LLMs handle probabilistic reasoning, starting from simple univariate distributions, moving through recent research on their capabilities, and finally testing them on the real challenge: inference in multivariate Bayesian networks. Along the way, I'll show you exactly how these models think—their reasoning traces, their successes, and their failures.

## What Is Probabilistic Inference, Really?

At its core, probabilistic inference is about answering questions under uncertainty using probability theory. Given what we observe, what can we conclude about what we don't observe?

This might sound abstract, so let's make it concrete. Suppose you're a doctor. A patient comes in with symptoms, and you need to estimate the probability they have a particular disease. You know:
- How common the disease is in the population
- How likely various symptoms are for people with and without the disease  
- Which symptoms this specific patient exhibits

Probabilistic inference is the mathematical machinery that lets you combine this information to answer: "Given these symptoms, what's the probability this patient has the disease?"

It's fundamental to how we reason about the world. Weather forecasting, spam filtering, medical diagnosis, autonomous driving, financial modeling—they all rely on probabilistic inference. And if we want AI systems that can make good decisions under uncertainty, they need to be able to do this kind of reasoning.

The question is: can they?

## Starting Simple: Univariate Distributions

Let's begin with the simplest case: reasoning about a single random variable.

### The Gaussian Example

Imagine we're modeling the height of adults in a population with a Gaussian (normal) distribution:

$$X \sim \mathcal{N}(\mu = 170\text{cm}, \sigma = 10\text{cm})$$

A basic inference question: *What's the probability that a randomly selected person is taller than 180cm?*

To answer this, we need to compute:

$$P(X > 180) = 1 - \Phi\left(\frac{180 - 170}{10}\right) = 1 - \Phi(1) \approx 0.159$$

where \\(\Phi\\) is the cumulative distribution function of the standard normal distribution.

This requires looking up (or computing) a value from the standard normal table, recognizing we need to standardize the variable, and doing some basic arithmetic. Not trivial, but straightforward.

### The Discrete Case

What about discrete distributions? Consider a biased coin modeled as a Bernoulli distribution:

$$X \sim \text{Bernoulli}(p = 0.6)$$

Here, inference is even simpler: \\(P(X = \text{heads}) = 0.6\\). We just read off the probability.

### Can LLMs Handle This?

These univariate cases involve direct probability calculations—there's a formula, you apply it, you get an answer. It's essentially numerical reasoning combined with knowledge of probability distributions.

Recent research suggests modern LLMs can handle these reasonably well. A particularly relevant study is **["What Are the Odds? Language Models Are Capable of Probabilistic Reasoning"](https://arxiv.org/pdf/2406.12830)** by Jiang et al. (2024) from Google DeepMind.

The authors systematically evaluated LLMs on univariate probabilistic reasoning tasks across different distribution families:

**Key findings:**
- **Top models (Gemini 1.5 Pro, GPT-4) achieved 70-80% accuracy** on questions involving Gaussian distributions, binomial distributions, and other standard families
- **Performance scaled with model size and training** - larger, more capable models showed better probability sense
- **Chain-of-thought prompting significantly improved performance** - when models showed their work, they got better at the numerical computations involved
- **Common failure modes** included calculation errors (arithmetic mistakes) and misunderstanding problem setup

What's particularly interesting is that the *reasoning patterns* LLMs exhibited were often correct—they knew they needed to standardize a Gaussian, they understood how to use the binomial formula—but they would make arithmetic errors in execution.

This tells us something important: **For univariate inference, the bottleneck isn't understanding probability theory, it's accurate numerical computation.**

Modern LLMs have reasonably good "probability sense." They understand distributions conceptually and can often set up the right approach. The question is whether they can execute it precisely.

But here's where it gets interesting: What happens when we move beyond single variables?

## The Multivariate Challenge: When One Variable Isn't Enough

Real-world problems rarely involve just one variable. Let's see what changes when we add even one more variable.

### From Heights to Heights and Weights

Instead of just modeling height, suppose we want to model both height and weight together. These variables are correlated—taller people tend to weigh more. We might use a bivariate Gaussian:

$$
\begin{bmatrix} X_1 \\ X_2 \end{bmatrix} \sim \mathcal{N}\left(
\begin{bmatrix} 170 \\ 70 \end{bmatrix},
\begin{bmatrix} 100 & 60 \\ 60 & 100 \end{bmatrix}
\right)
$$

where \\(X_1\\) is height (cm) and \\(X_2\\) is weight (kg).

Now suppose we want to answer: *Given someone is 180cm tall, what's their expected weight?*

This is a **conditional inference** problem: \\(E[X_2 \mid X_1 = 180]\\).

The formula exists—it involves the covariance matrix, means, and some linear algebra:

$$E[X_2 \mid X_1 = 180] = \mu_2 + \frac{\sigma_{12}}{\sigma_1^2}(180 - \mu_1)$$

But notice the complexity has increased. We're no longer just looking up a value in a table. We need to:
1. Understand conditional probability
2. Extract the right parameters from the covariance matrix  
3. Apply the conditional expectation formula
4. Execute multiple arithmetic operations

And this is just *two* continuous variables with a convenient parametric form.

### The Discrete Explosion

The situation becomes even more dramatic with discrete variables. Consider a simple medical scenario with four binary variables:
- Disease (present/absent)
- Symptom 1 (yes/no)
- Symptom 2 (yes/no)
- Test Result (positive/negative)

To fully specify the joint distribution \\(P(\text{Disease, Symptom}_1, \text{Symptom}_2, \text{Test})\\), we'd need a table with \\(2^4 = 16\\) entries. Manageable.

But scale this up to 20 binary variables—perhaps a more realistic medical model—and we need \\(2^{20} \approx 1\\) million entries. With 50 variables? \\(2^{50} \approx 10^{15}\\) entries—far more than we could ever store or estimate from data.

This is the **curse of dimensionality** for probability distributions, and it mirrors exactly the problem I discussed with decision trees in my [earlier post](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html): naive enumeration doesn't scale.

More critically for our discussion: **there's no simple formula anymore.** You can't just plug numbers into an equation.

### Enter Bayesian Networks

This is why Bayesian networks were invented. Instead of storing the full joint distribution, they exploit **conditional independence** structure to factor it into manageable pieces.

A Bayesian network represents the joint distribution as:

$$P(X_1, \ldots, X_n) = \prod_{i=1}^{n} P(X_i \mid \text{Parents}(X_i))$$

Each variable only depends on its parents in a directed graph, not on all other variables. This dramatically reduces the parameters we need to specify.

For our 20-variable example, instead of ~1 million parameters, if each variable has at most 2 parents, we need roughly \\(20 \times 2^3 = 160\\) parameters. That's a 99.98% reduction.

But here's the catch: **we've traded storage efficiency for computational complexity.**

To answer inference queries on a Bayesian network—questions like "Given these observations, what's the probability of this disease?"—we can't just look up values. We need to run **algorithms**.

## The Algorithmic Leap: Inference Isn't Formula-Based Anymore



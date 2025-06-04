---
layout: post
title: "Introduction to Decision Theory"
date: 2025-06-01
categories: blog
description: "An introduction to decision theory through a practical oil field investment example, covering key concepts like expected monetary value, risk preferences, and decision analysis frameworks."
tags: [Research, Decision Theory, Decision Analysis]
---

> This is the first of a series of posts where we explore **decision theory**:
> 1. **Introduction to Decision Theory**

> **TODO**
> Seguir con el ejemplo con Arboles de decision, luego comentar sus problemas / limitaciones y comentar que existe una alternativa, que son los diagramas de influencia, los cuales los comentaremos en el siguiente post.


## The Challenge of Decision-Making

Imagine you are the CEO of an oil company and you are offered the opportunity to purchase a new oil field. Like any diligent executive, you gather your team to examine satellite images, geological surveys, and consult the team's experience with similar fields in the region.

This research helps form your initial assessment of the field's potential. However, the reality is that until you actually start drilling, there's no way to know for sure how much oil is down there. This leaves you with a classic dilemma:

* Play it safe and walk away.
* Make a calculated bet based on the evidence you've gathered.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/oil_field_image.jpg" alt="Oil field image" width="400">
    </td>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/oil_field_heatmap.jpg" alt="Oil field heatmap" width="400">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Satellite imagery and heatmap of the oil field</i>
    </td>
  </tr>
</table>
</center>

This tension between what you know, what you don't know, and what you truly value is at the heart of every important decision. How do you weigh the potential upside against the risk of a bad draw? How much should your assessment count in the final call? 

<u><a href="https://en.wikipedia.org/wiki/Decision_theory"><strong>Decision theory</strong></a></u> offers a framework to answer exactly these questions. It's about systematically looking at the likelihood of different scenarios and weighing them against how much you value each potential result. By doing this, it guides you toward the action that's most likely to give you the best overall outcome.

Let's return to the oil field example. Suppose you've sized up the field and think it could fall into one of three quality levels:
* **High**, promising oil reserves.
* **Medium**, meaning a decent output but nothing groundbreaking.
* **Low**, where you'd barely break even or could even end up losing money.

The dilemma, then, becomes quite clear. If you decide to buy and the field turns out to be high-quality, you've struck gold. If you buy and it's low-quality, you'll lose your investment. But if you choose not to buy, you avoid any potential loss, though you might also miss out on a good opportunity.

## The Anatomy of a Decision Problem

At its core, any decision problem can be broken down into a few fundamental components: the actions we can take, the uncertain conditions that might influence the outcome (often referred to as states of nature), the probabilities we assign to these conditions based on our best estimates, and the potential outcomes for each action under each condition.

So, let's use the Decision theory framework for our oil field case.

### Structuring the Oil field Decision Problem

First, what are the <span style="color:red; font-weight:bold;">possible actions</span>? The company faces a straightforward choice: either <span style="color:red;">buy the oil field</span>, investing capital now with the hope of future profits, or <span style="color:red;">do not buy</span>, which means avoiding the risk but also potentially missing out on gains.

Next, we consider the <span style="color:purple; font-weight:bold;">states of nature</span> – the things we can't control. In this case, it's the true quality of the oil field. We've simplified this into three possibilities: the field could be <span style="color:purple;">high</span> quality, <span style="color:purple;">medium</span> quality, or <span style="color:purple;">low</span> quality.

Then, we need to assign <span style="color:purple; font-weight:bold;">probabilities</span> to these states. The company doesn't know the field's true quality for sure, but based on all the geological data and expert opinions, they've estimated the chances: a <span style="color:purple;">35%</span> chance of it being high quality, a <span style="color:purple;">45%</span> chance for medium quality, and a <span style="color:purple;">20%</span> chance for low quality.

Finally, let's look at the <span style="color:blue; font-weight:bold;">outcomes</span>, specifically the financial implications (in millions of dollars) for each scenario. These are summarized in the table below:

<center>
<table align="center">
  <tr>
    <th style="color:red;">Action</th>
    <th style="color:purple;">Field Quality</th>
    <th style="color:blue;">Outcome ($M)</th>
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">High</td>
    <td style="color:blue;">+$1,250M</td>
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">Medium</td>
    <td style="color:blue;">+$630M</td>
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">Low</td>
    <td style="color:blue;">+$0M</td>
  </tr>
  <tr>
    <td style="color:red;">Do not buy</td>
    <td style="color:purple;">Any</td>
    <td style="color:blue;">+$350M</td>
  </tr>
</table>
</center>

> ***Why is there a profit for not buying?***
>
> This could represent a baseline alternative, like investing the capital elsewhere for a guaranteed return of $350M.

### Calculating Expected Monetary Value

So, how do we weigh these possibilities financially? A common approach is to calculate the Expected Monetary Value (EMV). For the 'Buy' option, the EMV considers each potential outcome, its likelihood, and its financial value. Here's how it breaks down:

$$
\begin{align*}
EMV(\text{Buy}) &= (0.35 \times \$1,250\text{M}) + (0.45 \times \$630\text{M}) + (0.20 \times \$0\text{M}) \\
&= \$437.5\text{M} + \$283.5\text{M} + \$0\text{M} \\
&= \$721\text{M}
\end{align*}
$$

This gives us an EMV of $721 million if we decide to buy. Now, let's look at the 'Do not buy' option. Its EMV is simpler:

$$ EMV(\text{Do not buy}) = \$350\text{M} $$

Purely from an EMV perspective, buying the field seems to be the stronger choice, offering an expected $721 million versus $350 million.

### Beyond Money: Utility and Risk Preferences

But EMV doesn't always tell the full story. What if not making any profit from this project could be catastrophic for our company, or conversely, where a large payout isn't absolutely essential. EMV values each dollar equally, but real-world decisions often hinge on our risk tolerance.

That's where <a href="https://plato.stanford.edu/entries/rationality-normative-utility/"><u><b>Utility theory</b></u></a> comes in handy. Instead of just using dollar amounts, we assign a "utility score" to each outcome, reflecting how much it's *truly* worth to us. Then we calculate an Expected Utility (EU) by weighing these scores by their probabilities, similar to EMV.

For this article, we'll keep things straightforward and assume EMV and EU point to the same decision. In reality, though, considering utility can completely change which option looks best.

## Decision Analysis: A Dynamic, Iterative Process

Decision-making isn't a one-shot task—it's a cycle of refinement. As new information emerges or priorities shift, we revisit and update our analysis. Here's the structured flow:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/decision_analysis.png" alt="Decision analysis process" width="200">
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 2.</b> Flow diagram of the decision analysis process</i>
    </td>
  </tr>
</table>
</center>

1. **Define Objectives**: Break down the global objective (e.g., "Maximize long-term profits") into specific, measurable sub-objectives.

    *Example for oil company:*
    - Goal: Maximize the company's profit from the oil field
    - Sub-objectives:
        - Minimize downside risk
        - Limit upfront cost
        - Align with strategic reserves

2. **Generate Alternatives**: Brainstorm all feasible actions—not just obvious ones.

    *Example for oil company:*
    - Buy the field
    - Don't buy
    - **New:** Delay decision and commission an extra study

3. **Model the Decision Problem**: Structure uncertainty, outcomes and preferences.

    *Example for oil company:*
    - Define states (field quality: high/medium/low)
    - Assign probabilities (35%/45%/20%)
    - Map outcomes to utilities (e.g., profit values)

    **Toolkit:** Decision trees, influence diagrams

4. **Calculate Optimal Decision**: Compute expected utilities and select the best action.

    *Example for oil company:*
    
    $$ EMV(\text{Buy}) = (0.35 \times \$1,250\text{M}) + (0.45 \times \$630\text{M}) + (0.20 \times \$0\text{M}) = \$721\text{M} $$
    
    $$ EMV(\text{Do not buy}) = \$350\text{M} $$
    
    Optimal choice: Buy ($721M > $350M)

5. **Sensitivity Analysis**: Test robustness by perturbing key inputs.

    *Example for oil company:*

    What if "high quality" probability drops to 25%?
    
    $$ EMV(\text{Buy}) = (0.25 \times \$1,250\text{M}) + (0.55 \times \$630\text{M}) + (0.20 \times \$0\text{M}) = \$616.5\text{M} $$
    
    → Still better than $350M (robust)

    What if "low quality" outcome worsens to $-200M$?
    
    $$ EMV(\text{Buy}) = (0.35 \times \$1,250\text{M}) + (0.45 \times \$630\text{M}) + (0.20 \times -\$200\text{M}) = \$681.5\text{M} $$
    
    → Still optimal, but riskier

6. **Implement or Iterate**

    Decision point:
    - If satisfied (optimal choice is robust and aligns with objectives) → Implement
    - If not → Revisit earlier phases

    *Example for oil company:*
    
    Triggers for iteration:
    - Uncertainty too high? → Gather more data (e.g., seismic tests)
    - Missing variables? → Add environmental/social costs
    - New alternatives? → Explore partnerships

## When New Information Becomes an Option

Just as the company is about to move forward, a new opportunity arises: it can choose to perform a geological test before deciding whether to purchase the oil field. This test doesn't reveal the true quality of the field directly—it provides a report on the porosity of the reservoir rock. High porosity often suggests greater oil potential, but the test is imperfect, and its results come with uncertainty.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/rock_porosity.jpg" alt="Rock porosity illustration" width="600">
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 3.</b> Reservoir quality illustrated through porosity and permeability characteristics</i>
    </td>
  </tr>
</table>
</center>

The test has two possible outcomes:

* Pass: Porosity is ≥ 15%, indicating significant percentage of pore (void)space in the rocks that can hold fluids like oil or gas.
* Fail: Porosity is < 15%, indicating lower void space and thus lower oil potential.

The test itself comes at a cost, and even after receiving its result, the company will still need to decide whether to proceed with the purchase. So now, instead of a single decision, we have two decisions in sequence:

* Should we perform the test?
* Depending on the result, should we buy the field?

This two-stage problem—with interdependent decisions and probabilistic updates—can't be solved with simple payoff tables. We'll need:

* Decision trees (not to be confused with the ones used in machine learning), which map out possible actions, chance events, and outcomes in a step-by-step visual format.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/oil_decision_tree.png" alt="Oil decision tree" width="400">
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 4.</b> Oil decision tree</i>
    </td>
  </tr>
</table>
</center>

* Decision networks (or influence diagrams), which provide a more compact and flexible way to represent complex decision problems with multiple variables and dependencies.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-01-decision-theory-I/oil_influence_diagram.png" alt="Oil influence diagram" width="700">
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 5.</b> Oil decision network, before and after introducing memory arcs</i>
    </td>
  </tr>
</table>
</center>

## Where to Read More

<center>
<table>
  <tr>
    <th>Book Cover</th>
    <th>Reference</th>
    <th>Key Focus</th>
  </tr>
  <tr>
    <td align="center"><img src="/assets/2025-06-01-decision-theory-I/howard_matheson_1983.jpg" width="100" height="100" style="object-fit: cover;"></td>
    <td><strong>Howard & Matheson (1983)</strong><br><em>Readings on Decision Analysis</em><br>DOI: 10.1287/opre.31.4.813</td>
    <td>Classic collection of papers on decision analysis methodology and applications</td>
  </tr>
  <tr>
    <td align="center"><img src="/assets/2025-06-01-decision-theory-I/robert_clemens_1995.jpg" width="100" height="100" style="object-fit: cover;"></td>
    <td><strong>Robert T. Clemens (1995)</strong><br><em>Making Hard Decisions</em><br>ISBN: 978-0534260347</td>
    <td>Practical guide to structuring decisions and handling uncertainty with real-world examples</td>
  </tr>
  <tr>
    <td align="center"><img src="/assets/2025-06-01-decision-theory-I/russel_norvig_2021.jpg" width="100" height="100" style="object-fit: cover;"></td>
    <td><strong>Russell & Norvig (2010)</strong><br><em>AI: A Modern Approach</em> (Ch. 16)<br>ISBN: 978-0134610993</td>
    <td>Decision Theory & Decision Networks</td>
  </tr>
  <tr>
    <td align="center"><img src="/assets/2025-06-01-decision-theory-I/koller_friedman.jpg" width="100" height="100" style="object-fit: cover;"></td>
    <td><strong>Koller & Friedman (2009)</strong><br><em>Probabilistic Graphical Models</em> (Ch. 22, 23)<br>ISBN: 978-0262013192</td>
    <td>Advanced coverage of decision networks and their integration with probabilistic reasoning</td>
  </tr>
  <tr>
    <td align="center"><img src="/assets/2025-06-01-decision-theory-I/insua_lozoya_2002.jpg" width="100" height="100" style="object-fit: cover;"></td>
    <td><strong>Ríos Insua et al. (2002)</strong><br><em>Fundamentos de los Sistemas de Ayuda a la Decisión</em><br>ISBN: 978-8478972746</td>
    <td>Comprehensive introduction to decision support systems with emphasis on theoretical foundations</td>
  </tr>
</table>
</center>

## Next Post

In Part II, we'll:

1. Build and solve a decision tree for the oil field problem, incorporating the geological test

2. Present the limitations of Decision Trees and why decision networks may be preferred in certain situations.
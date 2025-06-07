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
    <th style="color:blue;">Monetary Outcome</th>
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

>**Why is there a profit for not buying?**
>
>This could represent a baseline alternative, like investing the capital elsewhere for a guaranteed return of $350M.

### Calculating Expected Monetary Value

So, how do we weigh these possibilities financially? A common approach is to calculate the Expected Monetary Value (EMV). For the 'Buy' option, the EMV considers each potential outcome, its likelihood, and its financial value. Here's how it breaks down:

$$
\begin{align*}
\mathbb{E}[MV(\text{Buy})] &= (0.35 \cdot \$1,250\text{M}) + (0.45 \cdot \$630\text{M}) + (0.20 \cdot \$0\text{M}) \\
&= \$437.5\text{M} + \$283.5\text{M} + \$0\text{M} \\
&= \$721\text{M}
\end{align*}
$$

This gives us an EMV of $721M if we decide to buy. Now, let's look at the 'Do not buy' option. Its EMV is simpler:

$$ \mathbb{E}[MV(\text{Do not buy})] = \$350\text{M} $$

Purely from an EMV perspective, buying the field seems to be the stronger choice, offering an expected $721M versus $350M.

### Beyond Money: Utility and Risk Preferences

But EMV doesn't always tell the whole story. What if not making a profit from this project could be disastrous for our company, or on the flip side, a big payout isn't really necessary? EMV treats every dollar the same. However, real-world decisions often depend on how much risk we're willing to take.

That's where <a href="https://plato.stanford.edu/entries/rationality-normative-utility/"><u><b>Utility theory</b></u></a> comes in. Instead of just looking at dollar amounts, we give each outcome a "utility score" to show how much it really matters to us. EMV assumes linear utility, which only holds if the decision maker is risk-neutral. Utility theory allows us to account for different risk preferences. Then we calculate an Expected Utility (EU) by weighing these scores by their probabilities, just like we do with EMV.

**So how do we figure out these utility scores?** We start by anchoring the utility scale to simplify comparisons: 

* Set best monetary outcome → $$U(\$1,250\text{M}) = 1$$
* Set worst monetary outcome → $$U(\$0) = 0$$

Then, we need to find utility values for those outcomes in the middle ($350M, $630M). This depends on the **decision maker's risk preferences**. A common method is the <a href="https://ontosight.ai/glossary/term/von-neumann-morgenstern-standard-gamble-theory--679f4e9e38099fda3c01d216"><u><b>standard gamble</b></u></a>. It works like this: ask the decision maker what chance of winning the best outcome (i.e., \$1,250M) they'd accept in a lottery — versus taking a guaranteed amount. For example:

*"Would you rather take a sure \$630M, or a gamble with a 70% chance of \$1,250M and 30% chance of \$0M?"*

If they say they're indifferent, we assign: $$U(350\text{M}) = 0.7$$. If they are also indifferent between a sure \$630M, and a lottery with 90% chance of \$1250M and 10% chance of \$0, we assign: $$U(630\text{M}) = 0.7$$.

<center>
<table align="center">
  <tr>
    <th style="color:red;">Action</th>
    <th style="color:purple;">Field Quality</th>
    <th style="color:blue;">Monetary Outcome</th>
    <th style="color:blue;">Utility Outcome</th>
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">High</td>
    <td style="color:blue;">+$1,250M</td>
    <td style="color:blue;">1</td>    
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">Medium</td>
    <td style="color:blue;">+$630M</td>
    <td style="color:blue;">0.9</td>        
  </tr>
  <tr>
    <td style="color:red;">Buy</td>
    <td style="color:purple;">Low</td>
    <td style="color:blue;">+$0M</td>
    <td style="color:blue;">0</td>    
  </tr>
  <tr>
    <td style="color:red;">Do not buy</td>
    <td style="color:purple;">Any</td>
    <td style="color:blue;">+$350M</td>
    <td style="color:blue;">0.7</td>    
  </tr>
</table>
</center>

Let's compute the EU:

$$
\begin{align*}
&\mathbb{E}[U(\text{Buy})] = (0.35 \cdot 1.0) + (0.45 \cdot 0.9) + (0.20 \cdot 0.0) = 0.755 \\ \\
&\mathbb{E}[U(\text{Do not buy})] = 0.7
\end{align*}
$$

EMV suggests to **Buy** (\$721M > \$350M). EU also suggests to **Buy**, but the margin is smaller (0.755 > 0.7). A more risk-averse person (e.g., someone with $$U(\$350M)=0.8$$) would flip the decision.

Previous case is just a hypothetical example. For this article, we'll keep things straightforward and **assume EMV and EU point to the same decision** (i.e., risk neutral decision maker). In reality, though, considering utility can change which option looks best.

> Another well-known example illustrating EMV's limitations is the <a href="https://en.wikipedia.org/wiki/St._Petersburg_paradox"><u><b>St. Petersburg Paradox</b></u></a>. In this scenario, a casino offers a gamble where a fair coin is tossed until heads appears. If the first head appears on the nth toss, the prize is $$2^{n}$$. Assuming the game continues indefinitely and the casino has unlimited resources, the EMV is infinite. This suggests one should pay any amount to play, yet most people wouldn't pay more than \$8 - \$16. The reason is that the large payouts are so improbable that we mentally discount them, thus creating the paradox.

<!-- ## Decision Analysis: A Dynamic, Iterative Process

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
    
    $$ EMV(\text{Buy}) = (0.35 \cdot \$1,250\text{M}) + (0.45 \cdot \$630\text{M}) + (0.20 \cdot \$0\text{M}) = \$721\text{M} $$
    
    $$ EMV(\text{Do not buy}) = \$350\text{M} $$
    
    Optimal choice: Buy (\$721M > \$350M)

5. **Sensitivity Analysis**: Test robustness by perturbing key inputs.

    *Example for oil company:*

    What if "high quality" probability drops to 25%?
    
    $$ EMV(\text{Buy}) = (0.25 \cdot \$1,250\text{M}) + (0.55 \cdot \$630\text{M}) + (0.20 \cdot \$0\text{M}) = \$616.5\text{M} $$
    
    → Still better than \$350M (robust)

    What if "low quality" outcome worsens to $-200M$?
    
    $$ EMV(\text{Buy}) = (0.35 \cdot \$1,250\text{M}) + (0.45 \cdot \$630\text{M}) + (0.20 \cdot -\$200\text{M}) = \$681.5\text{M} $$
    
    → Still optimal, but riskier

6. **Implement or Iterate**

    Decision point:
    - If satisfied (optimal choice is robust and aligns with objectives) → Implement
    - If not → Revisit earlier phases

    *Example for oil company:*
    
    Triggers for iteration:
    - Uncertainty too high? → Gather more data (e.g., seismic tests)
    - Missing variables? → Add environmental/social costs
    - New alternatives? → Explore partnerships -->

## Decision Analysis: A Dynamic, Iterative Process

Decision-making isn't a one-shot task—it's a cycle of refinement. As new information emerges or priorities shift, we revisit and update our analysis. This structured approach ensures that our choices are not only well-founded but also adaptable.

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

The process begins with getting clear on what we're trying to achieve. Instead of a vague goal like "maximize profits," we break it down into specific, measurable objectives. For our oil company, this means not only aiming for the highest return but also minimizing downside risk, limiting upfront costs, and ensuring the project aligns with their strategic reserves.

With these objectives in mind, the next step is to brainstorm all feasible actions, not just the obvious ones. Beyond simply buying or not buying the field, perhaps there's a third path, like delaying the decision to commission an extra study for more data.

Once the alternatives are on the table, we model the decision. This involves structuring the uncertainties (like the field's quality), assigning probabilities (a 35% chance of high quality, etc.), and mapping outcomes to their values. This is where tools like <b><u><a href="https://en.wikipedia.org/wiki/Decision_tree">decision trees</a></u></b> and <b><u><a href="https://en.wikipedia.org/wiki/Influence_diagram">decision networks</a></u></b> (i.e., influence diagrams) become useful for visualizing the entire problem.

With the model built, we can calculate the optimal path forward. As we saw, computing the EU helps us compare the options. Based on the EU, we know that buying is the stronger choice. But a good analysis doesn't stop there. We need to ask, "what if?" This is the role of <b><u><a href="https://en.wikipedia.org/wiki/Sensitivity_analysis">sensitivity analysis</a></u></b>: testing how robust our decision is by tweaking the key inputs. What if the outcome for a "low quality" field isn't breaking even, but a loss of \$200M? 

$$ 
\mathbb{E}[U(\text{Buy})] = (0.35 \cdot \$1,250\text{M}) + (0.45 \cdot \$630\text{M}) + (0.20 \cdot -\$200\text{M}) = \$681.5\text{M} 
$$

The EU for buying is now \$681.5M, still the optimal choice, but the risk profile has clearly changed. 

This stress-testing leads to the final step: implement or iterate. If the optimal choice proves robust and aligns with the company's objectives, it's time to move forward. But if the analysis reveals too much uncertainty or uncovers new risks, it’s a signal to revisit the earlier stages. Maybe the uncertainty is too high, and it's worth gathering more data. Perhaps other variables, like environmental costs, need to be factored into the model. Or maybe new alternatives, like exploring a partnership to share the risk, have become more attractive.

## When New Information Becomes an Option

Just as the company is about to move forward, a new opportunity arises: it can choose to perform a geological test before deciding whether to purchase the oil field. This test won't reveal the true quality of the field, but it will measure the rock's porosity, which measures how much empty space the rock contains that could hold oil. The test has two possible outcomes:

* **Pass:** Porosity is ≥ 15%, indicating a significant amount of pore (void) space in the rocks, which suggests a higher likelihood of finding oil.
* **Fail:** Porosity is < 15%, indicating less void space and therefore a lower potential for oil.

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

In an ideal situation, the test would be extremely accurate. However, real-world tests are not perfect. The table below illustrates these measurement inaccuracies by presenting the conditional probability of each test result based on the quality of the oil field:

<table>
  <tr>
    <th></th>
    <th>high</th>
    <th>medium</th>
    <th>low</th>      
  </tr>
  <tr>
    <td>pass</td>
    <td>0.95</td>
    <td>0.7</td>
    <td>0.15</td>      
  </tr>
  <tr>
    <td>fail</td>
    <td>0.05</td>
    <td>0.3</td>
    <td>0.85</td> 
  </tr>
</table>


The test costs $30 million, and even after getting the results, the company still has to decide whether to buy the field. This means there are now two decisions to make: first, whether to conduct the test, and second, whether to purchase the field based on the test results. This kind of two-step decision-making, where each choice affects the next and involves probabilities, can't be handled with simple payoff tables. Instead, we'll need to use a decision tree or a decision network to figure it out.

## Modelling the Problem with a Decision Tree

Decision trees, originating from the work of <a href="https://gwern.net/doc/statistics/decision/1961-raiffa-appliedstatisticaldecisiontheory.pdf"><u><b>Raiffa & Schlaifer (1961)</b></u></a>, are a powerful tool for visualizing and analyzing decision-making problems. They map out the sequence of decisions and chance events, providing a clear picture of the possible outcomes and their associated probabilities. A decision tree consists of three types of nodes:

* <span style="color:red;"><strong>Decision nodes</strong></span>. These are points where you need to make a choice. In our case, the first decision here is whether to do the geological test. If the test is conducted, the next decision is whether to buy the oil field based on the test results.

* <span style="color:purple;"><strong>Chance nodes</strong></span>. These nodes represent states of nature or events that can affect the outcome. For our problem, the chance nodes include the possible results of the geological test and the actual quality of the oil field.

* <span style="color:blue;"><strong>Outcome nodes</strong></span>. These are the final nodes that show the result of a particular path through the tree. 

To construct the tree, begin by identifying the root node, which represents the first event observed over time: either a decision or an uncertainty factor. From the root, add chance or decision nodes, outlining the different paths to follow, until you reach a terminal node, where the corresponding consequence will be indicated. The decision tree is then completed by including the utilities at the terminal nodes. At these nodes, a value is assigned to a final result, assuming this result has been achieved without considering probabilities.

Below is the decision tree for the oil drilling scenario:

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

## Evaluating the Decision Tree

To figure out the best course of action in a decision tree, we need to look at every possible decision path. This boils down to two key steps:

1. **Estimating Probabilities**. This involves using both marginal and conditional probabilities.
2. **Calculating Expected Utilities**. This requires evaluating the outcomes for each decision.

The expected utility of a decision is computed by multiplying the utility of each outcome by its associated probability and summing these products across all possible outcomes under that decision. The decision with the highest expected utility at each decision node is the optimal choice.

## Next Post

In Part II, we'll:

2. Present the limitations of Decision Trees and why decision networks may be preferred in certain situations.

* Decision networks (or influence diagrams), which provide a more compact and flexible way to represent complex decision problems with multiple variables and dependencies.

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


## References

1. Wikipedia page on
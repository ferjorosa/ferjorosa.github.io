---
layout: post
title: "Introduction to Decision Theory: Part II"
date: 2025-06-14
categories: blog
description: "Explores the strengths and limitations of decision trees, introduces influence diagrams as a scalable alternative, and surveys Python libraries (PyAgrum, PyCID) for practical decision-analysis."
tags: [Decision Theory]
---

<h2 id="decision-trees-strengths-limitations">Strengths and Limitations of Decision Trees</h2>

Decision trees provide a straightforward way to model decisions under uncertainty. Each path from start to finish shows a sequence of choices and events that lead to a specific outcome. The left-to-right layout makes the timing of decisions and chance events visually clear, helping to avoid confusion about what is known at each point. 

For small problems with only a few stages, decision trees can be evaluated using basic arithmetic. This simplicity makes them accessible to a wide audience, including those without technical training. They serve as effective tools for teaching, storytelling, and supporting real-world decisions. 

Yet this intuitive structure comes with notable drawbacks. One issue is the risk of combinatorial explosion. Another limitation is that decision trees do not explicitly show conditional independencies.

<h3 id="combinatorial-explosion">Combinatorial Explosion</h3>
The memory required to store a decision tree and the time required to process it both **increase
exponentially** with the number of variables and their possible states, whether they are decisions or
probabilistic outcomes. In a symmetric problem with $$n$$ variables, each having $$k$$ possible outcomes, you face $$k^{n}$$ distinct paths. Since a decision tree represents all scenarios explicitly, a problem with 50 binary variables would yield an impractical $$2^{50}$$ paths ([Shenoy, 2009](https://pshenoy.ku.edu/Papers/EOLSS09.pdf)).

The number of decision paths is profoundly affected by the order and meaning of the variables (i.e., the problem's definition). In our original oil field investment problem from <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html">Part I</a>, the options "Not Test" and "Do Not Buy" prune the tree, resulting in 12 distinct decision paths. This is an *asymmetric* problem structure:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_asymmetric_tree.png" alt="Decision tree diagram of the asymmetric oil problem from Part I" height="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Decision tree diagram of the asymmetric oil field investment problem from Part I.</i>
    </td>
  </tr>
</table>
</center>

Conversely, a problem with the same types of variables, but structured *symmetrically*, would yield significantly more paths. For instance, imagine the company must always choose to either "Invest in Field A" or "Invest in Field B" (instead of "Buy" or "Do Not Buy"). Both fields then undergo a geological test (say, "Test X" or "Test Y", each with different costs and accuracy profiles), followed by the actual drilling revealing "High", "Medium", or "Low" quality. This structure forces every path to be fully explored, doubling the number of distinct paths from 12 to 24:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_symmetric_tree.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 2.</b> Decision tree diagram of a hypothetical symmetric oil field investment problem.</i>
    </td>
  </tr>
</table>
</center>

Even this revised example demonstrates how swiftly a decision tree can escalate beyond practical use. For instance, merely replacing the three-level oil quality (high/medium/low) with a more granular five-level scale (excellent/good/average/poor/dry) would push the total from 24 to 40 terminal nodes. This occurs without even considering longer time horizons, dynamic market-price scenarios, or additional complex choices.

This **combinatorial explosion** not only affects computational tractability but, even at more modest levels, severely compromises interpretability. As a rule of thumb, once a tree approaches about 100 terminal nodes, they lose their key strength: easy readability and intuitive understanding.


<h3 id="hidden-independence">Hidden Conditional Independencies</h3>

In addition to the issue of combinatorial explosion, decision trees have another important limitation: they assume a strict, linear chain of dependence. In a decision tree, every variable is implicitly conditioned on *all* previous events along its particular path. This rigid structure prevents us from explicitly representing one of the most important concepts in probabilistic modeling: <b><a href="https://en.wikipedia.org/wiki/Conditional_independence"><u>conditional independence</u></a></b>.

To illustrate this, consider a generic problem with four random variables: $$A$$ and $$B$$ (each with two possible states, $$a_1, a_2$$ and $$b_1, b_2$$, respectively), and $$C$$ and $$D$$ (each with three possible states, $$c_1, c_2, c_3$$ and $$d_1, d_2, d_3$$). In a traditional decision tree, where conditional independencies cannot be explicitly represented, you must specify the entire joint probability distribution for all variables. This means assigning a probability to every possible combination of outcomes, as shown in the joint probability table below:

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(A, B, C, D)</summary>

<table>
  <thead>
    <tr>
      <th>$$A$$</th>
      <th>$$B$$</th>
      <th>$$C$$</th>
      <th>$$D$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{1},c_{1},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{1},c_{1},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{1},c_{1},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{1},c_{2},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{1},c_{2},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{1},c_{2},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{1},c_{3},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{1},c_{3},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{1},c_{3},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{2},c_{1},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{2},c_{1},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{2},c_{1},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{2},c_{2},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{2},c_{2},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{2},c_{2},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{1},b_{2},c_{3},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{1},b_{2},c_{3},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{1},b_{2},c_{3},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{1},c_{1},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{1},c_{1},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{1},c_{1},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{1},c_{2},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{1},c_{2},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{1},c_{2},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{1},c_{3},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{1},c_{3},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{1},c_{3},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{2},c_{1},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{2},c_{1},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{2},c_{1},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{2},c_{2},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{2},c_{2},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{2},c_{2},d_{3})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(a_{2},b_{2},c_{3},d_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(a_{2},b_{2},c_{3},d_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(a_{2},b_{2},c_{3},d_{3})$$</td>
    </tr>
  </tbody>
</table>

</details>

In this example, that means $$2$$ (for A) $$\times 2$$ (for B) $$\times 3$$ (for C) $$\times 3$$ (for D) $$= \mathbf{36}$$ **distinct probabilities** that must be elicited and entered into the joint probability table.

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
  This example demonstrates conditional independencies using a simplified version of a decision tree, where all nodes are probabilistic (often called a <a href="https://en.wikipedia.org/wiki/Tree_diagram_(probability_theory)"><u>probability tree</u></a>). However, the core concepts and benefits of explicit representation apply equally to the chance nodes within any general decision tree.
</div>
<br>

Now, let's say that conditional independencies do exist in this problem. For instance, let's say that $$B$$ is conditionally independent of $$C$$ and $$D$$ given $$A$$. We denote that statement by $$(B \bot \{C, D\} \mid A)$$. In that case:

$$
P(B \mid A, C, D) = P(B \mid A)
$$

This fundamental concept allows us to represent relationships far more efficiently. Consider Figure 3, which implies the following conditional independence statements:
* &nbsp;$$ (B \bot \{C, D\} \mid A)$$
* &nbsp;$$ (C \bot B \mid A)$$
* &nbsp;$$ (D \bot \{A,B\} \mid C)$$

The diagram corresponds to the directed acyclic graph of a Bayesian network, which visually encodes these independencies: arrows indicate direct probabilistic influence, while the absence of an arrow between two nodes reflects a conditional independence given their parents.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/bayesian_network_example.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> Bayesian network illustrating conditional independencies among A, B, C, and D.</i>
    </td>
  </tr>
</table>
</center>

When these conditional independencies are recognized and modeled, the burden of data elicitation drastically shrinks. Instead of one big joint table, the full joint probability can be decomposed into a product of smaller, more manageable conditional probability tables. For our example, this decomposition means we only need to specify:

* &nbsp;$$ P(A) \rightarrow 2 = 2 $$ entries
* &nbsp;$$ P(B \mid A) \rightarrow 2 \cdot 2 = 4 $$ entries  
* &nbsp;$$ P(C \mid A) \rightarrow 2 \cdot 3 = 6 $$ entries
* &nbsp;$$ P(D \mid C) \rightarrow 3 \cdot 3 = 9 $$ entries

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(A)</summary>

<table>
  <thead>
    <tr>
      <th>$$A$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$P(a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$P(a_{2})$$</td>
    </tr>
  </tbody>
</table>

</details>


<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(B | A)</summary>

<table>
  <thead>
    <tr>
      <th>$$A$$</th>
      <th>$$B$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$P(b_{1} \mid a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$P(b_{2} \mid a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{1}$$</td>
      <td>$$P(b_{1} \mid a_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$b_{2}$$</td>
      <td>$$P(b_{2} \mid a_{2})$$</td>
    </tr>
  </tbody>
</table>

</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(C | A)</summary>

<table>
  <thead>
    <tr>
      <th>$$A$$</th>
      <th>$$C$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$P(c_{1} \mid a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$P(c_{2} \mid a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{1}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$P(c_{3} \mid a_{1})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$c_{1}$$</td>
      <td>$$P(c_{1} \mid a_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$c_{2}$$</td>
      <td>$$P(c_{2} \mid a_{2})$$</td>
    </tr>
    <tr>
      <td>$$a_{2}$$</td>
      <td>$$c_{3}$$</td>
      <td>$$P(c_{3} \mid a_{2})$$</td>
    </tr>
  </tbody>
</table>

</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(D | C)</summary>

<table>
  <thead>
    <tr>
      <th>$$C$$</th>
      <th>$$D$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$c_{1}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(d_{1} \mid c_{1})$$</td>
    </tr>
    <tr>
      <td>$$c_{1}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(d_{2} \mid c_{1})$$</td>
    </tr>
    <tr>
      <td>$$c_{1}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(d_{3} \mid c_{1})$$</td>
    </tr>
    <tr>
      <td>$$c_{2}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(d_{1} \mid c_{2})$$</td>
    </tr>
    <tr>
      <td>$$c_{2}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(d_{2} \mid c_{2})$$</td>
    </tr>
    <tr>
      <td>$$c_{2}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(d_{3} \mid c_{2})$$</td>
    </tr>
    <tr>
      <td>$$c_{3}$$</td>
      <td>$$d_{1}$$</td>
      <td>$$P(d_{1} \mid c_{3})$$</td>
    </tr>
    <tr>
      <td>$$c_{3}$$</td>
      <td>$$d_{2}$$</td>
      <td>$$P(d_{2} \mid c_{3})$$</td>
    </tr>
    <tr>
      <td>$$c_{3}$$</td>
      <td>$$d_{3}$$</td>
      <td>$$P(d_{3} \mid c_{3})$$</td>
    </tr>
  </tbody>
</table>

</details>

**Total distinct probabilities:** $$2 + 4 + 6 + 9 = \mathbf{21}$$.

This is a remarkable reduction from the original 36 entries in the full joint table. Not only does this significantly cut down the amount of data that needs to be estimated, but it also makes the model far more transparent and easier to update. Each table focuses on a localized relationship, simplifying parameter estimation and model maintenance. As problems grow more complex, the benefits of explicitly representing conditional independencies become exponentially more pronounced.

<!-- However, you *dont need* to have those values written in the table because since they are independent you know their value is simply the multiplication of P(A) * P(B)-->

<h2 id="references">References</h2>

1. Shenoy, P. P. (2009). <a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Decision trees and influence diagrams</u></a>. Encyclopedia of life support systems, 280-298.
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
probabilistic outcomes. In a symmetric problem with $$n$$ variables, each having $$k$$ possible outcomes, you face $$k^{n}$$ distinct paths. Since a decision tree represents all scenarios explicitly, a problem with 50 binary variables would yield an impractical $$2^{50}$$ paths (<a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Shenoy, 2009</u></a>).

The number of decision paths is profoundly affected by the order and meaning of the variables (i.e., the problem's definition). In our original oil field investment problem from <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html"><u>Part I</u></a>, the options <span style="color:red;">Do not perform test</span> and <span style="color:red;">Do not buy</span> prune the tree, resulting in 12 distinct decision paths. This is an *asymmetric* problem structure:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_asymmetric_tree_annotated.png" alt="Decision tree diagram of the asymmetric oil problem from Part I" height="240">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Decision tree diagram of the asymmetric oil field investment problem from Part I.</i>
    </td>
  </tr>
</table>
</center>

Conversely, a problem with the same types of variables, but structured *symmetrically*, would yield significantly more paths. For instance, imagine the company must always choose to either <span style="color:red;">Invest in Field A</span> or <span style="color:red;">Invest in Field B</span>. Both fields then undergo a geological test (say, <span style="color:red;">Test X</span> or <span style="color:red;">Test Y</span>, each with different costs and accuracy profiles), followed by the actual drilling revealing the field's quality. This structure forces every path to be fully explored, doubling the number of distinct paths from 12 to 24:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_symmetric_tree_annotated.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="240">
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

This **combinatorial explosion** not only affects computational tractability but, even at more modest levels, severely compromises interpretability. As a rule of thumb, once a tree approaches about 100 terminal nodes, it loses its key strength: easy readability and intuitive understanding.


<h3 id="hidden-independence">Hidden Conditional Independencies</h3>

In addition to the issue of combinatorial explosion, decision trees have another important limitation: they assume a strict, linear chain of dependence. In a decision tree, every variable is implicitly conditioned on *all* previous events along its particular path. This rigid structure prevents us from explicitly representing one of the most important concepts in probabilistic modeling: <b><a href="https://en.wikipedia.org/wiki/Conditional_independence"><u>conditional independence</u></a></b>.

To illustrate this, consider a generic problem with four <span style="color:purple;"><b>random variables</b></span>: $$A$$ and $$B$$ (each with two possible states, $$a_1, a_2$$ and $$b_1, b_2$$, respectively), and $$C$$ and $$D$$ (each with three possible states, $$c_1, c_2, c_3$$ and $$d_1, d_2, d_3$$. In a traditional decision tree, where conditional independencies cannot be explicitly represented, you must specify the entire joint probability distribution for all variables. This means assigning a probability to every possible combination of outcomes, as shown in the joint probability table below:

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

**Total distinct probabilities:** $$ 2 \; (\text{for } A) \times 2 \; (\text{for } B) \times 3 \; (\text{for } C) \times 3 \; (\text{for } D) = \mathbf{36} $$.

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

The diagram corresponds to the directed acyclic graph of a <a href="https://en.wikipedia.org/wiki/Bayesian_network"><u>Bayesian network</u></a>, which visually encodes these independencies: arrows indicate direct probabilistic influence, while the absence of an arrow between two nodes reflects a conditional independence given their parents.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/bayesian_network_example.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="300">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> Bayesian network illustrating conditional independencies among A, B, C, and D.</i>
    </td>
  </tr>
</table>
</center>

When these conditional independencies are recognized and modeled, we no longer need to construct a single large joint probability table. Instead, the full joint probability distribution can be factored into a product of smaller, more manageable conditional probability tables. In our example, this means we only need to specify:

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

This represents a **42% decrease** from the 36 entries required in the full joint probability table. By reducing the number of parameters that must be specified, the model becomes much more manageable, transparent, and easier to modify. As decision problems increase in complexity, the advantages of explicitly modeling conditional independencies grow even more significant.

<h2 id="decision_networks">Influence Diagrams</h2>

Building on the foundation of Bayesian networks, **influence diagrams** (<a href=""><u>Howard & Matheson, 1984</u></a>), also known as **decision network**, provide a powerful extension that seamlessly integrates decision-making into probabilistic models. Unlike decision trees, influence diagrams avoid combinatorial explosion by factorizing the joint probability distribution and naturally express conditional independencies through their graphical structure.

An influence diagram enhances a Bayesian network by adding two types of nodes:

* <span style="color:red;"><b>Decision nodes</b></span>: Shown as squares, these represent points where the decision-maker chooses among available actions.
* <span style="color:blue;"><b>Outcome nodes</b></span>: Illustrated as diamonds, these indicate the resulting utilities or values associated with different decision paths.

<span style="color:purple;"><b>Chance nodes</b></span> (circles) function as in Bayesian networks, often reusing the same conditional probability tables. In influence diagrams, arcs serve two main purposes: **informational arcs** (into decision nodes) indicate what information is available when a choice is made, while **conditional arcs** (into chance or utility nodes) represent probabilistic or functional dependencies on parent variables, showing which factors affect outcomes or payoffs—without implying causality or temporal order.


<h2 id="modelling_oil_problem">Modelling the Oil Problem</h2>

Modeling takes place at multiple levels. Similar to constructing a decision tree, drawing the influence diagram represents the qualitative description of the problem (structural or graphical level). Next, quantitative information is incorporated (numerical level) to fully specify the model.

One important caveat of influence diagrams is that they only work with symmetric problems. In the case of an asymmetric problem, techniques are used to convert it into a symmetric one. This leads to an increase in the size of the problem, since artificial states (sometimes unintuitive) are usually defined, and as a result, the computational burden increases.

In large and highly asymmetric problems, it is not so straightforward to use these kinds of resources (artificial alternatives and states, degenerate probabilities and utilities) to convert a problem into an equivalent symmetric one. For more information on this topic, see <a href="https://cig.fi.upm.es/wp-content/uploads/2024/01/A-Comparison-of-Graphical-Techniques-for-Asymmetric-Decision-Problems.pdf"><u>Bielza & Shenoy (1999)</u></a>.

In this article, we will use a standard influence diagram. To maintain problem symmetry, an extra state <span style="color:purple;">no results</span> should be added to the test results (<span style="color:purple;"><b>R</b></span>) variable . This is because results are only observed if the test is performed.

<h3 id="modelling_oil_problem_qualitative">Modelling Qualitative Information</h3>

The following image displays the influence diagram structure for the oil problem:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/decision_network_oil.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1a.</b> Traditional influence diagram for the oil problem. Informational arcs</i>
    </td>
  </tr>
</table>
</center>

This diagram illustrates a traditional influence diagram, which operates under the assumption of perfect recall. The information arcs indicate that the Test / No Test (<span style="color:red;"><b>T</b></span>) decision is made prior to the Buy / No Buy (<span style="color:red;"><b>B</b></span>) decision. Furthermore, no information is available before making the test decision, and the test results are known when making the buy decision. This establishes the temporal sequence of variables: <span style="color:red;"><b>T</b></span>, <span style="color:purple;"><b>R</b></span>, <span style="color:red;"><b>B</b></span>, and finally <span style="color:purple;"><b>Q</b></span> (oil field quality).

However, traditional influence diagrams can become computationally complex to solve, particularly for intricate problems, and they may not accurately reflect the realistic limitations of human decision-making. For these reasons, LIMIDs (<a href="https://web.math.ku.dk/~lauritzen/papers/limids.pdf">Lauritzen & Nilsson, 2001)</a> are often the preferred choice. These models relax the perfect recall assumption and allow for explicit representation of limited memory. Memory arcs in LIMIDs explicitly specify which past decisions and observations are remembered and used for each current decision.

The subsequent image presents the corresponding LIMID, enhanced with a green memory arc. This memory arc extends from <span style="color:red;"><b>T</b></span> to <span style="color:red;"><b>B</b></span> because the outcome of the porosity test decision is crucial for the subsequent decision on buying or not buying the field.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/decision_network_oil_limid.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1b.</b> LIMID for the oil problem with a memory arc shown in green.</i>
    </td>
  </tr>
</table>
</center>

For this problem, we will utilize the LIMID version of the oil decision problem.

<h3 id="modelling_oil_problem_quantitative">Modelling Quantitative Information</h3>

Since all our random variables are categorical, we can conveniently represent the quantitative information of the model in tabular form. Below, we specify the prior probabilities, the conditional probability tables, and the utility values relevant to the oil field decision problem.

Prior probabilities for the oil field quality (<b><span style="color: purple;">Q</span></b>):

<table>
  <tr>
    <th colspan="2" style="text-align: center;">P(<span style="color: purple"><b>Q</b></span>)</th>
  </tr>
  <tr>
    <td><span style="color: purple;">high</span></td>
    <td>0.35</td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td>0.45</td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td>0.2</td>
  </tr>
</table>

Conditional probabilities of observing each possible test result (<b><span style="color: purple;">R</span></b>), given the true oil field quality (<b><span style="color: purple;">Q</span></b>) and whether the test was performed (<b><span style="color: red;">T</span></b>):

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">P(<span style="color: purple">R</span> | <span style="color: purple">Q</span>, <span style="color: red">T</span>)</th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">Perform test</span></th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">Do not perform test</span></th>
  </tr>
  <tr>
    <th style="text-align: center;"><span style="color: purple;">high</span></th>
    <th style="text-align: center;"><span style="color: purple;">medium</span></th>
    <th style="text-align: center;"><span style="color: purple;">low</span></th>
    <th style="text-align: center;"><span style="color: purple;">high</span></th>
    <th style="text-align: center;"><span style="color: purple;">medium</span></th>
    <th style="text-align: center;"><span style="color: purple;">low</span></th>
  </tr>
  <tr>
    <td><span style="color: purple;">pass</span></td>
    <td>0.95</td>
    <td>0.7</td>
    <td>0.15</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td><span style="color: purple;">fail</span></td>
    <td>0.05</td>
    <td>0.3</td>
    <td>0.85</td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
  </tr>
  <tr>
    <td><span style="color: purple;">no results</span></td>
    <td>0</td>
    <td>0</td>
    <td>0</td>
    <td>1</td>
    <td>1</td>
    <td>1</td>
  </tr>
</table>

Utility (<b><span style="color: blue;">U</span></b>) for each combination of test decision (<b><span style="color: red;">T</span></b>), buy decision (<b><span style="color: red;">B</span></b>), and oil field quality (<b><span style="color: purple;">Q</span></b>):

<table>
  <tr>
    <th style="text-align: center;"><span style="color: red;">T</span></th>
    <th style="text-align: center;"><span style="color: red;">B</span></th>
    <th style="text-align: center;"><span style="color: purple;">Q</span></th>
    <th style="text-align: center;"><span style="color: blue;">U</span></th>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">Perform test</span></td>
    <td rowspan="3"><span style="color: red;">Buy</span></td>
    <td><span style="color: purple;">high</span></td>
    <td><span style="color: blue;">1220</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td><span style="color: blue;">600</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td><span style="color: blue;">-30</span></td>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">Do not buy</span></td>
    <td><span style="color: purple;">high</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">Do not perform test</span></td>
    <td rowspan="3"><span style="color: red;">Buy</span></td>
    <td><span style="color: purple;">high</span></td>
    <td><span style="color: blue;">1250</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td><span style="color: blue;">630</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td><span style="color: blue;">0</span></td>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">Do not buy</span></td>
    <td><span style="color: purple;">high</span></td>
    <td><span style="color: blue;">350</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td><span style="color: blue;">350</span></td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td><span style="color: blue;">350</span></td>
  </tr>
</table>

<h2 id="evaluating_influence_diagram"> Influence Diagram Evaluation </h2>

Influence diagrams were conceived as a compact, intuitive way to describe decision problems, yet practitioners still had to transform them into a different format (i.e., a decision tree) in order to evaluate them. Until the 1980s, when Shachter (1986) showed how to evaluate the network directly, turning the diagram into a self-contained modelling and inference language.

Shachter's **arc-reversal / node-reduction algorithm** reverses arcs and sequentially eliminates variables, summing over chance nodes and maximising over decision nodes while pushing expected-utility information forward.

<h3 id="local-graph-operations">Four Local Graph Operations</h3>

The arc-reversal / node-reduction algorithm employs a set of fundamental, local graph operations. Each operation ensures that the decision problem remains *semantically equivalent*, meaning the attainable utilities under any strategy are preserved:

1. **Barren-Node Deletion:**
    Any chance or decision node that has no children and is not a parent of a outcome node can be immediately removed from the diagram. Such nodes do not affect the utility and are therefore irrelevant to the decision problem.

    Figure X illustrates the process of barren node elimination. The first diagram becomes the second, and then the third, since removing a barren node can create new barren nodes that can also be eliminated.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-06-14-decision-theory-II/1_barren_node_elimination.png" alt="Barren node elimination example" height="400">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure.</b> Barren node elimination example.</i>
        </td>
      </tr>
    </table>
    </center> 

2. **Chance-Node Removal:**
    Once a chance node $$C$$ becomes a leaf (i.e., **it has no children except outcome nodes**), it can be eliminated via marginalization (taking an expectation). For every outcome node $$O$$ that has $$C$$ as a parent, a new utility table, $$u'_O$$, is computed. This new table will depend on the original parents of $$O$$ (excluding $$C$$) and all the parents of $$C$$.

    $$
    u'_O((\mathbf{\text{Pa}}_{O} \setminus \{C\}) \cup \mathbf{\text{Pa}}_{C}) = \sum_c u_O(\mathbf{\text{Pa}}_{O}) P(C = c \mid \mathbf{\text{Pa}}_{C})
    $$

    Here:
    *   $$\mathbf{\text{Pa}}_{O}$$ denotes the set of parents of $$O$$ in the diagram *before* removing $$C$$.
    *   $$\mathbf{\text{Pa}}_{C}$$ denotes the set of parents of $$C$$.
    *   $$u'_O$$ represents the *new* utility table for node $$O$$.

    <br>
    Node $$C$$ and its conditional probability table are then deleted. This operation "pushes expected utility forward" by embedding the influence of $$C$$ into the successor utility tables. The outcome node $$O$$ effectively "inherits" the predecessors of $$C$$, ensuring that all relevant dependencies are preserved.

    Figure X showcases the process of chance node removal. The first diagram becomes the second, where parents of $$C_{2}$$ become then parents of $$O$$.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-06-14-decision-theory-II/2_chance_node_removal.png" alt="Chance node removal example" height="150">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure.</b> Chance node removal example.</i>
        </td>
      </tr>
    </table>
    </center> 

3. **Decision-Node Removal:**
    When a decision node $$D$$ becomes a leaf in the influence diagram, meaning its only children are outcome nodes, it can be eliminated. This step requires identifying the optimal decision for $$D$$ in every possible situation, or "information state," defined by the specific combination of observed values of $$D$$'s parent nodes.

    For each information state $$i$$, we select the action $$d$$ that maximizes the expected utility $$\mathbb{E}[u(d, i)]$$. This action represents the best choice for that information state and forms part of the overall optimal policy:

    $$
    \delta^*(i) = \text{argmax}_d \ \mathbb{E}[u(d, i)]
    $$

    The function $$\delta^*(i)$$ is recorded as the optimal decision rule for node $$D$$ in information state $$i$$. After removing $$D$$, each outcome node $$O$$ that was a child of $$D$$ has its utility table updated to reflect the maximum expected utility achievable after making the optimal decision at $$D$$, given the information state $$i$$.

    This process "locks in" the optimal strategy for $$D$$ and propagates the maximum expected utility information forward through the diagram, much like how chance nodes are eliminated by marginalization.

    Figure X illustrates the process of decision node elimination: the first diagram becomes the second, and the utility table for variable U is updated accordingly.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-06-14-decision-theory-II/3_decision_node_removal.png" alt="Decision node removal example" width="600">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure.</b> Decision node removal example.</i>
        </td>
      </tr>
    </table>
    </center>     

4. **Arc Reversal (between chance nodes):**
    In most influence diagrams, nodes are not naturally leaves. They may have children that prevent use from eliminating them directly. To solve this, we use arc reversal to make a target node into a leaf by pushing its influence "backwards" to its children and adjusting the rest of the diagram so that it still represents the same probabilistic relationships.

    Let's say we want to reverse an arc $$X \rightarrow Y$$ where $$\mathbf{\text{Pa}}_{X}$$ is the set of parents of $$X$$ and $$\mathbf{\text{Pa}}_{Y}$$ is the parents of $$Y$$, including $$X$$ itself.

    To reverse, we remove the arc $$X \rightarrow Y$$, add a new arc $$Y \rightarrow X$$, add arcs from $$\mathbf{\text{Pa}}_{X}$$ to $$Y$$ if they are not already parents of $$Y$$, and add arcs $$\mathbf{\text{Pa}}_{Y}$$ to $$X$$, if needed, to preserve dependencies. This means the new  parents of $$X$$ and $$Y$$ are:

    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{Y} = \mathbf{\text{Pa}}_{X} \cup \mathbf{\text{Pa}}_{Y}  \setminus \{Y\}$$
    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{X} = \mathbf{\text{Pa}}_{X} \cup \mathbf{\text{Pa}}_{Y}  \cup \{Y\} \setminus \{X\}$$
    
    <br>
    To maintain consistency (i.e., preserve the joint distribution under the new structure), we must compute the new conditional probabilities using Bayes' Theorem:
    
    $$
    \begin{aligned}
    P(Y \mid \mathbf{\text{Pa}}^{\text{new}}_{Y}) 
    &= \sum_{X} P(Y \mid \mathbf{\text{Pa}}_{Y}) \cdot P(X \mid \mathbf{\text{Pa}}_{X}) \\ \\
    
    P(X \mid \mathbf{\text{Pa}}^{\text{new}}_{X}) 
    &= \frac{P(Y \mid \mathbf{\text{Pa}}_{Y}) \cdot P(X \mid \text{Pa}(X))}{P(Y \mid \text{Pa}_{\text{new}}(Y))}
    \end{aligned}
    $$

    As an example, Figure X showcases an influence diagram with three chance nodes before and after reversing the arc $$X \rightarrow Y$$.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-06-14-decision-theory-II/4_arc_reversal.png" alt="Decision node removal example" width="600">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure.</b> Arc reversal example.</i>
        </td>
      </tr>
    </table>
    </center>  

    Assume binary variables for simplicity:

    <table>
      <thead>
        <tr>
          <th colspan="2" style="text-align:center">$$P(Z)$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$z_{0}$$</td><td>0.7</td></tr>
        <tr><td>$$z_1$$</td><td>0.3</td></tr>
      </tbody>
    </table>

      <table>
      <thead>
        <tr>
          <th>$$P(X \mid Z)$$</th><th>$$z_0$$</th><th>$$z_1$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$x_0$$</td><td>0.6</td><td>0.1</td></tr>
        <tr><td>$$x_1$$</td><td>0.4</td><td>0.9</td></tr>
      </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th>$$P(Y \mid X)$$</th><th>$$x_0$$</th><th>$$x_1$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$y_0$$</td><td>0.9</td><td>0.2</td></tr>
        <tr><td>$$y_1$$</td><td>0.1</td><td>0.8</td></tr>
      </tbody>
    </table>

    Reversing $$X \rightarrow Y$$ yields the following parent sets:

    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{Y} = \{Z\}$$
    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{X} = \{Z, Y\}$$

    <br>

    Marginalize $$X$$ to compute the new CPT for $$Y$$:

    $$
    P(Y \mid Z) = \sum_{x} P(Y \mid x) P(x \mid Z).
    $$

    Let's compute all probabilities:

    $$z_{0}$$:

    $$
    \begin{aligned}
    P(y_1 \mid z_0) &= P(y_1 \mid x_1)P(x_1 \mid z_0) + P(y_1 \mid x_0)P(x_0 \mid z_0) \\
                    &= 0.8 \times 0.4 + 0.1 \times 0.6 \\
                    &= 0.32 + 0.06 = 0.38 \\
    P(y_0 \mid z_0) &= 1 - P(y_1 \mid z_0) = 1 - 0.38 = 0.62
    \end{aligned}
    $$

    $$z_{1}$$:
    
    $$
    \begin{aligned}
    P(y_1 \mid z_1) &= P(y_1 \mid x_1)P(x_1 \mid z_1) + P(y_1 \mid x_0)P(x_0 \mid z_1) \\
                    &= 0.8 \times 0.9 + 0.1 \times 0.1 \\
                    &= 0.72 + 0.01 = 0.73 \\
    P(y_0 \mid z_1) &= 1 - P(y_1 \mid z_1) = 1 - 0.73 = 0.27 \\
    \end{aligned}
    $$

    These values can be summarized as:

    <table>
      <thead>
        <tr><th>$$P(Y \mid Z)$$</th><th>$$y_0$$</th><th>$$y_1$$</th></tr>
      </thead>
      <tbody>
        <tr><td>$$z_0$$</td><td>0.62</td><td>0.38</td></tr>
        <tr><td>$$z_1$$</td><td>0.27</td><td>0.73</td></tr>
      </tbody>
    </table>

    Apply Bayes' Theorem to compute the new CPT for $$X$$:

    $$
    P(X \mid Z, Y) = \frac{P(Y \mid X) \, P(X \mid Z)}{P(Y \mid Z)}.
    $$

    For clarity, here are the calculations for each $$(Z, Y)$$ pair (all values rounded to 3 decimal places):

    ($$z_{0}$$, $$y_{0}$$):

    $$
    \begin{aligned}
    &\quad P(x_1 \mid z_0, y_0) = \frac{P(y_0 \mid x_1) \, P(x_1 \mid z_0)}{P(y_0 \mid z_0)} = \frac{0.2 \times 0.4}{0.62} = 0.129 \\
    &\quad P(x_0 \mid z_0, y_0) = 1 - P(x_1 \mid z_0, y_0) = 1 - 0.129 = 0.871
    \end{aligned}
    $$

    ($$z_{0}$$, $$y_{1}$$):

    $$
    \begin{aligned}
    &\quad P(x_1 \mid z_0, y_1) = \frac{P(y_1 \mid x_1) \, P(x_1 \mid z_0)}{P(y_1 \mid z_0)} = \frac{0.8 \times 0.4}{0.38} = 0.842 \\
    &\quad P(x_0 \mid z_0, y_1) = 1 - P(x_1 \mid z_0, y_1) = 1 - 0.842 = 0.158 \\[3ex]
    \end{aligned}
    $$

    ($$z_{1}$$, $$y_{0}$$):

    $$
    \begin{aligned}
    &\quad P(x_1 \mid z_1, y_0) = \frac{P(y_0 \mid x_1) \, P(x_1 \mid z_1)}{P(y_0 \mid z_1)} = \frac{0.2 \times 0.9}{0.27} = 0.667 \\
    &\quad P(x_0 \mid z_1, y_0) = 1 - P(x_1 \mid z_1, y_0) = 1 - 0.667 = 0.333 \\[3ex]
    \end{aligned}
    $$

    ($$z_{1}$$, $$y_{1}$$):

    $$
    \begin{aligned}
    &\quad P(x_1 \mid z_1, y_1) = \frac{P(y_1 \mid x_1) \, P(x_1 \mid z_1)}{P(y_1 \mid z_1)} = \frac{0.8 \times 0.9}{0.73} = 0.986 \\
    &\quad P(x_0 \mid z_1, y_1) = 1 - P(x_1 \mid z_1, y_1) = 1 - 0.986 = 0.014 \\[3ex]
    \end{aligned}
    $$

    These values can be summarized as:

    <table>
      <thead>
        <tr><th>$$P(X \mid Z,Y)$$</th><th>$$x_0$$</th><th>$$x_1$$</th></tr>
      </thead>
      <tbody>
        <tr><td>$$(z_0, y_0)$$</td><td>0.871</td><td>0.129</td></tr>
        <tr><td>$$(z_0, y_1)$$</td><td>0.158</td><td>0.842</td></tr>
        <tr><td>$$(z_1, y_0)$$</td><td>0.333</td><td>0.667</td></tr>
        <tr><td>$$(z_1, y_1)$$</td><td>0.014</td><td>0.986</td></tr>
      </tbody>
    </table>

<h3 id="node-reduction-algorithm">The Node-Reduction Algorithm</h3>

The algorithm incrementally eliminates nodes by repeatedly applying the four local graph operations described above, until only a single value node remains. The number stored in this final value node is the **maximum expected utility (MEU)**, and the collection of recorded decision rules forms an **optimal policy** for the original decision problem.

**Input:** A well-formed influence diagram (or LIMID).  
**Output:** MEU and an optimal policy for every decision node.

**Preparatory steps:** 
- **Canonical form:** If the diagram does not already satisfy the standard conventions (total order of decisions, and no arcs from decisions to chance nodes), perform a sequence of **Arc Reversals (Rule 4)** to obtain a canonical influence diagram.
- **LIMID transformation:** Transform the influence diagram into a LIMID by adding *memory arcs* so that each decision node has, as parents, all information variables that are remembered at the time of the decision.

---

**Main loop - repeat until only one value node remains:**

1. **Select a node $$N$$ to eliminate**
   - If there is any *barren node* (no children), delete it immediately using **Barren-Node Deletion (Rule 1)**.
   - Otherwise, choose any *leaf node* (a chance or decision node whose only children are value nodes).
   - If no leaf exists, pick a non-value node and repeatedly apply **Arc Reversal (Rule 4)** to its outgoing arcs until it becomes a leaf.

2. **Eliminate $$N$$**
   - If $$N$$ is a **chance node**, apply **Chance-Node Removal (Rule 2)**: marginalize over $$N$$ and update the affected value tables.
   - If $$N$$ is a **decision node**, apply **Decision-Node Removal (Rule 3)**: maximize over the actions of $$N$$, record the optimal decision rule $$\delta^*$$, and update the value tables.

3. **Merge duplicate value nodes** that may have arisen during elimination.

---

When the loop terminates, only one value node remains. Its single numerical entry is the MEU.  
The set $$\{\delta^*\}$$ collected along the way provides an optimal decision rule for every decision node.

<h3 id="relationship-to-bayesian-network-elimination">Relationship to Bayesian Network Variable Elimination</h3>

Arc reversal/node reduction in influence diagrams is structurally similar to variable elimination in Bayesian networks. The main difference being the handling of utilities via **maximization** 
over decision nodes (instead of **summation** over chance nodes). In both approaches, information is propagated through the graph by combining local factors (such as conditional probability tables or utility functions) and eliminating variables—either by summing over uncertainties for chance nodes or optimizing (maximizing) over decisions for decision nodes.

This similarity also extends to computational complexity: since both methods generate and manipulate similar intermediate factors, their efficiency is determined by the **induced width** (or **treewidth**) of the chosen elimination order.

<h3 id="related-work-evaluation">Related Work</h3>

Several alternative strategies exist for evaluating influence diagrams beyond the arc-reversal / node-reduction procedure described above.

A more compact exact method is **junction-tree propagation** (also inspired from the Bayesian network equivalent). In this approach, the diagram is moralized, triangulated, and compiled into a tree of cliques. Local probability-utility factors are then exchanged between cliques via message passing (using Shafer–Shenoy or HUGIN style algorithms) until convergence. Junction-tree algorithms are often more memory-efficient than flat variable elimination and form the basis of many commercial tools such as PyAgrum (Jensen et al., 1994; Madsen & Nilsson, 2001).

<div style="background-color:rgb(250, 224, 224); padding: 10px; border-radius: 5px;">

Creo que esto deberia ponerlo en la parte de Software

</div>


However, even junction-tree propagation can become infeasible in practice: the required clique tables may become prohibitively large for densely connected models, and exact arc-reversal is challenging when the diagram includes continuous variables. In such cases, analysts often turn to **approximate methods**. The most common is Monte Carlo sampling, which estimates expected utility by simulating random scenarios (Shachter & Kenley, 1989). Subsequent research has shown that this approach can be extended to non-Gaussian or hybrid diagrams (Bielza et al., 1999; Cobb & Shenoy, 2005). 

Finally, another avenue is variational inference, although I haven't yet found published work applying it to influence diagrams. In principle one could adapt techniques such as variational message passing (Winn & Bishop, 2005) to do so.

<h2 id="evaluating-oil-influence-diagram">Evaluating the Oil Influence Diagram</h2>

We will use the arc-reversal / node-reduction algorithm to solve the oil decision problem. Observe that the influence diagram is already a LIMID since we added the arc T $$\rightarrow$$ B and it is in canonical form.

We observe that there are no barren nodes, nor any leaf nodes. In such a case, we need to choose one of the chance nodes and apply arc reversal until it becomes a leaf.

For the first step, we choose node Q, and therefore, we must reverse the arc Q $$\rightarrow$$ R. To reverse it, we eliminate Q $$\rightarrow$$ R, add R $$\rightarrow$$ Q, and add arcs from the parents of R to Q, if they were not already parents of Q. This means we also add the arc T $$\rightarrow$$ R.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_reverse_q.png" alt="TODO" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1b.</b> TODO</i>
    </td>
  </tr>
</table>
</center>

In order to obtain the P(R \mid T) distribution, we need to first marginalize Q in P(R \mid Q):


$$
\begin{aligned}
P(R = \text{pass} \mid Q) &= P(\text{pass}  \mid \text{high})P(\text{high}) + P(\text{pass}  \mid \text{medium})P(\text{medium}) + P(\text{pass}  \mid \text{low})P(\text{low}) \\
                &= 0.95 \times 0.35 + 0.7 \times 0.45 + 0.15 \times 0.2 \\
                &= 0.3325 + 0.315 + 0.03 \\
                &= 0.6775 \\
P(R = \text{fail} \mid Q) &= P(\text{fail}  \mid \text{high})P(\text{high}) + P(\text{fail}  \mid \text{medium})P(\text{medium}) + P(\text{fail}  \mid \text{low})P(\text{low}) \\
                &= 0.05 \times 0.35 + 0.3 \times 0.45 + 0.85 \times 0.2 \\
                &= 0.0175 + 0.135 + 0.17 \\
                &= 0.3225 \\
\end{aligned}
$$

Now, given that $R$ only applies when we make the test, we know that P(R \mid Q, T = \text{perform}) is basically P(R \mid Q) and that P(R \mid Q, T = \text{do_not_perform}) is all 0s except for "no results". Therefore:

<table>
  <tr>
    <th><span style="color: purple;">P(R \mid T)</span></th>
    <th><span style="color: purple;">perform test</span></th>
    <th><span style="color: purple;">do not perform test</span></th>      
  </tr>
  <tr>
    <td><span style="color: purple;">pass</span></td>
    <td>0.6775</td>
    <td>0</td>   
  </tr>
  <tr>
    <td><span style="color: purple;">fail</span></td>
    <td>0.3225</td>
    <td>0</td>
  </tr>
  <tr>
    <td><span style="color: purple;">no results</span></td>
    <td>0</td>
    <td>1</td>
  </tr>
</table>

Now for P(Q \mid R), we need to apply bayes theorem:

$$
\begin{aligned}
P(Q = \text{high} \mid R = \text{pass}) &= \frac{P(R = \text{pass} \mid Q = \text{high})P(Q = \text{high})}{P(R = \text{pass})} \\
&= \frac{0.95 \times 0.35}{0.6775} = \frac{0.3325}{0.6775} \approx 0.4908 \\
P(Q = \text{medium} \mid R = \text{pass}) &= \frac{P(R = \text{pass} \mid Q = \text{medium})P(Q = \text{medium})}{P(R = \text{pass})} \\
&= \frac{0.7 \times 0.45}{0.6775} = \frac{0.315}{0.6775} \approx 0.4649 \\
P(Q = \text{low} \mid R = \text{pass}) &= \frac{P(R = \text{pass} \mid Q = \text{low})P(Q = \text{low})}{P(R = \text{pass})} \\
&= \frac{0.15 \times 0.2}{0.6775} = \frac{0.03}{0.6775} \approx 0.0443 \\
P(Q = \text{high} \mid R = \text{fail}) &= \frac{P(R = \text{fail} \mid Q = \text{high})P(Q = \text{high})}{P(R = \text{fail})} \\
&= \frac{0.05 \times 0.35}{0.3225} = \frac{0.0175}{0.3225} \approx 0.0543 \\
P(Q = \text{medium} \mid R = \text{fail}) &= \frac{P(R = \text{fail} \mid Q = \text{medium})P(Q = \text{medium})}{P(R = \text{fail})} \\
&= \frac{0.3 \times 0.45}{0.3225} = \frac{0.135}{0.3225} \approx 0.4186 \\
P(Q = \text{low} \mid R = \text{fail}) &= \frac{P(R = \text{fail} \mid Q = \text{low})P(Q = \text{low})}{P(R = \text{fail})} \\
&= \frac{0.85 \times 0.2}{0.3225} = \frac{0.17}{0.3225} \approx 0.5271
\end{aligned}
$$

When T = do not perform then R does not make sense, so P(Q \mid R, T = do not perform) is basically P(R). Therefore:

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">P(<span style="color: purple">Q</span> | <span style="color: purple">R</span>, <span style="color: red">T</span>)</th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">Perform test</span></th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">Do not perform test</span></th>
  </tr>
  <tr>
    <th style="text-align: center;"><span style="color: purple;">pass</span></th>
    <th style="text-align: center;"><span style="color: purple;">fail</span></th>
    <th style="text-align: center;"><span style="color: purple;">no results</span></th>
    <th style="text-align: center;"><span style="color: purple;">pass</span></th>
    <th style="text-align: center;"><span style="color: purple;">fail</span></th>
    <th style="text-align: center;"><span style="color: purple;">no results</span></th>
  </tr>
  <tr>
    <td><span style="color: purple;">high</span></td>
    <td>0.4908</td>
    <td>0.0543</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.35</td>
  </tr>
  <tr>
    <td><span style="color: purple;">medium</span></td>
    <td>0.4649</td>
    <td>0.4186</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.45</td>
  </tr>
  <tr>
    <td><span style="color: purple;">low</span></td>
    <td>0.0443</td>
    <td>0.5271</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.2</td>
  </tr>
</table>

By making the problem symmetric, we have introduced many zero probabilities, which increases the chance of encountering 0/0 situations. We must remember that a conditional probability P(a \ mid b) is only defined for those b with P(b) > 0, so we should not expect to be able to compute all conditionals when reversing arcs. In any case, as will be seen below, these "x" values will not have any influence on the problem.

Once we have inverted the arc Q $$\rightarrow$$ R, Q becomes a leaf node and thus we can remove it. Figure X shows the resulting diagram.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_remove_q.png" alt="TODO" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1b.</b> TODO.</i>
    </td>
  </tr>
</table>
</center>

By removing Q, we need to marginalize it and update the utility table of U

$$
u'_U(T, R, B) = \sum_q u_U(T, B, Q)P(Q = q \mid T, R)
$$


$$
\begin{aligned}
u'(T = \text{perform}, R = \text{pass}, B = \text{buy}) &= u_U(\text{perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{pass}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{pass}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{pass}) \\
&= 1220 \times 0.4908 + 600 \times 0.4649 + (-30) \times 0.0443 \\
&= 598.776 + 278.94 - 1.329 \\
&= 876.387 \\[1em]
% -------------------
u'(T = \text{perform}, R = \text{pass}, B = \text{no_buy}) &= u_U(\text{perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{pass}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{pass}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{pass}) \\
&= 320 \times 0.4908 + 320 \times 0.4649 + 320 \times 0.0443 \\
&= 157.056 + 148.768 + 14.176 \\
&= 320 \\[1em]
% -------------------
u'(T = \text{perform}, R = \text{fail}, B = \text{buy}) &= u_U(\text{perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{fail}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{fail}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{fail}) \\
&= 1220 \times 0.0543 + 600 \times 0.4186 + (-30) \times 0.5271 \\
&= 66.246 + 251.16 - 15.813 \\
&= 301.593 \\[1em]
% -------------------
u'(T = \text{perform}, R = \text{fail}, B = \text{no_buy}) &= u_U(\text{perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{fail}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{fail}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{fail}) \\
&= 320 \times 0.0543 + 320 \times 0.4186 + 320 \times 0.5271 \\
&= 17.376 + 133.952 + 168.672 \\
&= 320 \\[1em]
% -------------------
% The following equations for T = no_perform and R = pass/fail are shown with 'x' as a placeholder multiplier, as requested by the user, even though 'x' in the provided table indicates an inapplicable or 'no results' scenario.
% For numerical calculation, 'x' is treated as 1 to reflect the original values.
u'(T = \text{no_perform}, R = \text{pass}, B = \text{buy}) &= u_U(\text{no_perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{pass}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{pass}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{pass}) \\
&= 1250 \times x + 630 \times x + 0 \times x \\
&= 1250x + 630x + 0x \\
&= 1880x \\[1em]
% -------------------
u'(T = \text{no_perform}, R = \text{pass}, B = \text{no_buy}) &= u_U(\text{no_perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{pass}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{pass}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{pass}) \\
&= 350 \times x + 350 \times x + 350 \times x \\
&= 350x + 350x + 350x \\
&= 1050x \\[1em]
% -------------------
u'(T = \text{no_perform}, R = \text{fail}, B = \text{buy}) &= u_U(\text{no_perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{fail}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{fail}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{fail}) \\
&= 1250 \times x + 630 \times x + 0 \times x \\
&= 1250x + 630x + 0x \\
&= 1880x \\[1em]
% -------------------
u'(T = \text{no_perform}, R = \text{fail}, B = \text{no_buy}) &= u_U(\text{no_perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{fail}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{fail}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{fail}) \\
&= 350 \times x + 350 \times x + 350 \times x \\
&= 350x + 350x + 350x \\
&= 1050x \\[1em]
% -------------------
% The following equations for T = perform and R = no_results are shown with 'x' as a placeholder multiplier, as requested by the user, even though 'x' in the provided table indicates an inapplicable or 'no results' scenario.
% For numerical calculation, 'x' is treated as 1 to reflect the original values.
u'(T = \text{perform}, R = \text{no_results}, B = \text{buy}) &= u_U(\text{perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{no_results}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{no_results}) \\
&\quad + u_U(\text{perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{no_results}) \\
&= 1220 \times x + 600 \times x + (-30) \times x \\
&= 1220x + 600x - 30x \\
&= 1790x \\[1em]
% -------------------
u'(T = \text{perform}, R = \text{no_results}, B = \text{no_buy}) &= u_U(\text{perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{perform}, \text{no_results}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{perform}, \text{no_results}) \\
&\quad + u_U(\text{perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{perform}, \text{no_results}) \\
&= 320 \times x + 320 \times x + 320 \times x \\
&= 320x + 320x + 320x \\
&= 960x \\[1em]
% -------------------
% When T = no_perform, the only relevant result R is 'no results', as indicated by the P(Q | T, R) table.
u'(T = \text{no_perform}, R = \text{no_results}, B = \text{buy}) &= u_U(\text{no_perform}, \text{buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{no_results}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{no_results}) \\
&\quad + u_U(\text{no_perform}, \text{buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{no_results}) \\
&= 1250 \times 0.35 + 630 \times 0.45 + 0 \times 0.2 \\
&= 437.5 + 283.5 + 0 \\
&= 721 \\[1em]
% -------------------
u'(T = \text{no_perform}, R = \text{no_results}, B = \text{no_buy}) &= u_U(\text{no_perform}, \text{no_buy}, \text{high}) P(\text{high} \mid \text{no_perform}, \text{no_results}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{medium}) P(\text{medium} \mid \text{no_perform}, \text{no_results}) \\
&\quad + u_U(\text{no_perform}, \text{no_buy}, \text{low}) P(\text{low} \mid \text{no_perform}, \text{no_results}) \\
&= 350 \times 0.35 + 350 \times 0.45 + 350 \times 0.2 \\
&= 122.5 + 157.5 + 70 \\
&= 350 \\
\end{aligned}
$$

> Note: In reality, we would not need to estimate the not applicable cases, we could put them as "None" and ignore them, even for next cases.

Table X represents the updated version of the utility table once we have removed Q:

<table>
  <tr>
    <th style="text-align: center;"><span style="color: red;">T</span></th>
    <th style="text-align: center;"><span style="color: purple;">R</span></th>
    <th style="text-align: center;"><span style="color: red;">B</span></th>
    <th style="text-align: center;"><span style="color: blue;">U'</span></th>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">Perform test</span></td>
    <td rowspan="2"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">876.387</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">301.593</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1790x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">960x</span></td>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">Do not perform test</span></td>
    <td rowspan="2"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">1050x</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">1050x</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">721</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">350</span></td>
  </tr>
</table>

We can now remove the decision node B since it is a leaf node. Below we can see the resulting influence diagram:


<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_remove_b.png" alt="TODO" width="300">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 1b.</b> TODO.</i>
    </td>
  </tr>
</table>
</center>

By removing B, we need to identify the optimal decision for B in every possible situation. This results in the following utility table:

<table>
  <tr>
    <th style="text-align: center;"><span style="color: red;">T</span></th>
    <th style="text-align: center;"><span style="color: purple;">R</span></th>
    <th style="text-align: center;"><span style="color: red;">$$\delta^*(B)$$</span></th>
    <th style="text-align: center;"><span style="color: blue;">U'</span></th>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">Perform test</span></td>
    <td rowspan="1"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">876.387</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">Do not buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1790x</span></td>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">Do not perform test</span></td>
    <td rowspan="1"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">Buy</span></td>
    <td><span style="color: blue;">721</span></td>
  </tr>
</table>

After removing B, R becomes a leaf node and we can remove via marginalization:

$$
\begin{aligned}
u''(T = \text{perform}) &= U'(T = \text{perform}, R = \text{pass}, B = \text{buy}) P(R = \text{pass} \mid T = \text{perform}) \\
&\quad + U'(T = \text{perform}, R = \text{fail}, B = \text{no_buy}) P(R = \text{fail} \mid T = \text{perform}) \\
&\quad + U'(T = \text{perform}, R = \text{no_results}, B = \text{buy}) P(R = \text{no_results} \mid T = \text{perform}) \\
&= 876.387 \times 0.6775 + 320 \times 0.3225 + 1790x \times 0 \\
&= 593.7388725 + 103.2 + 0 \\
&= 696.9388725 \\[1em]
% -------------------
u''(T = \text{no_perform}) &= U'(T = \text{no_perform}, R = \text{pass}, B = \text{buy}) P(R = \text{pass} \mid T = \text{no_perform}) \\
&\quad + U'(T = \text{no_perform}, R = \text{fail}, B = \text{buy}) P(R = \text{fail} \mid T = \text{no_perform}) \\
&\quad + U'(T = \text{no_perform}, R = \text{no_results}, B = \text{buy}) P(R = \text{no_results} \mid T = \text{no_perform}) \\
&= 1880x \times 0 + 1880x \times 0 + 721 \times 1 \\
&= 0 + 0 + 721 \\
&= 721 \\
\end{aligned}
$$

Table X represents the updated utility table once we have removed R:

<table>
  <thead>
    <tr>
      <th style="text-align:center"><span style="color: red;">T</span></th>
      <th style="text-align:center"><span style="color: blue;">U''</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span style="color: red;">Perform test</span></td>
      <td><span style="color: blue;">696.9388725</span></td>
    </tr>
    <tr>
      <td><span style="color: red;">Do not perform test</span></td>
      <td><span style="color: blue;">721</span></td>
    </tr>
  </tbody>
</table>

Now, the only remaining node is T, which is a decision node and we can remove it by following step 4:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_remove_r.png" alt="TODO" width="200">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 1b.</b> TODO.</i>
    </td>
  </tr>
</table>
</center>

Below is the table with the result of choosing the optimal decision in T. 

<table>
  <thead>
    <tr>
      <th style="text-align:center"><span style="color: red;">$$\delta^*(T)$$</span></th>
      <th style="text-align:center"><span style="color: blue;">U''</span></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span style="color: red;">Do not perform test</span></td>
      <td><span style="color: blue;">721</span></td>
    </tr>
  </tbody>
</table>

Also, Figure X shows the final version of the influence diagram once we have removed T.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/oil_remove_t.png" alt="TODO" width="50">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 1b.</b> TODO.</i>
    </td>
  </tr>
</table>
</center>

Como se puede observar, obtenemos el mismo resultado que con el arbol de decision, es decir, la compañia no deberia realizar el test y deberia comprar el oil field. 

<h2 id="influence-diagram-libraries">Influence Diagram Libraries</h2>

In practice, we do not need to manually perform each step of the arc-reversal or node-reduction algorithm to evaluate an influence diagram. Several open-source libraries automate this entire process and provide sophisticated inference algorithms that handle the computational complexity for us.

<a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> is currently the most widely supported open-source library for influence diagrams. Written in C++ with a Python interface, it implements the Shafer-Shenoy algorithm for LIMIDs. PyAgrum builds a junction tree representation of the influence diagram and uses message passing, alternating between summation (for chance nodes) and maximization (for decision nodes), to efficiently evaluate the diagram.

Other notable libraries include:

* <a href="https://support.bayesfusion.com/docs/"><code>GeNIe/SMILE</code></a>: Implemented in C++, GeNIe is a useful, though somewhat dated, tool for working with Bayesian networks and influence diagrams. SMILE is the underlying engine. Both are free for academic use but are not open-source.

* <a href="https://github.com/causalincentives/pycid"><code>PyCID</code></a>: Written in Python, PyCID is a specialized open-source library designed for working with causal influence diagrams.


<h2>Conclusion</h2>

Este chapter se ha centrado principalmente en como modelizar un problema con un diagram de influencia y como evaluarlo paara calcular la decision optima

Comentar donde seguir aprendiendo mas sobre este tema y aspectos interesantes actuales como que:

es un tema poco explorado, no hemos tocado causalidad (ahi hay mas chicha), relacion con LLMs, variables probabilisticas continuas (poner referencia), etc. 

En el siguiente articulo comentaremos un poco sobre Pyagrum, sensitivity analysis y multiples variables de utilidad (plano de decision, multiples decisiones posibles).

Comentar brevemente las fortalezas y limitaciones de los IDs


<h2 id="references">References</h2>

1. Shenoy, P. P. (2009). <a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Decision trees and influence diagrams</u></a>. Encyclopedia of life support systems, 280-298.

X. Howard, R. A., Matheson, J. E. (1984). <u>Influence diagrams</u>. The Principles and Applications of Decision Analysis (Vol. II), 719-762

Jensen, F., Jensen, F. V., & Dittmer, S. (1994). From influence diagrams to junction trees. In Proceedings of the 10th Conference on Uncertainty in Artificial Intelligence (UAI) (pp. 367-373).

Lauritzen, S. L., & Nilsson, D. (2001). Representing and solving decision problems with limited information. Management Science, 47(9), 1235-1251.

SHAFER, G., AND P. P. SHENOY. 1990. Probability Propagation. Ann. Math. Artif. Intell. 2, 327-352.
* https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content

Shachter, R. D. & Kenley, C. R. (1989). <i>Gaussian influence diagrams</i>. <i>Management Science</i>, 35(5), 527–550.<br>
Bielza, C., Müller, P. & Ríos-Insua, D. (1999). <i>Decision analysis by augmented probability simulation</i>. <i>Management Science</i>, 45(7), 995–1007.<br>
Cobb, B. R. & Shenoy, P. P. (2005). <i>Decision making with hybrid influence diagrams using mixtures of truncated exponentials</i>. In <i>Proc. UAI</i>, 85–93.<br>
Winn, J. & Bishop, C. M. (2005). <i>Variational message passing</i>. <i>Journal of Machine Learning Research</i>, 6, 661–694.</small>
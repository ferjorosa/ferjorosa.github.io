---
layout: post
title: "Introduction to Decision Theory: Part II"
date: 2025-06-14
categories: blog
description: "Explores the strengths and limitations of decision trees, introduces influence diagrams as a scalable alternative, and surveys Python libraries (PyAgrum, PyCID) for practical decision-analysis."
tags: [Decision Theory]
---

<!-- TODO: Añadir nombres de los caminos a las imagenes de los arboles de explosion combinatoria  -->

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
      <img src="/assets/2025-06-14-decision-theory-II/oil_asymmetric_tree_annotated.png" alt="Decision tree diagram of the asymmetric oil problem from Part I" height="200">
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
      <img src="/assets/2025-06-14-decision-theory-II/oil_symmetric_tree_annotated.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="200">
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

To illustrate this, consider a generic problem with four <span style="color:purple;"><b>random variables</b></span>: $$A$$ and $$B$$ (each with two possible states, $$a_1, a_2$$ and $$b_1, b_2$$, respectively), and $$C$$ and $$D$$ (each with three possible states, $$c_1, c_2, c_3$$ and $$d_1, d_2, d_3$$). In a traditional decision tree, where conditional independencies cannot be explicitly represented, you must specify the entire joint probability distribution for all variables. This means assigning a probability to every possible combination of outcomes, as shown in the joint probability table below:

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

This represents a dramatic decrease from the 36 entries required in the full joint probability table. By reducing the number of parameters that must be specified, the model becomes much more manageable, transparent, and easier to modify. As decision problems increase in complexity, the advantages of explicitly modeling conditional independencies grow even more significant.

<h2 id="decision_networks">Decision networks</h2>

Building on the foundation of Bayesian networks, **decision networks** (<a href=""><u>Howard & Matheson, 1984</u></a>), also known as an **influence diagrams** provide a powerful extension that seamlessly integrates decision-making into probabilistic models. Unlike decision trees, decision networks avoid combinatorial explosion by factorizing the joint probability distribution, and they naturally express conditional independencies through their graphical structure. 

A decision network augments a Bayesian network with two extra node types:

* <span style="color:red;"><b>Decision nodes</b></span>: Shown as squares, these indicate points where the decision-maker selects among available actions.
* <span style="color:blue;"><b>Outcome nodes</b></span>: Illustrated as diamonds, these reflect the resulting utilities or values associated with different decision paths.

<span style="color:purple;"><b>Chance nodes</b></span> (circles) are exactly the same as in a Bayesian network and often reuse the same conditional‐probability tables. Arcs into a decision node indicate what information will be available when the choice is made. Arcs into a utility node show which variables affect the final payoff.

<h2> Modelling the Oil Problem with a Decision Network</h2>

<h2> Evaluating the Decision Network </h2>

Decision networks were originally developed as a more compact way to represent decision problems, which were then converted into decision trees for evaluation. Their intuitive structure allowed decision makers to model problems as they understood them, making communication between decision makers and analysts much easier. However, the main drawback was that the decision network still had to be transformed into a different format—a decision tree—in order to be evaluated.

In the 1980s, algorithms were introduced for evaluating decision networks that operated directly on the network itself; see Olmsted (1983) and Shachter (1986). This transformed decision networks into a graphical modeling language that can be used both for decision analysis and probabilistic inference.

The main methods for evaluating decision networks are:

* **Arc Reversal and Node Reduction**: This technique systematically transforms the network by reversing arcs, eliminating chance nodes (by summing them out), and removing decision nodes (by maximizing over them) to determine the optimal expected utility. It was pioneered by Shachter (1986).
* **Variable Elimination**: An extension of variable elimination used in Bayesian networks, this method also incorporates decision and utility nodes. It involves calculating expected utilities and optimizing over decision variables.
* **Junction Tree Methods**: These approaches construct a tree of variable clusters (cliques) and use message passing to propagate information and optimize decisions. Junction tree methods are particularly effective for networks with low treewidth (Jensen et al., 1994).
* **Shenoy-Shafer Method**: An exact belief propagation algorithm that generalizes junction tree techniques. It is used for evidential reasoning and for handling imprecise probabilities in graphical models (Shafer & Shenoy, 1987).
* **Approximation Methods**: For highly complex problems, approximate solutions can be obtained using techniques such as Monte Carlo sampling or variational methods, which rely on tractable families of policies.

<h3 id="computational-complexity">Computational Complexity</h3>

The computational complexity of decision network evaluation depends fundamentally on the network's structural properties:

- **Treewidth**: Networks with low treewidth can be solved in polynomial time, while high treewidth networks may require exponential time.
- **Number of decision nodes**: Each additional decision node can multiply the complexity, though the actual impact depends on the temporal structure.
- **Domain sizes**: Larger state spaces for variables increase both time and space requirements.

In practice, most real-world decision networks have sufficient structure to be solved efficiently, but pathological cases can arise that challenge even the most sophisticated algorithms.


<h2 id="sensitivity_analysis">Sensitivity Analysis</h2>

<!-- <script
	type="module"
	src="https://gradio.s3-us-west-2.amazonaws.com/5.31.0/gradio.js"
></script> -->

<gradio-app src="https://ferjorosa-oil-field-purchase-decision.hf.space"></gradio-app>


<h2>Conclusion</h2>

<!-- Comentar donde seguir aprendiendo mas sobre este tema y aspectos interesantes actuales como que:

es un tema poco explorado, no hemos tocado causalidad (ahi hay mas chicha), relacion con LLMs, variables probabilisticas continuas (poner referencia), etc. -->

<h2 id="references">References</h2>

1. Shenoy, P. P. (2009). <a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Decision trees and influence diagrams</u></a>. Encyclopedia of life support systems, 280-298.

X. Howard, R. A., Matheson, J. E. (1984). <u>Influence diagrams</u>. The Principles and Applications of Decision Analysis (Vol. II), 719-762

Jensen, F., Jensen, F. V., & Dittmer, S. (1994). From influence diagrams to junction trees. In Proceedings of the 10th Conference on Uncertainty in Artificial Intelligence (UAI) (pp. 367-373).


Shachter, R. D. (1986). Evaluating Influence Diagrams. Operations Research, 34(6), 871-882.
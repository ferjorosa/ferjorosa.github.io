---
layout: post
title: "Introduction to Decision Theory: Part II"
date: 2025-06-14
categories: blog
description: "Explores the strengths and limitations of decision trees, introduces influence diagrams as a scalable alternative, and surveys Python libraries (PyAgrum, PyCID) for practical decision-analysis."
tags: [Decision Theory]
---

<h2 id="decision-trees-strengths-limitations">Strenghts and Weaknesses of Decision Trees</h2>

Decision trees provide a straightforward way to model decisions under uncertainty. Each path from start to finish shows a sequence of choices and events that lead to a specific outcome. The left-to-right layout makes the timing of decisions and chance events visually clear, helping to avoid confusion about what is known at each point. 

For small problems with only a few stages, decision trees can be evaluated using basic arithmetic. This simplicity makes them accessible to a wide audience, including those without technical training. They serve as effective tools for teaching, storytelling, and supporting real-world decisions. 

Yet this intuitive structure comes with notable drawbacks. One issue is the risk of combinatorial explosion. Another limitation is that decision trees do not explicitly show conditional independencies. Let's 

<h3 id="combinatorial-explosion">Combinatorial Explosion</h3>
The memory required to store a decision tree and the time required to process it both **increase
exponentially** with the number of variables and their possible states, whether they are decisions or
probabilistic outcomes. In a symmetric problem with $$n$$ variables, each having $$k$$ possible outcomes, you face $$k^{n}$$ distinct paths. Since a decision tree represents all scenarios explicitly, a problem with 50 binary variables would yield an impractical $$2^{50}$$ paths ([Shenoy, 2009](https://pshenoy.ku.edu/Papers/EOLSS09.pdf)).

The number of decision paths is profoundly affected by the order and meaning of the variables (i.e., the problem's definition). In our original oil field investment problem from <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html">Part I</a>, the options to "Not Test" or "Do Not Buy" prune the tree, resulting in 12 distinct decision paths. This is an *asymmetric* problem structure:

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

This **combinatorial explosion** not only affects computational tractability but, even at more modest levels, severely compromises interpretability. As trees grow larger (e.g., once they reach around a hundred terminal nodes), they lose their key strength: easy readability and intuitive understanding.


<h3 id="hidden-independence">Hidden Conditional Independencies</h3>

Decision trees, by their very structure, imply a strict chain of dependence. Every variable in a given branch is implicitly assumed to be conditioned on *all* preceding events on that path. This makes it impossible to represent that two random variables are independent once a third variable is known.

Let's consider an example where we have 4 random variables. Variables $$A$$ and $$B$$ have three states each ($$a_{1}$$, $$a_{2}$$, $$a_{3}$$ and $$b_{1}$$, $$b_{2}$$, $$b_{3}$$), while variables $$C$$ and $$D$$ are binary ($$c_{0}$$, $$c_{1}$$ and $$d_{0}$$, $$d_{1}$$). A decision tree cannot represent conditional independencies and thus we must esplicitly specify the joint probability distribution:

| State of A | State of B | State of C | State of D | Probability     |
|------------|------------|------------|------------|-----------------|
| A1         | B1         | C1         | D1         | P(A1,B1,C1,D1)  |
| A1         | B1         | C1         | D2         | P(A1,B1,C1,D2)  |
| A1         | B1         | C1         | D3         | P(A1,B1,C1,D3)  |
| A1         | B1         | C2         | D1         | P(A1,B1,C2,D1)  |
| A1         | B1         | C2         | D2         | P(A1,B1,C2,D2)  |
| A1         | B1         | C2         | D3         | P(A1,B1,C2,D3)  |
| A1         | B1         | C3         | D1         | P(A1,B1,C3,D1)  |
| A1         | B1         | C3         | D2         | P(A1,B1,C3,D2)  |
| A1         | B1         | C3         | D3         | P(A1,B1,C3,D3)  |
| A1         | B2         | C1         | D1         | P(A1,B2,C1,D1)  |
| A1         | B2         | C1         | D2         | P(A1,B2,C1,D2)  |
| A1         | B2         | C1         | D3         | P(A1,B2,C1,D3)  |
| A1         | B2         | C2         | D1         | P(A1,B2,C2,D1)  |
| A1         | B2         | C2         | D2         | P(A1,B2,C2,D2)  |
| A1         | B2         | C2         | D3         | P(A1,B2,C2,D3)  |
| A1         | B2         | C3         | D1         | P(A1,B2,C3,D1)  |
| A1         | B2         | C3         | D2         | P(A1,B2,C3,D2)  |
| A1         | B2         | C3         | D3         | P(A1,B2,C3,D3)  |
| A2         | B1         | C1         | D1         | P(A2,B1,C1,D1)  |
| A2         | B1         | C1         | D2         | P(A2,B1,C1,D2)  |
| A2         | B1         | C1         | D3         | P(A2,B1,C1,D3)  |
| A2         | B1         | C2         | D1         | P(A2,B1,C2,D1)  |
| A2         | B1         | C2         | D2         | P(A2,B1,C2,D2)  |
| A2         | B1         | C2         | D3         | P(A2,B1,C2,D3)  |
| A2         | B1         | C3         | D1         | P(A2,B1,C3,D1)  |
| A2         | B1         | C3         | D2         | P(A2,B1,C3,D2)  |
| A2         | B1         | C3         | D3         | P(A2,B1,C3,D3)  |
| A2         | B2         | C1         | D1         | P(A2,B2,C1,D1)  |
| A2         | B2         | C1         | D2         | P(A2,B2,C1,D2)  |
| A2         | B2         | C1         | D3         | P(A2,B2,C1,D3)  |
| A2         | B2         | C2         | D1         | P(A2,B2,C2,D1)  |
| A2         | B2         | C2         | D2         | P(A2,B2,C2,D2)  |
| A2         | B2         | C2         | D3         | P(A2,B2,C2,D3)  |
| A2         | B2         | C3         | D1         | P(A2,B2,C3,D1)  |
| A2         | B2         | C3         | D2         | P(A2,B2,C3,D2)  |
| A2         | B2         | C3         | D3         | P(A2,B2,C3,D3)  |


Now, let's say that conditional independies do exist in this problem. For instance, let's say that $$D$$ is conditionally independent of $$A$$ and $$B$$ given $$C$$. In that case:

$$
P(A, B, D \mid C) = P(A,B \mid C) \codt P(D \mid C)
$$

We denote this statement $$ D \bot \{A,B\} \mid C$$. Now, we can represent those conditional independencies with a graph, this is one of the core ideas of Bayesian networks. Figure 3 implies the following conditional independence statements over the set of variables:

* $$ B \bot \{C, D\} \mid A$$
* $$ C \bot B \mid A$$
* $$ D \bot \{A,B\} \mid C$$

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/bayesian_network_example.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> TODO.</i>
    </td>
  </tr>
</table>
</center>

If conditional independencies are present. It does not make sense to have this big of a table, we can use a Bayesian network and decompose the table into smaller ones. With this we go from $2 \times 2 \times 3 \times 3 = 36$ possible outcomes to $2 + 4 + 6 + 9 = 21$.

<table>
  <caption>P(A)</caption>
  <thead>
    <tr>
      <th>State of A</th>
      <th>Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A1</td>
      <td>P(A1)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>P(A2)</td>
    </tr>
  </tbody>
</table>

<table>
  <caption>P(B | A)</caption>
  <thead>
    <tr>
      <th>State of A</th>
      <th>State of B</th>
      <th>Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A1</td>
      <td>B1</td>
      <td>P(B1 | A1)</td>
    </tr>
    <tr>
      <td>A1</td>
      <td>B2</td>
      <td>P(B2 | A1)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>B1</td>
      <td>P(B1 | A2)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>B2</td>
      <td>P(B2 | A2)</td>
    </tr>
  </tbody>
</table>

<table>
  <caption>P(C | A)</caption>
  <thead>
    <tr>
      <th>State of A</th>
      <th>State of C</th>
      <th>Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>A1</td>
      <td>C1</td>
      <td>P(C1 | A1)</td>
    </tr>
    <tr>
      <td>A1</td>
      <td>C2</td>
      <td>P(C2 | A1)</td>
    </tr>
    <tr>
      <td>A1</td>
      <td>C3</td>
      <td>P(C3 | A1)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>C1</td>
      <td>P(C1 | A2)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>C2</td>
      <td>P(C2 | A2)</td>
    </tr>
    <tr>
      <td>A2</td>
      <td>C3</td>
      <td>P(C3 | A2)</td>
    </tr>
  </tbody>
</table>

<table>
  <caption>P(D | C)</caption>
  <thead>
    <tr>
      <th>State of C</th>
      <th>State of D</th>
      <th>Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>C1</td>
      <td>D1</td>
      <td>P(D1 | C1)</td>
    </tr>
    <tr>
      <td>C1</td>
      <td>D2</td>
      <td>P(D2 | C1)</td>
    </tr>
    <tr>
      <td>C1</td>
      <td>D3</td>
      <td>P(D3 | C1)</td>
    </tr>
    <tr>
      <td>C2</td>
      <td>D1</td>
      <td>P(D1 | C2)</td>
    </tr>
    <tr>
      <td>C2</td>
      <td>D2</td>
      <td>P(D2 | C2)</td>
    </tr>
    <tr>
      <td>C2</td>
      <td>D3</td>
      <td>P(D3 | C2)</td>
    </tr>
    <tr>
      <td>C3</td>
      <td>D1</td>
      <td>P(D1 | C3)</td>
    </tr>
    <tr>
      <td>C3</td>
      <td>D2</td>
      <td>P(D2 | C3)</td>
    </tr>
    <tr>
      <td>C3</td>
      <td>D3</td>
      <td>P(D3 | C3)</td>
    </tr>
  </tbody>
</table>

<!-- However, you *dont need* to have those values written in the table because since they are independent you know their value is simply the multiplication of P(A) * P(B)-->

<h2 id="references">References</h2>

1. Shenoy, P. P. (2009). <a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Decision trees and influence diagrams</u></a>. Encyclopedia of life support systems, 280-298.
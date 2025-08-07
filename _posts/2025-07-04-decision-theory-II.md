---
layout: post
title: "Introduction to Decision Theory: Part II"
date: 2025-07-04
categories: blog
description: "Explores the strengths and limitations of decision trees, introduces influence diagrams as a scalable alternative, details their evaluation using the arc-reversal / node-reduction algorithm, and surveys Python libraries (PyAgrum, PyCID) for practical decision analysis."
tags: [Decision Theory]
---

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">Table of Contents</summary>

<ul style="margin-top: 0.5em;">
  <li style="margin-bottom: 0.5em;"><a href="#decision-trees-strengths-limitations">Strengths and Limitations of Decision Trees</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#combinatorial-explosion">Combinatorial Explosion</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#hidden-independence">Hidden Conditional Independencies</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#decision_networks">Influence Diagrams</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#modelling_oil_problem">Modelling the Oil Field Decision Problem</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#modelling_oil_problem_qualitative">Modelling Qualitative Information</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#modelling_oil_problem_quantitative">Modelling Quantitative Information</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#evaluating_influence_diagram">Influence Diagram Evaluation</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#local-graph-operations">Four Local Graph Operations</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#node-reduction-algorithm">The Arc-Reversal / Node-Reduction Algorithm</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#relationship-to-bayesian-network-elimination">Relationship to Bayesian Network Variable Elimination</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#related-work-evaluation">Related Work</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#evaluating-oil-influence-diagram">Evaluating the Oil Influence Diagram</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#influence-diagram-libraries">Influence Diagram Libraries</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#conclusion">Conclusion</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#references">References</a></li>
</ul>

</details>

<h2 id="decision-trees-strengths-limitations">Strengths and Limitations of Decision Trees</h2>

Decision trees provide a straightforward way to model decisions under uncertainty. Each path from start to finish shows a sequence of choices and events that lead to a specific outcome. The directed layout makes the timing of decisions and chance events visually clear, helping to avoid confusion about what is known at each point. 

For small problems with only a few stages, decision trees can be evaluated using basic arithmetic. This simplicity makes them accessible to a wide audience, including those without technical training. They serve as effective tools for teaching, storytelling, and supporting real-world decisions. 

Yet this intuitive structure comes with notable drawbacks. One issue is the risk of combinatorial explosion. Another limitation is that decision trees do not explicitly show conditional independencies.

<h3 id="combinatorial-explosion">Combinatorial Explosion</h3>
The memory required to store a decision tree and the time required to process it both **increase
exponentially** with the number of variables and their possible states, whether they are decisions or
probabilistic outcomes. In a symmetric problem with $$n$$ variables, each having $$k$$ possible outcomes, you face $$k^{n}$$ distinct paths. Since a decision tree represents all scenarios explicitly, a problem with 50 binary variables would yield an impractical $$2^{50}$$ paths (<a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Shenoy, 2009</u></a>).

The number of decision paths is profoundly affected by the order and meaning of the variables (i.e., the problem's definition). In our original oil field decision problem from <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html"><u>Part I</u></a>, the options <span style="color:red;">Do not perform test</span> and <span style="color:red;">Do not buy</span> prune the tree, resulting in 12 distinct decision paths. This is an *asymmetric* problem structure:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/1_oil_asymmetric_tree_annotated.png" alt="Decision tree diagram of the asymmetric oil problem from Part I" height="240">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Decision tree diagram of the asymmetric oil field investment problem from Part I.</i>
    </td>
  </tr>
</table>
</center>

Conversely, a problem with the same types of variables, but structured *symmetrically*, would yield significantly more paths. For example, suppose the company must always begin by performing one of two possible geological tests (such as <span style="color:red;">Test X</span> or <span style="color:red;">Test Y</span>, each with different costs and accuracy profiles) on the field. Based on the test result, the company then chooses whether to <span style="color:red;">Invest in Field A</span> or <span style="color:red;">Invest in Field B</span>. After the investment decision, drilling reveals the field's quality. This structure forces every path to be fully explored, doubling the number of distinct paths from 12 to 24:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/2_oil_symmetric_tree_annotated.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="240">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 2.</b> Decision tree diagram of a hypothetical symmetric oil field investment problem.</i>
    </td>
  </tr>
</table>
</center>

Even this revised example demonstrates how swiftly a decision tree can escalate beyond practical use. For instance, merely replacing the three-level oil quality (<span style="color:purple;">high</span>/<span style="color:purple;">medium</span>/<span style="color:purple;">low</span>) with a more granular five-level scale (<span style="color:purple;">excellent</span>/<span style="color:purple;">good</span>/<span style="color:purple;">average</span>/<span style="color:purple;">poor</span>/<span style="color:purple;">dry</span>) would push the total from 24 to 40 terminal nodes. This occurs without even considering longer time horizons, dynamic market-price scenarios, or additional complex choices.

This **combinatorial explosion** not only affects computational tractability but, even at more modest levels, severely compromises interpretability. As a rule of thumb, once a tree approaches about 100 terminal nodes, it loses its key strength: easy readability and intuitive understanding.


<h3 id="hidden-independence">Hidden Conditional Independencies</h3>


In addition to the issue of combinatorial explosion, decision trees have another important limitation: they assume a strict, linear chain of dependence. In a decision tree, every variable is implicitly conditioned on **all** previous events along its particular path. This rigid structure prevents us from explicitly representing one of the most important concepts in probabilistic modeling: <b><a href="https://en.wikipedia.org/wiki/Conditional_independence"><u>conditional independence</u></a></b>.

To illustrate this, consider a generic problem with four random variables: $$\textcolor{purple}{A}$$ and $$\textcolor{purple}{B}$$ (each with two possible states, $$\textcolor{purple}{a_1}, \textcolor{purple}{a_2}$$ and $$\textcolor{purple}{b_1}, \textcolor{purple}{b_2}$$, respectively), and $$\textcolor{purple}{C}$$ and $$\textcolor{purple}{D}$$ (each with three possible states, $$\textcolor{purple}{c_1}, \textcolor{purple}{c_2}, \textcolor{purple}{c_3}$$ and $$\textcolor{purple}{d_1}, \textcolor{purple}{d_2}, \textcolor{purple}{d_3}$$). In a traditional decision tree, where conditional independencies cannot be explicitly represented, you must specify the entire joint probability distribution for all variables. This means assigning a probability to every possible combination of outcomes, as shown in the joint probability table below:

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">A</span>, <span style="color:purple;">B</span>, <span style="color:purple;">C</span>, <span style="color:purple;">D</span>)</summary>


<table>
  <thead>
    <tr>
      <th>$$\textcolor{purple}{A}$$</th>
      <th>$$\textcolor{purple}{B}$$</th>
      <th>$$\textcolor{purple}{C}$$</th>
      <th>$$\textcolor{purple}{D}$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{1}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{1}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{2}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}},\textcolor{purple}{b_{2}},\textcolor{purple}{c_{3}},\textcolor{purple}{d_{3}})$$</td>
    </tr>
  </tbody>
</table>

</details>

**Total distinct probabilities:** $$ 2 \; (\text{for } \textcolor{purple}{A}) \cdot 2 \; (\text{for } \textcolor{purple}{B}) \cdot 3 \; (\text{for } \textcolor{purple}{C}) \cdot 3 \; (\text{for } \textcolor{purple}{D}) = \mathbf{36} $$.

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
  This example demonstrates conditional independencies using a simplified version of a decision tree, where all nodes are probabilistic (often called a <a href="https://en.wikipedia.org/wiki/Tree_diagram_(probability_theory)"><u>probability tree</u></a>). However, the core concepts and benefits of explicit conditional independence representation apply equally to the chance nodes of any general decision tree.
</div>
<div style="height: 1.1em;"></div>

Now, let's say that conditional independencies do exist in this problem. For instance, let's say that $$\textcolor{purple}{B}$$ is conditionally independent of $$\textcolor{purple}{C}$$ and $$\textcolor{purple}{D}$$ given $$\textcolor{purple}{A}$$. We denote that statement by $$(\textcolor{purple}{B} \bot \{\textcolor{purple}{C}, \textcolor{purple}{D}\} \mid \textcolor{purple}{A})$$. In that case:

$$
P(\textcolor{purple}{B} \mid \textcolor{purple}{A}, \textcolor{purple}{C}, \textcolor{purple}{D}) = P(\textcolor{purple}{B} \mid \textcolor{purple}{A})
$$

This fundamental concept allows us to represent relationships far more efficiently. Consider Figure 3, which implies the following conditional independence statements:
* &nbsp;$$ (\textcolor{purple}{B} \bot \{\textcolor{purple}{C}, \textcolor{purple}{D}\} \mid \textcolor{purple}{A})$$
* &nbsp;$$ (\textcolor{purple}{C} \bot \textcolor{purple}{B} \mid \textcolor{purple}{A})$$
* &nbsp;$$ (\textcolor{purple}{D} \bot \{\textcolor{purple}{A},\textcolor{purple}{B}\} \mid \textcolor{purple}{C})$$

The diagram corresponds to the directed acyclic graph of a <a href="https://en.wikipedia.org/wiki/Bayesian_network"><u>Bayesian network</u></a>, which visually encodes these independencies: arrows indicate direct probabilistic influence, while the absence of an arrow between two nodes reflects a conditional independence given their parents.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/3_bayesian_network_example.png" alt="Decision tree diagram of a hypothetical symmetric oil problem" height="300">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> Bayesian network illustrating conditional independencies among A, B, C, and D.</i>
    </td>
  </tr>
</table>
</center>

When these conditional independencies are recognized and modeled, we no longer need to construct a single large joint probability table. Instead, the full joint probability distribution can be factored into a product of smaller, more manageable conditional probability tables (CPTs). In our example, this means we only need to specify:

* &nbsp;$$ P(\textcolor{purple}{A}) \rightarrow 2 = 2 $$ entries
* &nbsp;$$ P(\textcolor{purple}{B} \mid \textcolor{purple}{A}) \rightarrow 2 \cdot 2 = 4 $$ entries  
* &nbsp;$$ P(\textcolor{purple}{C} \mid \textcolor{purple}{A}) \rightarrow 2 \cdot 3 = 6 $$ entries
* &nbsp;$$ P(\textcolor{purple}{D} \mid \textcolor{purple}{C}) \rightarrow 3 \cdot 3 = 9 $$ entries

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">A</span>)</summary>

<table>
  <thead>
    <tr>
      <th>$$\textcolor{purple}{A}$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$P(\textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$P(\textcolor{purple}{a_{2}})$$</td>
    </tr>
  </tbody>
</table>

</details>


<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">B</span> | <span style="color:purple;">A</span>)</summary>

<table>
  <thead>
    <tr>
      <th>$$\textcolor{purple}{A}$$</th>
      <th>$$\textcolor{purple}{B}$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$P(\textcolor{purple}{b_{1}} \mid \textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$P(\textcolor{purple}{b_{2}} \mid \textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{1}}$$</td>
      <td>$$P(\textcolor{purple}{b_{1}} \mid \textcolor{purple}{a_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{b_{2}}$$</td>
      <td>$$P(\textcolor{purple}{b_{2}} \mid \textcolor{purple}{a_{2}})$$</td>
    </tr>
  </tbody>
</table>

</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">C</span> | <span style="color:purple;">A</span>)</summary>

<table>
  <thead>
    <tr>
      <th>$$\textcolor{purple}{A}$$</th>
      <th>$$\textcolor{purple}{C}$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$P(\textcolor{purple}{c_{1}} \mid \textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$P(\textcolor{purple}{c_{2}} \mid \textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{1}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$P(\textcolor{purple}{c_{3}} \mid \textcolor{purple}{a_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$P(\textcolor{purple}{c_{1}} \mid \textcolor{purple}{a_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$P(\textcolor{purple}{c_{2}} \mid \textcolor{purple}{a_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{a_{2}}$$</td>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$P(\textcolor{purple}{c_{3}} \mid \textcolor{purple}{a_{2}})$$</td>
    </tr>
  </tbody>
</table>

</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">

<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">D</span> | <span style="color:purple;">C</span>)</summary>

<table>
  <thead>
    <tr>
      <th>$$\textcolor{purple}{C}$$</th>
      <th>$$\textcolor{purple}{D}$$</th>
      <th style="text-align: center;">Probability</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{d_{1}} \mid \textcolor{purple}{c_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{d_{2}} \mid \textcolor{purple}{c_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{1}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{d_{3}} \mid \textcolor{purple}{c_{1}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{d_{1}} \mid \textcolor{purple}{c_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{d_{2}} \mid \textcolor{purple}{c_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{2}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{d_{3}} \mid \textcolor{purple}{c_{2}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{1}}$$</td>
      <td>$$P(\textcolor{purple}{d_{1}} \mid \textcolor{purple}{c_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{2}}$$</td>
      <td>$$P(\textcolor{purple}{d_{2}} \mid \textcolor{purple}{c_{3}})$$</td>
    </tr>
    <tr>
      <td>$$\textcolor{purple}{c_{3}}$$</td>
      <td>$$\textcolor{purple}{d_{3}}$$</td>
      <td>$$P(\textcolor{purple}{d_{3}} \mid \textcolor{purple}{c_{3}})$$</td>
    </tr>
  </tbody>
</table>

</details>

**Total distinct probabilities:** $$2 + 4 + 6 + 9 = \mathbf{21}$$.

This represents a **42% decrease** from the 36 entries required in the full joint probability table. By reducing the number of parameters that must be specified, the model becomes much more manageable, transparent, and easier to modify. As decision problems increase in complexity, the advantages of explicitly modeling conditional independencies grow even more significant.

<h2 id="decision_networks">Influence Diagrams</h2>

Building on the foundation of Bayesian networks, **influence diagrams** (<a href=""><u>Howard & Matheson, 1984</u></a>), also known as **decision networks**, provide a powerful extension that seamlessly integrates decision-making into probabilistic models. Unlike decision trees, influence diagrams avoid combinatorial explosion by factorizing the joint probability distribution and naturally express conditional independencies through their graphical structure.

An influence diagram enhances a Bayesian network by adding two types of nodes:

* <span style="color:red;"><b>Decision nodes</b></span>: Shown as squares, these represent points where the decision-maker chooses among available actions.
* <span style="color:blue;"><b>Outcome nodes</b></span>: Illustrated as diamonds, these indicate the resulting utilities or values associated with different decision paths.

<span style="color:purple;"><b>Chance nodes</b></span> (circles) function as in Bayesian networks; when they are categorical, they are described by CPTs. 

In influence diagrams, arcs serve two main purposes: **informational arcs** (into decision nodes) indicate what information is available when a choice is made, while **conditional arcs** (into chance or utility nodes) represent probabilistic or functional dependencies on parent variables, showing which factors affect outcomes or payoffs, without implying causality or temporal order.


<h2 id="modelling_oil_problem">Modelling the Oil Field Decision Problem</h2>

Modeling takes place at multiple levels. Drawing the influence diagram, much like constructing a decision tree, represents the qualitative description of the problem (structural level). Next, quantitative information is incorporated (numerical level) to fully specify the model.

A key limitation of influence diagrams is that **they are only designed to handle symmetric problems**. When faced with an asymmetric problem, it is necessary to transform it into a symmetric one, typically by introducing *artificial* states (which may be unintuitive). This transformation increases the size and complexity of the model, resulting in greater computational demands.

In large and highly asymmetric problems, using these resources (artificial states, degenerate probabilities, and utilities) to convert them into an equivalent symmetric one is not straightforward. For more information on this topic, see <a href="https://cig.fi.upm.es/wp-content/uploads/2024/01/A-Comparison-of-Graphical-Techniques-for-Asymmetric-Decision-Problems.pdf"><u>Bielza & Shenoy (1999)</u></a>.

To model the oil field decision problem, we will use a standard influence diagram. To maintain problem symmetry, an extra state called <span style="color:purple;">no results</span> should be added to the porosity test results variable (<span style="color:purple;"><b>R</b></span>), since results are only observed when the test is performed.

<h3 id="modelling_oil_problem_qualitative">Modelling Qualitative Information</h3>

The following image displays the influence diagram structure for the decision problem:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/4_influence_diagram_oil.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 4.</b> Influence diagram for the oil field decision problem. Informational arcs are displayed with dashes.</i>
    </td>
  </tr>
</table>
</center>

This diagram illustrates a traditional influence diagram, which operates under the assumption of perfect recall. The information arcs indicate that the Test / No Test ($$\textcolor{red}{T}$$) decision is made prior to the Buy / No Buy ($$\textcolor{red}{B}$$) decision. Furthermore, no information is available before making the test decision, and the test results ($$\textcolor{purple}{R}$$) are known when making the buy decision. This establishes the temporal sequence of variables: $$\textcolor{red}{T}$$, $$\textcolor{purple}{R}$$, $$\textcolor{red}{B}$$, and finally $$\textcolor{purple}{Q}$$ (oil field quality).

However, traditional influence diagrams can become computationally complex to solve, particularly for intricate problems, and they may not accurately reflect the realistic limitations of human decision-making. For these reasons, LIMIDs (<a href="https://web.math.ku.dk/~lauritzen/papers/limids.pdf"><u>Lauritzen & Nilsson, 2001</u></a>) are often the preferred choice. These models relax the perfect recall assumption and allow for explicit representation of limited memory. Memory arcs in LIMIDs explicitly specify which past decisions and observations are remembered and used for each current decision.

The subsequent image presents the corresponding LIMID, enhanced with a green memory arc. This memory arc extends from $$\textcolor{red}{T}$$ to $$\textcolor{red}{B}$$ because the outcome of the porosity test decision is crucial for the subsequent decision on buying or not buying the field.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/5_limid_oil.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 5.</b> LIMID for the oil field decision problem with a memory arc shown in green.</i>
    </td>
  </tr>
</table>
</center>

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
For this problem, we will utilize the LIMID version of the oil decision problem.
</div>
<div style="height: 1.1em;"></div>

<h3 id="modelling_oil_problem_quantitative">Modelling Quantitative Information</h3>

Since all our random variables are categorical, we can conveniently represent the quantitative information of the model in tabular form. Below, we specify the prior probabilities, the CPTs, and the utility values relevant to the oil field decision problem.

Prior probabilities for the oil field quality ($$\textcolor{purple}{Q}$$):

<table>
  <tr>
    <th colspan="2" style="text-align: center;">$$P(\textcolor{purple}{Q})$$</th>
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

Conditional probabilities of observing each possible test result $$\textcolor{purple}{R}$$, given the true oil field quality $$\textcolor{purple}{Q}$$ and whether the test was performed $$\textcolor{red}{T}$$:

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{R} \mid \textcolor{purple}{Q},\, \textcolor{red}{T})$$</th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">perform</span></th>
    <th colspan="3" style="text-align: center;"><span style="color: red;">no perform</span></th>
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
    <th style="text-align: center;">$$\textcolor{red}{T}$$</th>
    <th style="text-align: center;">$$\textcolor{red}{B}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{Q}$$</th>
    <th style="text-align: center;">$$\textcolor{blue}{U}$$</th>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">perform</span></td>
    <td rowspan="3"><span style="color: red;">buy</span></td>
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
    <td rowspan="3"><span style="color: red;">no buy</span></td>
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
    <td rowspan="6"><span style="color: red;">no perform</span></td>
    <td rowspan="3"><span style="color: red;">buy</span></td>
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
    <td rowspan="3"><span style="color: red;">no buy</span></td>
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

Influence diagrams were conceived as a compact, intuitive way to describe decision problems, yet practitioners initially had to transform them into a different format (i.e., a decision tree) in order to evaluate them. Until the 1980s, when <a href="http://www.cis.umassd.edu/~x2zhang/courses/CIS561/readings/EvaluatingID.pdf"><u>Shachter (1986)</u></a> showed how to evaluate the network directly, turning the diagram into a self-contained modelling and inference language.

Shachter's **arc-reversal / node-reduction algorithm** reverses arcs and sequentially eliminates variables, summing over chance nodes and maximising over decision nodes while pushing expected-utility information forward.

<h3 id="local-graph-operations">Four Local Graph Operations</h3>

The arc-reversal / node-reduction algorithm employs a set of fundamental, local graph operations. Each operation ensures that the decision problem remains *semantically equivalent*, meaning the attainable utilities under any strategy are preserved:

1. **Barren-Node Deletion:**
    Any chance or decision node that has no children and is not a parent of an outcome node can be immediately removed from the diagram. Such nodes do not affect the utility and are therefore irrelevant to the decision problem.

    Figure 6 illustrates the process of barren node elimination. The first diagram becomes the second, and then the third, since removing a barren node can create new barren nodes that can also be eliminated.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-07-04-decision-theory-II/6_barren_node_elimination.png" alt="Barren node elimination example" height="400">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure 6.</b> Barren node elimination example.</i>
        </td>
      </tr>
    </table>
    </center> 

2. **Chance-Node Removal:**
    Once a chance node $$\textcolor{purple}{C}$$ becomes a leaf (i.e., **it has no children except outcome nodes**), it can be eliminated via marginalization (taking an expectation). For every outcome node $$\textcolor{blue}{O}$$ that has $$\textcolor{purple}{C}$$ as a parent, a new utility table, $$u'_{\textcolor{blue}{O}}$$, is computed. This new table will depend on the original parents of $$\textcolor{blue}{O}$$ (excluding $$\textcolor{purple}{C}$$) and all the parents of $$\textcolor{purple}{C}$$.

    $$
    u'_{\textcolor{blue}{O}}\left(\mathbf{\text{Pa}}_{\textcolor{blue}{O}} \cup \mathbf{\text{Pa}}_{\textcolor{purple}{C}} \setminus \{\textcolor{purple}{C}\}\right) = \sum_{\textcolor{purple}{c}} u_{\textcolor{blue}{O}}(\mathbf{\text{Pa}}_{\textcolor{blue}{O}}) \; P(\textcolor{purple}{c} \mid \mathbf{\text{Pa}}_{\textcolor{purple}{C}})
    $$

    Here:
    *   $$\mathbf{\text{Pa}}_{\textcolor{blue}{O}}$$ denotes the set of parents of $$\textcolor{blue}{O}$$ in the diagram *before* removing $$\textcolor{purple}{C}$$.
    *   $$\mathbf{\text{Pa}}_{\textcolor{purple}{C}}$$ denotes the set of parents of $$\textcolor{purple}{C}$$.
    *   $$u'_{\textcolor{blue}{O}}$$ represents the *new* utility table for node $$\textcolor{blue}{O}$$.

    <br>
    Node $$\textcolor{purple}{C}$$ and its CPT are then deleted. This operation "pushes expected utility forward" by embedding the influence of $$\textcolor{purple}{C}$$ into the successor utility tables. The outcome node $$\textcolor{blue}{O}$$ effectively inherits the predecessors of $$\textcolor{purple}{C}$$, ensuring that all relevant dependencies are preserved.

    Figure 7 showcases the process of chance node removal, specifically $$\textcolor{purple}{C_2}$$. The first diagram becomes the second, where parents of $$\textcolor{purple}{C_{2}}$$ become the parents of $$\textcolor{blue}{O_1}$$.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-07-04-decision-theory-II/7_chance_node_removal.png" alt="Chance node removal example" height="150">
        </td>
      </tr>
      <tr>
        <td colspan="2" align="center">
          <i><b>Figure 7.</b> Chance node removal example.</i>
        </td>
      </tr>
    </table>
    </center> 

3. **Decision-Node Removal:**
    When a decision node $$\textcolor{red}{D}$$ becomes a leaf in the influence diagram, meaning its only children are outcome nodes $$\textcolor{blue}{O}$$, it can be eliminated. This step requires identifying the optimal decision for $$\textcolor{red}{D}$$ in every possible situation, or "information state", defined by the specific combination of observed values of $$\textcolor{red}{D}$$'s parent nodes.

    For each information state $$i$$, we choose the action $$\textcolor{red}{d}$$ that maximizes the expected utility $$\mathbb{E}[u(\textcolor{red}{d}, i)]$$. This action represents the best possible choice for that information state and forms part of the overall optimal policy:

    $$
    \delta^*(i) = \text{argmax}_{\textcolor{red}{d}} \ \mathbb{E}[u(\textcolor{red}{d}, i)]
    $$

    The function $$\delta^*(i)$$ is recorded as the optimal decision rule for node $$\textcolor{red}{D}$$ in information state $$i$$. After removing $$\textcolor{red}{D}$$, each outcome node $$\textcolor{blue}{O}$$ that was a child of $$\textcolor{red}{D}$$ has its utility table updated to reflect the maximum expected utility (MEU) achievable by making the optimal decision at $$\textcolor{red}{D}$$, given the information state $$i$$.

    This process "locks in" the optimal strategy for $$\textcolor{red}{D}$$ and propagates the MEU forward through the diagram, similar to how chance nodes $$\textcolor{purple}{C}$$ are eliminated by marginalization.

    Figure 8 demonstrates the process of eliminating a decision node, specifically $$\textcolor{red}{D_2}$$. In the first diagram, the decision node is present; in the second, it has been removed, and the utility table has been updated to incorporate the optimal decision rule $$\delta^*(\textcolor{red}{D_2})$$ for each information state (i.e., each combination of parent values). Only the maximum attainable utilities for each state are preserved.

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-07-04-decision-theory-II/8_decision_node_removal.png" alt="Decision node removal example" width="600">
        </td>
      </tr>
              <tr>
          <td colspan="2" align="center">
            <i><b>Figure 8.</b> Decision node removal example.</i>
          </td>
        </tr>
    </table>
    </center>     

4. **Arc Reversal (between chance nodes):**
    In most influence diagrams, nodes are not naturally leaves. They may have children that prevent us from eliminating them directly. To solve this, we use arc reversal to make a target node into a leaf by pushing its influence "backwards" to its children and adjusting the rest of the diagram so that it still represents the same probabilistic relationships.

    Let's say we want to reverse an arc $$\textcolor{purple}{X} \rightarrow \textcolor{purple}{Y}$$ where $$\mathbf{\text{Pa}}_{\textcolor{purple}{X}}$$ is the set of parents of $$\textcolor{purple}{X}$$ and $$\mathbf{\text{Pa}}_{\textcolor{purple}{Y}}$$ is the parents of $$\textcolor{purple}{Y}$$, including $$\textcolor{purple}{X}$$ itself.

    To reverse, we remove the arc $$\textcolor{purple}{X} \rightarrow \textcolor{purple}{Y}$$, add a new arc $$\textcolor{purple}{Y} \rightarrow \textcolor{purple}{X}$$, add arcs from $$\mathbf{\text{Pa}}_{\textcolor{purple}{X}}$$ to $$\textcolor{purple}{Y}$$ if they are not already parents of $$\textcolor{purple}{Y}$$, and add arcs from $$\mathbf{\text{Pa}}_{\textcolor{purple}{Y}}$$ to $$\textcolor{purple}{X}$$, if needed, to preserve dependencies. This means the new parents of $$\textcolor{purple}{X}$$ and $$\textcolor{purple}{Y}$$ are:

    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{Y}} = \mathbf{\text{Pa}}_{\textcolor{purple}{X}} \cup \mathbf{\text{Pa}}_{\textcolor{purple}{Y}}  \setminus \{\textcolor{purple}{Y}\}$$
    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{X}} = \mathbf{\text{Pa}}_{\textcolor{purple}{X}} \cup \mathbf{\text{Pa}}_{\textcolor{purple}{Y}}  \cup \{\textcolor{purple}{Y}\} \setminus \{\textcolor{purple}{X}\}$$
    
    <br>
    To ensure the joint distribution remains unchanged under the new structure, we compute the new CPT using Bayes' Theorem:
    
    $$
    \begin{aligned}
    P(\textcolor{purple}{Y} \mid \mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{Y}}) 
    &= \sum_{\textcolor{purple}{X}} P(\textcolor{purple}{Y} \mid \mathbf{\text{Pa}}_{\textcolor{purple}{Y}}) \cdot P(\textcolor{purple}{X} \mid \mathbf{\text{Pa}}_{\textcolor{purple}{X}}) \\ \\
    
    P(\textcolor{purple}{X} \mid \mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{X}}) 
    &= \frac{P(\textcolor{purple}{Y} \mid \mathbf{\text{Pa}}_{\textcolor{purple}{Y}}) \cdot P(\textcolor{purple}{X} \mid \mathbf{\text{Pa}}_{\textcolor{purple}{X}})}{P(\textcolor{purple}{Y} \mid \mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{Y}})}
    \end{aligned}
    $$

    As an example, consider the influence diagram shown in Figure 9, which contains three chance nodes. We will reverse the arc $$\textcolor{purple}{C_2} \rightarrow \textcolor{purple}{C_3}$$. Before reversal, the parent sets are:
    
    * &nbsp;$$\mathbf{\text{Pa}}_{\textcolor{purple}{C_2}} = \{\textcolor{purple}{C_1}\}$$
    * &nbsp;$$\mathbf{\text{Pa}}_{\textcolor{purple}{C_3}} = \{\textcolor{purple}{C_2}\}$$

    <div style="height: 1.1em;"></div>

    After reversal, the new parent sets become:

    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{C_2}} = \{\textcolor{purple}{C_1}, \textcolor{purple}{C_3}\}$$
    * &nbsp;$$\mathbf{\text{Pa}}^{\text{new}}_{\textcolor{purple}{C_3}} = \{\textcolor{purple}{C_1}\}$$

    <div style="height: 1.1em;"></div>

    <center>
    <table>
      <tr>
        <td align="center">
          <img src="/assets/2025-07-04-decision-theory-II/9_arc_reversal.png" alt="Decision node removal example" width="600">
        </td>
      </tr>
              <tr>
          <td colspan="2" align="center">
            <i><b>Figure 9.</b> Arc reversal example.</i>
          </td>
        </tr>
    </table>
    </center>  

    We are given the following initial CPTs:

    <table>
      <thead>
        <tr>
          <th colspan="2" style="text-align:center">$$P(\textcolor{purple}{C_1})$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$\textcolor{purple}{c_{1,1}}$$</td><td>0.7</td></tr>
        <tr><td>$$\textcolor{purple}{c_{1,2}}$$</td><td>0.3</td></tr>
      </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th>$$P(\textcolor{purple}{C_2} \mid \textcolor{purple}{C_1})$$</th><th>$$\textcolor{purple}{c_{1,1}}$$</th><th>$$\textcolor{purple}{c_{1,2}}$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$\textcolor{purple}{c_{2,1}}$$</td><td>0.6</td><td>0.1</td></tr>
        <tr><td>$$\textcolor{purple}{c_{2,2}}$$</td><td>0.4</td><td>0.9</td></tr>
      </tbody>
    </table>

    <table>
      <thead>
        <tr>
          <th>$$P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_2})$$</th><th>$$\textcolor{purple}{c_{2,1}}$$</th><th>$$\textcolor{purple}{c_{2,2}}$$</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>$$\textcolor{purple}{c_{3,1}}$$</td><td>0.9</td><td>0.2</td></tr>
        <tr><td>$$\textcolor{purple}{c_{3,2}}$$</td><td>0.1</td><td>0.8</td></tr>
      </tbody>
    </table>
    
    <!-- To compute the new CPT for $$C_3$$ we have to marginalize $$C_2$$: -->

    **Step 1: Compute new CPT for $$P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_1})$$**

    Using marginalization:

    $$
    P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_1}) = \sum_{\textcolor{purple}{c_2}} P(\textcolor{purple}{C_3} \mid \textcolor{purple}{c_2}) P(\textcolor{purple}{c_2} \mid \textcolor{purple}{C_1}).
    $$

    $$\textcolor{purple}{c_{1,1}}$$:
    

    $$
    \begin{aligned}
    P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,1}}) &= P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,2}})P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,1}}) + P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,1}})P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}}) \\
                        &= 0.2 \cdot 0.4 + 0.9 \cdot 0.6 \\
                        &= 0.08 + 0.54 = 0.62 \\
    P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{1,1}}) &= 1 - P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,1}}) = 1 - 0.62 = 0.38
    \end{aligned}
    $$

    $$\textcolor{purple}{c_{1,2}}$$:
    
    $$
    \begin{aligned}
    P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,2}}) &= P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,2}})P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,2}}) + P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,1}})P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}}) \\
                        &= 0.2 \cdot 0.9 + 0.9 \cdot 0.1 \\
                        &= 0.18 + 0.09 = 0.27 \\
    P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{1,2}}) &= 1 - P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,2}}) = 1 - 0.27 = 0.73
    \end{aligned}
    $$

    Summarized as:

    <table>
      <thead>
        <tr><th>$$P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_1})$$</th><th>$$\textcolor{purple}{c_{1,1}}$$</th><th>$$\textcolor{purple}{c_{1,2}}$$</th></tr>
      </thead>
      <tbody>
        <tr><td>$$\textcolor{purple}{c_{3,1}}$$</td><td>0.62</td><td>0.27</td></tr>
        <tr><td>$$\textcolor{purple}{c_{3,2}}$$</td><td>0.38</td><td>0.73</td></tr>
      </tbody>
    </table>

    **Step 2: Compute new CPT for $$P(\textcolor{purple}{C_2} \mid \textcolor{purple}{C_1}, \textcolor{purple}{C_3})$$**

    Using Bayes' Theorem, rounding results to three decimal places:

    $$
    P(\textcolor{purple}{C_2} \mid \textcolor{purple}{C_1}, \textcolor{purple}{C_3}) = \frac{P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_2}) \, P(\textcolor{purple}{C_2} \mid \textcolor{purple}{C_1})}{P(\textcolor{purple}{C_3} \mid \textcolor{purple}{C_1})}.
    $$

    ($$\textcolor{purple}{c_{1,1}}$$, $$\textcolor{purple}{c_{3,1}}$$):

    $$
    \begin{aligned}
    &\quad P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,1}}) = \frac{P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,1}}) \, P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}})}{P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,1}})} = \frac{0.9 \cdot 0.6}{0.62} = 0.871 \\
    &\quad P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,1}}) = 1 - P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,1}}) = 1 - 0.871 = 0.129
    \end{aligned}
    $$

    ($$\textcolor{purple}{c_{1,2}}$$, $$\textcolor{purple}{c_{3,1}}$$):

    $$
    \begin{aligned}
    &\quad P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,1}}) = \frac{P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{2,1}}) \, P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}})}{P(\textcolor{purple}{c_{3,1}} \mid \textcolor{purple}{c_{1,2}})} = \frac{0.9 \cdot 0.1}{0.27} = 0.333 \\
    &\quad P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,1}}) = 1 - P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,1}}) = 1 - 0.333 = 0.667 \\[3ex]
    \end{aligned}
    $$

    ($$\textcolor{purple}{c_{1,1}}$$, $$\textcolor{purple}{c_{3,2}}$$):

    $$
    \begin{aligned}
    &\quad P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,2}}) = \frac{P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{2,1}}) \, P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}})}{P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{1,1}})} = \frac{0.1 \cdot 0.6}{0.38} = 0.158 \\
    &\quad P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,2}}) = 1 - P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,1}}, \textcolor{purple}{c_{3,2}}) = 1 - 0.158 = 0.842 \\[3ex]
    \end{aligned}
    $$

    ($$\textcolor{purple}{c_{1,2}}$$, $$\textcolor{purple}{c_{3,2}}$$):

    $$
    \begin{aligned}
    &\quad P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,2}}) = \frac{P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{2,1}}) \, P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}})}{P(\textcolor{purple}{c_{3,2}} \mid \textcolor{purple}{c_{1,2}})} = \frac{0.1 \cdot 0.1}{0.73} = 0.014 \\
    &\quad P(\textcolor{purple}{c_{2,2}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,2}}) = 1 - P(\textcolor{purple}{c_{2,1}} \mid \textcolor{purple}{c_{1,2}}, \textcolor{purple}{c_{3,2}}) = 1 - 0.014 = 0.986 \\[3ex]
    \end{aligned}
    $$

    Summarized as:

    <table>
      <thead>
        <tr>
          <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{C_2} \mid \textcolor{purple}{C_1}, \textcolor{purple}{C_3})$$</th>
          <th colspan="2" style="text-align: center;">$$\textcolor{purple}{c_{3,1}}$$</th>
          <th colspan="2" style="text-align: center;">$$\textcolor{purple}{c_{3,2}}$$</th>
        </tr>
        <tr>
          <th style="text-align: center;">$$\textcolor{purple}{c_{1,1}}$$</th>
          <th style="text-align: center;">$$\textcolor{purple}{c_{1,2}}$$</th>
          <th style="text-align: center;">$$\textcolor{purple}{c_{1,1}}$$</th>
          <th style="text-align: center;">$$\textcolor{purple}{c_{1,2}}$$</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>$$\textcolor{purple}{c_{2,1}}$$</td>
          <td>0.871</td>
          <td>0.333</td>
          <td>0.158</td>
          <td>0.014</td>
        </tr>
        <tr>
          <td>$$\textcolor{purple}{c_{2,2}}$$</td>
          <td>0.129</td>
          <td>0.667</td>
          <td>0.842</td>
          <td>0.986</td>
        </tr>
      </tbody>
    </table>

<h3 id="node-reduction-algorithm">The Arc-Reversal / Node-Reduction Algorithm</h3>

The algorithm incrementally eliminates nodes by repeatedly applying the four local graph operations described above, until only a single value node remains. The number stored in this final value node is the **MEU**, and the collection of recorded decision rules forms an **optimal policy** for the original decision problem.

**Input:** A well-formed influence diagram (or LIMID).  
**Output:** The MEU and an optimal policy for each decision node.

**Preparatory steps:** 
- **Canonical form:** If the diagram does not already satisfy the standard conventions (total order of decisions, and no arcs from decisions to chance nodes), perform a sequence of **Arc Reversals (Rule 4)** to obtain a canonical influence diagram.
- **LIMID transformation:** Transform the influence diagram into a LIMID by adding *memory arcs* so that each decision node has, as parents, all information variables that are remembered at the time of the decision.

---

**Main loop - repeat until only one value node remains:**

1. **Select a node $$N$$ to eliminate**
   - If there is any *barren node* (a node with no children), delete it immediately using **Barren-Node Deletion (Rule 1)**.
   - Otherwise, select any *leaf node* (a chance or decision node whose only children are value nodes).
   - If no leaf exists, choose a non-value node and repeatedly apply **Arc Reversal (Rule 4)** to its outgoing arcs until it becomes a leaf.

2. **Eliminate $$N$$**
   - If $$N$$ is a **chance node**, apply **Chance-Node Removal (Rule 2)**: marginalize over $$N$$ and update the relevant value tables.
   - If $$N$$ is a **decision node**, apply **Decision-Node Removal (Rule 3)**: maximize over the possible actions of $$N$$, record the optimal decision rule $$\delta^*$$, and update the value tables.

3. **Merge any duplicate value nodes** that may have arisen during elimination.

---

When the loop ends, only one value node remains. Its single numerical entry is the MEU. The set $$\{\delta^*\}$$ collected during the process provides an optimal decision rule for each decision node.

<h3 id="relationship-to-bayesian-network-elimination">Relationship to Bayesian Network Variable Elimination</h3>

Arc reversal/node reduction in influence diagrams is structurally similar to <a href="https://artint.info/3e/html/ArtInt3e.Ch4.S5.html"><u>variable elimination</u></a> in Bayesian networks. The main difference is the handling of utilities via **maximization** over decision nodes (instead of **summation** over chance nodes). In both approaches, information is propagated through the graph by combining local factors (such as CPTs or utility functions) and eliminating variables, either by summing over uncertainties for chance nodes or optimizing (maximizing) over decisions for decision nodes.

This similarity also extends to computational complexity: since both methods generate and manipulate similar intermediate factors, their efficiency is determined by the treewidth of the chosen elimination order.

<h3 id="related-work-evaluation">Related Work</h3>

There are several alternative strategies for evaluating influence diagrams beyond the arc-reversal and node-reduction procedures described above.

A more compact exact method is **junction-tree propagation**, which is also inspired by techniques from Bayesian networks. In this approach, the influence diagram is first moralized and triangulated, then compiled into a tree of cliques. Local probability and utility factors are passed between cliques using message-passing algorithms such as Shafer-Shenoy (<a href="https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content"><u>Shafer & Shenoy, 1990</u></a>) or HUGIN until convergence is reached. Junction-tree algorithms are often more memory-efficient than straightforward variable elimination and form the foundation of many commercial and open-source tools, including PyAgrum (<a href="https://arxiv.org/pdf/1302.6824"><u>Jensen et al., 1994</u></a>; <a href="https://arxiv.org/pdf/1301.6716"><u>Madsen & Jensen, 1999</u></a>; <a href="https://www.stats.ox.ac.uk/~steffen/papers/limids.pdf"><u>Lauritzen & Nilsson, 2001</u></a>).

However, even junction-tree propagation can become impractical for very complex or densely connected models, as the required clique tables may grow prohibitively large. Additionally, exact arc-reversal is difficult when the diagram contains continuous variables. In these situations, we need to rely on **approximate methods**. The most common of these is Monte Carlo sampling, which estimates expected utility by simulating random scenarios (<a href="https://www.jstor.org/stable/2632102"><u>Shachter & Kenley, 1989</u></a>; <a href="https://proceedings.mlr.press/r0/jenzarli95a/jenzarli95a.pdf"><u>Jenzarli, 1995</u></a>). Later research has shown that Monte Carlo methods can be extended to handle non-Gaussian or hybrid influence diagrams (<a href="https://cig.fi.upm.es/wp-content/uploads/2024/01/Decision-Analysis-by-Augmented-Probability-Simulation.pdf"><u>Bielza et al., 1999</u></a>; <a href="https://doi.org/10.1016/j.ejor.2007.01.036"><u>Cobb & Shenoy, 2008</u></a>).

Finally, another avenue is **variational inference**, although I haven't yet found published work applying it to influence diagrams. In principle, one could adapt techniques such as variational message passing (<a href="https://jmlr.org/papers/volume6/winn05a/winn05a.pdf"><u>Winn & Bishop, 2005</u></a>) to do so.

<h2 id="evaluating-oil-influence-diagram">Evaluating the Oil Influence Diagram</h2>

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<b>IMPORTANT:</b> To keep the section clear and focused, detailed computations are placed inside expandable sections below. Click to reveal them as needed.
</div>
<div style="height: 1.1em;"></div>

We will use the arc-reversal / node-reduction algorithm to solve the oil field decision problem. Note that the influence diagram is already a LIMID, since we added the arc $$\textcolor{red}{T} \rightarrow \textcolor{red}{B}$$, and it is in canonical form.

In Figure 5, we observe that there are neither barren nodes nor leaf nodes. Therefore, we must select one of the chance nodes and apply arc reversal until it becomes a leaf.

For the first step, we select node $$\textcolor{purple}{Q}$$ (oil field quality). Therefore, we need to reverse the arc $$\textcolor{purple}{Q} \rightarrow \textcolor{purple}{R}$$. To do this, we remove the arc $$\textcolor{purple}{Q} \rightarrow \textcolor{purple}{R}$$, add the arc $$\textcolor{purple}{R} \rightarrow \textcolor{purple}{Q}$$, and add arcs from the parents of $$\textcolor{purple}{R}$$ to $$\textcolor{purple}{Q}$$ if they are not already parents of $$\textcolor{purple}{Q}$$. This also means adding the arc $$\textcolor{red}{T} \rightarrow \textcolor{purple}{R}$$.

Figure 10 shows the result of reversing $$\textcolor{purple}{Q} \rightarrow \textcolor{purple}{R}$$:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/10_oil_reverse_q.png" alt="Influence diagram after reversing arc Q &rarr; R" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 10.</b> Influence diagram after reversing arc Q &rarr; R.</i>
    </td>
  </tr>
</table>
</center>

To obtain the distribution $$P(\textcolor{purple}{R} \mid \textcolor{red}{T})$$, we first marginalize over $$\textcolor{purple}{Q}$$ in $$P(\textcolor{purple}{R} \mid \textcolor{purple}{Q})$$:

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">Posteriors for <span style="color:purple;">pass</span> and <span style="color:purple;">fail</span> results</summary>

$$
\begin{aligned}
P(\textcolor{purple}{\text{pass}} \mid \textcolor{purple}{Q}) &= P(\textcolor{purple}{\text{pass}}  \mid \textcolor{purple}{\text{high}})P(\textcolor{purple}{\text{high}}) + P(\textcolor{purple}{\text{pass}}  \mid \textcolor{purple}{\text{medium}})P(\textcolor{purple}{\text{medium}}) + P(\textcolor{purple}{\text{pass}}  \mid \textcolor{purple}{\text{low}})P(\textcolor{purple}{\text{low}}) \\
                &= 0.95 \cdot 0.35 + 0.7 \cdot 0.45 + 0.15 \cdot 0.2 \\
                &= 0.3325 + 0.315 + 0.03 \\
                &= 0.6775 \\[1em]
P(\textcolor{purple}{\text{fail}} \mid \textcolor{purple}{Q}) &= P(\textcolor{purple}{\text{fail}}  \mid \textcolor{purple}{\text{high}})P(\textcolor{purple}{\text{high}}) + P(\textcolor{purple}{\text{fail}}  \mid \textcolor{purple}{\text{medium}})P(\textcolor{purple}{\text{medium}}) + P(\textcolor{purple}{\text{fail}}  \mid \textcolor{purple}{\text{low}})P(\textcolor{purple}{\text{low}}) \\
                &= 0.05 \cdot 0.35 + 0.3 \cdot 0.45 + 0.85 \cdot 0.2 \\
                &= 0.0175 + 0.135 + 0.17 \\
                &= 0.3225 \\
\end{aligned}
$$

</details>

Now, given that <span style="color: purple;">R</span> only applies when we make the test, we know that 
$$P\left(\textcolor{purple}{R} \mid \textcolor{purple}{Q},\, \textcolor{red}{T} = \textcolor{red}{\text{perform}}\right)$$ 
is simply 
$$P\left(\textcolor{purple}{R} \mid \textcolor{purple}{Q}\right)$$, 
and that 
$$P\left(\textcolor{purple}{R} \mid \textcolor{purple}{Q},\, \textcolor{red}{T} = \textcolor{red}{\text{no perform}}\right)$$ 
is all zeros except for the <span style="color: purple;">no results</span> case. Therefore:

<table>
  <tr>
    <th>$$P(\textcolor{purple}{R} \mid \textcolor{red}{T})$$</th>
    <th style="text-align:center;"><span style="color:red;">perform</span></th>
    <th style="text-align:center;"><span style="color:red;">no perform</span></th>      
  </tr>
  <tr>
    <td><span style="color:purple;">pass</span></td>
    <td>0.6775</td>
    <td>0</td>   
  </tr>
  <tr>
    <td><span style="color:purple;">fail</span></td>
    <td>0.3225</td>
    <td>0</td>
  </tr>
  <tr>
    <td><span style="color:purple;">no results</span></td>
    <td>0</td>
    <td>1</td>
  </tr>
</table>

Now for $$P(\textcolor{purple}{Q} \mid \textcolor{purple}{R})$$, we need to apply Bayes' theorem:

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">
P(<span style="color:purple;">Q</span> | <span style="color:purple;">R</span> = <span style="color:purple;">pass</span>)
</summary>

$$
\begin{aligned}
P(\textcolor{purple}{\text{high}} \mid \textcolor{purple}{\text{pass}}) &= \frac{P(\textcolor{purple}{\text{pass}} \mid \textcolor{purple}{\text{high}})P(\textcolor{purple}{\text{high}})}{P(\textcolor{purple}{\text{pass}})} \\
&= \frac{0.95 \cdot 0.35}{0.6775} = \frac{0.3325}{0.6775} \approx 0.4908 \\[1em]
P(\textcolor{purple}{\text{medium}} \mid \textcolor{purple}{\text{pass}}) &= \frac{P(\textcolor{purple}{\text{pass}} \mid \textcolor{purple}{\text{medium}})P(\textcolor{purple}{\text{medium}})}{P(\textcolor{purple}{\text{pass}})} \\
&= \frac{0.7 \cdot 0.45}{0.6775} = \frac{0.315}{0.6775} \approx 0.4649 \\[1em]
P(\textcolor{purple}{\text{low}} \mid \textcolor{purple}{\text{pass}}) &= \frac{P(\textcolor{purple}{\text{pass}} \mid \textcolor{purple}{\text{low}})P(\textcolor{purple}{\text{low}})}{P(\textcolor{purple}{\text{pass}})} \\
&= \frac{0.15 \cdot 0.2}{0.6775} = \frac{0.03}{0.6775} \approx 0.0443
\end{aligned}
$$

</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">P(<span style="color:purple;">Q</span> | <span style="color:purple;">R</span> = <span style="color:purple;">fail</span>)</summary>

$$
\begin{aligned}
P(\textcolor{purple}{\text{high}} \mid \textcolor{purple}{\text{fail}}) &= \frac{P(\textcolor{purple}{\text{fail}} \mid \textcolor{purple}{\text{high}})P(\textcolor{purple}{\text{high}})}{P(\textcolor{purple}{\text{fail}})} \\
&= \frac{0.05 \cdot 0.35}{0.3225} = \frac{0.0175}{0.3225} \approx 0.0543 \\[1em]
P(\textcolor{purple}{\text{medium}} \mid \textcolor{purple}{\text{fail}}) &= \frac{P(\textcolor{purple}{\text{fail}} \mid \textcolor{purple}{\text{medium}})P(\textcolor{purple}{\text{medium}})}{P(\textcolor{purple}{\text{fail}})} \\
&= \frac{0.3 \cdot 0.45}{0.3225} = \frac{0.135}{0.3225} \approx 0.4186 \\[1em]
P(\textcolor{purple}{\text{low}} \mid \textcolor{purple}{\text{fail}}) &= \frac{P(\textcolor{purple}{\text{fail}} \mid \textcolor{purple}{\text{low}})P(\textcolor{purple}{\text{low}})}{P(\textcolor{purple}{\text{fail}})} \\
&= \frac{0.85 \cdot 0.2}{0.3225} = \frac{0.17}{0.3225} \approx 0.5271
\end{aligned}
$$

</details>

When $$\textcolor{red}{T} = \textcolor{red}{\text{no perform}}$$, then $$\textcolor{purple}{R}$$ does not make sense, so $$P\left(\textcolor{purple}{Q} \mid \textcolor{purple}{R},\, \textcolor{red}{T} = \textcolor{red}{\text{no perform}}\right)$$ is simply $$P\left(\textcolor{purple}{Q}\right)$$. Therefore:

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{Q} \mid \textcolor{purple}{R},\, \textcolor{red}{T})$$</th>
    <th colspan="3" style="text-align: center;"><span style="color:red;">perform</span></th>
    <th colspan="3" style="text-align: center;"><span style="color:red;">no perform</span></th>
  </tr>
  <tr>
    <th style="text-align: center;"><span style="color:purple;">pass</span></th>
    <th style="text-align: center;"><span style="color:purple;">fail</span></th>
    <th style="text-align: center;"><span style="color:purple;">no results</span></th>
    <th style="text-align: center;"><span style="color:purple;">pass</span></th>
    <th style="text-align: center;"><span style="color:purple;">fail</span></th>
    <th style="text-align: center;"><span style="color:purple;">no results</span></th>
  </tr>
  <tr>
    <td><span style="color:purple;">high</span></td>
    <td>0.4908</td>
    <td>0.0543</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.35</td>
  </tr>
  <tr>
    <td><span style="color:purple;">medium</span></td>
    <td>0.4649</td>
    <td>0.4186</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.45</td>
  </tr>
  <tr>
    <td><span style="color:purple;">low</span></td>
    <td>0.0443</td>
    <td>0.5271</td>
    <td>x</td>
    <td>x</td>
    <td>x</td>
    <td>0.2</td>
  </tr>
</table>

By making the problem symmetric, we have introduced many zero probabilities, which increases the likelihood of encountering undefined expressions such as $$0/0$$. Recall that a conditional probability $$P(\textcolor{purple}{a} \mid \textcolor{purple}{b})$$ is only defined when $$P(\textcolor{purple}{b}) > 0$$, so we should not expect to be able to compute every conditional probability when reversing arcs. However, as will be shown below, these "x" values will not affect the outcome of the problem.

After reversing the arc $$\textcolor{purple}{Q} \rightarrow \textcolor{purple}{R}$$, the node $$\textcolor{purple}{Q}$$ becomes a leaf and can be eliminated. Figure 11 illustrates the resulting diagram.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/11_oil_remove_q.png" alt="Influence diagram after removing node Q" width="320">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 11.</b> Influence diagram after removing node Q.</i>
    </td>
  </tr>
</table>
</center>

By removing $$\textcolor{purple}{Q}$$, we need to marginalize it and update the utility table of $$\textcolor{blue}{U}$$

$$
u'_\textcolor{blue}{U}(\textcolor{red}{T}, \textcolor{purple}{R}, \textcolor{red}{B}) = \sum_{\textcolor{purple}{q}} u_\textcolor{blue}{U}(\textcolor{red}{T}, \textcolor{red}{B}, \textcolor{purple}{Q})P(\textcolor{purple}{q} \mid \textcolor{red}{T}, \textcolor{purple}{R})
$$

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">
<span style="color:blue;">U'</span>(<span style="color:purple;">R</span>, <span style="color:red;">B</span>, <span style="color:red;">T</span> = <span style="color:red;">perform</span>)
</summary>
$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{pass}},\ \textcolor{red}{\text{buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&= 1220 \cdot 0.4908 + 600 \cdot 0.4649 + (-30) \cdot 0.0443 \\
&= 598.776 + 278.94 - 1.329 \\
&= 876.387 \\[1em]
% -------------------
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{pass}},\ \textcolor{red}{\text{no buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{pass}}) \\
&= 320 \cdot 0.4908 + 320 \cdot 0.4649 + 320 \cdot 0.0443 \\
&= 157.056 + 148.768 + 14.176 \\
&= 320
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{fail}},\ \textcolor{red}{\text{buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&= 1220 \cdot 0.0543 + 600 \cdot 0.4186 + (-30) \cdot 0.5271 \\
&= 66.246 + 251.16 - 15.813 \\
&= 301.593\\[1em]
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{fail}},\ \textcolor{red}{\text{no buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{fail}}) \\
&= 320 \cdot 0.0543 + 320 \cdot 0.4186 + 320 \cdot 0.5271 \\
&= 17.376 + 133.952 + 168.672 \\
&= 320
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{no results}},\ \textcolor{red}{\text{buy}}) &= u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&= 1220 \cdot x + 600 \cdot x + (-30) \cdot x \\
&= 1220x + 600x - 30x \\
&= 1790x \\[1em]
% -------------------
u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}},\ \textcolor{purple}{\text{no results}},\ \textcolor{red}{\text{no buy}}) &= u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u'_\textcolor{blue}{U}(\textcolor{red}{\text{perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{perform}}, \textcolor{purple}{\text{no results}}) \\
&= 320 \cdot x + 320 \cdot x + 320 \cdot x \\
&= 320x + 320x + 320x \\
&= 960x
\end{aligned}
$$
</details>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">
<span style="color:blue;">U'</span>(<span style="color:purple;">R</span>, <span style="color:red;">B</span>, <span style="color:red;">T</span> = <span style="color:red;">no perform</span>)
</summary>
$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{pass}},\ \textcolor{red}{\text{buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&= 1250 \cdot x + 630 \cdot x + 0 \cdot x \\
&= 1250x + 630x + 0x \\
&= 1880x
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{pass}},\ \textcolor{red}{\text{no buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{pass}}) \\
&= 350 \cdot x + 350 \cdot x + 350 \cdot x \\
&= 350x + 350x + 350x \\
&= 1050x
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{fail}},\ \textcolor{red}{\text{buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&= 1250 \cdot x + 630 \cdot x + 0 \cdot x \\
&= 1250x + 630x + 0x \\
&= 1880x
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{fail}},\ \textcolor{red}{\text{no buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{fail}}) \\
&= 350 \cdot x + 350 \cdot x + 350 \cdot x \\
&= 350x + 350x + 350x \\
&= 1050x
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{no results}},\ \textcolor{red}{\text{buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&= 1250 \cdot 0.35 + 630 \cdot 0.45 + 0 \cdot 0.2 \\
&= 437.5 + 283.5 + 0 \\
&= 721
\end{aligned}
$$

$$
\begin{aligned}
u'_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}},\ \textcolor{purple}{\text{no results}},\ \textcolor{red}{\text{no buy}}) &= u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{high}}) P(\textcolor{purple}{\text{high}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{medium}}) P(\textcolor{purple}{\text{medium}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&\quad + u_\textcolor{blue}{U}(\textcolor{red}{\text{no perform}}, \textcolor{red}{\text{no buy}}, \textcolor{purple}{\text{low}}) P(\textcolor{purple}{\text{low}} \mid \textcolor{red}{\text{no perform}}, \textcolor{purple}{\text{no results}}) \\
&= 350 \cdot 0.35 + 350 \cdot 0.45 + 350 \cdot 0.2 \\
&= 122.5 + 157.5 + 70 \\
&= 350
\end{aligned}
$$
</details>

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
In practice, it is not necessary to estimate the cases that are not applicable (i.e., the ones marked multiplied by "x"); we can simply assign them as "None" and disregard them in subsequent calculations.
</div>
<div style="height: 1.1em;"></div>

The following table shows the updated utility table $$u'_\textcolor{blue}{U}$$ table after removing $$\textcolor{purple}{Q}$$:

<table>
  <tr>
    <th style="text-align: center;">$$\textcolor{red}{T}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{R}$$</th>
    <th style="text-align: center;">$$\textcolor{red}{B}$$</th>
    <th style="text-align: center;">$$\textcolor{blue}{U}$$</th>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">perform</span></td>
    <td rowspan="2"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">876.387</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">301.593</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1790x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">960x</span></td>
  </tr>
  <tr>
    <td rowspan="6"><span style="color: red;">no perform</span></td>
    <td rowspan="2"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">1050x</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">1050x</span></td>
  </tr>
  <tr>
    <td rowspan="2"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">721</span></td>
  </tr>
  <tr>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">350</span></td>
  </tr>
</table>

We can now remove the decision node $$\textcolor{red}{B}$$, as it is a leaf node. The resulting influence diagram is shown below:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/12_oil_remove_b.png" alt="Influence diagram after removing decision node B" width="300">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 12.</b> Influence diagram after removing decision node B.</i>
    </td>
  </tr>
</table>
</center>

By removing $$\textcolor{red}{B}$$, we must determine the optimal choice for $$\textcolor{red}{B}$$ in every possible scenario. This yields the following utility table, $$u''_\textcolor{blue}{U}$$:

<table>
  <tr>
    <th style="text-align: center;">$$\textcolor{red}{T}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{R}$$</th>
    <th style="text-align: center;">$$\textcolor{red}{\delta^*(B)}$$</th>
    <th style="text-align: center;">$$\textcolor{blue}{U}$$</th>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">perform</span></td>
    <td rowspan="1"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">876.387</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">no buy</span></td>
    <td><span style="color: blue;">320</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1790x</span></td>
  </tr>
  <tr>
    <td rowspan="3"><span style="color: red;">no perform</span></td>
    <td rowspan="1"><span style="color: purple;">pass</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">fail</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">1880x</span></td>
  </tr>
  <tr>
    <td rowspan="1"><span style="color: purple;">no results</span></td>
    <td><span style="color: red;">buy</span></td>
    <td><span style="color: blue;">721</span></td>
  </tr>
</table>

After removing $$\textcolor{red}{B}$$, $$\textcolor{purple}{R}$$ becomes a leaf node, allowing us to eliminate it by marginalization.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/13_oil_remove_r.png" alt="Influence diagram after removing chance node R" width="180">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 13.</b> Influence diagram after removing chance node R.</i>
    </td>
  </tr>
</table>
</center>

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">
<span style="color:blue;">U'''</span>(<span style="color:red;">T</span>)
</summary>

$$
\begin{aligned}
u'''_{\textcolor{blue}{U}}(\textcolor{red}{\text{perform}}) &= u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{perform}},\,\textcolor{purple}{\text{pass}},\,\textcolor{red}{\text{buy}})\; P(\textcolor{purple}{\text{pass}} \mid \textcolor{red}{\text{perform}}) \\
&\quad + u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{perform}},\,\textcolor{purple}{\text{fail}},\,\textcolor{red}{\text{no buy}})\; P(\textcolor{purple}{\text{fail}} \mid \textcolor{red}{\text{perform}}) \\
&\quad + u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{perform}},\,\textcolor{purple}{\text{no results}},\,\textcolor{red}{\text{buy}})\; P(\textcolor{purple}{\text{no results}} \mid \textcolor{red}{\text{perform}}) \\
&= 876.387 \cdot 0.6775 + 320 \cdot 0.3225 + 1790x \cdot 0 \\
&= 593.738 + 103.2 + 0 \\
&= 696.938 \\[1em]
% -------------------
u'''_{\textcolor{blue}{U}}(\textcolor{red}{\text{no perform}}) &= u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{no perform}},\,\textcolor{purple}{\text{pass}},\,\textcolor{red}{\text{buy}})\; P(\textcolor{purple}{\text{pass}} \mid \textcolor{red}{\text{no perform}}) \\
&\quad + u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{no perform}},\,\textcolor{purple}{\text{fail}},\,\textcolor{red}{\text{buy}})\; P(\textcolor{purple}{\text{fail}} \mid \textcolor{red}{\text{no perform}}) \\
&\quad + u''_{\textcolor{blue}{U}}(\textcolor{red}{\text{no perform}},\,\textcolor{purple}{\text{no results}},\,\textcolor{red}{\text{buy}})\; P(\textcolor{purple}{\text{no results}} \mid \textcolor{red}{\text{no perform}}) \\
&= 1880x \cdot 0 + 1880x \cdot 0 + 721 \cdot 1 \\
&= 0 + 0 + 721 \\
&= 721 \\
\end{aligned}
$$

</details>

The table below shows the updated utility values $$u'''_{\textcolor{blue}{U}}$$ after removing $$\textcolor{purple}{R}$$:

<table>
  <thead>
    <tr>
      <th style="text-align: center;">$$\textcolor{red}{T}$$</th>
      <th style="text-align: center;">$$\textcolor{blue}{U}$$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span style="color: red;">perform</span></td>
      <td><span style="color: blue;">696.938</span></td>
    </tr>
    <tr>
      <td><span style="color: red;">no perform</span></td>
      <td><span style="color: blue;">721</span></td>
    </tr>
  </tbody>
</table>

At this stage, the only remaining node is the decision node $$\textcolor{red}{T}$$, which we can now eliminate by selecting the optimal action. The table below summarizes the optimal decision for $$\textcolor{red}{T}$$, and Figure 14 shows the final influence diagram after its removal:

<table>
  <thead>
    <tr>
    <th style="text-align: center;">$$\textcolor{red}{\delta^*(T)}$$</th>
      <th style="text-align: center;">$$\textcolor{blue}{U}$$</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><span style="color: red;">no perform</span></td>
      <td><span style="color: blue;">721</span></td>
    </tr>
  </tbody>
</table>

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-07-04-decision-theory-II/14_oil_remove_t.png" alt="Final influence diagram after removing decision node T" width="60">
    </td>
  </tr>
  <tr>
    <td colspan="1" align="center">
      <i><b>Figure 14.</b> Final influence diagram after removing decision node T.</i>
    </td>
  </tr>
</table>
</center>

As we can see, this yields the same result as the decision tree in <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html"><u>Part I</u></a>: **the company should not perform the test and should buy the oil field**.

<h2 id="influence-diagram-libraries">Influence Diagram Libraries</h2>

In practice, we do not need to manually perform each step of the arc-reversal or node-reduction algorithm to evaluate an influence diagram. Several open-source libraries automate this entire process and provide sophisticated inference algorithms that handle the computational complexity for us.

<a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> is currently the most widely supported open-source library for influence diagrams. Written in C++ with a Python interface, it implements the Shafer-Shenoy algorithm for LIMIDs (<a href="https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content"><u>Shafer & Shenoy, 1990</u></a>). PyAgrum builds a junction tree representation of the influence diagram and uses message passing, alternating between summation (for chance nodes) and maximization (for decision nodes), to efficiently evaluate the diagram.

Other notable libraries include:

* <a href="https://support.bayesfusion.com/docs/"><code>GeNIe/SMILE</code></a>: Implemented in C++, GeNIe is a useful, though somewhat dated, tool for working with Bayesian networks and influence diagrams. SMILE is the underlying engine. Both are free for academic use but are not open-source.

* <a href="https://github.com/causalincentives/pycid"><code>PyCID</code></a>: Written in Python, PyCID is a specialized open-source library designed for working with causal influence diagrams.


<h2>Conclusion</h2>

This post has shown how influence diagrams can be used to model and solve decision problems under uncertainty. By applying the arc-reversal and node-reduction algorithms to the oil-field LIMID, we obtained a maximum expected utility of <b>721</b> and confirmed that the optimal strategy is to <b>skip the porosity test and buy the field</b>. As expected, this matches the recommendation from the equivalent decision tree discussed in <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html"><u>Part I</u></a>.

Influence diagrams excel at capturing conditional independencies, which helps control the combinatorial explosion that often plagues decision trees. However, their main limitation is that they are best suited for symmetric problems. Highly asymmetric scenarios may require introducing artificial states or degenerate probabilities, which can increase both the size and computational complexity of the model.

**In the next post**, we'll demonstrate how to build and evaluate LIMIDs using open-source tools like <a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a>, perform sensitivity analysis and value-of-information calculations, and explore advanced features such as multiple utility nodes and decision planes. Finally, we'll show how to integrate Gradio with PyAgrum to create interactive, web-based decision problem demos, making it easy to experiment with and communicate complex decision models.

<!-- Future exploration could delve deeper into topics such as causality, the relationship with Large 
Language Models (LLMs), and handling continuous probabilistic variables. -->


<h2 id="references">References</h2>


1. Shenoy, P. P. (2009). <a href="https://pshenoy.ku.edu/Papers/EOLSS09.pdf"><u>Decision trees and influence diagrams</u></a>. Encyclopedia of life support systems, 280-298.
<br><br>
2. Rodriguez, F. (2025, June 8). <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html">Introduction to decision theory: Part I</a>. 
<br><br>
1. Wikipedia article on <u><a href="https://en.wikipedia.org/wiki/Conditional_independence">conditional independence</a></u>.
<br><br>
2. Wikipedia article on <u><a href="https://en.wikipedia.org/wiki/Tree_diagram_(probability_theory)">probability trees</a></u>.
<br><br>
3. Wikipedia article on <u><a href="https://en.wikipedia.org/wiki/Bayesian_network">Bayesian networks</a></u>.
<br><br>
5. Howard, R. A., & Matheson, J. E. (1984). <u>Influence diagrams</u>. The Principles and Applications of Decision Analysis (Vol. II), 719-762.
<br><br>
6. Bielza, C., & Shenoy, P. P. (1999). <a href="https://cig.fi.upm.es/wp-content/uploads/2024/01/A-Comparison-of-Graphical-Techniques-for-Asymmetric-Decision-Problems.pdf"><u>A comparison of graphical techniques for asymmetric decision problems</u></a>. European Journal of Operational Research, 119(1), 1-13.
<br><br>
7. Lauritzen, S. L., & Nilsson, D. (2001). <a href="https://web.math.ku.dk/~lauritzen/papers/limids.pdf"><u>Representing and solving decision problems with limited information</u></a>. Management Science, 47(9), 1235-1251.
<br><br>
8. Shachter, R. D. (1986). <a href="http://www.cis.umassd.edu/~x2zhang/courses/CIS561/readings/EvaluatingID.pdf"><u>Evaluating influence diagrams</u></a>. Operations research, 34(6), 871-882.
<br><br>
9. Wikipedia article on <u><a href="https://artint.info/3e/html/ArtInt3e.Ch4.S5.html">variable elimination</a></u>.
<br><br>
10. Jensen, F., Jensen, F. V., & Dittmer, S. (1994). <a href="https://arxiv.org/pdf/1302.6824"><u>From influence diagrams to junction trees</u></a>. In Proceedings of the 10th Conference on Uncertainty in Artificial Intelligence (UAI) (pp. 367-373).
<br><br>
11. Madsen, A. L., & Jensen, F. (1999). <a href="https://arxiv.org/pdf/1301.6716"><u>Lazy evaluation of symmetric Bayesian decision problems</u></a>. In Proceedings of the Fifteenth Conference on Uncertainty in Artificial Intelligence (UAI) (pp. 382–390). Morgan Kaufmann.
<br><br>
12. Shachter, R. D., & Kenley, C. R. (1989). <a href="https://www.jstor.org/stable/2632102"><u>Gaussian influence diagrams</u></a>. Management Science, 35(5), 527–550.
<br><br>
13. Jenzarli, A. (1995). <a href="https://proceedings.mlr.press/r0/jenzarli95a/jenzarli95a.pdf"><u>Solving influence diagrams using Gibbs sampling</u></a>. In Pre-proceedings of the Fifth International Workshop on Artificial Intelligence and Statistics (pp. 278-284). PMLR.
<br><br>
14. Bielza, C., Müller, P., & Ríos-Insua, D. (1999). <a href="https://cig.fi.upm.es/wp-content/uploads/2024/01/Decision-Analysis-by-Augmented-Probability-Simulation.pdf"><u>Decision analysis by augmented probability simulation</u></a>. Management Science, 45(7), 995–1007.
<br><br>
15. Cobb, B. R., & Shenoy, P. P. (2008). <a href="https://doi.org/10.1016/j.ejor.2007.01.036"><u>Decision making with hybrid influence diagrams using mixtures of truncated exponentials</u></a>. European Journal of Operational Research, 186(1), 261-275.
<br><br>
16. Winn, J., & Bishop, C. M. (2005). <a href="https://jmlr.org/papers/volume6/winn05a/winn05a.pdf"><u>Variational message passing</u></a>. Journal of Machine Learning Research, 6, 661–694.
<br><br>
17. Shafer, G., & Shenoy, P. P. (1990). <a href="https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content"><u>Probability Propagation</u></a>. Annals of Mathematics and Artificial Intelligence, 2, 327-352.
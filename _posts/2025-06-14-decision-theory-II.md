---
layout: post
title: "Introduction to Decision Theory: Part II"
date: 2025-06-14
categories: blog
description: "Explores the strengths and limitations of decision trees, introduces influence diagrams as a scalable alternative, and surveys Python libraries (PyAgrum, PyCID) for practical decision-analysis."
tags: [Decision Theory]
---

<!-- Comentar que durante años la unica manera de resolver estos problemas era con arboles de decision y hasta que en 1980 surgen los diagramas de influence, pero realmente no hubo software comun para >

<h2 id="decision-trees-strengths-limitations">Decision Trees: Strengths and Limitations</h2>

Decision trees are a crowd-pleaser. As we saw in <a href="/2025/06/08/decision-theory-I.html">Part&nbsp;I</a>, a left-to-right layout tells a self-explanatory story: *if this happens, then we choose that*. Their visual simplicity makes them ideal for workshops with non-technical stakeholders, offers an audit trail regulators love, and—when the problem is small—lets you "roll back" the expected utility with nothing more exotic than a spreadsheet.

However, those same trees can buckle once real-world complexity sneaks in. Extra decisions, shared uncertainties, feedback loops, or multi-attribute objectives quickly turn a tidy diagram into a wall-sized poster.

<h3 id="combinatorial-explosion" style="color:purple;">Combinatorial Explosion</h3>
Every additional decision point or uncertain variable rapidly increases the number of possible paths through the tree. For instance, if you add just one more binary decision and one more binary chance node, the number of potential outcomes (leaves) can quadruple. This has direct consequences for memory usage, the computational cost of operations (e.g., numerous Bayes theorem calls), and significantly impacts readability because the tree diagram becomes unmanageably large, even for moderately complex problems, making it difficult to visualize, analyze, or communicate.

<!-- Hay que escribir un ejemplo claro de la limitacion con numeros y a poder ser siguiendo el ejemplo anterior, aunque no tiene por que... -->

<h3 id="hidden-independence" style="color:purple;">Hidden Conditional Independencies</h3>
Trees cannot state explicitly that two diagnostics are independent given reservoir quality; instead you must encode the full joint distribution, inflating elicitation effort. Decision trees inherently encode the full joint probability distribution, even when certain variables are conditionally independent. For example, if two diagnostic tests are independent given the underlying state of a system (e.g., reservoir quality), a decision tree still requires you to specify the probabilities for all combinations, rather than explicitly stating the independence. This inflates the data elicitation effort and obscures the underlying probabilistic relationships.

<!-- Lo mismo para este caso, mostrar de forma clara esta limitacion -->

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<strong>Bottom line:</strong> decision trees shine as teaching tools and for *small*, strictly sequential problems. For anything larger, <u><a href="https://en.wikipedia.org/wiki/Influence_diagram">influence diagrams</a></u> offer a compact, maintainable, and transparent alternative. The next section shows how they tame the explosion while preserving the logic.
</div>

<!-- * Comentar las limitaciones
* Hablar de que librerias en Python tenemos disponibles. Centrarme en PyAgrum y PyCID -->


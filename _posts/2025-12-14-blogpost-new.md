---
layout: post
title: "How Capable Are Language Models At Probabilistic Reasoning?"
date: 2025-12-13
categories: blog
description: "TODO"
tags: [Probabilistic Reasoning]
---

<h2 id="the-challenge-of-decision-making">Can large language models think "rationally"?</h2>

This question has been on my mind for a while. It has motivated me to revise probabilistic graphical models and write my blog series on Decision Theory during summer. [In my last post of that series](https://ferjorosa.github.io/blog/2025/08/07/decision-theory-III.html), I talked about combining large language models (LLMs) with influence diagrams. 

The truth is, I had already started exploring that idea even before writing the first blog post. Back in May 2025, I put together a [notebook](https://github.com/ferjorosa/decision-theory-llms/blob/main/notebooks/how_good_are_llms_decision_problems.ipynb) testing how well LLMs could solve decision problems. The results were interesting. LLMs like O3 and Gemini 2.5 Pro reached correct solutions on the three small problems I tested. 

Now, interestingly, they solved those problems using decision trees which, [as I explained in another post](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html), have theoretical limitations. In that same post I have shown how we can solve this problems "manually" with all the operations that were required.

So, I wondered, were LLMs solving those problems with decision trees because it was easier for them or because they "dont know" how to apply the algorithms themselves. To test that idea I set out to run more extensive experiments and for that I needed a dataset of synthetic decision problems. But I found that generating decision problems is not easy to scale. I still need a way to figure it out. For example, those 3 examples were done "hybrid process" where I manually defineed influence diagrams manually and then doing back-and-forth iterations with LLMs to define a good "story" around them.

Then, I thought about ignoring the context part and just focusing on the numerical reasoning capabilities but since influence diagrams are are essentially Bayesian networks augmented with decisions and utilities, I thought it would be interesting to start understand how LLMs handle basic probabilistic inference. If they struggle with probability calculations on Bayesian networks, expecting them to solve influence diagrams could be premature.


<!-- 

No se si ponerlo aqui, pero la idea es resolver una probabilistic query a mano con variable elimination y luego comparar ese resultado con el resultado de LLMs, comparar si llegan a la solucion y ver que clase de tokens escriben en su thinking. Me voy a centrar principalmente en reasoning models. 

Me parece igual de interesante ver si llegan a la solucion que ver como difiere una solucion a mano de lo que haga yo. Tambien puede ser que no aplicquen variable elimination, hay otras opciones como junction tree of belief propagation. Explicare variable elimination porque es de los mas "faciles" de entender a mi parecer
-->

## Bayesian networks

A Bayesian network (BN) is a directed acyclic graph (DAG) in which nodes represent random variables. Arcs encode conditional dependencies between variables in a way that allows us to factorize the joint probability distribution into a product of conditional probability distributions (CPDs),

$$
\begin{equation}
P(\mathbf{\textcolor{purple}{V}}) = P(\textcolor{purple}{V_1}, \ldots, \textcolor{purple}{V_n}) = \prod_{i=1}^{n} P(\textcolor{purple}{V_i} | \mathbf{Pa}_{\textcolor{purple}{V_i}})
\end{equation}
$$

where $$\mathbf{Pa}_{\textcolor{purple}{V_i}}$$ denotes the parents of variable $$\textcolor{purple}{V_i}$$ in the DAG. 


As an example, consider a Bayesian network with 4 binary variables ($$\textcolor{purple}{V_0}, \textcolor{purple}{V_1}, \textcolor{purple}{V_2}, \textcolor{purple}{V_3}$$). The structure is a simple diamond-like shape where $$\textcolor{purple}{V_0}$$ is the root, $$\textcolor{purple}{V_1}$$ and $$\textcolor{purple}{V_2}$$ depend on $$\textcolor{purple}{V_0}$$, and $$\textcolor{purple}{V_3}$$ depends on both $$\textcolor{purple}{V_0}$$ and $$\textcolor{purple}{V_1}$$.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-12-14-llms-bn-inference/bn_example.png" alt="Bayesian network example" 
      height="300">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Bayesian network example with 4 variables</i>
    </td>
  </tr>
</table>
</center>

<table>
  <tr>
    <th colspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_0})$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.5072</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.4928</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_1} \mid \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.3110</td>
    <td>0.0704</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.6890</td>
    <td>0.9296</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_2} \mid \textcolor{purple}{V_0})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.8950</td>
    <td>0.0562</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.1050</td>
    <td>0.9438</td>
  </tr>
</table>

<table>
  <tr>
    <th rowspan="2" style="text-align: center;">$$P(\textcolor{purple}{V_3} \mid \textcolor{purple}{V_0},\, \textcolor{purple}{V_1})$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0 = s_0}$$</th>
    <th colspan="2" style="text-align: center;">$$\textcolor{purple}{V_0 = s_1}$$</th>
  </tr>
  <tr>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_1}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_0}$$</th>
    <th style="text-align: center;">$$\textcolor{purple}{V_1 = s_1}$$</th>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_0}$$</td>
    <td>0.0607</td>
    <td>0.8173</td>
    <td>0.8890</td>
    <td>0.2251</td>
  </tr>
  <tr>
    <td>$$\textcolor{purple}{s_1}$$</td>
    <td>0.9393</td>
    <td>0.1827</td>
    <td>0.1110</td>
    <td>0.7749</td>
  </tr>
</table>

## Probabilistic inference on Bayesian networks

Once we have a BN, we can use it to reason by performing probabilistic inference. This task involves computing the probability of query variables $$\mathbf{\textcolor{purple}{Q}}$$ given some observed evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$.

Theoretically, this is straightforward. The Bayesian network defines the full joint distribution, so we could sum over all unobserved "nuisance" variables $$\mathbf{\textcolor{purple}{Z}}$$:

$$
\begin{equation}
P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}} \mid \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}) = \frac{\sum_{\mathbf{\textcolor{purple}{z}}} P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}, \mathbf{\textcolor{purple}{Z}} = \mathbf{\textcolor{purple}{z}})}{\sum_{\mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{z}}} P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}}, \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}, \mathbf{\textcolor{purple}{Z}} = \mathbf{\textcolor{purple}{z}})}
\end{equation}
$$

However, this naive approach is computationally unfeasible. It requires building the full joint distribution table, which has $$2^{\textcolor{purple}{n}}$$ rows for $$\textcolor{purple}{n}$$ binary variables. For example, this would result in over a billion entries for just 30 variables.

Efficient inference algorithms avoid this by working directly with the factorized representation. Rather than constructing the full joint, they manipulate individual CPTs and perform marginalization locally. Well-known examples include Variable Elimination, Junction Tree algorithm, and Belief Propagation. We'll focus on Variable Elimination since it's the easiest to explain and commonly used when teaching BN inference.

## Variable elimination algorithm

As the name suggests, the **Variable Elimination** algorithm works by eliminating the variables of the network until it yields the answer to a specific query. This algorithm is
typically defined in terms of factors.

A **factor** $$\phi(\mathbf{\textcolor{purple}{X}})$$ is a function that maps a set of variables $$\mathbf{\textcolor{purple}{X}}$$ to a real positive value. CPDs are an example of factors. In fact, the initial set of factors corresponds exactly to he CPDs of the network.

During inference, new factors are created by multiplying and marginalizing existing ones. These **intermediate factors** are generally **unnormalized**, meaning their values do not sum to one. This is not a problem, since normalization is only required for the final result. Working with unnormalized factors simplifies computation and allows inference algorithms to focus on local operations.

### Operations on factors

Variable elimination relies on three operations:

1. **Factor Product:** Combine two factors $$\phi_1(\textcolor{purple}{V_1})$$ and $$\phi_2(\textcolor{purple}{V_2})$$ into a new factor $$\phi_{new}$$ over $$\textcolor{purple}{V_1} \cup \textcolor{purple}{V_2}$$ by multiplying their values for every consistent assignment:

$$
\phi_{new}(\textcolor{purple}{v_1}, \textcolor{purple}{v_2}) = \phi_1(\textcolor{purple}{v_1}) \cdot \phi_2(\textcolor{purple}{v_2})
$$

2. **Marginalization:** Eliminate a variable $$\textcolor{purple}{Z}$$ from factor $$\phi(\textcolor{purple}{V}, \textcolor{purple}{Z})$$ by summing over all its values to produce a new factor $$\phi_{new}$$:

   $$\phi_{new}(\textcolor{purple}{v}) = \sum_{\textcolor{purple}{z}} \phi(\textcolor{purple}{v}, \textcolor{purple}{z})$$

3. **Evidence restriction:** If variable $$\textcolor{purple}{E}$$ is observed to be $$\textcolor{purple}{e}$$, restrict any factor containing $$\textcolor{purple}{E}$$ to that value—essentially selecting the slice of the table consistent with the observation.

### The algorithm

Given a Bayesian network, query variables $$\mathbf{\textcolor{purple}{Q}}$$, and evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$:

1. **Initialize:** Treat each CPT as a factor. Restrict all factors to be consistent with the evidence $$\mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}}$$.

2. **Choose elimination order:** Pick an ordering for the hidden variables $$\mathbf{\textcolor{purple}{Z}}$$ (neither query nor evidence). The choice of ordering affects efficiency—bad orders create large intermediate factors.

3. **Eliminate variables:** For each variable $$\textcolor{purple}{Z_i}$$ in order:
   - **Collect** all factors containing $$\textcolor{purple}{Z_i}$$
   - **Multiply** them into a single factor $$\textcolor{purple}{\phi_{prod}}$$
   - **Sum out** $$\textcolor{purple}{Z_i}$$ to get a new factor $$\textcolor{purple}{\phi_{new}}$$
   - **Replace** the collected factors with $$\textcolor{purple}{\phi_{new}}$$

4. **Normalize:** Multiply remaining factors (now only over $$\mathbf{\textcolor{purple}{Q}}$$) and normalize to obtain $$P(\mathbf{\textcolor{purple}{Q}} = \mathbf{\textcolor{purple}{q}} \mid \mathbf{\textcolor{purple}{E}} = \mathbf{\textcolor{purple}{e}})$$.

### Example

<!-- Aqui usamos el ejemplo de BN que hemos definido arriba y vamos paso a paso -->

## How LLMs do it

<!-- 

Aqui puedo comentar un par de papers que me he encontrado, uno de ellos no se centra en redes Bayesianas sino en evaluar los LLMs para problemas con distribuciones univariates. El otro si que se centra en redes Bayesianas 

-->

### Experiment setup

<!--

Comentamos como es el prompt y que modelos vamos a utilizar, distinguiendo en que modelos son open-source y closed-source. Comentar que vamos a ejecutarlo usando OpenRouter y que se nos provee de las trazas de razonamiento completas en el caso open-source y un resumen de las mismas en el caso closed-source

Comentar donde se encuentra el codigo disponible y que para ejecutarlo simplemente se necesita unos pocos creditos de OpenRouter. De cualquier forma comparto los resultados como archivos JSON para que puedan ser analizados.

-->

### Results

## Related work

<!-- Hablar de los 2 papers y de otros -->

## Conclusions

<!-- 

Aparte de las conclusiones que obtenga, comentar como pasos siguientes es que estoy escribiendo un paper con Bojan donde hacemos un estudio sistematizado de este problema. En parte esta inspirado por el trabajo de Nafar.

We extend their study by means of a more comprehensive analysis of different query complexities. 
In addition, we consider powerful, reasoning models. 
We want to establish a baseline, where there is no specific prompting and where the underlying model is given explicitly.
We also carefully consider the query complexity, not just in terms of the computational cost of variable elimiantion,
but also in terms of relevance complexity [@druzdzel1993]. 

Creo que es importante comentar que no hemos evaluado que ocurre cuando damos herramientas a los LLMs, ver si son capaces de resolver el problema mas rapido. Creo que en tal caso nos estariamos introduciendo mas en aspectos tipo agente con function calling y multiples pasos, aunque se podria evaluar tambien mediante un unico paso, forzandoles a 1 try.
-->
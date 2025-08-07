---
layout: post
title: "Introduction to Decision Theory: Part III"
date: 2025-08-07
categories: blog
description: "Deep dive into sensitivity analysis for decision problems, implementing the oil field purchase decision using PyAgrum's library, and creating an interactive web interface with Gradio to explore how changes in probabilities and utilities affect optimal decisions."
tags: [Decision Theory]
---

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">Table of Contents</summary>

<ul style="margin-top: 0.5em;">
  <li style="margin-bottom: 0.5em;"><a href="#closing-the-loop">Closing the Loop</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#building-the-oil-field-limid-in-pyagrum">Building the Oil-Field LIMID in PyAgrum</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#setting-up-the-network-structure">Setting Up the Network Structure</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#filling-in-the-numbers">Filling in the Numbers</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#solving-the-network">Solving the Network</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#testing-robustness-with-sensitivity-analysis">Testing Robustness with Sensitivity Analysis</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#single-parameter-sensitivity-analysis">Single Parameter Sensitivity Analysis</a>
        <ul style="margin-top: 0.2em;">
          <li style="margin-bottom: 0.2em;"><a href="#example-1-prior-probability-of-high-quality-fields">Example 1: Prior Probability of High-Quality Fields</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#example-2-test-precision-for-medium-quality-fields">Example 2: Test Precision for Medium-Quality Fields</a></li>
        </ul>
      </li>
      <li style="margin-bottom: 0.3em;"><a href="#tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</a>
        <ul style="margin-top: 0.2em;">
          <li style="margin-bottom: 0.2em;"><a href="#example-1-direct-utility-value-sensitivity">Example 1: Direct Utility Value Sensitivity</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#example-2-test-cost-sensitivity">Example 2: Test Cost Sensitivity</a></li>
        </ul>
      </li>
      <li style="margin-bottom: 0.3em;"><a href="#interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface</a>
        <ul style="margin-top: 0.2em;">
          <li style="margin-bottom: 0.2em;"><a href="#implementation-overview">Implementation Overview</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#live-interactive-interface">Demo</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#conclusion-building-robust-decision-strategies">Conclusion</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#references">References</a></li>
</ul>

</details>

<h2 id="closing-the-loop">Closing the Loop</h2>

In [Part I](https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html), we explored the oil company's dilemma: should we buy the field or walk away? We used a decision tree to analyze the problem step by step, weighing probabilities and payoffs to determine the optimal choice. In [Part II](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html), we examined the limitations of decision trees and introduced influence diagrams as a more scalable alternative. We solved the same problem manually using influence diagrams, confirming that they yield the same result as decision trees.

But let's be honest, constantly redrawing diagrams and recalculating expected utilities every time geological estimates change or market conditions shift is not realistic. Real-world decision problems need tools that adapt quickly. That's what we'll build in this final part, focusing on two crucial questions:

1. **How do we actually implement these models in code?** We'll see how to recreate our oil field analysis using <a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a>, transforming those tedious manual calculations into just a few lines of Python.

2. **How much should we trust the model's recommendation?** Using sensitivity analysis, we'll discover whether our "buy the field" decision is robust to parameter changes. We'll build different types of visualizations and create an interactive <a href="https://www.gradio.app/"><code>Gradio</code></a> interface where we can adjust any parameter and immediately see the impact.

<h2 id="building-the-oil-field-limid-in-pyagrum">Building the Oil-Field LIMID in PyAgrum</h2>

<a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> is a Python wrapper around the C++ <a href="https://agrum.gitlab.io/pages/agrum.html"><code>aGrUM</code></a> library for building and solving probabilistic graphical models such as Bayesian networks, LIMIDs, causal networks, and more. With a few lines of Python code we can define the influence diagram's structure, add the probabilities and utilities, execute, and get the optimal policy. 

Let's now code the decision problem.

<h3 id="setting-up-the-network-structure">Setting Up the LIMID Structure</h3>

We start by importing <code>pyagrum</code> and creating an empty influence diagram. Then we add our four variables: oil field quality ($$\textcolor{purple}{Q}$$), test results ($$\textcolor{purple}{R}$$), the test decision ($$\textcolor{red}{T}$$), the buy decision ($$\textcolor{red}{B}$$), and a utility node ($$\textcolor{blue}{U}$$).

```python
import pyagrum as grum
from pyagrum import InfluenceDiagram

# Create the influence diagram
influence_diagram = InfluenceDiagram()

# Initialize with 0 states, then manually add the labels we need
Q = influence_diagram.addChanceNode(
    grum.LabelizedVariable("Q", "Q", 0).addLabel('high').addLabel('medium').addLabel('low'))
R = influence_diagram.addChanceNode(
    grum.LabelizedVariable("R", "R", 0).addLabel('pass').addLabel('fail').addLabel('no_results'))
T = influence_diagram.addDecisionNode(
    grum.LabelizedVariable("T", "T", 0).addLabel('do').addLabel('not_do'))
B = influence_diagram.addDecisionNode(
    grum.LabelizedVariable("B", "B", 0).addLabel('buy').addLabel('not_buy'))
U = influence_diagram.addUtilityNode("U")  # Utility node takes just a name
```

Next, we connect the nodes with arcs to capture the dependencies from our diagram. Notice the memory arc from $$\textcolor{red}{T}$$ to $$\textcolor{red}{B}$$ that transforms the diagram into a LIMID.

```python
# Add arcs to define dependencies
influence_diagram.addArc("T", "R")   
influence_diagram.addArc("T", "B")    # Memory arc: buy decision remembers test choice
influence_diagram.addArc("T", "U")    
influence_diagram.addArc("R", "B")
influence_diagram.addArc("B", "U")
influence_diagram.addArc("Q", "R")
influence_diagram.addArc("Q", "U")
```

<a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> makes it easy to visualize what we've built. We can generate a diagram directly from our code:

```python
import pyagrum.lib.notebook as gnb
from pyagrum.lib import image

# Display if run in Jupyter notebook
gnb.sideBySide(influence_diagram, captions=["Oil field influence diagram"])

# Or export to PNG for use elsewhere
image.export(influence_diagram, "influence_diagram.png")
```

Here's the resulting <code>influence_diagram.png</code>, the same LIMID from [Part II](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html).

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-08-07-decision-theory-III/1_limid_oil_pyagrum.png" alt="Visual representation of the oil field LIMID generated by PyAgrum" width="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Visual representation of the oil field LIMID generated by PyAgrum</i>
    </td>
  </tr>
</table>
</center>

<h3 id="filling-in-the-numbers">Filling in the Numbers</h3>

The network structure is just the skeleton. Now we need to populate it with the probabilities and utilities from our original problem. 

First, we set the prior probabilities for oil field quality:

```python
influence_diagram.cpt(Q)[:] = [0.35, 0.45, 0.2]  # high, medium, low
```

Next, we define how test results depend on both the true field quality and whether we actually perform the test:

```python
# When test is performed ('do')
influence_diagram.cpt(R)[{"Q": "high", "T": "do"}] = [0.95, 0.05, 0.0]    # pass, fail, no_results
influence_diagram.cpt(R)[{"Q": "medium", "T": "do"}] = [0.7, 0.3, 0.0]
influence_diagram.cpt(R)[{"Q": "low", "T": "do"}] = [0.15, 0.85, 0.0]

# When test is not performed ('not_do') - always get 'no_results'
influence_diagram.cpt(R)[{"Q": "high", "T": "not_do"}] = [0.0, 0.0, 1.0]
influence_diagram.cpt(R)[{"Q": "medium", "T": "not_do"}] = [0.0, 0.0, 1.0]
influence_diagram.cpt(R)[{"Q": "low", "T": "not_do"}] = [0.0, 0.0, 1.0]
```

Finally, we specify the utility values for each combination of decisions and outcomes. Note the $30M test cost when we choose to perform the test:

```python
import numpy as np

# Test performed: subtract $30M test cost from original values
influence_diagram.utility(U)[{"T": "do", "B": "buy"}] = np.array([1220, 600, -30])[:, np.newaxis]    # Q: high, medium, low
influence_diagram.utility(U)[{"T": "do", "B": "not_buy"}] = np.array([320, 320, 320])[:, np.newaxis]

# No test performed: original values
influence_diagram.utility(U)[{"T": "not_do", "B": "buy"}] = np.array([1250, 630, 0])[:, np.newaxis]
influence_diagram.utility(U)[{"T": "not_do", "B": "not_buy"}] = np.array([350, 350, 350])[:, np.newaxis]
```

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
The <code>[:, np.newaxis]</code> reshaping is used to align the data with the expected order of parent nodes. While not confirmed to be a universal PyAgrum requirement, this approach proved effective in this specific implementation.
</div>
<div style="height: 1.1em;"></div>

<h3 id="solving-the-network">Solving the Network</h3>

With structure and parameters in place, we can create an inference engine and solve the decision problem. In this case, we use the Shafer-Shenoy algorithm for LIMIDs (<a href="https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content"><u>Shafer & Shenoy, 1990</u></a>):

```python
# Create inference engine and solve
inference_engine = grum.ShaferShenoyLIMIDInference(influence_diagram)
inference_engine.makeInference()

print(f"Is the diagram solvable?: {inference_engine.isSolvable()}")
```

We can examine the optimal decision for each decision node. For example, the test decision ($$\textcolor{red}{T}$$):

```python
from IPython.display import display

optimal_decision_T = inference_engine.optimalDecision(T)

print(optimal_decision_T)
display(optimal_decision_T)
```

This outputs both a text representation and a formatted table in Jupyter notebooks:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-08-07-decision-theory-III/2_optimal_decision_t.png" alt="Optimal decision T displayed as text and table in PyAgrum" width="250">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 2.</b> Optimal decision for test variable T shown in both text and table format</i>
    </td>
  </tr>
</table>
</center>

We can also generate a visual representation of the solved network, showing the optimal decisions and expected utilities:

```python
# Note: On macOS, you may need this line to avoid cairo issues
import os
import pyagrum.lib.notebook as gnb

os.environ["DYLD_FALLBACK_LIBRARY_PATH"] = "/opt/homebrew/opt/cairo/lib"

# Visualize the solved network
gnb.showInference(influence_diagram, engine=inference_engine, size="6!")

# Or export the inference result as an image
image.exportInference(influence_diagram, "inference_result.png", engine=inference_engine)
```

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-08-07-decision-theory-III/3_inference_result.png" alt="Evaluated oil field LIMID generated by PyAgrum" width="500">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> Solved oil field LIMID showing optimal decisions and expected utilities</i>
    </td>
  </tr>
</table>
</center>

The results confirm our hand-written calculations: the optimal strategy is to skip the test and buy the field directly, with a maximum expected utility of 721 million dollars. What took us pages of manual calculations, <a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> solved in just 0.24 milliseconds.

<h2 id="testing-robustness-with-sensitivity-analysis">Testing Robustness with Sensitivity Analysis</h2>

Now that we've found the best strategy for buying the oil field, we may wonder: What happens if we got some of our numbers wrong? Maybe the geological survey isn't as accurate as we thought, or test costs could jump higher than expected. At what point do these changes actually matter for our decision?

This is exactly what sensitivity analysis helps us figure out. Once we have our optimal strategy, we need to test how much our answer depends on the specific numbers we plugged in. Some parameters might barely affect our decision, while others could completely flip our recommendation with just small changes.

We'll tackle this challenge with three complementary approaches:

1. **Single-parameter sweeps**: Vary one parameter at a time to see how the expected utility changes, helping us understand individual parameter sensitivity.

2. **Tornado diagrams**: Create visual summaries that show which variables have the most impact on our decision, sorted by magnitude of influence.

3. **Interactive Gradio interface**: Build a web app where we can change multiple parameters simultaneously, and instantly see how the optimal decision and expected utility respond.

<h3 id="single-parameter-sensitivity-analysis">Single Parameter Sensitivity Analysis</h3>

Single parameter sensitivity analysis examines how changes in one specific parameter affect 
the optimal decision and expected utility while keeping all other parameters constant. This 
approach is particularly valuable because it:

- **Identifies critical thresholds**: We can discover specific values where the optimal decision changes.
- **Guides data collection**: Parameters with high sensitivity may warrant additional 
research or more precise estimation.

Let's apply this to two key parameters in our oil field problem.

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<a href="https://github.com/ferjorosa/decision-theory-llms/tree/main/decision_problems/oil_field_purchase/sensitivity_analysis">You can find  the complete source code for this implementation on GitHub</a>
</div>
<div style="height: 1.1em;"></div>

<h4 id="example-1-prior-probability-of-high-quality-fields">Example 1: Prior Probability of High-quality Fields</h4>

Our first analysis explores how varying the prior probability that a field is high quality influences our decision strategy. Beginning with the baseline value $$P(\textcolor{purple}{Q}=\textcolor{purple}{\text{high}}) = 0.35$$, we adjust this probability by $$\pm0.15$$ in increments of $$0.05$$, producing seven scenarios. The probabilities of the remaining quality categories are rescaled proportionally so that the distribution still sums to one.


<center>
<table>
  <tr>
    <td align="center">
      <div id="q-cpt-sensitivity-plot" class="plotly-graph-div" style="height:500px; width:100%; max-width:700px;"></div>
      <script type="text/javascript">
      // Ensure syntax highlighting is preserved before creating Plotly chart
      document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit to ensure syntax highlighting is stable
        setTimeout(function() {
          if (typeof Plotly !== 'undefined') {
            window.PLOTLYENV = window.PLOTLYENV || {};
            Plotly.newPlot(
              "q-cpt-sensitivity-plot",
              [{"hovertemplate":"%{hovertext}<extra></extra>","hovertext":["Parameter: 0.200<br>MEU: 598.9<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.250<br>MEU: 639.6<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.300<br>MEU: 680.3<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.350<br>MEU: 721.0<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.400<br>MEU: 761.7<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.450<br>MEU: 802.4<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.500<br>MEU: 843.1<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]"],"line":{"color":"steelblue","width":3},"marker":{"color":"steelblue","line":{"color":"navy","width":2},"size":12},"mode":"markers+lines","name":"Sensitivity Analysis","x":[598.9230769230769,639.6153846153846,680.3076923076924,721.0,761.6923076923076,802.3846153846154,843.0769230769231],"y":[0.19999999999999998,0.24999999999999997,0.3,0.35,0.39999999999999997,0.44999999999999996,0.5],"type":"scatter"}],
              {"template":{"data":{"barpolar":[{"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"#C8D4E3","linecolor":"#C8D4E3","minorgridcolor":"#C8D4E3","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"#C8D4E3","linecolor":"#C8D4E3","minorgridcolor":"#C8D4E3","startlinecolor":"#2a3f5f"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scattermap":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermap"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"white","showlakes":true,"showland":true,"subunitcolor":"#C8D4E3"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"white","polar":{"angularaxis":{"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":""},"bgcolor":"white","radialaxis":{"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"},"yaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"},"zaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"ternary":{"aaxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""},"baxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""},"bgcolor":"white","caxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":"","title":{"standoff":15},"zerolinecolor":"#EBF0F8","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":"","title":{"standoff":15},"zerolinecolor":"#EBF0F8","zerolinewidth":2}}},"annotations":[{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"598.9","x":598.9230769230769,"xshift":15,"y":0.19999999999999998,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"639.6","x":639.6153846153846,"xshift":15,"y":0.24999999999999997,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"680.3","x":680.3076923076924,"xshift":15,"y":0.3,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"721.0","x":721.0,"xshift":15,"y":0.35,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"761.7","x":761.6923076923076,"xshift":15,"y":0.39999999999999997,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"802.4","x":802.3846153846154,"xshift":15,"y":0.44999999999999996,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"843.1","x":843.0769230769231,"xshift":15,"y":0.5,"yshift":5},{"showarrow":false,"text":"Baseline MEU: 721.0","x":721.0,"xanchor":"center","xref":"x","y":1,"yanchor":"bottom","yref":"y domain"}],"shapes":[{"line":{"color":"red","dash":"dash"},"type":"line","x0":721.0,"x1":721.0,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"title":{"text":"Sensitivity Analysis: P(Q=high) vs MEU"},"xaxis":{"title":{"text":"Maximum Expected Utility (MEU)"}},"yaxis":{"title":{"text":"P(Q=high)"}},"width":700,"height":500,"showlegend":false},
              {"responsive": true}
            );
          }
        }, 200); // Small delay to let syntax highlighting settle
      });
      </script>
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 4.</b> Sensitivity analysis of prior probability P(Q=high) showing the relationship between field quality expectations and maximum expected utility</i>
    </td>
  </tr>
</table>
</center>

These changes definitely affect how much money we expect to make, but they don't change the optimal policy: skip the test and buy the field directly. This makes sense when you think about it: knowing that fields in this region are more likely to be high quality affects our expected profits, but it doesn't change how useful the test would be.

<h4 id="example-2-test-precision-for-medium-quality-fields">Example 2: Test Precision for Medium-quality Fields</h4>

For our second analysis, let's look at the geological test's accuracy, specifically focusing on its ability to correctly identify medium-quality fields. Medium-quality fields are particularly interesting because they are profitable but seem easy to mistake for 
low-grade ones.

What if we could improve the test to better identify these medium-quality fields? We'll vary the test's pass rate for true medium fields $$P(\textcolor{purple}{R}=\textcolor{purple}{\text{pass}} \mid \textcolor{purple}{Q}=\textcolor{purple}{\text{medium}})$$ from $$0.70$$ to $$0.95$$ to see when the improved accuracy makes testing worthwhile.

<center>
<table>
  <tr>
    <td align="center">
      <div id="r-cpt-sensitivity-plot" class="plotly-graph-div" style="height:500px; width:100%; max-width:700px;"></div>
      <script type="text/javascript">
      // Ensure syntax highlighting is preserved before creating second Plotly chart
      document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit longer to ensure first plot and syntax highlighting are stable
        setTimeout(function() {
          if (typeof Plotly !== 'undefined') {
            window.PLOTLYENV = window.PLOTLYENV || {};
            Plotly.newPlot(
              "r-cpt-sensitivity-plot",
              [{"hovertemplate":"%{hovertext}<extra></extra>","hovertext":["Parameter: 0.700<br>MEU: 721.0<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.750<br>MEU: 721.0<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.800<br>MEU: 721.0<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.850<br>MEU: 721.0<br>T: not_do<br>B: [R=pass→buy, R=fail→buy, R=no_results→buy]","Parameter: 0.900<br>MEU: 722.1<br>T: do<br>B: [R=pass→buy, R=fail→not_buy, R=no_results→buy]","Parameter: 0.950<br>MEU: 728.5<br>T: do<br>B: [R=pass→buy, R=fail→not_buy, R=no_results→buy]"],"line":{"color":"steelblue","width":3},"marker":{"color":"steelblue","line":{"color":"navy","width":2},"size":12},"mode":"markers+lines","name":"Sensitivity Analysis","x":[721.0,721.0,721.0,721.0,722.15,728.45],"y":[0.7,0.75,0.7999999999999999,0.85,0.8999999999999999,0.95],"type":"scatter"}],
              {"template":{"data":{"barpolar":[{"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"white","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"#C8D4E3","linecolor":"#C8D4E3","minorgridcolor":"#C8D4E3","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"#C8D4E3","linecolor":"#C8D4E3","minorgridcolor":"#C8D4E3","startlinecolor":"#2a3f5f"},"type":"carpet"}],"choropleth":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"choropleth"}],"contourcarpet":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"contourcarpet"}],"contour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"contour"}],"heatmap":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"heatmap"}],"histogram2dcontour":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2dcontour"}],"histogram2d":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"histogram2d"}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"mesh3d":[{"colorbar":{"outlinewidth":0,"ticks":""},"type":"mesh3d"}],"parcoords":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"parcoords"}],"pie":[{"automargin":true,"type":"pie"}],"scatter3d":[{"line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatter3d"}],"scattercarpet":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattercarpet"}],"scattergeo":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergeo"}],"scattergl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattergl"}],"scattermapbox":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermapbox"}],"scattermap":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scattermap"}],"scatterpolargl":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolargl"}],"scatterpolar":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterpolar"}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"scatterternary":[{"marker":{"colorbar":{"outlinewidth":0,"ticks":""}},"type":"scatterternary"}],"surface":[{"colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"type":"surface"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}]},"layout":{"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"autotypenumbers":"strict","coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]],"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]},"colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"geo":{"bgcolor":"white","lakecolor":"white","landcolor":"white","showlakes":true,"showland":true,"subunitcolor":"#C8D4E3"},"hoverlabel":{"align":"left"},"hovermode":"closest","mapbox":{"style":"light"},"paper_bgcolor":"white","plot_bgcolor":"white","polar":{"angularaxis":{"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":""},"bgcolor":"white","radialaxis":{"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":""}},"scene":{"xaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"},"yaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"},"zaxis":{"backgroundcolor":"white","gridcolor":"#DFE8F3","gridwidth":2,"linecolor":"#EBF0F8","showbackground":true,"ticks":"","zerolinecolor":"#EBF0F8"}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"ternary":{"aaxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""},"baxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""},"bgcolor":"white","caxis":{"gridcolor":"#DFE8F3","linecolor":"#A2B1C6","ticks":""}},"title":{"x":0.05},"xaxis":{"automargin":true,"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":"","title":{"standoff":15},"zerolinecolor":"#EBF0F8","zerolinewidth":2},"yaxis":{"automargin":true,"gridcolor":"#EBF0F8","linecolor":"#EBF0F8","ticks":"","title":{"standoff":15},"zerolinecolor":"#EBF0F8","zerolinewidth":2}}},"annotations":[{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"721.0","x":721.0,"xshift":15,"y":0.7,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"721.0","x":721.0,"xshift":15,"y":0.75,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"721.0","x":721.0,"xshift":15,"y":0.7999999999999999,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"721.0","x":721.0,"xshift":15,"y":0.85,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"722.1","x":722.15,"xshift":15,"y":0.8999999999999999,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"728.5","x":728.45,"xshift":15,"y":0.95,"yshift":5},{"bgcolor":"rgba(255,255,255,0.8)","bordercolor":"black","borderwidth":1,"font":{"color":"black","size":10},"showarrow":false,"text":"Baseline MEU: 721.0","x":721.0,"xanchor":"center","xref":"x","y":1,"yanchor":"bottom","yref":"y domain"}],"shapes":[{"line":{"color":"red","dash":"dash"},"type":"line","x0":721.0,"x1":721.0,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"title":{"text":"Sensitivity Analysis: P(R=pass | Q=medium) vs MEU"},"xaxis":{"title":{"text":"Maximum Expected Utility (MEU)"}},"yaxis":{"title":{"text":"P(R=pass | Q=medium)"}},"width":700,"height":500,"showlegend":false},
              {"responsive": true}
            );
          }
        }, 400); // Longer delay for second plot to let first one settle
      });
      </script>
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 5.</b> Sensitivity analysis of test precision P(R=pass | Q=medium) showing when improved test accuracy makes testing worthwhile</i>
    </td>
  </tr>
</table>
</center>

Interestingly, once the test becomes good enough at spotting medium-quality fields (achieving $$0.9$$ accuracy or better), testing suddenly becomes worth the cost. The takeaway is clear: if we can upgrade our testing technology to correctly identify medium-quality fields at least 90% of the time, we should start using the test before making purchase decisions.

<h3 id="tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</h3>

While single parameter analysis tells us how each variable affects our decision, <a href="https://en.wikipedia.org/wiki/Tornado_diagram"><u>tornado diagrams</u></a> give us the big picture by ranking all parameters by their **individual** impact. These charts get their name from their shape: wide at the top for the most important variables and narrow at the bottom for the least important.

These diagrams are particularly valuable when we have formulas that define the utilities. For instance, if our utility numbers depended on a formula based on factors like drilling costs, oil prices, or project timelines, a tornado diagram would easily show us whether a 10% change in oil prices matters more than a 20% change in drilling costs.

For our oil field problem, we'll look at two examples to see how this works.

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<a href="https://github.com/ferjorosa/decision-theory-llms/tree/main/decision_problems/oil_field_purchase/sensitivity_analysis">You can find  the complete source code for this implementation on GitHub</a>
</div>
<div style="height: 1.1em;"></div>

<h4 id="example-1-direct-utility-value-sensitivity">Example 1: Direct Utility Value Sensitivity</h4>

Our first tornado analysis examines how changes in the direct utility values affect the maximum expected utility. We test each utility parameter by applying a $$\pm100$$ million dollar variation while keeping all other parameters constant.

<center>
<table>
  <tr>
    <td align="center">
      <div id="tornado-plot-utility" class="plotly-graph-div" style="height:500px; width:100%; max-width:700px;"></div>
      <script type="text/javascript">
      // Ensure syntax highlighting is preserved before creating tornado plot
      document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit longer to ensure previous plots and syntax highlighting are stable
        setTimeout(function() {
          if (typeof Plotly !== 'undefined') {
            window.PLOTLYENV = window.PLOTLYENV || {};
            Plotly.newPlot(
              "tornado-plot-utility",
              [{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"Lower Impact","offsetgroup":"1","orientation":"h","showlegend":true,"width":0.6,"x":[-24.049999999999955],"y":["U(not_do, buy, medium)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"Higher Impact","offsetgroup":"1","orientation":"h","showlegend":true,"width":0.6,"x":[45.0],"y":["U(not_do, buy, medium)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, medium)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 696.95\u003cbr\u003e\n        Impact: -24.05\u003cbr\u003e\n        Optimal Decisions: T: do, B: [pass: buy, fail: not_buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[-12.024999999999977],"y":["U(not_do, buy, medium)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, medium)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 766.00\u003cbr\u003e\n        Impact: +45.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[22.5],"y":["U(not_do, buy, medium)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[-24.049999999999955],"y":["U(not_do, buy, high)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[35.0],"y":["U(not_do, buy, high)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, high)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 696.95\u003cbr\u003e\n        Impact: -24.05\u003cbr\u003e\n        Optimal Decisions: T: do, B: [pass: buy, fail: not_buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[-12.024999999999977],"y":["U(not_do, buy, high)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, high)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 756.00\u003cbr\u003e\n        Impact: +35.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[17.5],"y":["U(not_do, buy, high)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[-20.0],"y":["U(not_do, buy, low)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[20.0],"y":["U(not_do, buy, low)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, low)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 701.00\u003cbr\u003e\n        Impact: -20.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[-10.0],"y":["U(not_do, buy, low)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, buy, low)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 741.00\u003cbr\u003e\n        Impact: +20.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[10.0],"y":["U(not_do, buy, low)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(do, buy, medium)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[15.0],"y":["U(do, buy, medium)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, medium)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(do, buy, medium)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, medium)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 736.00\u003cbr\u003e\n        Impact: +15.00\u003cbr\u003e\n        Optimal Decisions: T: do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[7.5],"y":["U(do, buy, medium)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(do, buy, high)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[9.200000000000045],"y":["U(do, buy, high)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, high)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(do, buy, high)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, high)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 730.20\u003cbr\u003e\n        Impact: +9.20\u003cbr\u003e\n        Optimal Decisions: T: do, B: [pass: buy, fail: not_buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[4.600000000000023],"y":["U(do, buy, high)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(do, not_buy)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[8.200000000000045],"y":["U(do, not_buy)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, not_buy)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(do, not_buy)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, not_buy)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 729.20\u003cbr\u003e\n        Impact: +8.20\u003cbr\u003e\n        Optimal Decisions: T: do, B: [pass: buy, fail: not_buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[4.100000000000023],"y":["U(do, not_buy)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(do, buy, low)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(do, buy, low)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, low)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(do, buy, low)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(do, buy, low)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(do, buy, low)"],"type":"scatter"},{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(not_do, not_buy)"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"","offsetgroup":"1","orientation":"h","showlegend":false,"width":0.6,"x":[0.0],"y":["U(not_do, not_buy)"],"type":"bar"},{"hoverlabel":{"bgcolor":"lightcoral","bordercolor":"darkred","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, not_buy)\u003cbr\u003e\n        High Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(not_do, not_buy)"],"type":"scatter"},{"hoverlabel":{"bgcolor":"lightblue","bordercolor":"darkblue","font":{"color":"black"}},"hovertemplate":"\n        Variable: U(not_do, not_buy)\u003cbr\u003e\n        Low Scenario\u003cbr\u003e\n        MEU: 721.00\u003cbr\u003e\n        Impact: +0.00\u003cbr\u003e\n        Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n        \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["U(not_do, not_buy)"],"type":"scatter"}],
              {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"annotations":[{"font":{"size":10},"showarrow":false,"text":"-24.0","x":-26.45499999999995,"xanchor":"right","y":"U(not_do, buy, medium)"},{"font":{"size":10},"showarrow":false,"text":"45.0","x":49.5,"xanchor":"left","y":"U(not_do, buy, medium)"},{"font":{"size":10},"showarrow":false,"text":"-24.0","x":-26.45499999999995,"xanchor":"right","y":"U(not_do, buy, high)"},{"font":{"size":10},"showarrow":false,"text":"35.0","x":38.5,"xanchor":"left","y":"U(not_do, buy, high)"},{"font":{"size":10},"showarrow":false,"text":"-20.0","x":-22.0,"xanchor":"right","y":"U(not_do, buy, low)"},{"font":{"size":10},"showarrow":false,"text":"20.0","x":22.0,"xanchor":"left","y":"U(not_do, buy, low)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"U(do, buy, medium)"},{"font":{"size":10},"showarrow":false,"text":"15.0","x":16.5,"xanchor":"left","y":"U(do, buy, medium)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"U(do, buy, high)"},{"font":{"size":10},"showarrow":false,"text":"9.2","x":10.12000000000005,"xanchor":"left","y":"U(do, buy, high)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"U(do, not_buy)"},{"font":{"size":10},"showarrow":false,"text":"8.2","x":9.02000000000005,"xanchor":"left","y":"U(do, not_buy)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"U(do, buy, low)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":1.0,"xanchor":"right","y":"U(do, buy, low)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"U(not_do, not_buy)"},{"font":{"size":10},"showarrow":false,"text":"0.0","x":1.0,"xanchor":"right","y":"U(not_do, not_buy)"}],"shapes":[{"line":{"color":"black","width":2},"type":"line","x0":0,"x1":0,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"title":{"font":{"size":16},"text":"Oil Field Purchase: Utility Sensitivity Analysis (Constant Variation)\u003cbr\u003e\u003csub\u003eBaseline Expected Utility: 721.00 | Utility values varied by ±100 units\u003c\u002fsub\u003e"},"xaxis":{"title":{"text":"Change in Expected Utility from Baseline"},"gridcolor":"lightgray","gridwidth":0.5,"zeroline":true,"zerolinecolor":"black","zerolinewidth":2},"yaxis":{"title":{"text":"Utility Variables"},"categoryorder":"array","categoryarray":["U(not_do, not_buy)","U(do, buy, low)","U(do, not_buy)","U(do, buy, high)","U(do, buy, medium)","U(not_do, buy, low)","U(not_do, buy, high)","U(not_do, buy, medium)"]},"legend":{"orientation":"h","yanchor":"bottom","y":1.02,"xanchor":"right","x":1},"width":700,"height":500,"bargap":0.1,"bargroupgap":0,"hovermode":"closest"},
              {"responsive": true}
            );
          }
        }, 400); // Delay for tornado plot to let previous ones settle
      });
      </script>
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 6.</b> Tornado diagram showing the impact of utility value variations on maximum expected utility</i>
    </td>
  </tr>
</table>
</center>

The analysis reveals that $$\textcolor{blue}{U}(\textcolor{red}{T} = \textcolor{red}{\text{not_do}},\ \textcolor{red}{B} = \textcolor{red}{\text{buy}},\ \textcolor{purple}{Q} = \textcolor{purple}{\text{medium}})$$ has the largest impact on our decision. This makes intuitive sense, since medium-quality fields have the highest prior probability ($$0.45$$), so changes to their utility values disproportionately affect the overall expected utility.

Changes to utilities involving testing ($$\textcolor{red}{T} = \textcolor{red}{\text{do}}$$ scenarios) have smaller impacts because testing is already suboptimal in our baseline analysis. These utility values would need to change enough to flip the optimal strategy from $$\textcolor{red}{\text{not_do}}$$ to $$\textcolor{red}{\text{do}}$$ before they could significantly affect the final result.

However, it's worth noting that while tornado diagrams can technically be applied to any parameter, **they're most meaningful when applied to underlying variables** that feed into the model through formulas rather than direct utility assignments.

<h4 id="example-2-test-cost-sensitivity">Example 2: Test Cost Sensitivity</h4>

Our second tornado analysis examines how changes in test cost affect the maximum expected utility. This variable would realistically vary based on market conditions, technology improvements, or operational 
factors. We evaluate the test cost parameter by applying a $$\pm25$$ million dollar variation while keeping all other parameters constant.

<center>
<table>
  <tr>
    <td align="center">
      <div id="tornado-plot-utility-test-cost" class="plotly-graph-div" style="height:400px; width:100%; max-width:700px;"></div>
      <script type="text/javascript">
      // Ensure syntax highlighting is preserved before creating test cost tornado plot
      document.addEventListener('DOMContentLoaded', function() {
        // Wait a bit longer to ensure previous plots and syntax highlighting are stable
        setTimeout(function() {
          if (typeof Plotly !== 'undefined') {
            window.PLOTLYENV = window.PLOTLYENV || {};
            Plotly.newPlot(
              "tornado-plot-utility-test-cost",
              [{"hoverinfo":"skip","marker":{"color":"lightcoral","line":{"color":"black","width":0.5}},"name":"Lower Impact","offsetgroup":"1","orientation":"h","width":0.6,"x":[0.0],"y":["Test Cost"],"type":"bar"},{"hoverinfo":"skip","marker":{"color":"lightblue","line":{"color":"black","width":0.5}},"name":"Higher Impact","offsetgroup":"1","orientation":"h","width":0.6,"x":[0.9500000000000455],"y":["Test Cost"],"type":"bar"},{"hovertemplate":"\n    Variable: Test Cost\u003cbr\u003e\n    High Cost (Cost: +25)\u003cbr\u003e\n    MEU: 721.00\u003cbr\u003e\n    Impact: +0.00\u003cbr\u003e\n    Optimal Decisions: T: not_do, B: [pass: buy, fail: buy, no_results: buy]\n    \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.0],"y":["Test Cost"],"type":"scatter"},{"hovertemplate":"\n    Variable: Test Cost\u003cbr\u003e\n    Low Cost (Cost: -25)\u003cbr\u003e\n    MEU: 721.95\u003cbr\u003e\n    Impact: +0.95\u003cbr\u003e\n    Optimal Decisions: T: do, B: [pass: buy, fail: not_buy, no_results: buy]\n    \u003cextra\u003e\u003c\u002fextra\u003e","marker":{"color":"rgba(0,0,0,0)","size":0.1},"mode":"markers","name":"","showlegend":false,"x":[0.47500000000002274],"y":["Test Cost"],"type":"scatter"}],
              {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"}}},"annotations":[{"font":{"size":12},"showarrow":false,"text":"0.0","x":-1.0,"xanchor":"left","y":"Test Cost"},{"font":{"size":12},"showarrow":false,"text":"1.0","x":1.0450000000000501,"xanchor":"left","y":"Test Cost"}],"shapes":[{"line":{"color":"black","width":2},"type":"line","x0":0,"x1":0,"xref":"x","y0":0,"y1":1,"yref":"y domain"}],"title":{"font":{"size":16},"text":"Test Cost Tornado Diagram\u003cbr\u003e\u003csub\u003eBaseline Expected Utility: 721.00 | Test cost varied by ±25 units\u003c\u002fsub\u003e"},"xaxis":{"title":{"text":"Change in Expected Utility from Baseline"},"gridcolor":"lightgray","gridwidth":0.5,"zeroline":true,"zerolinecolor":"black","zerolinewidth":2},"yaxis":{"title":{"text":"Variable"},"showticklabels":true},"legend":{"orientation":"h","yanchor":"bottom","y":1.02,"xanchor":"right","x":1},"width":700,"height":400,"bargap":0.1,"bargroupgap":0,"hovermode":"closest"},
              {"responsive": true}
            );
          }
        }, 600); // Longer delay for third plot to let previous ones settle
      });
      </script>
    </td>
  </tr>
  <tr>
    <td align="center">
      <i><b>Figure 7.</b> Tornado diagram showing the impact of test cost variations on maximum expected utility</i>
    </td>
  </tr>
</table>
</center>

The diagram shows that test cost has a limited impact on our decision strategy. Even with a substantial 83% cost reduction (from $30M to $5M), the optimal strategy remains virtually unchanged: the MEU increases from 721 million (not testing) to only 721.95 million (testing when it costs $5M), representing a marginal 0.13% improvement.

This suggests that **cost reduction alone is insufficient** to make testing attractive. To meaningfully shift our strategy toward testing, we would likely need either significant improvements in test reliability (as demonstrated in Example 2 of the single-parameter analysis) or a combination of cost reduction paired with enhanced test accuracy.

<h3 id="interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface</h3>

<a href="https://www.gradio.app/"><code>Gradio</code></a> is an open-source Python library that lets you turn any machine-learning model, API, or plain Python function into a shareable web app in minutes. With its built-in hosting and share links, you can demo your project without writing a single line of JavaScript, CSS, or backend code.

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-08-07-decision-theory-III/gradio-gif.gif" alt="Gradio example" width="800">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 8.</b> Gradio example for image generation</i>
    </td>
  </tr>
</table>
</center>

Although <a href="https://www.gradio.app/"><code>Gradio</code></a> first became popular for showcasing large-language-model and image-generation demos on Hugging Face Spaces, its simplicity is just as useful here. We'll use the same drag-and-drop interface to create an interactive decision-analysis tool, proving that <a href="https://www.gradio.app/"><code>Gradio</code></a>'s convenience extends well beyond mainstream ML examples.

Single-parameter analyses and tornado diagrams show how each variable influences the model on its own. Real decisions, however, often involve several factors moving at once. To explore those multi-parameter scenarios, we can pair PyAgrum's visualisation tools (see Figure 3) with <a href="https://www.gradio.app/"><code>Gradio</code></a>'s simple web-app builder to create an interactive playground.

An interactive app brings two key advantages:
- **Real-time exploration**: Adjust several parameters at once and immediately see how the optimal decision and expected utility change.
- **No technical hurdles**: Executives and domain experts can experiment freely without touching the underlying PyAgrum code.

<h4 id="implementation-overview">Implementation Overview</h4>

I have built a <a href="https://www.gradio.app/"><code>Gradio</code></a> app with three editable input tables: $$\textcolor{purple}{Q}$$, $$\textcolor{purple}{R}$$ and $$\textcolor{blue}{U}$$. It then returns:

- **Visual influence diagram** with the optimal decision and MEU
- **Decision summary** providing clear, natural language recommendations

Here's the high-level structure of the code:

```python
import gradio as gr
import pyagrum as gum
import pandas as pd

q_cpt = pd.DataFrame({
    "Q": ["high", "medium", "low"],
    "Probability": [0.35, 0.45, 0.2]
})

r_cpt  = pd.DataFrame(
  ...
)

u_table = pd.DataFrame(
  ...
)

def analyze_decision(q_probabilities, r_probabilities, utilities):
    # Create influence diagram with user parameters
    influence_diagram = create_influence_diagram(q_probabilities, r_probabilities, utilities)
    
    # Solve using PyAgrum inference engine  
    inference_engine = gum.ShaferShenoyLIMIDInference(influence_diagram)
    inference_engine.makeInference()
    
    # Generate visualization and recommendations
    diagram_image = generate_diagram_visualization(influence_diagram, inference_engine)
    decision_summary = generate_policy_summary(influence_diagram, inference_engine)
    
    return diagram_image, decision_summary

# Create Gradio interface with interactive components
with gr.Blocks() as demo:
    # Input components for probabilities and utilities
    q_input = gr.Dataframe(label="Oil Field Quality Probabilities")
    r_input = gr.Dataframe(label="Test Result Probabilities") 
    u_input = gr.Dataframe(label="Utility Values")
    
    # Output components
    diagram_output = gr.Image(label="Influence Diagram")
    summary_output = gr.Textbox(label="Decision Recommendations")
    
    # Connect inputs to analysis function
    calculate_btn = gr.Button("Calculate Optimal Decision")
    calculate_btn.click(analyze_decision, 
                       inputs=[q_input, r_input, u_input],
                       outputs=[diagram_output, summary_output])

demo.launch(share=True)
```

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
<a href="https://github.com/ferjorosa/decision-theory-llms/tree/main/decision_problems/oil_field_purchase/gradio_app">You can find  the complete source code for this implementation on GitHub</a>
</div>
<div style="height: 1.1em;"></div>

<h4 id="live-interactive-interface">Demo</h4>

I have deployed the Gradio application using HuggingFace Spaces. Try adjusting different parameters to see how they affect the optimal strategy and expected utility:

<div style="background-color: #e0f7fa; padding: 10px; border-radius: 5px;">
If after 10 seconds or so you don't see the loaded application, you can go here and restart the space. It is a public HuggingFace space so you dont need permissions to restart it.
</div>
<div style="height: 1.1em;"></div>

<script type="text/javascript">
// Preserve page formatting and prevent Gradio CSS interference
function preservePageFormatting() {
  // Store original styles for key elements
  var originalStyles = new Map();
  
  // Elements to protect from Gradio CSS changes
  var protectedSelectors = [
    '.post-content p',
    '.post-content h1, .post-content h2, .post-content h3, .post-content h4, .post-content h5, .post-content h6',
    '.post-content li',
    '.post-content blockquote',
    '.highlight',
    'body'
  ];
  
  // Store original computed styles
  protectedSelectors.forEach(function(selector) {
    var elements = document.querySelectorAll(selector);
    elements.forEach(function(element) {
      var computedStyle = window.getComputedStyle(element);
      originalStyles.set(element, {
        lineHeight: computedStyle.lineHeight,
        fontSize: computedStyle.fontSize,
        fontFamily: computedStyle.fontFamily,
        margin: computedStyle.margin,
        padding: computedStyle.padding
      });
    });
  });
  
  // Store highlighted code blocks and their HTML
  var highlightedBlocks = document.querySelectorAll('.highlight');
  var preservedHTML = [];
  
  highlightedBlocks.forEach(function(block, index) {
    preservedHTML[index] = block.innerHTML;
  });
  
  // Function to restore both syntax highlighting and original formatting
  function restoreFormatting() {
    // Restore syntax highlighting
    var currentBlocks = document.querySelectorAll('.highlight');
    currentBlocks.forEach(function(block, index) {
      if (preservedHTML[index] && block.innerHTML !== preservedHTML[index]) {
        block.innerHTML = preservedHTML[index];
      }
    });
    
    // Restore original styles
    originalStyles.forEach(function(styles, element) {
      if (document.contains(element)) {
        element.style.lineHeight = styles.lineHeight;
        element.style.fontSize = styles.fontSize;
        element.style.fontFamily = styles.fontFamily;
        // Only restore margin/padding if significantly changed
        var currentStyle = window.getComputedStyle(element);
        if (Math.abs(parseFloat(currentStyle.margin) - parseFloat(styles.margin)) > 5) {
          element.style.margin = styles.margin;
        }
      }
    });
  }
  
  return restoreFormatting;
}

// Isolate Gradio loading and prevent CSS conflicts
function loadGradioIsolated() {
  // Create shadow DOM for better isolation (if supported)
  var container = document.getElementById('gradio-container');
  
  // Add extra protection class
  container.classList.add('gradio-isolated');
  
  // Create style isolation
  var isolationStyle = document.createElement('style');
  isolationStyle.textContent = `
    .gradio-isolated {
      /* Create containment boundary */
      contain: layout style;
      /* Isolate font changes */
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      /* Reset line height */
      line-height: 1.4;
    }
    
    /* Prevent Gradio from affecting parent elements */
    .gradio-isolated * {
      box-sizing: border-box;
    }
    
    /* Additional protection for surrounding content */
    body:not(.gradio-isolated) .post-content {
      line-height: 1.6 !important;
      font-family: inherit !important;
    }
  `;
  
  document.head.appendChild(isolationStyle);
  
  // Load Gradio with isolation
  var script = document.createElement('script');
  script.type = 'module';
  script.src = 'https://gradio.s3-us-west-2.amazonaws.com/5.31.0/gradio.js';
  
  // Apply additional isolation on load
  script.onload = function() {
    var gradioApp = document.createElement('gradio-app');
    gradioApp.setAttribute('src', 'https://ferjorosa-oil-field-purchase-decision.hf.space');
    container.appendChild(gradioApp);
    
    // Apply final isolation styles
    setTimeout(function() {
      gradioApp.style.contain = 'layout style';
      gradioApp.style.isolation = 'isolate';
    }, 100);
  };
  
  document.head.appendChild(script);
}

// Wait for page to be fully loaded
window.addEventListener('load', function() {
  setTimeout(function() {
    // Preserve page formatting first
    var restoreFunction = preservePageFormatting();
    
    // Load Gradio with isolation
    loadGradioIsolated();
    
    // Monitor and restore formatting periodically
    var restoreInterval = setInterval(restoreFunction, 200);
    
    // Stop aggressive restoration after 15 seconds
    setTimeout(function() {
      clearInterval(restoreInterval);
      // Do a final restoration
      restoreFunction();
    }, 15000);
    
    // Also restore on window resize (common trigger for style changes)
    window.addEventListener('resize', restoreFunction);
    
  }, 500);
});
</script>

<div id="gradio-container"></div>

<h2 id="conclusion-building-robust-decision-strategies">Conclusion</h2>

This post concludes our introductory series on decision theory. We've explored everything from manual decision trees to programmatic influence diagrams, demonstrating how <a href="https://pyagrum.readthedocs.io"><code>PyAgrum</code></a> can solve real-world problems in milliseconds. More importantly, we've shown how sensitivity analysis helps us test whether our decisions are truly robust.

We covered three key approaches: single-parameter analysis, tornado diagrams, and <a href="https://www.gradio.app/"><code>Gradio</code></a> interfaces, each serving a unique purpose. Through these methods, we uncovered an important insight: while changing parameters often affects expected utilities, it doesn’t always change the optimal decision. Recognizing the difference between sensitivity in outcomes and sensitivity in decisions is crucial for practical decision-making.

Looking ahead, **I'm optimistic about integrating Large Language Models (LLMs) with influence diagrams** to enhance decision-making. Here's how this could unfold:

* **Short-term goal**: Combine LLMs with predefined influence diagrams to improve decision quality, helping generate more rational and data-driven choices.

* **Long-term goal**: Enable LLMs to automatically build decision models from natural language descriptions, generate sensitivity analysis code, and highlight the most critical parameters based on domain expertise.

We’ll dive deeper into these possibilities in a future post, so stay tuned!

<h2 id="references">References</h2>
1. Rodriguez, F. (2025, June 8). <a href="https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html">Introduction to decision theory: Part I</a>. 
<br><br>
1. Rodriguez, F. (2025, July 4). <a href="https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html">Introduction to decision theory: Part II</a>. 
<br><br>
1. Shafer, G., & Shenoy, P. P. (1990). <a href="https://kuscholarworks.ku.edu/server/api/core/bitstreams/c353aa52-11ad-46c0-b867-f5d05f7f1962/content"><u>Probability Propagation</u></a>. Annals of Mathematics and Artificial Intelligence, 2, 327-352.
<br><br>
1. Wikipedia article on <a href="https://en.wikipedia.org/wiki/Tornado_diagram"><u>tornado diagrams</u></a>.

---
layout: post
title: "Introduction to Decision Theory: Part III"
date: 2025-07-15
categories: blog
description: "Deep dive into sensitivity analysis for decision problems, implementing the oil field purchase decision using PyAgrum's library, and creating an interactive web interface with Gradio to explore how changes in probabilities and utilities affect optimal decisions."
tags: [Decision Theory]
---

<details style="margin: 1em 0; padding: 0.5em; border: 1px solid #ddd; border-radius: 4px;">
<summary style="cursor: pointer; font-weight: bold; padding: 0.5em;">Table of Contents</summary>

<ul style="margin-top: 0.5em;">
  <li style="margin-bottom: 0.5em;"><a href="#closing-the-loop">Closing the Loop</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#building-the-oil-field-limid-in-pyagrum">Building the Oil-Field LIMID in PyAgrum</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#testing-robustness-with-deterministic-sensitivity-analysis">Testing Robustness with Deterministic Sensitivity Analysis</a></li>
</ul>

</details>

## Closing the Loop

In Part I, we faced the oil company's dilemma: buy the field or walk away? A decision tree helped us think through the problem systematically, weighing probabilities and payoffs to find the best choice. Part II revealed the limitations of decision trees and introduced influence diagrams as a more scalable alternative. Then, just as we did in our first post, we showed how to evaluate them by hand, confirming they yield the same recommendation as a decision tree.

But here's the thing: no one wants to redraw diagrams and recalculate expected utilities every time a geological estimate changes or market conditions shift. Real decision problems need tools that can adapt quickly. That's where this final part comes in. We'll tackle two essential questions:

1. How do we actually build and solve these models in code? We'll recreate our oil-field analysis using PyAgrum, turning those manual calculations into a few lines of Python.

2. How confident should we be in our recommendation? Through sensitivity analysis, we'll stress-test our assumptions and see just how robust—or fragile—our "buy the field" decision really is. We'll explore different types of plots and show how Gradio can turn our decision problem into an interactive tool where you can tweak any variable and instantly see what happens.

## Building the Oil-Field LIMID in PyAgrum

**PyAgrum** is a Python wrapper around the C++ aGrUM library, designed for building and solving probabilistic graphical models—including Bayesian networks, influence diagrams, and LIMIDs. What took us pages of manual calculation in Part II becomes a few lines of code: describe the network structure, plug in the probabilities and utilities, solve, and extract the optimal policy. Let's recreate our oil-field analysis and see the difference.

### Setting Up the Network Structure

We start by importing PyAgrum and creating an empty influence diagram. Then we add our four variables: oil field quality (Q), test results (R), the test decision (T), the buy decision (B), and a utility node (U).

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

Next, we connect the nodes with arcs to capture the dependencies from our LIMID. The memory arc from T to B is crucial—it tells PyAgrum that when making the buy decision, we remember what we chose for the test.

```python
# Add arcs to define dependencies
influence_diagram.addArc("T", "R")    # Test decision affects test results
influence_diagram.addArc("T", "B")    # Memory arc: buy decision remembers test choice
influence_diagram.addArc("T", "U")    # Test decision affects utility (cost)
influence_diagram.addArc("R", "B")    # Test results inform buy decision  
influence_diagram.addArc("B", "U")    # Buy decision affects utility
influence_diagram.addArc("Q", "R")    # Oil quality affects test results
influence_diagram.addArc("Q", "U")    # Oil quality affects utility
```

PyAgrum makes it easy to visualize what we've built. We can generate a diagram directly from our code:

```python
import pyagrum.lib.notebook as gnb
from pyagrum.lib import image

# Display in notebook (if using Jupyter)
gnb.sideBySide(influence_diagram, captions=["Oil field influence diagram"])

# Or export to PNG for use elsewhere
image.export(influence_diagram, "influence_diagram.png")
```

Here's the resulting diagram—the same LIMID from Part II, now built and visualized entirely in code:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-08-01-decision-theory-III/1_limid_oil_pyagrum.png" alt="Visual representation of the oil field LIMID generated by PyAgrum" width="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1.</b> Visual representation of the oil field LIMID generated by PyAgrum</i>
    </td>
  </tr>
</table>
</center>

### Filling in the Numbers

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

The `[:, np.newaxis]` reshaping is a PyAgrum requirement for multi-dimensional utility tables—the library expects utilities organized by the order of parent nodes.

### Solving the Network

With structure and parameters in place, PyAgrum can solve the entire problem in just a few lines. We create an inference engine, run the computation, and extract the results:

```python
# Create inference engine and solve
inference_engine = grum.ShaferShenoyLIMIDInference(influence_diagram)
inference_engine.makeInference()

print(f"Is the diagram solvable?: {inference_engine.isSolvable()}")
```

We can examine the optimal decision for each decision node. For example, the test decision (T):

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
      <img src="/assets/2025-08-01-decision-theory-III/2_optimal_decision_t.png" alt="Optimal decision T displayed as text and table in PyAgrum" width="200">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 2.</b> Optimal decision for test variable T shown in both text and table format</i>
    </td>
  </tr>
</table>
</center>

PyAgrum can also generate a visual representation of the solved network, showing the optimal decisions and expected utilities:

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
      <img src="/assets/2025-08-01-decision-theory-III/3_inference_result.png" alt="Evaluated oil field LIMID generated by PyAgrum" width="500">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 3.</b> Solved oil field LIMID showing optimal decisions and expected utilities</i>
    </td>
  </tr>
</table>
</center>

The results confirm our Part II calculations: the optimal strategy is to skip the test and buy the field directly, with a maximum expected utility of 721 million dollars—exactly matching our manual computation. What took us pages of manual calculations in Part II, PyAgrum solved in just 0.24 milliseconds.

## Testing Robustness with Deterministic Sensitivity Analysis

A recommendation without a "what-if" range is little comfort to executives betting hundreds of millions. We'll probe the model with three classic tools—single-parameter sweeps, two-parameter heat maps, and tornado plots—to see how far the numbers can drift before "buy" turns into "walk away".
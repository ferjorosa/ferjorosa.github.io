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
  <li style="margin-bottom: 0.5em;"><a href="#testing-robustness-with-deterministic-sensitivity-analysis">Testing Robustness with Deterministic Sensitivity Analysis</a>
    <ul style="margin-top: 0.3em;">
      <li style="margin-bottom: 0.3em;"><a href="#single-parameter-sensitivity-analysis">Single Parameter Sensitivity Analysis</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</a></li>
      <li style="margin-bottom: 0.3em;"><a href="#interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface: Real-Time Multi-Parameter Exploration</a></li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#conclusion-building-robust-decision-strategies">Conclusion: Building Robust Decision Strategies</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#references">References</a></li>
</ul>

</details>

<h2 id="closing-the-loop">Closing the Loop</h2>

In Part I, we faced the oil company's dilemma: buy the field or walk away? A decision tree helped us think through the problem systematically, weighing probabilities and payoffs to find the best choice. Part II revealed the limitations of decision trees and introduced influence diagrams as a more scalable alternative. Then, just as we did in our first post, we showed how to evaluate them by hand, confirming they yield the same recommendation as a decision tree.

But here's the thing: no one wants to redraw diagrams and recalculate expected utilities every time a geological estimate changes or market conditions shift. Real decision problems need tools that can adapt quickly. That's where this final part comes in. We'll tackle two essential questions:

1. How do we actually build and solve these models in code? We'll recreate our oil-field analysis using PyAgrum, turning those manual calculations into a few lines of Python.

2. How confident should we be in our recommendation? Through sensitivity analysis, we'll stress-test our assumptions and see just how robust—or fragile—our "buy the field" decision really is. We'll explore different types of plots and show how Gradio can turn our decision problem into an interactive tool where you can tweak any variable and instantly see what happens.

<h2 id="building-the-oil-field-limid-in-pyagrum">Building the Oil-Field LIMID in PyAgrum</h2>

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

<h2 id="testing-robustness-with-deterministic-sensitivity-analysis">Testing Robustness with Deterministic Sensitivity Analysis</h2>

The boardroom went quiet when you presented the recommendation: "Skip the test, buy the field." Then came the inevitable questions. The CFO leaned forward: "What if our estimate of high-quality probability is off by 10%?" The head geologist chimed in: "And what if the test cost isn't $30M but $50M?" The CEO, fingers drumming on the mahogany table, asked the real question: "How sure are we that this decision won't fall apart if our assumptions are wrong?"

This is where sensitivity analysis becomes your best friend. After finding the optimal decision strategy, it's crucial to understand how sensitive our results are to changes in the input parameters. Sensitivity analysis helps identify which uncertainties have the greatest impact on the expected utility and, consequently, on the optimal decisions.

We'll tackle this challenge with three complementary approaches:

1. **Single-parameter sweeps**: Vary one parameter at a time to see how the expected utility changes, helping us understand individual parameter sensitivity.

2. **Tornado diagrams**: Create visual summaries that show which variables have the most impact on our decision, sorted by magnitude of influence.

3. **Interactive Gradio interface**: Build a web app where anyone can drag sliders, change multiple parameters simultaneously, and instantly see how the optimal decision and expected utility respond.

<h3 id="single-parameter-sensitivity-analysis">Single Parameter Sensitivity Analysis</h3>

Single parameter sensitivity analysis examines how changes in one specific parameter affect the optimal decision and expected utility while keeping all other parameters constant. This approach is particularly valuable because it:

- **Isolates parameter impact**: By varying only one parameter at a time, we can clearly see its individual effect on the decision outcome
- **Identifies critical thresholds**: We can discover specific values where the optimal decision changes
- **Guides data collection**: Parameters with high sensitivity may warrant additional research or more precise estimation
- **Supports robust decision-making**: Understanding sensitivity helps assess the reliability of our recommendations

Let's examine two key parameters in our oil field decision problem to demonstrate this approach.

#### Example 1: Prior Probability of High-Quality Fields - P(Q=high)

Our first analysis examines how changes in the prior probability that a field is of high quality affect our decision strategy. We test four scenarios where P(Q=high) increases from the baseline 0.35 to 0.40, 0.45, and 0.50, while maintaining the proportional distribution among the remaining quality levels.

[PLACEHOLDER FOR P(Q=HIGH) SENSITIVITY PLOT]

The results reveal an interesting pattern:

- **Decision stability**: Across all tested values, the optimal strategy remains unchanged - we still recommend not conducting the test and directly purchasing the field
- **Utility sensitivity**: While the decision doesn't change, the expected utility increases significantly from the baseline 721.0 to 761.7, 802.4, and 843.1 respectively
- **Linear relationship**: The utility increase follows an approximately linear pattern, with each 0.05 increase in P(Q=high) adding roughly 40 points to the expected utility

This analysis demonstrates that while our strategic recommendation is robust to changes in prior beliefs about field quality, the economic value of the decision is highly sensitive to these beliefs. Even without changing our action plan, more optimistic priors about field quality substantially improve the expected outcome.

#### Example 2: Test Precision for Medium-Quality Fields - P(R=pass | Q=medium)

Our second analysis examines the precision of the geological test, specifically focusing on its ability to correctly identify medium-quality fields. Medium-quality fields represent a particularly interesting case because:

- They are **profitable** (unlike low-quality fields)
- They are **harder to detect** due to intermediate porosity levels that make classification more challenging
- Improved test precision for this category could significantly impact the value of testing

We analyze scenarios where the test becomes more precise at identifying medium-quality fields, increasing P(R=pass | Q=medium) from the baseline 0.70 to values up to 0.95.

[PLACEHOLDER FOR P(R=PASS|Q=MEDIUM) SENSITIVITY PLOT]

This analysis reveals a **critical decision threshold**:

- **Below 0.9**: The optimal strategy remains "don't test, buy the field" - the same as our baseline recommendation
- **At 0.9 and above**: The optimal strategy shifts to "conduct the test first" - if the test passes, buy the field; if it fails, don't buy

**Why does this threshold matter?**

When the test becomes sufficiently precise at identifying medium-quality fields (P(R=pass | Q=medium) ≥ 0.9), the value of information increases enough to justify the testing cost. The improved ability to distinguish profitable medium-quality fields from unprofitable low-quality fields makes the test worthwhile, as we can now more confidently avoid the costly mistake of purchasing a low-quality field.

The economic intuition is clear: better test precision reduces uncertainty about field quality, and when this reduction is substantial enough, the value of this information exceeds the cost of obtaining it. This threshold analysis provides actionable insights - if we can improve our testing technology to achieve at least 90% accuracy for medium-quality fields, conducting the test becomes the preferred strategy.

<h3 id="tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</h3>

While single parameter analysis shows us how individual variables affect our decision, **tornado diagrams** provide a powerful visual summary that ranks all parameters by their impact on the expected utility. These charts get their name from their distinctive shape - wide at the top (high impact variables) and narrow at the bottom (low impact variables), resembling a tornado.

Tornado diagrams are particularly valuable when we have **underlying variables that feed into our model through formulas**. For instance, if our utility calculations involved complex discounted cash flow models, we could analyze how changes in drilling time, labor costs, oil prices, or discount rates affect the final decision. Each of these variables would feed into the utility calculations, and tornado diagrams would show us which ones deserve the most attention.

In our simplified oil field problem, we'll examine two different types of tornado analyses to illustrate the concept.

#### Example 1: Direct Utility Value Sensitivity

Our first tornado analysis examines how changes in the direct utility values affect the maximum expected utility. We test each utility parameter by applying a ±100 million dollar variation while keeping all other parameters constant.

**Baseline Expected Utility: 721.00 million**

[PLACEHOLDER FOR UTILITY TORNADO PLOT]

The analysis reveals that **U(not_do, buy, medium)** - the utility of buying a medium-quality field without testing - has the largest impact on our decision. This makes intuitive sense when we consider the underlying probabilities:

- Medium-quality fields have a substantial probability (45% prior)
- The "not_do, buy" scenario represents our current optimal strategy  
- Medium-quality fields are profitable, so changes in their utility values significantly affect the overall expected outcome

However, it's worth noting that while tornado diagrams can technically be applied to any parameter, **they're most meaningful when applied to underlying variables** that feed into the model through formulas rather than direct utility assignments.

#### Example 2: Test Cost Sensitivity - A More Natural Application

A more natural application of tornado analysis in our problem focuses on the **test cost** - a variable that would realistically vary based on market conditions, technology improvements, or operational factors.

**Baseline MEU: 721.00 million | Cost variation: ±25 million**

[PLACEHOLDER FOR TEST COST TORNADO PLOT]

This analysis reveals a fascinating threshold effect:

- **Test cost reduction (-25)**: MEU increases to 721.95 million - **the optimal decision changes** from "don't test, buy" to "test first" because testing now provides higher expected utility (721.95) than buying directly (721.00)
- **Test cost increase (+25)**: MEU remains at 721.00 million with zero impact because we already choose not to test at the baseline cost, so making testing even more expensive doesn't affect our decision

This demonstrates the power of tornado analysis for **operational variables**: a relatively modest 25 million reduction in test cost (from 30 to 5 million) is sufficient to flip our strategic recommendation. This insight could guide negotiations with testing contractors or investments in testing technology.

**The Key Insight**: Tornado diagrams shine brightest when analyzing variables that represent real-world parameters you can actually influence - costs, timeframes, technological capabilities, market conditions - rather than abstract utility assignments. These are the variables where sensitivity analysis translates directly into actionable business decisions.

<h3 id="interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface: Real-Time Multi-Parameter Exploration</h3>

While single parameter analysis and tornado diagrams provide valuable insights into individual variable impacts, **Gradio** offers a powerful way to explore multiple parameters simultaneously through an interactive web interface. Gradio is a Python library that transforms our PyAgrum decision analysis code into a user-friendly web application that anyone can use - no Python knowledge required.

#### Why Gradio for Decision Analysis?

The beauty of Gradio lies in its ability to democratize complex decision analysis:

- **Real-time exploration**: Users can adjust multiple parameters simultaneously and instantly see how changes affect both the optimal decision and expected utility
- **No technical barriers**: Stakeholders, executives, and domain experts can interact with the model without needing to understand the underlying code
- **Comprehensive parameter space**: Unlike the focused analysis of single parameter or tornado methods, users can explore any combination of parameters to discover unexpected interactions
- **Immediate feedback**: Changes in probabilities, utilities, or test costs are reflected instantly in both the influence diagram visualization and decision recommendations

#### Implementation Overview

Our Gradio interface provides interactive controls for all key model parameters:

**Input Components:**
- **Prior probability tables** for oil field quality (Q) - editable dataframes where users can adjust the likelihood of high, medium, and low quality fields
- **Conditional probability tables** for test results (R) - allowing exploration of different test precision scenarios
- **Utility tables** - enabling what-if analysis on the financial consequences of each decision path

**Output Components:**
- **Visual influence diagram** with calculated optimal decisions highlighted
- **Decision summary** providing clear, natural language recommendations
- **Expected utility calculations** showing the quantitative impact of parameter changes

The interface is built using PyAgrum for the decision analysis engine and Gradio's intuitive components for user interaction. Here's the high-level structure:

```python
import gradio as gr
import pyagrum as gum

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

[LINK TO FULL IMPLEMENTATION CODE IN REPOSITORY]

#### Live Interactive Interface

You can explore the decision problem yourself using our deployed Gradio interface. Try adjusting different parameters to see how they affect the optimal strategy:

[PLACEHOLDER FOR HUGGING FACE SPACES GRADIO INTERFACE HTML EMBED]

**Try This Experiment:** Start with the default parameters, then gradually increase the probability of high-quality fields from 35% to 60%. Notice how this affects both the expected utility and potentially the optimal decision strategy. Then experiment with improving test precision - increase P(R=pass | Q=medium) from 70% to 95% and observe the threshold where testing becomes worthwhile.

This interactive exploration reveals insights that would be difficult to discover through static analysis alone, making Gradio an invaluable tool for comprehensive sensitivity analysis and stakeholder engagement.

<h2 id="conclusion-building-robust-decision-strategies">Conclusion: Building Robust Decision Strategies</h2>

Throughout this exploration of sensitivity analysis for decision theory, we've built a comprehensive toolkit that transforms theoretical models into practical, robust decision-making frameworks. Each method we've covered serves a distinct and valuable purpose in the decision analyst's arsenal.

**Single parameter sensitivity analysis** provides the foundation - allowing us to isolate and understand how individual variables affect our decisions. Through our analysis of P(Q=high) and P(R=pass | Q=medium), we discovered that while some parameters affect expected utility significantly, they don't always change the optimal strategy. This granular understanding is crucial for identifying which uncertainties matter most for decision outcomes.

**Tornado diagrams** elevate our analysis by providing visual, comparative insights into parameter importance. They excel at highlighting which real-world variables - like test costs, operational parameters, or market conditions - have the greatest leverage on our decisions. The revelation that a modest 25 million reduction in test cost could flip our strategic recommendation from "don't test" to "test first" exemplifies how tornado analysis guides actionable business decisions.

**Interactive Gradio interfaces** complete our toolkit by democratizing access to sophisticated decision analysis. They enable stakeholders at all technical levels to explore parameter combinations, discover unexpected interactions, and build intuitive understanding of the decision problem. This accessibility transforms decision analysis from an expert-only exercise into a collaborative, organization-wide capability.

**The Integration Advantage**

The real power emerges when these methods work together:

1. **Start with single parameter analysis** to understand fundamental relationships and identify critical thresholds
2. **Use tornado diagrams** to prioritize which variables deserve the most attention and investment
3. **Deploy Gradio interfaces** to facilitate ongoing exploration, stakeholder engagement, and real-time decision support

This multi-layered approach ensures that your decision strategies are not only mathematically optimal but also robust to uncertainty, practical to implement, and comprehensible to decision-makers. In our oil field example, we've shown how each method reveals different aspects of the same underlying decision problem, providing complementary insights that strengthen our overall analysis.

**Looking Forward**

The techniques demonstrated here extend far beyond oil field decisions. Whether you're evaluating investment strategies, designing clinical trials, optimizing supply chains, or making any complex decision under uncertainty, this sensitivity analysis framework provides the foundation for confident, well-informed choices.

The combination of rigorous mathematical analysis (PyAgrum), systematic parameter exploration (single parameter and tornado methods), and accessible interfaces (Gradio) represents the future of practical decision science - where theoretical rigor meets real-world applicability.

By mastering these tools, you're equipped to transform uncertain, complex decisions into clear, justifiable strategies backed by comprehensive sensitivity analysis.


<h2 id="references">References</h2>
1. Wikipedia article on <u><a href="https://en.wikipedia.org/wiki/Conditional_independence">conditional independence</a></u>.
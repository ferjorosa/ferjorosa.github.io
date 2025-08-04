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
          <li style="margin-bottom: 0.2em;"><a href="#example-1-prior-probability-of-high-quality-fields">Example 1: Prior Probability of High-Quality Fields - P(Q=high)</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#example-2-test-precision-for-medium-quality-fields">Example 2: Test Precision for Medium-Quality Fields - P(R=pass | Q=medium)</a></li>
        </ul>
      </li>
      <li style="margin-bottom: 0.3em;"><a href="#tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</a>
        <ul style="margin-top: 0.2em;">
          <li style="margin-bottom: 0.2em;"><a href="#example-1-direct-utility-value-sensitivity">Example 1: Direct Utility Value Sensitivity</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#example-2-test-cost-sensitivity">Example 2: Test Cost Sensitivity - A More Natural Application</a></li>
        </ul>
      </li>
      <li style="margin-bottom: 0.3em;"><a href="#interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface: Real-Time Multi-Parameter Exploration</a>
        <ul style="margin-top: 0.2em;">
          <li style="margin-bottom: 0.2em;"><a href="#why-gradio-for-decision-analysis">Why Gradio for Decision Analysis?</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#implementation-overview">Implementation Overview</a></li>
          <li style="margin-bottom: 0.2em;"><a href="#live-interactive-interface">Live Interactive Interface</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li style="margin-bottom: 0.5em;"><a href="#conclusion-building-robust-decision-strategies">Conclusion: Building Robust Decision Strategies</a></li>
  <li style="margin-bottom: 0.5em;"><a href="#references">References</a></li>
</ul>

</details>

<h2 id="closing-the-loop">Closing the Loop</h2>

In [Part I](https://ferjorosa.github.io/blog/2025/06/08/decision-theory-I.html), we tackled the oil company's dilemma: buy the field or walk away? We used a decision tree to work through the problem step by step, weighing probabilities and payoffs to find the optimal choice. In [Part II](https://ferjorosa.github.io/blog/2025/07/04/decision-theory-II.html), we discussed the limitations of decision trees and learned about influence diagrams as a more scalable approach. We worked through the same problem by hand again, proving that influence diagrams give us the same answer as decision trees.

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

<h4 id="example-1-prior-probability-of-high-quality-fields">Example 1: Prior Probability of High-quality Fields</h4>

Our first analysis explores how varying the prior probability that a field is high quality influences our decision strategy. Beginning with the baseline value $$P(Q=\text{high}) = 0.35$$, we adjust this probability by $$\pm0.15$$ in increments of $$0.05$$, producing seven scenarios. The probabilities of the remaining quality categories are rescaled proportionally so that the distribution still sums to one.

placeholder for plot

These changes definitely affect how much money we expect to make, but they don't change the optimal policy: skip the test and buy the field directly. This makes sense when you think about it: knowing that fields in this region are more likely to be high quality affects our expected profits, but it doesn't change how useful the test would be.

<h4 id="example-2-test-precision-for-medium-quality-fields">Example 2: Test Precision for Medium-Quality Fields - P(R=pass | Q=medium)</h4>

For our second analysis, let's look at the geological test's accuracy, specifically focusing on its ability to correctly identify medium-quality fields. Medium-quality fields are particularly interesting because they are profitable but seem easy to mistake for 
low-grade ones.

What if we could improve the test to better identify these medium-quality fields? We'll vary the test's pass rate for true medium fields from $$0.70$$ to $$0.95$$ to see when the improved accuracy makes testing worthwhile.

[PLACEHOLDER FOR P(R=PASS|Q=MEDIUM) SENSITIVITY PLOT]

Interestingly, once the test becomes good enough at spotting medium-quality fields (achieving $$0.9$$ accuracy or better), testing suddenly becomes worth the cost. The takeaway is clear: if we can upgrade our testing technology to correctly identify medium-quality fields at least 90% of the time, we should start using the test before making purchase decisions.

<h3 id="tornado-diagrams-visualizing-parameter-impact">Tornado Diagrams: Visualizing Parameter Impact</h3>

While single parameter analysis tells us how each variable affects our decision, <a href="https://en.wikipedia.org/wiki/Tornado_diagram"><u>tornado diagrams</u></a> give us the big picture by ranking all parameters by their **individual** impact. These charts get their name from their shape: wide at the top for the most important variables and narrow at the bottom for the least important.

These diagrams are particularly valuable when we have formulas that define the utilities. For instance, if our utility numbers depended on a formula based on factors like drilling costs, oil prices, or project timelines, a tornado diagram would easily show us whether a 10% change in oil prices matters more than a 20% change in drilling costs.

For our oil field problem, we'll look at two examples to see how this works.

<h4 id="example-1-direct-utility-value-sensitivity">Example 1: Direct Utility Value Sensitivity</h4>

Our first tornado analysis examines how changes in the direct utility values affect the maximum expected utility. We test each utility parameter by applying a $$\pm100$$ million dollar variation while keeping all other parameters constant.

[PLACEHOLDER FOR UTILITY TORNADO PLOT]

The analysis reveals that **U(not_do, buy, medium)** - the utility of buying a 
medium-quality field without testing - has the largest impact on our decision, which makes 
intuitive sense given that medium-quality fields have the highest prior probability (0.45), so changes to their utility values disproportionately affect the overall expected utility.

Changes to utilities involving testing ("do" scenarios) have smaller impacts because testing is already suboptimal in our baseline analysis. These utility values would need to change enough to flip the optimal strategy from "not_do" to "do" before they could significantly affect the final result.

However, it's worth noting that while tornado diagrams can technically be applied to any parameter, **they're most meaningful when applied to underlying variables** that feed into the model through formulas rather than direct utility assignments.

<h4 id="example-2-test-cost-sensitivity">Example 2: Test Cost Sensitivity</h4>

Our second tornado analysis examines how changes in test cost affect the maximum expected utility. This variable would realistically vary based on market conditions, technology improvements, or operational 
factors. We evaluate the test cost parameter by applying a $$\pm25$$ million dollar variation while keeping all other parameters constant.

[PLACEHOLDER FOR TEST COST TORNADO PLOT]

The diagram shows that test cost has a limited impact on our decision strategy. Even with a substantial 83% cost reduction (from $30M to $5M), the optimal strategy remains virtually unchanged: the MEU increases from 721 million (not testing) to only 721.95 million (testing when it costs $5M), representing a marginal 0.13% improvement.

This suggests that **cost reduction alone is insufficient** to make testing attractive. To meaningfully shift our strategy toward testing, we would likely need either significant improvements in test reliability (as demonstrated in Example 2 of the single-parameter analysis) or a combination of cost reduction paired with enhanced test accuracy.

<h3 id="interactive-gradio-interface-real-time-multi-parameter-exploration">Interactive Gradio Interface: Real-Time Multi-Parameter Exploration</h3>

While single parameter analysis and tornado diagrams provide valuable insights into individual variable impacts, **Gradio** offers a powerful way to explore multiple parameters simultaneously through an interactive web interface. Gradio is a Python library that transforms our PyAgrum decision analysis code into a user-friendly web application that anyone can use - no Python knowledge required.

<h4 id="why-gradio-for-decision-analysis">Why Gradio for Decision Analysis?</h4>

The beauty of Gradio lies in its ability to democratize complex decision analysis:

- **Real-time exploration**: Users can adjust multiple parameters simultaneously and instantly see how changes affect both the optimal decision and expected utility
- **No technical barriers**: Stakeholders, executives, and domain experts can interact with the model without needing to understand the underlying code
- **Comprehensive parameter space**: Unlike the focused analysis of single parameter or tornado methods, users can explore any combination of parameters to discover unexpected interactions
- **Immediate feedback**: Changes in probabilities, utilities, or test costs are reflected instantly in both the influence diagram visualization and decision recommendations

<h4 id="implementation-overview">Implementation Overview</h4>

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

<h4 id="live-interactive-interface">Live Interactive Interface</h4>

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
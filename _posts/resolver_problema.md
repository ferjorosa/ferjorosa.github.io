<h3 id="modelling_oil_problem_qualitative">Modelling Qualitative Information</h3>

The following image displays the influence diagram structure for the oil problem:

<center>
<table>
  <tr>
    <td align="center">
      <img src="/assets/2025-06-14-decision-theory-II/decision_network_oil.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" height="175">
    </td>
  </tr>
  <tr>
    <td colspan="2" align="center">
      <i><b>Figure 1a.</b> Traditional influence diagram for the oil problem. Informational arcs arcs</i>
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
      <img src="/assets/2025-06-14-decision-theory-II/decision_network_oil_limid.png" alt="Influence diagram structure of the asymmetric oil problem from Part I" height="175">
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

<h2 id="evaluating_oil_problem"> Evaluating the Influence Diagram </h2>

<!-- BEGIN Arc-reversal / Node-reduction evaluation -->
<h3 id="oil_problem_arc_reversal">Solving the LIMID by Arc-reversal / Node-reduction</h3>

The limited-memory influence diagram (LIMID) for the oil-field decision problem contains
three types of nodes:

<ul>
  <li><b>Chance</b> – oil-field quality <b><span style="color:purple;">Q</span></b> and test result <b><span style="color:purple;">R</span></b></li>
  <li><b>Decision</b> – perform test? <b><span style="color:red;">T</span></b> and buy field? <b><span style="color:red;">B</span></b></li>
  <li><b>Utility</b> – profit/loss <b><span style="color:blue;">U</span></b></li>
</ul>

Directed arcs encode information flow and memory: 

<center><code>T → R,   Q → R,   T → B,   R → B,   T → U,   R → U,   Q → U</code></center>

Shachter's (1986) <em>arc-reversal / node-reduction</em> algorithm repeatedly

<ol>
  <li><b>reverses arcs</b> so that a target node becomes a child of all its current parents, then</li>
  <li><b>removes</b> that node, <i>marginalising</i> (summing) over chance nodes or <i>maximising</i> over decision nodes, and pushes the resulting expected-utility table forward.</li>
</ol>

The procedure below evaluates the diagram completely, exposing every intermediate number so you can reproduce the arithmetic with a calculator.

<hr/>
<h4>Step 0 – Original data</h4>

<b>States</b>

<table>
  <tr><th>Variable</th><th>Values</th></tr>
  <tr><td><b>T</b></td><td>perf, no</td></tr>
  <tr><td><b>R</b></td><td>pass, fail, no-results</td></tr>
  <tr><td><b>B</b></td><td>buy, not-buy</td></tr>
  <tr><td><b>Q</b></td><td>high, med, low</td></tr>
</table>

<b>Prior on Q</b>

$$
P(Q)=(0.35,\,0.45,\,0.20).
$$

<b>Likelihoods</b>  (the laboratory test is only informative when it is performed)

<table>
  <tr><th rowspan="2">P(R | Q,T)</th><th colspan="3">T = perf</th><th colspan="3">T = no</th></tr>
  <tr><th>high</th><th>med</th><th>low</th><th>high</th><th>med</th><th>low</th></tr>
  <tr><td>pass</td><td>0.95</td><td>0.70</td><td>0.15</td><td>0</td><td>0</td><td>0</td></tr>
  <tr><td>fail</td><td>0.05</td><td>0.30</td><td>0.85</td><td>0</td><td>0</td><td>0</td></tr>
  <tr><td>no-results</td><td>0</td><td>0</td><td>0</td><td>1</td><td>1</td><td>1</td></tr>
</table>

<b>Utility table U(T,B,Q)</b> (dollar amounts)

<table>
  <tr><th rowspan="2">T</th><th rowspan="2">B</th><th colspan="3">Q</th></tr>
  <tr><th>high</th><th>med</th><th>low</th></tr>
  <tr><td rowspan="2">perf</td><td>buy</td><td>1220</td><td>600</td><td>-30</td></tr>
  <tr><td>not-buy</td><td>320</td><td>320</td><td>320</td></tr>
  <tr><td rowspan="2">no</td><td>buy</td><td>1250</td><td>630</td><td>0</td></tr>
  <tr><td>not-buy</td><td>350</td><td>350</td><td>350</td></tr>
</table>

<hr/>
<h4>Step 1 – Reverse arc Q&nbsp;→&nbsp;R (compute posteriors)</h4>

We need $$P(Q\,|\,T,R)$$ so we turn Q into a child of (T,R):

$$
P(Q=q\mid T=t,R=r)=\frac{P(R=r\mid Q=q,T=t)\,P(Q=q)}{\sum_{q'}P(R=r\mid Q=q',T=t)\,P(Q=q')}.
$$

<b>Predictive distribution of R when T = perf</b>

$$
\begin{aligned}
P(\text{pass}|T=\text{perf}) &=0.95\,0.35+0.70\,0.45+0.15\,0.20 = 0.6775\\
P(\text{fail }|T=\text{perf}) &=0.05\,0.35+0.30\,0.45+0.85\,0.20 = 0.3225
\end{aligned}
$$

<b>Posterior T = perf, R = pass</b>

$$
P(Q|\text{perf,pass})=(0.4907,\,0.4649,\,0.0443)
$$

<b>Posterior T = perf, R = fail</b>

$$
P(Q|\text{perf,fail})=(0.05426,\,0.41802,\,0.52772).
$$

If the test is not performed, R is deterministically "no-results" and the posterior equals the prior.

<hr/>
<h4>Step 2 – Collapse Q into a local expected-utility table U′(T,R,B)</h4>

$$
U'(T,R,B)=\sum_q U(T,B,q)\;P(q\mid T,R).
$$

<table>
  <tr><th>T</th><th>R</th><th>B</th><th>Arithmetic</th><th>U′</th></tr>
  <tr><td rowspan="4">perf</td><td rowspan="2">pass</td><td>buy</td><td>1220·0.4907 + 600·0.4649 − 30·0.0443</td><td>876.3</td></tr>
  <tr><td>not-buy</td><td>320·1</td><td>320</td></tr>
  <tr><td rowspan="2">fail</td><td>buy</td><td>1220·0.05426 + 600·0.41802 − 30·0.52772</td><td>301.2</td></tr>
  <tr><td>not-buy</td><td>320·1</td><td>320</td></tr>
  <tr><td rowspan="2">no</td><td rowspan="2">no-results</td><td>buy</td><td>1250·0.35 + 630·0.45 + 0·0.20</td><td>721</td></tr>
  <tr><td>not-buy</td><td>350·1</td><td>350</td></tr>
</table>

<hr/>
<h4>Step 3 – Remove decision B (maximise)</h4>

$$
U''(T,R)=\max_B U'(T,R,B).
$$

<ul>
  <li>(perf, pass) → 876.3 (buy)</li>
  <li>(perf, fail) → 320   (not-buy)</li>
  <li>(no, no-results) → 721 (buy)</li>
</ul>

These values form the new utility node and the chosen actions constitute the optimal <i>policy</i> for B.

<hr/>
<h4>Step 4 – Eliminate chance node R (expectation)</h4>

We fold R into its parent T:

$$
U'''(T)=\sum_r P(r\mid T)\;U''(T,r).
$$

<b>When T = perf</b>

$$
U'''(\text{perf}) = 0.6775·876.3 + 0.3225·320 = 696.9.
$$

<b>When T = no</b>

R is always "no-results", therefore $$U'''(\text{no})=721.$$

<hr/>
<h4>Step 5 – Remove decision T (maximise)</h4>

The maximal expected utility (MEU) is

$$
\text{MEU}=\max_T U'''(T)=\max(696.9,\,721)=721.
$$

Optimal first decision: <b>do not perform the porosity test</b>.

<hr/>
<h4>Step 6 – Resulting optimal policy</h4>

<table>
  <tr><th>Decision stage</th><th>Information available</th><th>Optimal action</th></tr>
  <tr><td>T</td><td>—</td><td>Do not perform test</td></tr>
  <tr><td rowspan="2">B <span style="font-size:smaller;">(only if test were actually performed)</span></td><td>R = pass</td><td>Buy</td></tr>
  <tr><td>R = fail</td><td>Do not buy</td></tr>
</table>

<center><b>MEU = 721 dollars</b></center>

<hr/>
<p>The modest informational value of the porosity test (a 30-dollar cost for running it is embedded in the utility numbers) does not compensate for its price. Skipping the test and buying the field immediately yields the best expected profit. Should the engineer still order the test, the posterior beliefs computed in Step 1 would dictate the subsequent buy / do-not-buy decision exactly as indicated above.</p>

<!-- END Arc-reversal / Node-reduction evaluation -->
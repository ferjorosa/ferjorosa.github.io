    <!-- Now, we must recompute the conditional probabilities to maintain consistency. Using Bayes' Theorem, we derive a new distribution
    
    In order to do that, we first remove the arc $$X \rightarrow Y$$ and add a new arc

    In order to be able to remove nodes by making them leafs, Shachter applies an arc reversal approach that keeps information stable by using Bayes theorem.

    This operation is only permitted for arcs between two chance nodes, say $$X \rightarrow Y$$. It transforms the arc to $$Y \rightarrow X$$ and requires recomputing the conditional distributions of both nodes using Bayes' rule.

    $$
    P(X \mid \text{pa}(X)) = \alpha P(X \mid \text{pa}(X)) P(Y \mid \text{pa}(Y))
    $$

    $$
    P(Y \mid \text{pa}(Y)) = \sum_x P(X = x \mid \text{pa}(X)) P(Y \mid \text{pa}(Y))
    $$

    where $$\alpha$$ is a normalizing constant, and the new parent sets are $$\text{pa}(X) = (\text{pa}(X) \cup \text{pa}(Y)) \setminus \{Y\}$$ and $$\text{pa}(Y) = \text{pa}(Y) \setminus \{X\}$$. This intuitively means that statistical information is propagated through the arc.  -->



-------------------

<p><b>We now evaluate the influence diagram with the Shenoy–Shafer (valuation-based) algorithm, step by step.</b></p>

<p>The algorithm handles two kinds of <em>valuations</em>: probability valuations <em>φ</em> (non-negative and normalised) and utility valuations <em>ϑ</em> (real-valued). Two local operations are enough:</p>
<ul>
  <li><b>Combination</b> (⊗)&nbsp;– multiply probability factors and add utilities defined over the same variables.</li>
  <li><b>Marginalisation</b> (↓X)&nbsp;– eliminate X: sum over a chance variable, maximise over a decision variable.</li>
</ul>
<p><em>Fusion</em> is simply doing those two things—<b>combine</b> everything that mentions X, then <b>marginalise</b> X—so there are still only <i>two</i> basic operations under the hood.</p>
<p>By carrying out one fusion step after another—working <em>backwards in time</em> so that future decisions are treated first—we eventually get rid of every variable. The very last number left on the table is the <b>maximum expected utility&nbsp;(MEU)</b>, and the choices that achieved each intermediate maximum together form the <b>optimal policy</b>.</p>

<h4>1. Variables and valuations</h4>
<ul>
  <li>Chance Q ∈ {high, medium, low}</li>
  <li>Decision T ∈ {perform, skip}  (test decision)</li>
  <li>Chance R ∈ {pass, fail, no&nbsp;results}</li>
  <li>Decision B ∈ {buy, not&nbsp;buy}</li>
</ul>
<p>Valuations used:</p>
<ul>
  <li>φ<sub>1</sub>(Q) = P(Q)&nbsp; (prior)</li>
  <li>φ<sub>2</sub>(Q,T,R) = P(R&nbsp;|&nbsp;Q,T)&nbsp; (test reliability; if T=skip we force R=no&nbsp;results)</li>
  <li>ϑ<sub>1</sub>(Q,T,B) = Utility(Q,T,B)</li>
</ul>

<p><b>Why these valuations?</b>  A <em>valuation</em> is simply a piece of information attached to a subset of variables.  In the Shenoy–Shafer framework we keep two flavours side-by-side:</p>
<ul>
  <li><b>Probability valuations</b> (φ) carry beliefs about chance variables.  They always multiply (because joint probabilities factorise) and are summed out when the variable disappears.</li>
  <li><b>Utility valuations</b> (ϑ) encode our preferences.  When we combine utilities defined over the <em>same</em> variables we just add them – a standard assumption of additive utility.  When a decision variable is eliminated we <em>maximise</em> the utility to pick the best action.</li>
</ul>
<p>In our oil-field diagram each node with incoming arrows contributes one valuation:</p>
<ol style="margin-top:-8px">
  <li>φ<sub>1</sub>(Q) – prior belief about quality.</li>
  <li>φ<sub>2</sub>(Q,T,R) – reliability of the test (because R depends on Q and on whether we tested).</li>
  <li>ϑ<sub>1</sub>(Q,T,B) – monetary outcome of buying/not buying under each quality and test decision.</li>
</ol>
<p>Nothing else is needed: the full joint model <em>factorises</em> as the product φ<sub>1</sub>·φ<sub>2</sub> plus the additive utility ϑ<sub>1</sub>.</p>

<h4>2. Elimination order</h4>
<p>The algorithm works by successively <em>fusing</em> one variable at a time.  A sensible order is the <b>reverse chronological order</b> of decisions and observations:</p>
<div style="text-align:center;font-weight:bold">Q → B → R → T</div>

<p>Why reverse time?</p>
<ul>
  <li>At each fusion step we need all the information that will <em>ever</em> be relevant for the variable being eliminated.  Looking backwards guarantees that – future decisions have not been fixed yet, so they would not supply extra information.</li>
  <li>It respects the information flow of a LIMID: a decision can only depend on what is known <em>up to that point</em>.  Eliminating from the future to the past preserves this constraint automatically.</li>
  <li>Practically, it often keeps the intermediate tables small because parents are eliminated <em>before</em> their children gather many dependencies.</li>
</ul>
<p>Other orders are possible and give the same final MEU, but they may create larger intermediate valuations and thus require more computation.</p>

<h4>3. Fusion steps</h4>
<ol>
  <li><b>Initial combination</b><br/>
      F<sub>0</sub>(Q,T,R,B) = φ<sub>1</sub> ⊗ φ<sub>2</sub> ⊗ ϑ<sub>1</sub></li>
  <li><b>Eliminate Q&nbsp;(chance)</b><br/>
      We compute
      \[
      F_1(t,r,b) 
      = \sum_{q \in \{h,m,l\}} P(q)\;P(r\mid q, t)\;U(q,t,b).
      \]
      Concretely:
      <ul>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{perform},\,\text{pass},\,\text{buy}) &= 0.35\times0.95\times1220 + 0.45\times0.70\times600 + 0.20\times0.15\times(-30)\\
                                                             &= 415.65 + 189.00 - 0.90 \\ &= 593.75.
          \end{aligned}
          \]
        </li>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{perform},\,\text{pass},\,\text{not buy}) &= 0.35\times0.95\times320 + 0.45\times0.70\times320 + 0.20\times0.15\times320\\
                                                                  &= 106.40 + 100.80 + 9.60 = 216.80.
          \end{aligned}
          \]
        </li>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{perform},\,\text{fail},\,\text{buy}) &= 0.35\times0.05\times1220 + 0.45\times0.30\times600 + 0.20\times0.85\times(-30)\\
                                                              &= 21.35 + 81.00 - 5.10 = 97.25.
          \end{aligned}
          \]
        </li>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{perform},\,\text{fail},\,\text{not buy}) &= 0.35\times0.05\times320 + 0.45\times0.30\times320 + 0.20\times0.85\times320\\
                                                                   &= 5.60 + 43.20 + 54.40 = 103.20.
          \end{aligned}
          \]
        </li>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{skip},\,\text{no res},\,\text{buy}) &= 0.35\times1\times1250 + 0.45\times1\times630 + 0.20\times1\times0\\
                                                             &= 437.50 + 283.50 + 0 = 721.00.
          \end{aligned}
          \]
        </li>
        <li>
          \[
          \begin{aligned}
          F_1(&\text{skip},\,\text{no res},\,\text{not buy}) &= 0.35\times1\times350 + 0.45\times1\times350 + 0.20\times1\times350\\
                                                                  &= 122.50 + 157.50 + 70.00 = 350.00.
          \end{aligned}
          \]
        </li>
      </ul>
      <p>The computed values can be summarised as follows:</p>
      <table>
        <tr><th rowspan="2">T</th><th rowspan="2">R</th><th colspan="2">F<sub>1</sub> (expected utility)</th></tr>
        <tr><th>Buy</th><th>Not&nbsp;Buy</th></tr>
        <tr><td>Perform</td><td>Pass</td><td align="right">593.75</td><td align="right">216.80</td></tr>
        <tr><td>Perform</td><td>Fail</td><td align="right">97.25</td><td align="right">103.20</td></tr>
        <tr><td>Skip</td><td>No&nbsp;Res</td><td align="right">721.00</td><td align="right">350.00</td></tr>
      </table>
  </li>
  <li><b>Eliminate B&nbsp;(decision)</b><br/>
      For every pair \((t,r)\)
      \[
        g(t,r) = \max_{b \in \{\text{buy},\,\text{not buy}\}} F_1(t,r,b).
      \]
      Evaluations:
      \[
      \begin{aligned}
      g(\text{perform},\text{pass}) &= \max(593.75,\;216.80)=593.75\\
      g(\text{perform},\text{fail}) &= \max(97.25,\;103.20)=103.20\\
      g(\text{skip},\text{no res}) &= \max(721.00,\;350.00)=721.00.
      \end{aligned}
      \]
      The associated optimal action (argmax) yields the policy
      \(\delta_B\) stated above.
  </li>
  <li><b>Eliminate R&nbsp;(chance)</b><br/>
      Expected utility for each test decision:
      \[
      \begin{aligned}
      \text{EU}(t=\text{perform}) &= g(\text{perform},\text{pass}) + g(\text{perform},\text{fail})\\
                                   &= 593.75 + 103.20 = 696.95,\\[6pt]
       \text{EU}(t=\text{skip})    &= g(\text{skip},\text{no res}) = 721.00.
      \end{aligned}
      \]
  </li>
  <li><b>Eliminate T&nbsp;(decision)</b><br/>
      Select the larger of the two expected utilities:
      \[
        \text{MEU}=\max(696.95,\;721.00)=721.00,\quad\delta_T=\text{skip}.
      \]
  </li>
</ol>

<h4>4. Optimal policy</h4>
<ul>
  <li><b>Test decision T:</b> Skip the porosity test.</li>
  <li><b>Purchase decision B:</b> (contingent) If a test were performed and you saw <em>Pass</em> then Buy; if <em>Fail</em> then Don't Buy; however, because δ<sub>T</sub> says Skip, the only realised situation is R=no&nbsp;results and the policy is Buy.</li>
</ul>

<p><b>Interpretation&nbsp;:</b> The test is not worth its 30-million cost. The company should buy the field outright, yielding an expected profit of $721&nbsp;million.</p>



<h3 id="oil_problem_solution">Putting it to work: solving the oil-field LIMID</h3>

To ground these ideas, let's solve the oil-field LIMID with the Shenoy–Shafer algorithm.  At the heart of the method are messages that flow between cliques.  For example, the message sent from the clique containing \(Q,R\) to the one containing the buy decision \(B\) is

\[
 m_{QR \rightarrow B}(B,R)=\sum_{Q}\,\max_{B}\;U(T,B,Q)\,P(Q)\,P(R\mid Q,T),
\]

which marginalises the unknown field quality while preserving exactly the information the decision needs.

Carrying out all message computations produces an expected utility of <strong>721</strong> and the policy "Skip the test, Buy" — precisely the result obtained in Part&nbsp;I by expanding the full decision tree.

Below is a minimal PyAgrum script that replicates this calculation.<br/>Feel free to open the accompanying notebook in the repository for the complete, ready-to-run version.

```python
import pyAgrum as gum
import pyAgrum.lib.pylimid as pl

# Build a new LIMID
oil = pl.Limid()

# Chance nodes
Q = oil.addChanceNode("Q", ["high", "medium", "low"])
R = oil.addChanceNode("R", ["pass", "fail", "no_results"])

# Decision nodes
T = oil.addDecisionNode("T", ["test", "no_test"])
B = oil.addDecisionNode("B", ["buy", "no_buy"])

# Utility node
U = oil.addUtilityNode("U")

# Arcs
for parent, child in [(Q, R), (T, R), (R, B), (T, B), (B, U), (Q, U), (T, U)]:
    oil.addArc(parent, child)

# CPTs (truncated to save space — see tables above for full numbers)
oil.cpt(Q).fillWith([0.35, 0.45, 0.20])
oil.cpt(R)[{"T": "test", "Q": "high"}] = [0.95, 0.05, 0.0]
# … populate remaining rows as in the article …

# Utilities (again shortened here)
oil.utility(U)[{"T": "test", "B": "buy", "Q": "high"}] = 1250
# … remaining utility entries …

# Solve with Shenoy–Shafer
solver = pl.ShenoyShaferLIMID(oil)
solver.solve()
print("Optimal policy for B:", solver.optimalDecision(b=B))
print("Expected utility:", solver.expectedUtility())
```

Running the script prints something like:

```
Optimal policy for B: {'pass': 'buy', 'fail': 'no_buy', 'no_results': 'buy'}
Expected utility: 721.0
```

For detailed theoretical background on the algorithm, see Shafer & Shenoy (1987). For a broader comparison of evaluation methods, consult Shachter (1986) and Jensen et al. (1994).
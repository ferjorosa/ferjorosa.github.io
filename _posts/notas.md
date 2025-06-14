Yo creo que deberia comentar 2 limitaciones principales y explicarlas bien (todo en una seccion, quizas con subsecciones)

https://chat.qwen.ai/c/547f489b-00f5-4844-91da-183664fcb5b6

* Explosion combinatoria, lo cual tiene consecuencias tanto a nivel computacional (memoria y numero de computaciones) y a nivel de interpretabilidad porque los arboles se vuelven enormes y muy dificiles de manejar

* Hidden Conditional Independencies


Comentamos estas limitaciones sin hablar de los diagramas de influencia, simplemente exponemos claramente cuales son

Luego abrimos ya el tema de los diagramas de influencia en otradecimos que no fue hasta 1980 donde se introdujo otra manera de resolver estos problemas que atacaban las limitaciones anteriores

Lueggo no se si en esta seccion o mas adelante me gustaria hablar de las librerias, quizas en su propia seccion y comentar que nunca ha habido mucho como ha pasado con deep learning lo cual en parte limita su desarrollo. Sin embargo hoy en dia hay un par de librerias buenas en Python: Pyagrum y PyCID

------

Las ventajas de los decision trees son:

But decision trees still shine at…
Pedagogy & storytelling
Non-technical stakeholders instantly grasp “if this, then that” paths.
Step-by-step simulation / audit trails
Each complete path spells out exactly which events happen and when—a great audit log for regulators or auditors.
Tiny to medium-sized, sequential problems where conditional independence offers little compression; building a diagram would be overhead.
Visualising temporal order explicitly
The left-to-right layout forces you to check that information sets are correct; diagrams can sometimes hide timing mistakes if arcs are drawn sloppily.
Quick hand calculations
For a two- or three-stage problem you can solve the tree with pencil and paper; diagram solvers usually require software.
Teaching backward induction and the idea of “rolling back” expected utility.


---------------

Why decision trees start to creak
Combinatorial explosion
Every extra decision or chance variable multiplies the number of branches.
Even modest problems (e.g., 4 decisions × 3 outcomes each) balloon into hundreds of terminal nodes.
Redundancy and lack of factorisation
The same chance variable may appear in many branches, forcing you to repeat conditional probabilities rather than specify them once.
Hidden conditional independencies
Trees can’t explicitly show that two uncertainties are independent given a third; everything is hard-wired in branch order.
Awkward for shared information or feedback loops
If a later decision revisits an earlier uncertainty, a tree must be “unfolded” again, duplicating sub-trees.
Harder sensitivity analysis
You usually need to regenerate or prune a whole tree to test a new probability or cost; an influence diagram lets you flip one arrow or table.
Poor at multi-attribute utilities
Utilities that depend on several variables require large terminal tables; diagrams can keep a separate utility node for each attribute.
Single-player bias
Multi-agent or adversarial choices are clumsy; game trees exist, but influence diagrams generalise more naturally to multi-party settings.
Cosmetic but real: readability
Large trees rarely fit on a slide or page; navigating them in code or on paper is error-prone.


Why influence diagrams ease the pain
Compact graph: each variable (decision, chance, utility) is shown once.
Explicit conditional independence – fewer numbers to assess.
Easier to edit: adding or deleting a node/arc can update the entire optimisation automatically.
Clean separation of structure (arcs) and tables (CPTs, utility functions).
Built-in hooks for VOI (value of information) and sensitivity analysis.
Supported by specialised libraries (PyAgrum, PyCID, GeNIe/SMILE, Hugin).
Closer to Bayesian-network tooling and mindset—good for analysts already using probabilistic graphical models.
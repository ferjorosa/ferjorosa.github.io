---
layout: post
title: "Introduction to Decision Theory: Part III"
date: 2025-07-15
categories: blog
description: "Deep dive into sensitivity analysis for decision problems, implementing the oil field purchase decision using PyAgrum's library, and creating an interactive web interface with Gradio to explore how changes in probabilities and utilities affect optimal decisions."
tags: [Decision Theory]
---


La primera parte del blogpost habla de PyAgrum y de como podemos implementar el diagrama de influencia de la parte 2.

De lo relativamente facil que es ejecutar la inferencia y lo rapido que es.

Luego comentamos que parte de analizar un problema de decision es entender como de robusta es dicha decision ante cambios en los parametros y comentamos que hay diferentes posibilidades para hacerlo.

En este punto o quizas antes podemos comentar la importancia de tener interfaces graficos como lo que hacemos con Gradio par amodificar los valores con combinaciones especificas y evaluar diferentes hipotesis del tipo de:

que pasa si el coste del test sube 10 millones y la probabilidad a priori de que el oil field sea de alta calidad baja 5 puntos porcentuale?

Ademas de esto, existen tecnicas "estandar" para observar la importancia de variables con respecto a otras de forma mas "generica"

-----

Pensando en diagramas, podemos evaluar el impacto de una variable univariante:
* X: utilidad esperada
* Y: valor de la variable

Pintamos cada punto con colores donde las diferentes combinaciones de las variables de decision. Por ejemplo, en nuestro caso ponemos 4 combinaciones, cada una de un color

Para 2 variables, la manera que se me ocurre es que pintamos los puntos como arriba y que al posar sobre ellos te salga el valor de la MEU

Con respecto a los diagramas, yo los haria con Seaborn para que pudieran ser exportados a Javascript y pegados en el blogpost.

-----

Leyendo el libro veo que cuando crean las regiones de decision lo hacen porque utilizan un arbol de decision "simple". En nuestro caso que es con un diagrama de influencia yo creo que tiene sentido hacerlo con sampleo.

-----

Un tema interesante de porque investigar el impacto de variables es cosas como:
* Si pudieramos incrementar el accuracy de nuestras priors de tal forma que los campos a los que fueramos a comprar tuvieran una mayor probabilidad de ser high, cuanto seria lo que deberiamos pagar? Cuanto cuesta esa informacion
* Cuanto afecta el precio del test a si lo hacemos o no asumiendo que las probabilidades no cambian o
* Cuanto podriamos pagar de mas si el test vale mas pero es mas preciso, etc.


<h2 id="sensitivity_analysis">Sensitivity Analysis</h2>


Actualizar los valores de utilidad tanto en este blogpost, como en el viejo, como en el código.

<!-- 
<script
	type="module"
	src="https://gradio.s3-us-west-2.amazonaws.com/5.31.0/gradio.js"
></script> 

<gradio-app src="https://ferjorosa-oil-field-purchase-decision.hf.space"></gradio-app>
-->
La idea de este blog-post es reflexionar sobre los posibles casos de uso  de los modelos tiny, hablar sobre los modelos modernos mini como function-gemma, Monad y similar, y mostrar que tal funcionan y si sirven para algo

en mi caso he entrenado un modelo de historias con el dato de tiny-stories que me parece interesante y por otro lado, he entrenado un modelo de codigo con el swallow-code dataset

Puedo poner informacion de esos runs si estoy interesado, de como las metricas de validacion siguen bajando incluso cuando parece que no deberian...

Creo que lo primero que habria que hacer en este caso es correr VLLM con esos mini-modelos y ver como podemos benchmarkear de alguna forma cuantas instancias simultaneas podriamos correr en una unica GPU, para entender cuanto seria el pool de "agentes", entendiendose como agente un mini-LLM que vive en su mundo


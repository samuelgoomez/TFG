Problema: El artículo aborda la generación de abstracts científicos mediante Inteligencia Artificial. El problema principal es que usar un único LLM para todo el proceso genera texto con alucinaciones y mala estructura, por lo que se busca solucionarlo imitando el proceso humano paso a paso.

Objetivo: El objetivo principal es diseñar y desarrollar un sistema multiagente compuesto por 7 agentes especializados que colaboren para estructurar, redactar y revisar abstracts científicos de forma automatizada, siguiendo las directrices académicas de Scribbr.

Metodología: Se ha implementado una arquitectura jerárquica utilizando el framework CrewAI. Se han configurado 7 agentes con roles especializados y prompts específicos, y se ha integrado con modelos de lenguaje grandes (Llama) a través de la API de OpenRouter para ejecutar las tareas de forma secuencial y validada.

Resultados: Se ha desarrollado con éxito un prototipo funcional que entrevista al usuario, valida los datos y redacta el texto final. Las pruebas demuestran que este enfoque multiagente reduce drásticamente las alucinaciones y produce abstracts con una estructura y rigor académico muy superiores a los generados con un único LLM.

Conclusión: La principal conclusión es que segmentar tareas cognitivas complejas en agentes de IA especializados es mucho más efectivo y seguro que depender de un único modelo generalista. La mayor aportación es el diseño de este flujo de trabajo modular que simula el razonamiento humano y garantiza que la redacción académica se fundamente únicamente en datos validados.

Restricciones: El abstract debe tener una extensión máxima de 250 palabras. El contexto específico es que servirá como presentación de un Trabajo de Fin de Grado (TFG) universitario en el ámbito tecnológico, por lo que debe mantener un tono formal, objetivo y estrictamente académico alineado con las recomendaciones de Scribbr.
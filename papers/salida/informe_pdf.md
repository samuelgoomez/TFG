**Problema**  
El problema abordado en el artículo "Attention Is All You Need" es la limitación de las redes neuronales recurrentes (RNN) en tareas de modelado secuencial, como la traducción automática, que requieren computación secuencial y dificultan el paralelismo, especialmente con secuencias largas.

**Objetivo**  
El objetivo principal del trabajo es proponer un nuevo modelo de arquitectura denominado Transformer, que elimine la recurrencia y se base completamente en un mecanismo de atención para mejorar la eficiencia y calidad en tareas de traducción automática.

**Metodología**  
La metodología seguida incluye el uso de un modelo Transformer que consta de secciones de codificación y decodificación apiladas, cada una compuesta por sub-capacidades de auto-atención y redes neuronales totalmente conectadas. Se utilizó un mecanismo de atención ponderado, así como codificaciones posicionales para proporcionar información sobre la orden en la que aparecen las palabras.

**Resultados**  
Los resultados obtenidos indican que el modelo Transformer logra un puntaje BLEU de 28.4 en la tarea de traducción inglés-alemán, y un puntaje de 41.0 en inglés-francés, estableciendo un nuevo estado del arte. Estos resultados se lograron en 12 horas de entrenamiento en 8 GPU P100 para el modelo básico y 3.5 días para el modelo grande.

**Conclusión**  
La principal conclusión del trabajo es que el modelo Transformer no solo supera el rendimiento de modelos previos basados en RNN y convolucionales en tareas de traducción, sino que también permite un entrenamiento significativamente más rápido al eliminar la naturaleza secuencial de los cálculos.

**Restricciones**  
Las restricciones de formato no se especifican de manera explícita en el documento. Sin embargo, se mencionan limitaciones en términos de dependencia de la longitud del texto, donde el modelo se probó en conjuntos de datos estándar como WMT 2014.
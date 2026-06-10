Problema:
El artículo aborda el problema de las limitaciones de los modelos de redes neuronales recurrentes (RNNs) y las arquitecturas seq2seq en el procesamiento de lenguajes, específicamente en la traducción automática, destacando la dificultad de aprender dependencias de largo alcance debido a la naturaleza secuencial de dichos modelos.

Objetivo:
El objetivo principal del trabajo es presentar el Transformer, un nuevo modelo de arquitectura que reemplaza las capas recurrentes de los modelos de codificación-decodificación con mecanismos de atención, permitiendo así una mejor paralelización y mejorando la calidad de las traducciones.

Metodología:
La metodología seguida incluye la implementación de un modelo de Transformer que utiliza múltiples capas de atención y redes neuronales completamente conectadas en las etapas de codificación y decodificación. La atención se calcula mediante un mecanismo conocido como "atención escalada por producto punto", que permite a cada palabra en la entrada conectar directamente con todas las palabras en la salida a través de cálculos de similitud.

Resultados:
Los resultados obtenidos muestran que el modelo / Transformer logra un puntaje BLEU de 28.4 en la tarea de traducción inglés-alemán y un puntaje BLEU de 41.0 en la tarea de traducción inglés-francés, estableciendo un nuevo estado del arte en ambas tareas con un costo de entrenamiento significativamente menor en comparación con modelos anteriores.

Conclusión:
La principal conclusión del trabajo es que el Transformer, al basarse completamente en el mecanismo de atención, no solo mejora la calidad de traducción en comparación con las arquitecturas recurrentes, sino que también se entrena de manera más rápida, sugiriendo el potencial para aplicaciones en tareas relacionadas que implican entradas y salidas más allá de texto.

Restricciones:
No se especifican limitaciones concretas de formato en términos de extensión de palabras o contexto del documento en el artículo.
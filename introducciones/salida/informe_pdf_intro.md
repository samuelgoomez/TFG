# 1. Tipo de Artículo y Ejes de Shaw
El artículo "Attention Is All You Need" es un trabajo técnico que propone un nuevo modelo de arquitectura basado enteramente en mecanismos de atención, llamado Transformador, para el tratamiento de tareas de traducción automática. La pregunta de investigación que aborda es cómo mejorar la calidad de la traducción automática a través de un modelo que supere las limitaciones de los modelos existentes que utilizan redes neuronales recurrentes o convolucionales. La contribución principal es la introducción del modelo Transformador, que se centra en la atención sin recurrencia ni convoluciones. La validación se realiza a través de experimentos en tareas de traducción, donde se reportan mejoras significativas en la calidad de las traducciones. El artículo fue publicado en la conferencia NIPS 2017, en inglés.

# 2. Territorio
El contexto del trabajo se sitúa en la traducción automática, un área crítica en la inteligencia artificial que busca convertir texto de un idioma a otro. La relevancia de este tema radica en que las traducciones automáticas tienen aplicaciones en numerosas industrias y contribuyen a la superación de barreras lingüísticas en la comunicación y el acceso a la información.

# 3. Hueco
Reconociendo que muchos modelos existentes de traducción automática se basan en arquitecturas complejas que enfrentan problemas para aprender dependencias de largo alcance, el trabajo sostiene que el uso de un vector de longitud fija para codificar oraciones completas es una limitación crítica. En este sentido, los trabajos citados como Bahdanau et al. (2014) y Sutskever et al. (2014) abordan aspectos de dependencia de largo alcance, pero el modelo básico de codificación-decodificación presenta desafíos significativos en este aspecto.

# 4. Idea
La propuesta central del trabajo es que el modelo Transformador, que utiliza exclusivamente mecanismos de atención, puede manejar de manera mas efectiva las dependencias de largo alcance en la traducción automática. Esta arquitectura permite una mejor paralelización y requiere menos tiempo de entrenamiento en comparación con enfoques anteriores.

# 5. Contribuciones
Las principales contribuciones incluyen:
- Introducción del modelo Transformador, descrito en la sección 3 del documento.
- Superación de los resultados anteriores en tareas de traducción del conjunto de datos WMT 2014 con puntuaciones BLEU mejoradas, detalladas en la sección 6.
- Validación de la robustez del modelo frente a la longitud de las oraciones.

# 6. Evaluación
La evaluación del modelo se realizó a través de experimentos con conjuntos de datos en tareas de traducción automatizada, donde se utilizó la puntuación BLEU para medir la calidad de las traducciones generadas. Los resultados mostraron que el modelo Transformador lograba puntuaciones significativamente más altas que los modelos anteriores, requería menos tiempo de entrenamiento y tenía mejores capacidades para la generalización en tareas de traducción.

# 7. Estructura del Documento
El documento se organiza en secciones que comienzan con la introducción del contexto y problema (sección 1), seguido de antecedentes (sección 2), la descripción del modelo y sus componentes (sección 3), la presentación de resultados experimentales (sección 4), discusiones y conclusiones (sección 5), y posteriormente, la referencia a trabajos relacionados y agradecimientos en la conclusión.
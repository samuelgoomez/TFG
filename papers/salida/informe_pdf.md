Problema:
El trabajo aborda el problema de preentrenamiento de modelos de lenguaje para mejorar el rendimiento en diversas tareas de procesamiento de lenguaje natural (NLP), tanto a nivel de oración como a nivel de token, tales como inferencia natural del lenguaje, parafraseo, reconocimiento de entidades nombradas y preguntas-respuestas. Un problema clave es superar las limitaciones de los modelos unidireccionales para capturar el contexto completo de una secuencia.

Objetivo:
El objetivo principal es proponer BERT (Bidirectional Encoder Representations from Transformers), un modelo de preentrenamiento bidireccional profundo basado en Transformers, que utiliza dos objetivos de preentrenamiento (enmascarado de lenguaje y predicción de siguiente oración) para aprender representaciones contextuales que mejoren el desempeño en once tareas principales de NLP, estableciendo un nuevo estado del arte.

Metodología:
BERT utiliza una arquitectura de Transformer bidireccional con 12 o 24 capas, con 768 o 1024 unidades ocultas y distintas cabezas de atención. El preentrenamiento se realiza en dos tareas: (1) Masked Language Model (MLM), donde se enmascaran aleatoriamente el 15% de los tokens y el modelo predice los originales; (2) Next Sentence Prediction (NSP), que clasifica si una oración B es la siguiente oración verdadera después de A o no. Se preentrena con el BooksCorpus (800M palabras) y Wikipedia (2,500M palabras). Luego, se realiza fine-tuning ajustando todos los parámetros del modelo en tareas específicas usando las representaciones preentrenadas.

Resultados:
BERT mejora significativamente el estado del arte en múltiples benchmarks de NLP:
- En GLUE, BERT LARGE obtiene un promedio de exactitud del 82.1%, superando al OpenAI GPT (75.1%) y a otros modelos, con mejoras de 4.5% a 7.0% en varios conjuntos.
- En SQuAD v1.1, BERT LARGE alcanza un F1 de 91.0%, superando el mejor resultado previo.
- En SQuAD v2.0, BERT LARGE logra mejoras de +5.1 puntos F1 sobre el siguiente mejor sistema.
- En SWAG, BERT LARGE (con datos adicionales) alcanza un accuracy de hasta 93.2% en test.
- Para NER en CoNLL-2003, BERT LARGE logra un F1 del 92.8% al fine-tunear todo el modelo.
Además, ablation studies demuestran que la combinación MLM + NSP y la bidireccionalidad son fundamentales para el rendimiento. También se observa que modelos mayores (más capas y dimensiones) mejoran consistentemente la precisión.

Conclusión:
El trabajo demuestra que el preentrenamiento profundo y bidireccional de modelos Transformer con las tareas MLM y NSP permite obtener representaciones de lenguaje universalmente útiles para una amplia gama de tareas de NLP, elevando el rendimiento a nuevos niveles y reduciendo la dependencia de arquitecturas específicas. BERT es efectivo tanto para fine-tuning como para uso como extractor de características.

Restricciones:
- No se especifican limitaciones de formato para el resumen.
- El contexto del documento es un artículo científico de investigación en NLP.
- Se usó un vocabulario WordPiece de 30,000 tokens, secuencias máximas de 512 tokens en preentrenamiento.
- El preentrenamiento se ejecutó con batch size de 256 secuencias, 1M pasos.
- El fine-tuning generalmente usa batches de 16 o 32 y de 2 a 4 epochs según tarea.

Esta información se extrajo estrictamente del texto del PDF sin inferencias adicionales.
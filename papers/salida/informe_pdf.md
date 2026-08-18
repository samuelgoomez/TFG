Problema:
El problema abordado es la mejora del aprendizaje de representaciones de lenguaje natural mediante preentrenamiento de modelos de lenguaje profundos y bidireccionales, que permitan un mejor desempeño en múltiples tareas de procesamiento del lenguaje natural (NLP), tanto a nivel de oración como de token, superando las limitaciones de modelos unidireccionales o basados en concatenaciones superficiales.

Objetivo:
El objetivo principal es proponer y evaluar BERT (Bidirectional Encoder Representations from Transformers), un modelo basado en Transformers bidireccionales preentrenado con tareas de lenguaje enmascarado y predicción de la siguiente oración, que mejora el estado del arte en once tareas de NLP, reduciendo la necesidad de arquitecturas específicas para tareas y permitiendo un fine-tuning eficiente y efectivo.

Metodología:
- Se utiliza un modelo basado en un Transformer bidireccional con preentrenamiento en dos tareas:
  1. Máscara de lenguaje (masked language model, MLM): se enmascara aleatoriamente el 15% de los tokens y el modelo debe predecir esos tokens solo a partir del contexto bidireccional.
  2. Predicción de la siguiente oración (next sentence prediction, NSP): se entrena para predecir si una oración B sigue a una oración A en el texto o es una oración aleatoria.
- El preentrenamiento se realiza con el corpus BooksCorpus (800M palabras) y Wikipedia en inglés (2,500M palabras).
- El modelo tiene dos tamaños principales: BERT BASE (12 capas, 768 dimensiones, 110M parámetros) y BERT LARGE (24 capas, 1024 dimensiones, 340M parámetros).
- Se evalúa fine-tuning en múltiples conjuntos de tareas, incluyendo GLUE, SQuAD v1.1 y v2.0, SWAG, entre otros.
- El fine-tuning se hace ajustando todos los parámetros del modelo con los datos específicos de cada tarea.
- Se compara también un enfoque basado en extracción de características (feature-based) usando activaciones fijas del modelo sin fine-tuning.

Resultados:
- BERT mejora el estado del arte en once tareas de NLP con aumentos de hasta +7.0 puntos en promedio de exactitud sobre sistemas previos.
- En GLUE, BERT LARGE alcanza un promedio de 82.1% de exactitud, superando a OpenAI GPT (75.1%) y a modelos anteriores.
- En SQuAD v1.1, BERT LARGE logra un F1 de 91.0%, mejorando en +5.1 puntos el siguiente mejor sistema.
- En SQuAD v2.0 y SWAG, BERT también supera ampliamente a sistemas previos.
- BERT alcanza 97-98% de precisión en la tarea de NSP.
- Los ablations muestran la importancia de las dos tareas de preentrenamiento y el tamaño del modelo para el desempeño.
- El enfoque de extracción de características también obtiene resultados competitivos, con sólo 0.3 F1 menos en NER que el fine-tuning completo.

Conclusión:
BERT demuestra que el preentrenamiento bidireccional profundo con MLM y NSP permite obtener representaciones del lenguaje más ricas y generalizables que mejoran considerablemente el desempeño en un amplio rango de tareas NLP, simplificando las arquitecturas específicas para cada tarea y estableciendo un nuevo estándar que ha sido ampliamente adoptado.

Restricciones:
- No se especifican restricciones explícitas de formato o límites de palabras en el documento.
- Las secuencias de entrada tienen un máximo de 512 tokens.
- El preentrenamiento se realiza con grandes cantidades de datos no etiquetados (BooksCorpus y Wikipedia).
- El proceso de entrenamiento requiere hardware especializado (Cloud TPU) y es costoso en tiempo (varios días).
- Fine-tuning típico dura pocas horas y depende del tamaño del dataset específico.
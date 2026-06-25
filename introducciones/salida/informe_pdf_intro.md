# Tipo de Artículo y Ejes de Shaw
El artículo "Attention Is All You Need" es un artículo de investigación que propone un nuevo modelo de arquitectura de red, el Transformer, que transforma datos secuenciales utilizando únicamente mecanismos de atención. Los ejes de Shaw discutidos en el contexto del artículo son la eficiencia computacional y la capacidad para manejar dependencias a largo plazo en las secuencias.

# Territorio
El territorio de estudio abarca el campo de la traducción automática y los modelos de transducción de secuencias, específicamente comparando el rendimiento de modelos basados en atención frente a los modelos recurrentes y convolucionales tradicionales.

# Hueco
Se identifica un hueco en la literatura en la forma en que los modelos de transducción de secuencias tradicionalmente han utilizado redes neuronales recurrentes (RNNs) que dependen de un mapeo a un vector de longitud fija, lo que limita su eficacia para manejar secuencias largas y complejas. El documento propone cerrar este hueco al eliminar la dependencia de la recurrencia.

# Idea o Enfoque
La idea principal del artículo es introducir el Transformer, una arquitectura que elimina el uso de RNNs y CNNs y se basa exclusivamente en mecanismos de atención, lo que permite una mayor paralelización y mejora del tiempo de entrenamiento sin sacrificar la calidad de traducción.

# Contribuciones
Las contribuciones del artículo son múltiples: presenta una nueva arquitectura, el Transformer, que logra resultados de primer nivel en traducción automática (28.4 BLEU para el inglés-alemán y 41.8 para el inglés-francés) y mejora la capacidad de atención a partes relevantes de una secuencia de entrada a lo largo de toda la longitud de la secuencia.

# Evaluación
La evaluación se lleva a cabo utilizando métricas estándar como BLEU en conjuntos de datos bien establecidos (WMT 2014 para inglés-alemán y inglés-francés). El rendimiento del modelo Transformer es comparado con los mejores modelos existentes de la literatura, demostrando su superioridad en términos de calidad de traducción y eficiencia durante el entrenamiento.

# Estructura del Documento
La estructura del documento incluye una introducción que contextualiza el problema y el modelo, una descripción detallada de la arquitectura del Transformer, comparaciones con modelos existentes, experimentos y resultados, y finalmente una conclusión. Las secciones están diseñadas para llevar al lector a través del razonamiento detrás del diseño del modelo y su eficacia.
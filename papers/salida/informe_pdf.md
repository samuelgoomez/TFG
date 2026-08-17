Problema:
El trabajo aborda la limitación de los modelos de redes recurrentes y convolucionales en tareas de modelado y transducción de secuencias, específicamente la dificultad de paralelización y la modelación de dependencias largas en secuencias. Los modelos recurrentes como RNNs, LSTMs y GRUs, aunque efectivos, son inherentemente secuenciales y difíciles de paralelizar, lo que limita la eficiencia en secuencias largas.

Objetivo:
Proponer el Transformer, un modelo de transducción de secuencia que reemplaza las recurrencias con un mecanismo basado enteramente en atención, permitiendo paralelización significativa durante el entrenamiento y alcanzando un nuevo estado del arte en calidad de traducción.

Metodología:
El Transformer utiliza una arquitectura encoder-decoder con pilas de capas idénticas (6 en el modelo base) que contienen mecanismos de atención multi-cabeza y redes feed-forward posicionales. La atención escalada por producto punto es la base del mecanismo de atención. Se emplea atención multi-cabeza para atender a diferentes subespacios de representación simultáneamente. Se añade codificación posicional sinusoidal para inyectar información sobre el orden de las secuencias, dado que no hay recurrencia ni convolución. Se entrenó sobre los datasets WMT 2014 English-German (4.5M pares de oraciones) y English-French (36M pares) usando byte-pair encoding y word-piece. Se usaron 8 GPUs P100 con optimizador Adam y técnica de label smoothing y dropout para regularización.

Resultados:
- En la tarea de traducción inglés-alemán WMT 2014, el modelo Transformer grande ("Transformer (big)") logra un BLEU de 28.4, superando en más de 2.0 BLEU a los mejores modelos anteriores, incluidos ensamblajes. El entrenamiento tomó 3.5 días en 8 GPUs P100.
- En la tarea inglés-francés WMT 2014, el modelo grande alcanzó un BLEU de 41.0, superando todos los modelos individuales publicados previamente, con menos de 1/4 del costo de entrenamiento del estado del arte anterior.
- El modelo base también supera otros modelos y ensamblajes con menor costo de entrenamiento.
- Variaciones en el número de cabezas de atención, tamaños de claves/valores y dropout muestran que más cabezas no siempre mejoran BLEU, que la dimensión de la clave es crítica para la calidad, y que el dropout es efectivo contra overfitting.
- En análisis adicional, se aplicó para el parseo sintáctico del inglés con resultados competitivos (F1 91.3 WSJ solo; 92.7 semi-supervisado).
- Las métricas clave: BLEU para traducción (28.4 para EN-DE, 41.0 para EN-FR) y F1 para parseo (hasta 92.7), números de parámetros (base: 65M, big: 213M), y desempeño computacional detallado.

Conclusión:
El Transformer es el primer modelo de transducción secuencial basado completamente en atención que elimina la recurrencia, permite un entrenamiento más rápido y alcanza nuevos niveles de calidad en traducción automática. Se destaca por su paralelización efectiva y capacidad para modelar dependencias largas con menor costo computacional. Se plantea su uso futuro en otras modalidades como imagen, audio y video, y en generación no secuencial.

Restricciones:
- No se mencionan restricciones explícitas de formato o límite de palabras para el documento del modelo.
- En entrenamiento se usa agrupación por longitud de secuencia para batching, máximo output length en inferencia limitado a input length + 50 para traducción y +300 para parseo.
- Modelo base entrenado 12 horas/100,000 pasos, modelo grande 3.5 días/300,000 pasos en 8 GPUs P100.

Este es el informe con los detalles técnicos extraídos fielmente del PDF.
# Problema
El documento aborda las limitaciones de las redes neuronales recurrentes (RNNs) y los problemas relacionados con la modelación secuencial, como el aprendizaje de dependencias a larga distancia en tareas de traducción automática.

# Objetivo
El objetivo principal del trabajo es presentar el modelo Transformer, que reemplaza la recurrencia con un mecanismo de atención para capturar dependencias globales en los datos, lo que permite una mayor paralelización y mejora la calidad de la traducción.

# Metodología
El modelo Transformer utiliza una arquitectura de codificador-decodificador con capas de atención multi-cabeza y una red neuronal de alimentación hacia adelante. Utiliza codificaciones posicionales para mantener el orden de la secuencia sin recurrencia.

# Resultados
El modelo Transformer alcanzó un puntaje BLEU de 28.4 en la tarea de traducción de inglés a alemán y 41.0 en inglés a francés, superando los modelos previos. Utilizó 8 GPUs P100 y se entrenó en 12 horas para el modelo base y 3.5 días para el modelo grande.

# Conclusión
El Transformer es el primer modelo de transducción que depende únicamente de mecanismos de atención, logrando rapidez y calidad superior en tareas de traducción. Esto establece un nuevo estándar en la calidad de traducción y sugiere futuros usos en diferentes modalidades de entrada y salida.

# Restricciones
No se mencionan restricciones de formato específicas en el documento (límite de palabras, idioma, contexto del documento).
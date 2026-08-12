Problema:
El artículo aborda la problemática del modelado y transducción de secuencias en tareas como la traducción automática. Se critica la dependencia de modelos recurrentes y convolucionales que limitan el paralelismo y la eficiencia computacional, proponiendo un enfoque basado únicamente en mecanismos de atención para superar estas limitaciones.

Objetivo:
Presentar el Transformer, un modelo basado exclusivamente en mecanismos de atención (self-attention) que elimina la recurrencia y las convoluciones en tareas de transducción de secuencias, mejorando la eficiencia computacional y alcanzando nuevos estados del arte en calidad de traducción.

Metodología:
Se plantea una arquitectura encoder-decoder con capas apiladas que usan multi-head self-attention y redes feed-forward por posición. Introducen atención escalada por producto punto, multi-head attention para capturar diferentes subespacios representacionales, y codificación posicional basada en funciones seno y coseno para mantener información posicional sin recurrencias o convoluciones. El modelo se entrena en los datasets WMT 2014 EN-DE y EN-FR, usando el optimizador Adam con programación de tasa de aprendizaje, regularización con dropout y label smoothing.

Resultados:
- En traducción inglés-alemán (WMT 2014 EN-DE), el modelo big Transformer alcanzó un BLEU de 28.4, superando modelos previos incluyendo ensembles, entrenado en 3.5 días con 8 GPUs P100.
- En traducción inglés-francés (WMT 2014 EN-FR), logró un BLEU de 41.8, también superando modelos previos a menor coste de entrenamiento.
- El modelo base superó modelos previos y ensembles con menor coste computacional.
- El Transformer mostró buena generalización en análisis sintáctico, obteniendo resultados competitivos en regímenes de pocos datos.

Conclusión:
El Transformer es el primer modelo de transducción de secuencias basado totalmente en mecanismos de atención, eliminando la necesidad de recurrencias y convoluciones. Permite entrenamiento más rápido, mayor paralelismo, y supera el estado del arte en traducción automática a menor coste. Se avanza hacia su aplicación en otros dominios y modalidades, y se indican futuras investigaciones en atenciones restringidas y generación menos secuencial.

Restricciones:
No se mencionan restricciones explícitas de formato en el documento.
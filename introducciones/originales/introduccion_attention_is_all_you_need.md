# Attention Is All You Need
**Vaswani et al., 2017 — arXiv:1706.03762**
**Idioma:** Inglés

## Introducción original

Recurrent neural networks, long short-term memory [13] and gated recurrent [7] neural networks
in particular, have been firmly established as state of the art approaches in sequence modeling and
transduction problems such as language modeling and machine translation [35, 2, 5]. Numerous
efforts have since continued to push the boundaries of recurrent language models and encoder-decoder
architectures [38, 24, 15].

Recurrent models typically factor computation along the symbol positions of the input and output
sequences. Aligning the positions to steps in computation time, they generate a sequence of hidden
states ht, as a function of the previous hidden state ht−1 and the input for position t. This inherently
sequential nature precludes parallelization within training examples, which becomes critical at longer
sequence lengths, as memory constraints limit batching across examples. Recent work has achieved
significant improvements in computational efficiency through factorization tricks [21] and conditional
computation [32], while also improving model performance in case of the latter. The fundamental
constraint of sequential computation, however, remains.

Attention mechanisms have become an integral part of compelling sequence modeling and transduction
models in various tasks, allowing modeling of dependencies without regard to their distance in
the input or output sequences [2, 19]. In all but a few cases [27], however, such attention mechanisms
are used in conjunction with a recurrent network.

In this work we propose the Transformer, a model architecture eschewing recurrence and instead
relying entirely on an attention mechanism to draw global dependencies between input and output.
The Transformer allows for significantly more parallelization and can reach a new state of the art in
translation quality after being trained for as little as twelve hours on eight P100 GPUs.

## Puntos clave esperados (modelo CARS + ejes de Shaw)

| Punto | Contenido |
|---|---|
| Territorio | Las RNN, LSTM y GRU son el estado del arte en modelado de secuencias y traducción automática; trabajos recientes siguen mejorando estos modelos recurrentes |
| Hueco | El cómputo secuencial inherente de los modelos recurrentes impide la paralelización dentro de cada ejemplo de entrenamiento, especialmente en secuencias largas |
| Idea | Proponer el Transformer, una arquitectura que prescinde de la recurrencia y se basa únicamente en mecanismos de atención |
| Contribuciones | Arquitectura Transformer basada solo en atención; mayor paralelización; nuevo estado del arte en calidad de traducción entrenando en solo 12 horas con 8 GPUs P100 |
| Evaluación | Experimentos en dos tareas de traducción automática (WMT 2014 EN-DE y EN-FR) |
| Estructura del Documento | No se detalla explícitamente la organización de las siguientes secciones en la introducción original |

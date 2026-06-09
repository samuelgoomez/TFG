# Attention Is All You Need
**Vaswani et al., 2017 — arXiv:1706.03762**
**Idioma:** Inglés

## Abstract original

The dominant sequence transduction models are based on complex recurrent or convolutional neural networks in an encoder-decoder configuration. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine translation tasks show these models to be superior in quality while being more parallelizable and requiring significantly less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-to-German translation task, improving over the existing best results, including ensembles by over 2 BLEU. On the WMT 2014 English-to-French translation task, our model establishes a new single-model state-of-the-art BLEU score of 41.8 after training for 3.5 days on eight GPUs, a small fraction of the training costs of the best models from the literature. We show that the Transformer generalizes well to other tasks by applying it successfully to English constituency parsing both with large and limited training data.

## Puntos clave esperados

| Punto | Contenido |
|---|---|
| Problema | Los modelos dominantes de transducción de secuencias usan RNNs/CNNs complejas |
| Objetivo | Proponer una arquitectura nueva basada únicamente en mecanismos de atención |
| Metodología | Arquitectura Transformer con self-attention; experimentos en traducción WMT 2014 |
| Resultados | 28.4 BLEU (EN→DE) y 41.8 BLEU (EN→FR), nuevo estado del arte |
| Conclusión | El Transformer generaliza bien a otras tareas como parsing con datos limitados |
| Restricciones | No se mencionan en el paper |

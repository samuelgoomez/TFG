Tipo de Artículo y Ejes de Shaw:
El artículo es de tipo técnica/sistema y presenta una herramienta concreta con una arquitectura definida. La pregunta de investigación que aborda es de método/medios, específicamente cómo automatizar la revisión de código de forma fiable usando modelos de lenguaje. La contribución principal es un sistema funcional junto con un dataset público etiquetado. La validación se realiza mediante un experimento controlado con métricas F1 y un estudio de usuario con 12 desarrolladores y 100 pull requests. Está dirigido a un venue del área de ingeniería de software, como conferencias ICSE o FSE, y el idioma del artículo es español.

Territorio:
La revisión de código es fundamental en el desarrollo de software moderno para detectar defectos, mejorar mantenibilidad y transferir conocimiento. Con plataformas como GitHub y GitLab, el volumen de pull requests ha crecido mucho, generando un cuello de botella. Modelos preentrenados como CodeBERT y GraphCodeBERT han avanzado en comprensión semántica y estructural del código. La intersección entre ingeniería de software empírica y procesamiento de lenguaje natural aplicado al código es creciente. Trabajos recientes apuntan a detección de bugs, generación automática de tests y resumen automático de código, evidenciando la integración de técnicas NLP en el desarrollo de software.

Hueco:
Los trabajos previos tienen limitaciones específicas: Tufano et al. (2021) usan modelo T5 para sugerir cambios sintácticos, pero no generan comentarios en lenguaje natural; Li et al. (2022) basan su sistema en GPT-2 para proyectos Java pequeños y no hacen estudios de usuario; CodeReviewer (Lu et al., 2022) usa CodeBERT para clasificación binaria simplificada sin diferenciar categorías ni proveer feedback accionable. Falta un sistema que automatice la revisión con alta precisión y ofrezca retroalimentación detallada validada con usuarios reales, que es el hueco que este trabajo aborda.

Idea:
Se propone un sistema que supera la clasificación binaria en revisiones de pull requests, identificando y categorizando problemas en calidad, seguridad y estilo. Para cada problema detectado genera comentarios en lenguaje natural accionables. Usa fine-tuning de CodeBERT con clasificación multi-etiqueta entrenada con 5,000 pull requests etiquetados manualmente en Python y Java. Así, detecta problemas y ofrece retroalimentación comprensible, superando trabajos previos que solo clasifican o no generan comentarios.

Contribuciones:
1. Sistema basado en CodeBERT con clasificación multi-etiqueta (calidad, seguridad, estilo) generando comentarios en lenguaje natural accionables.
2. Dataset público de 5,000 pull requests reales etiquetados manualmente en Python y Java, primero de esta naturaleza disponible.
3. Evaluación empírica combinando métricas F1 por categoría y estudio de usuario con 12 desarrolladores y 100 pull requests.
4. Análisis de límites del sistema, identificando que vulnerabilidades de seguridad complejas son el principal desafío abierto.
Cada contribución se desarrolla en secciones específicas del documento.

Evaluación:
La validación combina un experimento controlado con métricas F1 para clasificación multi-etiqueta y un estudio de usuario con 12 desarrolladores evaluando 100 pull requests reales. Se obtienen evidencias cualitativas y cuantitativas sobre desempeño y usabilidad del sistema en contextos reales, asegurando solidez de resultados y respaldo para las contribuciones. Detalles completos en la Sección 4.

Estructura del Documento:
El artículo se organiza en seis secciones principales: Sección 1 introducción; Sección 2 descripción del dataset; Sección 3 arquitectura y técnica del sistema; Sección 4 evaluación con diseño experimental y resultados; Sección 5 análisis de limitaciones; Sección 6 trabajo relacionado, contrastando con Tufano et al., Li et al. y CodeReviewer. Finaliza con conclusiones y trabajo futuro.
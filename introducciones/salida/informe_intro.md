1. **Tipo de Artículo y Ejes de Shaw**: Es un artículo de tipo técnica/sistema que presenta una herramienta concreta con una arquitectura definida. Se centra en la investigación de método/medios sobre cómo automatizar la revisión de código usando modelos de lenguaje, propone un sistema funcional y un dataset público etiquetado, y combina experimentos controlados con estudios de usuario para validar sus resultados.

2. **Territorio**: El artículo se sitúa en la intersección de la ingeniería del software y el procesamiento de lenguaje natural, abordando la revisión de código dentro de un contexto donde el volumen de pull requests ha aumentado, destacando la necesidad de herramientas que faciliten este proceso.

3. **Hueco**: La literatura existente presenta limitaciones; por ejemplo, trabajos previos como los de Tufano et al. y Li et al. se centran en aspectos limitados de la revisión automática de código. Ningún trabajo ha ofrecido un dataset público etiquetado multilingüe con categorías múltiples, lo que limita la reproducibilidad y la comparación de enfoques.

4. **Idea Central**: Se propone un sistema automatizado que categoriza problemas en tres dimensiones (calidad, seguridad y estilo) y genera comentarios en lenguaje natural para cada uno, utilizando un fine-tuning de CodeBERT con un dataset diseñado para este propósito.

5. **Contribuciones**: Las contribuciones clave incluyen: el desarrollo de un sistema de revisión de código automatizada, un dataset público etiquetado, una evaluación empírica que combina métricas automáticas y un estudio de usuario, y un análisis de las limitaciones del sistema.

6. **Evaluación**: La validez del sistema se evalúa mediante una evaluación automática usando métricas sobre un conjunto de test y un estudio de usuario en el que desarrolladores profesionales comparan el feedback del sistema con el de revisores humanos.

7. **Estructura del Documento**: El documento está organizado en seis secciones: introducción, descripción del dataset, arquitectura del sistema, evaluación, análisis de limitaciones, y revisión del trabajo relacionado, cerrando con conclusiones y líneas futuras de trabajo.
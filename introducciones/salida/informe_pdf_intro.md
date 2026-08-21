Tipo de Artículo y Ejes de Shaw:
El artículo principal es un estudio técnico que propone una técnica basada en Redes Neuronales Artificiales (RNA) para la clasificación de actividades de la vida diaria (AVDs) en pacientes con Enfermedad de Parkinson (EP). La pregunta de investigación responde a cómo mejorar el seguimiento y apoyo en pacientes con EP mediante clasificación automática de actividades. La contribución es una propuesta de modelo clásico de aprendizaje supervisado con validación empírica alcanzando un 99% de precisión en clasificación con un perceptrón multicapa (MLP). La validación se basa en experimentos sobre una base de datos con señales de sensores inerciales. El artículo está en español y su venue es una revista científica mexicana (Revista Mexicana de Ingeniería Biomédica). 

Territorio:
El artículo sitúa la problemática en el contexto del monitoreo de pacientes con EP para mejorar la evaluación clínica, usando sensores inerciales y técnicas de inteligencia artificial, especialmente RNA. Destaca la complejidad de los síntomas motores y la necesidad de sistemas automáticos para seguimiento continuo. Se fundamenta en trabajos previos de sensores wearables, técnicas de análisis de señales (PCA) y modelos MLP aplicados en pacientes con EP y otras patologías.

Hueco:
- Jung et al. (2020): Revisión de sensores inerciales en entornos de vida libre, indica desafíos para aplicar algoritmos desarrollados en entornos controlados a datos obtenidos en condiciones naturales, sugiere necesidad de adaptación para poblaciones con patologías.
- Nguyen et al. (2018): Indica la dificultad y la falta de métodos robustos para la detección y segmentación automática de actividades no estructuradas de la vida diaria en pacientes con Parkinson en entornos simulados o libres.
- Pérez Sanpablo et al. (2021): Muestra limitaciones en la precisión de métodos de análisis discriminante para clasificación de actividades en EP, con exactitudes solo en torno al 60%.
- Rast y Labruyère (2020): Review sistemática que resalta la heterogeneidad de métodos, la falta de estándares y la escasa evaluación de usabilidad, además de la necesidad de algoritmos precisos adaptados a pacientes con movilidad reducida.
- Rodríguez Montero et al. (2023): Trabajos previos con técnica de redes neuronales para clasificación de AVDs con resultados aceptables pero menor que el artículo principal, con posibilidad de mejorar mediante selección de características y redes profundas.

Idea:
El artículo propone usar Redes Neuronales Artificiales multicapa diseñadas y entrenadas con señales inerciales preprocesadas y reducidas dimensionalmente mediante PCA, para clasificar seis actividades específicas de la vida diaria en pacientes con EP. Esta combinación permite una clasificación automática avanzada, con alta precisión, superando técnicas clásicas de clasificación y adaptándose a bases de datos con desequilibrios.

Contribuciones:
1. Desarrollo de un sistema basado en MLP para clasificación precisa de 6 AVDs en pacientes con EP (Sección de metodología y resultados).
2. Aplicación de técnicas de reducción dimensional (PCA) para mejorar la eficiencia y mantener precisión (detalles en modelos D y D-13).
3. Evaluación exhaustiva del modelo con validación cruzada y comparación con otros clasificadores (LDA, Naïve Bayes, etc.).
4. Propuesta de configuraciones y recomendaciones para futuras aplicaciones y reducción de sensores para facilitar implementación práctica.
5. Codificación y diseño implementado en Python con uso de librerías especializadas para facilitar la reproducibilidad y extensión.

Evaluación:
La evaluación se realizó con una base de datos que contiene 179,755 observaciones de sensores inerciales colocados en pie, muslo, pelvis y muñeca de pacientes con EP. Se expresó un 99% de precisión con la arquitectura óptima para el modelo completo y 80% para el modelo reducido mediante PCA. Se aplicó validación cruzada (10-fold) para confirmar robustez. Se compararon seis clasificadores con superior desempeño de la red neuronal. Se mostró matriz de confusión y análisis de errores para actividades. 

Estructura del Documento:
No se menciona explícitamente la organización del documento en el texto del artículo principal accesible.

Resumen:
Este estudio aporta un modelo avanzado de RNA para la clasificación automática de actividades de vida diaria en pacientes con Parkinson, validado con amplias muestras y técnicas modernas de aprendizaje supervisado y reducción de dimensionalidad, mejorando resultados previos y proponiendo un sistema escalable para uso clínico y rehabilitación. Los trabajos citados muestran los retos de la estimación en entornos naturales, la necesidad de segmentación robusta y la complejidad en clasificación, justificando la propuesta presentada.
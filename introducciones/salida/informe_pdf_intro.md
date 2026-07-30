Tipo de Artículo y Ejes de Shaw:
El artículo es del tipo sistema, concretamente presenta una herramienta/modelo: un lenguaje específico del dominio (DSL) para diseño, generación de código y ejecución de entornos de simulación IoT. Responde a preguntas de investigación sobre cómo diseñar y desplegar simulaciones de sistemas IoT complejos con alto nivel de abstracción y automatización. La contribución es una metodología basada en desarrollo guiado por modelos (model-driven development), con un metamodelo, sintaxis gráfica y transformación modelo-texto para la generación automática de código. La validación se realiza mediante dos estudios de caso concretos (edificio inteligente y agricultura). El venue corresponde a la revista IEEE Access, el artículo está en inglés.

Territorio:
El terreno es la simulación de sistemas Internet de las Cosas (IoT), donde el desarrollo, despliegue y prueba de sistemas IoT requieren altos costos y esfuerzos. La simulación ayuda a modelar, razonar y optimizar estos sistemas antes de su implementacion física. Existen enfoques previos de simulación a bajo nivel (focalizados en hardware, redes y capacidades de nodos) y a alto nivel (modelado de entornos, dispositivos y servicios con DSLs o MDD). Sin embargo, muchos requieren altos conocimientos técnicos y carecen de interfaces gráficas adecuadas, código generable o validación previa del entorno. Además, muchos simuladores no contemplan adecuadamente conceptos actuales como fog computing, cloud computing, procesamiento de eventos complejos y protocolos avanzados de comunicación publish-subscribe.

Hueco:
- Alwasel et al. (2020) con BigDataSDNSim centra en simulación de datos masivos en cloud SDN, pero no recoge un modelado integral de simulación IoT con alto nivel de abstracción para múltiples capas arquitectónicas.
- Clemente et al. (2018) aportan un DSL para domótica pero no incluye simulación ni aspectos de almacenamiento o procesamiento basados en eventos.
- Mehdi et al. (2014) con CupCarbon simulan redes de sensores WSN con editor gráfico pero no modelan almacenamiento ni procesamiento complejo ni comunicación publish-subscribe con brokers.
- Zeng et al. (2017) con IOTSim simulan aplicaciones IoT en cloud con enfoque big data pero requieren configuraciones complejas y no contemplan diseño gráfico ni validación previa.
Estos trabajos adolecen de: falta de abstracción visual adecuada para describir simulaciones IoT vinculadas a capas Edge/Fog/Cloud; dependencia de configuraciones técnicas bajas; ausencia de generación automática de código integral y despliegue en arquitecturas basadas en microservicios; y falta de mecanismos para validar modelos antes de la simulación.

Idea:
Se propone SimulateIoT, un enfoque basado en desarrollo guiado por modelos para definir, generar código y desplegar entornos de simulación IoT complejos sin necesidad de escribir código manual. Consiste en un metamodelo de dominio, una sintaxis gráfica para modelado visual, y transformaciones modelo-texto para generación del código asociado (microservicios, contenedores Docker, brokers MQTT, bases NoSQL, motores de procesamiento de eventos y flujos). Los nodos IoT (sensores, actuadores, nodos fog y cloud) se comunican con un protocolo de publicación-suscripción. Se proveen mecanismos de validación del modelo y monitorización.

Contribuciones:
1. Definición de un metamodelo que captura conceptos IoT a alto nivel, abarcando capas Edge, Fog, Cloud, sensores, actuadores, bases de datos, procesamiento de eventos y comunicación (Sección III.A).
2. Desarrollo de una sintaxis gráfica para modelar estos sistemas (Sección III.B).
3. Implementación de reglas OCL para la validación del modelo en base a restricciones estructurales y semánticas (Sección III.B).
4. Creación de transformaciones modelo-texto en Acceleo para generar código completo que materializa los modelos en microservicios desplegables (Sección III.C).
5. Implementación del sistema de despliegue y ejecución sobre Docker Swarm y monitorización integrada (Sección III.D).
6. Presentación de dos estudios de caso reales (edificio inteligente y agricultura) mostrando la capacidad descriptiva, generación y despliegue (Sección V).
7. Discusión sobre las limitaciones y futuras extensiones para movilidad y dinámicas de la simulación (Sección VI).

Evaluación:
La validación se realiza mediante dos estudios de caso prácticos. El primero simula un edificio inteligente con varios nodos fog configurados por edificios, sensores de temperatura, presencia, humo, reglas para encender la calefacción y monitorización con bases de datos y motores CEP. El segundo cubre un entorno agrícola con sensores de temperatura, humedad, pH, presión de agua y actuadores de riego, con nubes y nodos fog, almacenamiento MongoDB y reglas para notificaciones y control de riego. En ambos casos se genera código automático, se despliega en contenedores Docker y se ejecuta simulación, demostrando la expresividad y viabilidad del enfoque.

Estructura del Documento:
Tras la introducción, el documento se estructura en: revisión del estado del arte, presentación de la metodología SimulateIoT, descripción detallada del metamodelo y herramientas, implementación del despliegue y ejecución, presentación de casos de estudio, discusión limitaciones y conclusiones (implícito en la organización de las secciones mencionadas).

---

Este análisis cumple con los requisitos solicitados, basándose exclusivamente en la extracción de los textos principales del artículo y la lectura de los papers citados (usados solo para el hueco). Se han respetado las indicaciones para citar con autor y año cada paper del conjunto citado.
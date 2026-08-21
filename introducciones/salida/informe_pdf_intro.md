Tipo de Artículo y Ejes de Shaw:
El artículo presenta una contribución en el ámbito de sistemas y herramientas para la simulación de entornos IoT. Es un trabajo de desarrollo de una técnica/metodología basada en Model-Driven Development (MDD) para definir, generar código y desplegar simulaciones de sistemas IoT. Responde a la pregunta de investigación sobre cómo facilitar el diseño y ejecución de simulaciones IoT mediante abstracciones de alto nivel y DSL (Domain Specific Language). La contribución principal es un enfoque y herramienta para modelar sistemas IoT complejos para simulación sin escribir código manualmente, incluyendo la generación automática de código para microservicios y contenedores Docker. La validación se realiza mediante dos estudios de caso con entornos IoT reales (smart building y agricultura) mostrando la expresividad y aplicabilidad del enfoque. El artículo parece haber sido publicado en IEEE Access, es en idioma inglés.

Territorio:
El IoT está aplicado en dominios como ciudades inteligentes, agricultura, industria y hogar. Sin embargo, desarrollar y probar sistemas IoT requiere inversiones grandes en hardware y software y consume tiempo y esfuerzo. La simulación de entornos IoT ayuda a modelar, razonar y optimizar sistemas IoT antes de su despliegue físico. Los enfoques previos se han centrado en simulaciones a bajo nivel (hardware, redes) o alto nivel (contextos IoT), pero no suelen cubrir aspectos de alto nivel integrando Edge, Fog y Cloud, ni facilitan la reutilización ni la generación automática de código para despliegue. Por ello, hay necesidad de herramientas que permitan diseñar, generar y desplegar simulaciones IoT complejas desde modelos de alto nivel, facilitando la integración de capas Edge, Fog, Cloud y mecanismos de comunicación como publish-subscribe.

Hueco:
- Alwasel et al. (2020) presentan simuladores para análisis de big data en entornos cloud, pero no permiten modelar los aspectos específicos de simulación IoT con diferentes niveles de abstracción y dinamismo.
- Levis et al. (2003) presentan Tossim, simulador de redes de sensores de bajo nivel para TinyOS, pero no edge computing ni simulaciones a alto nivel.
- Ruppen et al. (2015) proponen un modelado para Web of Things, pero no contiene dominios específicos de simulación o almacenamiento para IoT.
- Mehdi et al. (2014) con CupCarbon permiten diseño y simulación gráfica de redes de sensores, pero no modelan almacenamiento ni comunicación compleja publish-subscribe basada en brokers.
- Zeng et al. (2017) con IoTSim simulan aplicaciones IoT en entornos cloud pero requieren configuraciones complejas y no proporcionan interfaz gráfica de alto nivel para modelar el sistema completo ni validación previa.
Estos trabajos carecen de una herramienta que integre modelado a alto nivel con generación automática de código listo para despliegue en arquitecturas distribuidas como servicios Docker, incluyendo capas Edge, Fog y Cloud, con capacidades de análisis en tiempo real y comunicación publish-subscribe nativa.

Idea:
El artículo propone SimulateIoT, un DSL de alto nivel basado en model-driven development para definir entornos de simulación IoT con componentes Edge, Fog y Cloud. Ofrece un metamodelo para representar sensores, actuadores, nodos y protocolos de comunicación publish-subscribe, junto con reglas para procesamiento complejo de eventos. Desde modelos en SimulateIoT, se genera código automáticamente para microservicios Docker desplegables, brokers MQTT, bases de datos NoSQL, y motores de procesamiento de eventos. Todo el sistema simulado se puede desplegar en máquinas físicas o virtuales, facilitando la experimentación y análisis sin necesidad de programación detallada.

Contribuciones:
1. Definición de un metamodelo y DSL para modelar ambientes de simulación IoT incluyendo Edge, Fog, Cloud, sensores, actuadores, protocolos y procesamiento de eventos (descrita en Sección III y IV).
2. Herramientas para edición visual de modelos con validación automática basada en OCL (Sección IV.B).
3. Generación automática de código para despliegue en microservicios Docker, brokers MQTT, bases NoSQL y motores CEP (Sección IV.C y IV.D).
4. Despliegue y ejecución orquestada del sistema simulado mediante Docker Swarm y monitoreo en tiempo real (Sección IV.D).
5. Evaluación del enfoque con dos estudios de caso: simulación de un edificio inteligente y simulación de un entorno agrícola, demostrando expresividad y escalabilidad (Sección V).
6. Discusión sobre limitaciones y futuras mejoras como movilidad de nodos y mecanismos dinámicos de descubrimiento (Sección VI).

Evaluación:
La validación se realiza mediante dos estudios de caso reales:
- Caso 1: Simulación de la Escuela de Tecnología con edificios que incluyen nodos Fog y Cloud, sensores y actuadores, bases de datos MongoDB, motores CEP (Esper) y comunicación MQTT para análisis y control de temperatura, humo y otros datos.
- Caso 2: Simulación agrícola con sensores de temperatura, humedad, pH, presión y actuadores para riego con nodos Fog/Cloud, bases MongoDB y motores de procesamiento WSO2.
Se genera código desplegable en contenedores Docker para cada nodo y componente. Se muestra monitoreo en tiempo real, análisis con reglas CEP y notificaciones. El sistema es capaz de simular ambientes escalables con interacción entre nodos y análisis en tiempo real.

Estructura del Documento:
- Introducción y estado del arte donde se contextualiza el problema.
- Descripción de la metodología y enfoque SimulateIoT (Sección III).
- Descripción detallada del metamodelo, editor gráfico, transformaciones y despliegue (Sección IV).
- Presentación de dos estudios de caso con sus modelos, despliegues y resultados (Sección V).
- Discusión de limitaciones y propuestas de trabajo futuro (Sección VI).
- Conclusiones (Sección VII).

---

Este informe muestra que se ha cumplido el requisito de extraer los 7 puntos clave para la introducción basados en el contenido del artículo principal y de los papers citados, basados en la lectura de ambos conjuntos de documentos aportados.
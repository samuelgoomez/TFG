Tipo de Artículo y Ejes de Shaw:
El artículo presenta un trabajo del tipo sistema y técnica, que desarrolla un Lenguaje Específico del Dominio (DSL) para el diseño, generación de código y ejecución de entornos de simulación en Internet de las Cosas (IoT). La pregunta de investigación está centrada en cómo facilitar la modelación y simulación de sistemas IoT complejos usando un enfoque basado en desarrollo dirigido por modelos (MDD). La contribución principal es el diseño de un metamodelo de dominio, una sintaxis concreta gráfica y transformaciones modelo a texto que permiten definir y desplegar simulaciones IoT sin escribir código manual. La validación se realiza mediante dos estudios de caso en entornos IoT de smart building (edificio inteligente) y agricultura, demostrando la expresividad del método. El artículo está publicado en la revista IEEE Access, en inglés, en 2021.

Territorio:
El contexto es la creciente aplicación de IoT en ámbitos como smart cities, hogares inteligentes, agricultura e industria, donde desarrollar, desplegar y probar proyectos IoT implica altos costes en hardware y software. Para reducir estos costes es necesario simular los sistemas IoT antes de su desarrollo real. Se han desarrollado entornos de simulación IoT que se centran más en aspectos de bajo nivel (redes, hardware) y requieren altos conocimientos técnicos y de programación. Por ello, se propone un enfoque de alto nivel basado en desarrollo dirigido por modelos para diseñar, generar y desplegar simulaciones IoT complejas con abstracciones propias del dominio (sensores, actuadores, nodos Edge, Fog y Cloud, comunicación publish-subscribe, microservicios, contenedores Docker).

Hueco:
Respecto a los papers citados en la carpeta de citas se han identificado las siguientes limitaciones específicas:
- Alwasel et al. (2020): Simulan Big Data y redes definidas en software en nube, pero no cuentan con interfaz gráfica ni validación de configuración previa de entornos IoT.
- Levis et al. (2003): Tossim simula nodos TinyOS a bajo nivel sin definir patrones de comunicación IoT ni modelar procesos de alto nivel.
- Mehdi et al. (2014): CupCarbon permite simulación con interfaz gráfica para contextos IoT, pero no modela almacenamiento ni protocolos complejos como publish/subscribe.
- Patel y Cassou (2015): IoTSuite facilita desarrollo de aplicaciones IoT, pero no incluye simulación ni modelado de almacenamiento ni procesamiento complejo.
- Zeng et al. (2017): IOTSim es un simulador para aplicaciones IoT en nube, focalizado en procesamiento big data pero sin herramientas para modelar arquitecturas IoT de alto nivel gráficamente.
Estos trabajos presentan, en líneas generales, ausencia de un lenguaje específico de alto nivel con validación, soporte para modelar toda la arquitectura IoT (Edge, Fog, Cloud), comunicación publish-subscribe y despliegue integrado en contenedores con microservicios.

Idea:
El enfoque central es un enfoque de desarrollo dirigido por modelos para definir, generar código y desplegar simulaciones IoT. Consta de un dominio metamodelo (SimulateIoT), una sintaxis gráfica para modelado visual, validación mediante reglas OCL, y transformaciones modelo a texto que generan el código necesario (microservicios, brokers MQTT, bases de datos NoSQL, motores CEP, contenedores Docker). La simulación integra sensores, actuadores y nodos heterogéneos (Edge, Fog, Cloud) desplegados en un entorno realista basado en una arquitectura orientada a servicios.

Contribuciones:
1. Desarrollo de un metamodelo completo para simulación IoT que incluye dispositivos, nodos, comunicación, almacenamiento y procesamiento (Sección III y IV).
2. Creación de una sintaxis gráfica para diseñar modelos de simulación conformes al metamodelo con validación OCL (Sección IV-B).
3. Implementación de una transformación modelo a texto para generación automática del código y despliegue (Sección IV-C).
4. Integración con tecnologías industriales (Docker, MQTT, motores CEP como Esper y WSO2) para simulación y despliegue real (Sección IV-D).
5. Presentación de dos estudios de caso completos, en ecosistemas de smart building y agricultura, que ilustran la potencia y aplicabilidad del enfoque (Sección V).
6. Generación e implementación de un entorno completo con monitorización y capacidades de análisis en tiempo real (Sección V y VI).

Evaluación:
La validación se realiza a través de dos estudios de caso detallados: 1) Escuela de Tecnología con varios edificios, sensores de temperatura, presencia y humo, actuadores y nodos Fog/Cloud. Se muestra el modelado, la generación de código, el despliegue con Docker y la simulación realista con gestión de eventos. 2) Ambiente agrícola con sensores de humedad, pH, temperatura y actuadores para riego distribuidos en diez hectáreas, con similar despliegue. En ambos casos, el sistema permite análisis en tiempo real, monitorización integrada, y generación de eventos y acciones basadas en reglas CEP. Se discuten además limitaciones y ampliaciones futuras.

Estructura del Documento:
El documento está estructurado en: Introducción; Trabajo relacionado; Metodología SimulateIoT; Herramientas SimulateIoT (Diseño, Validación, Transformación y Ejecución); Casos de Estudio (smart building y agricultura); discusión sobre limitaciones, usuarios objetivo y tecnologías; conclusiones y trabajos futuros. Las secciones principales son claramente diferenciadas para guiar al lector desde la motivación hasta la aplicación práctica.
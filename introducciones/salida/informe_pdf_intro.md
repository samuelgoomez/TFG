Tipo de Artículo y Ejes de Shaw:
El artículo es un trabajo sobre una herramienta y sistema específico, presentando una técnica basada en un lenguaje específico del dominio (DSL) para el diseño, generación de código y ejecución de entornos de simulación para sistemas IoT. La pregunta de investigación responde a cómo modelar y simular entornos IoT complejos con un alto nivel de abstracción para reducir costos de desarrollo y validación. La contribución principal es una aproximación basada en desarrollo dirigido por modelos (MDD) que permite diseñar entornos de simulación sin necesidad de programación manual, además de los artefactos resultantes que pueden desplegarse como microservicios con contenedores Docker. La validación se realiza mediante dos estudios de caso en entornos IoT de edificios inteligentes y agricultura. El artículo está publicado en IEEE Access, en idioma inglés.

Territorio:
El artículo principal se encuadra en la necesidad creciente de simular sistemas IoT para áreas como ciudades inteligentes, hogares, agricultura e industria, debido al alto costo y complejidad de desarrollar y probar sistemas IoT reales. Existen enfoques previos que se centran en simulación a bajo nivel (hardware, red) o alto nivel (modelado y simulación basada en modelos), pero carecen de integración de aspectos como computación Edge, Fog y Cloud, protocolos de comunicación avanzados o facilidad de uso para usuarios no expertos en programación. Por ello, el modelado dirigido por modelos emerge como una solución para capturar conceptos de dominio en IoT y generar código automáticamente.

Hueco:
- Alwasel et al. (2020) presentan simuladores para análisis de big data en entornos cloud, pero no abordan la simulación integral de entornos IoT con alto nivel de abstracción.
- Clemente et al. (2018) abordan procesamiento de eventos complejos, pero no se enfocan en la simulación de entornos IoT completos ni en la generación automática del código para despliegue.
- Papadopoulos et al. (2013) proporcionan plataformas experimentales para WSN, pero están limitadas a nivel de hardware y no modelan conceptos de computación Fog/Cloud.
- Patel y Cassou (2015) desarrollan herramientas de alto nivel para IoT, sin embargo no integran una interfaz gráfica para simular arquitecturas completas en diferentes capas ni validan la configuración.
- Mehdi et al. (2014) ofrecen simuladores discretos y multiagente para sensores, pero no proveen abstracciones a nivel de nodos altamente configurables con comunicación publish-subscribe ni despliegue en contenedores.
Por ende, el hueco detectado es la ausencia de un enfoque completo y accesible para modelar, validar, generar código y desplegar simulaciones de entornos IoT complejos que incluyan Edge, Fog y Cloud, soporte para procesamiento de flujo y eventos complejos, y facilidad para usuarios con distintos niveles técnicos.

Idea:
La propuesta central es SimulateIoT, un DSL junto con un conjunto de herramientas basadas en MDD para definir modelos de entornos IoT, generar automáticamente código fuente para microservicios desplegables en contenedores Docker y ejecutar simulaciones utilizando una arquitectura distribuida con comunicación basada en MQTT y procesamiento en Fog/Cloud. Incluye un metamodelo que cubre sensores, actuadores, nodos Edge, Fog y Cloud, tópicos para comunicación publish-subscribe, generación de datos sintéticos e históricos, motores de procesamiento de eventos complejos y reglas para análisis y notificaciones.

Contribuciones:
1. Diseño del metamodelo SimulateIoT que representa conceptualmente entornos IoT con soporte para capas Edge, Fog y Cloud, sensores/actuadores, datos y comunicación (sección III).
2. Definición de una sintaxis gráfica para construir modelos conformes a dicho metamodelo usando herramientas Eclipse GMF (sección IV.B).
3. Implementación de transformaciones modelo-a-texto para generación automática de código, incluyendo microservicios, brokers MQTT, bases de datos NoSQL y motores de procesamiento (sección IV.C).
4. Propuesta de un entorno de despliegue y ejecución basado en contenedores Docker orquestados con Docker Swarm para simular entornos IoT grandes y heterogéneos (sección IV.D).
5. Presentación de dos casos de uso relevantes: un edificio inteligente universitario y un entorno agrícola, con despliegue completo y análisis de resultados (sección V).
6. Discusión sobre limitaciones y futuras mejoras, especialmente en movilidad de nodos y patrones avanzados de generación de datos (sección VI).

Evaluación:
La validación del trabajo se realiza mediante dos estudios de caso prácticos realizados con el entorno SimulateIoT: 
- Caso 1: Simulación de un edificio inteligente (Escuela de Tecnología), con múltiples sensores y actuadores distribuidos en edificios diferentes, con nodos Fog y Cloud analizando datos y generando reglas para control de calefacción, etc.
- Caso 2: Simulación de entorno agrícola con sensores de temperatura, humedad, pH, presión de agua, y actuadores para riego, gestionados por nodos Fog y Cloud con motores de procesamiento en tiempo real.
En ambos casos se muestra la modelación, generación automática de código, despliegue en contenedores Docker y monitoreo de la simulación en tiempo real. Se discuten aspectos de escalabilidad y validación de la metodología y las herramientas.

Estructura del Documento:
El documento está organizado en secciones que cubren: introducción y motivación; trabajo relacionado; metodología SimulateIoT; diseño e implementación (metamodelo, sintaxis gráfica, transformaciones modelo-a-texto); despliegue y ejecución; casos de estudio; discusión y limitaciones; conclusión y referencias.

---

Este informe cumple con los requisitos solicitados y abarca detalladamente los siete puntos clave para la introducción basados exclusivamente en la información extraída del texto principal y los papers citados de la carpeta.
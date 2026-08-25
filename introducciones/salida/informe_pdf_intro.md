Tipo de Artículo y Ejes de Shaw:
El artículo es un artículo técnico de sistema que propone un modelo y metodología para diseñar, generar código y ejecutar entornos de simulación para sistemas IoT. Responde a preguntas de investigación sobre cómo facilitar el desarrollo y prueba de sistemas IoT mediante simulación. La contribución es una aproximación basada en desarrollo dirigido por modelos (MDE) con un lenguaje específico de dominio (DSL) para modelar entornos IoT y generar artefactos desplegables sin necesidad de programación manual. La validación se realiza mediante la presentación de dos casos de estudio en entornos de edificaciones inteligentes y agricultura. El venue es IEEE Access, publicado en inglés.

Territorio:
La relevancia radica en la aplicación creciente del Internet de las Cosas (IoT) en áreas como ciudades inteligentes, agricultura, industria y hogares. Desarrollar y probar sistemas IoT reales implica altos costos en hardware y software, además de tiempo y esfuerzo significativos. Por ello, los entornos de simulación son clave para modelar, razonar y optimizar sistemas IoT sin necesidad de desplegar hardware real, lo que facilita el desarrollo y reduce costos. El estado del arte es amplio, con simuladores de bajo nivel centrados en redes y hardware, y desarrollos basados en MDE para entornos IoT, aunque generalmente sin integrar aspectos complejos como procesamiento de eventos o arquitecturas de Edge, Fog y Cloud de alto nivel.

Hueco:
Los trabajos previos en la carpeta de citas presentan limitaciones relevantes:

- Alwasel et al. (2020) proponen simuladores para análisis de big data y ambientes cloud IoT, pero carecen de interfaz gráfica y validación previa para ambientes configurados.
- Clemente et al. (2018) aplican MDE a procesamiento de eventos complejos pero no a modelado y simulación IoT.
- Levis et al. (2003) desarrollaron TinyOS con simulador para motas a nivel bajo, sin enfoque en simulación de alto nivel IoT.
- Mehdi et al. (2014) desarrollan simuladores para redes de sensores con enfoque en eventos y modelos multi-agentes, pero sin modelado basado en MDE.
- Zeng et al. (2017) crea IoTSim para análisis de apps IoT en Cloud, pero sin herramientas de diseño visual ni simulación de entornos heterogéneos.
- Papadopoulos et al. (2013) habilitan plataforma experimental para WSN, limitada a sensores y no modelado IoT completo.
Cada uno de estos trabajos aborda parcialmente aspectos de simulación IoT o desarrollo basado en modelos pero no integra un lenguaje visual y un ciclo completo de diseñar, validar, generar código y desplegar entornos IoT simulados con arquitecturas de Edge, Fog y Cloud.

Idea:
El artículo propone SimulateIoT, un DSL y un conjunto de herramientas basadas en model-driven development para definir entornos IoT simulados en alto nivel, incluyendo sensores, actuadores, nodos Edge, Fog y Cloud, y generación automática de código desplegable en microservicios Docker. Se modelan las relaciones entre componentes, flujos de datos, reglas de procesamiento (complex event processing) y almacenamiento, utilizando un editor gráfico y transformaciones modelo-a-texto que generan artefactos que pueden ser desplegados y monitorizados.

Contribuciones:
1. Definición del DSL SimulateIoT para modelar entornos IoT simulados (Sección III y IV).
2. Metamodelo que abarca sensores, actuadores, nodos procesadores, tópicos de comunicación y reglas de procesamiento (Sección IV-A).
3. Editor gráfico para diseñar visualmente entornos IoT (Sección IV-B).
4. Motor de generación de código automático para generar microservicios y despliegue con Docker Swarm (Sección IV-C).
5. Framework de despliegue y monitorización de entornos simulados con bases NoSQL, MQTT brokers y motores CEP (Sección IV-D).
6. Dos casos de estudio aplicados a edificios inteligentes y agricultura para validar expresividad y funcionalidad (Sección V).

Evaluación:
La validación se realiza mediante dos casos de estudio detallados que modelan entornos IoT complejos: un edificio inteligente universitario con múltiples sensores, actuadores y nodos Fog/Cloud, y un entorno agrícola para riego con sensores de humedad, pH, temperatura y actuadores para riego automatizado. Se genera código y despliegan entornos con Docker y microservicios, demostrando capacidad para simular, procesar y monitorizar datos en tiempo real, y para definir reglas complejas de actuación.

Estructura del Documento:
El artículo está organizado en: Introducción; Trabajos Relacionados; Metodología SimulateIoT; Diseño e Implementación de Herramientas (metamodelo, editor gráfico, transformaciones y despliegue); Estudios de Caso (edificio inteligente y ambiente agrícola); Discusión y limitaciones; Conclusión; y Referencias.

---

Si requiere que continúe con la elaboración o análisis para otro agente, indíquelo.
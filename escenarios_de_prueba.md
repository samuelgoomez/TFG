# Batería de Pruebas para el Sistema Multiagente (TFG)

Este documento contiene respuestas listas para copiar y pegar cuando el sistema haga preguntas en modo interactivo.

---

## ESCENARIO A — Abstract interactivo: caso de éxito (validado a la primera)
*Datos empíricos completos; diseñado para pasar la validación sin bucle.*

**1. Problema:**
> El problema específico que aborda este artículo es la falta de interpretabilidad en los modelos de aprendizaje profundo (Deep Learning) aplicados al diagnóstico médico por imagen. Aunque las Redes Neuronales Convolucionales (CNN) son muy precisas, su naturaleza de 'caja negra' frena su adopción en entornos clínicos reales, donde los médicos necesitan comprender por qué el modelo toma una decisión.

**2. Objetivo:**
> El objetivo principal de este trabajo es evaluar y comparar cuantitativamente la efectividad de dos métodos de interpretabilidad post-hoc, específicamente Grad-CAM y LIME, aplicados a una arquitectura ResNet-50. Buscamos determinar cuál de estas técnicas proporciona explicaciones visuales más coherentes y útiles clínicamente para la detección de patologías torácicas.

**3. Metodología:**
> Utilizamos el conjunto de datos público CheXpert, seleccionando 50.000 radiografías de tórax. Entrenamos un modelo ResNet-50 preentrenado en ImageNet, ajustando sus pesos mediante transfer learning durante 30 épocas. Aplicamos Grad-CAM y LIME para generar mapas de calor, y evaluamos su calidad comparándolas con las cajas delimitadoras proporcionadas por radiólogos expertos utilizando la métrica de Intersección sobre Unión (IoU).

**4. Resultados:**
> El modelo alcanzó un AUC-ROC de 0.94 y una precisión global del 92.4%. Para la interpretabilidad, Grad-CAM logró un IoU promedio de 0.76 frente al 0.68 de LIME (p-valor < 0.01). Además, el tiempo de procesamiento medio fue de 0.2 segundos por imagen para Grad-CAM frente a 1.5 segundos para LIME.

**5. Conclusión:**
> El análisis demuestra que Grad-CAM supera significativamente a LIME tanto en precisión espacial anatómica como en eficiencia computacional. Nuestro estudio aporta un marco cuantitativo robusto que facilita la adopción segura y confiable de la IA en entornos de diagnóstico radiológico.

**6. Restricciones:**
> No debe superar las 150 palabras. La última frase debe ser obligatoriamente: "Future clinical validations are necessary."

---

## ESCENARIO B — Abstract interactivo: caso de rechazo (fuerza el "NO VALIDADO")
*Respuestas intencionadamente vagas, sin métricas. El validador rechaza el informe y el agente de adquisición vuelve a preguntar para demostrar que el bucle funciona.*

**1. Problema:**
> En la medicina hay un problema muy grande con la inteligencia artificial porque a los médicos no les gusta no saber cómo funcionan las cosas por dentro. Pasa mucho con las radiografías.

**2. Objetivo:**
> Pues el objetivo era hacer un programa de ordenador o un modelo que ayudara a los médicos a entender mejor las imágenes. Queríamos ver si funcionaba bien.

**3. Metodología:**
> Usamos un montón de imágenes médicas que sacamos de internet, bastantes miles. Luego usamos un ordenador potente para entrenar una red neuronal durante varios días hasta que pareció que ya funcionaba bien y detectaba las cosas.

**4. Resultados:**
> Los resultados fueron muy buenos. El modelo acertó casi todas las veces que probamos con pacientes nuevos y se equivocó muy poco. A los médicos que se lo enseñamos les gustó mucho y dijeron que era una buena herramienta. *(Sin ningún número ni métrica concretos.)*

**5. Conclusión:**
> La conclusión es que la inteligencia artificial es el futuro de la medicina y que nuestro programa funciona estupendamente para ayudar a los hospitales a ir más rápido.

**6. Restricciones:**
> Me da igual el idioma y la longitud, escríbelo como quieras pero que quede bonito.

---

## ESCENARIO C — Introducción interactiva: caso de éxito (validada a la primera)
*Artículo ficticio sobre revisión de código automatizada con CodeBERT. Datos completos, con referencias concretas en formato "Apellido et al. (Año)" y venue/idioma definidos; diseñado para pasar la validación sin bucle.*

**1. Tipo de artículo y ejes de Shaw:**
> Es un artículo de tipo técnica/sistema: presentamos una herramienta concreta con una arquitectura definida.
>
> Ejes de Shaw:
> - Pregunta de investigación: de método/medios — ¿cómo automatizar la revisión de código de forma fiable usando modelos de lenguaje?
> - Contribución: sistema funcional más dataset público etiquetado.
> - Validación: experimento controlado (métricas F1) combinado con estudio de usuario (12 desarrolladores, 100 pull requests).
>
> Venue: ICSE o FSE (ingeniería del software). Idioma: inglés.

**2. Territorio:**
> La revisión de código es una práctica fundamental en el desarrollo de software moderno: permite detectar defectos, mejorar la mantenibilidad y transferir conocimiento entre desarrolladores. Con la adopción masiva de GitHub y GitLab, el volumen de pull requests ha crecido exponencialmente, convirtiendo la revisión en un cuello de botella. En paralelo, los modelos preentrenados sobre código como CodeBERT o GraphCodeBERT han demostrado capacidad para entender semántica y estructura del código a un nivel cercano al humano. La intersección entre ingeniería del software empírica y NLP aplicado al código es un área en expansión, con trabajos recientes en detección de bugs, generación de tests y resumen automático de código.

**3. Hueco:**
> Los trabajos más relevantes presentan limitaciones claras. Tufano et al. (2021) propusieron un modelo basado en T5 para sugerir cambios en el código revisado, pero se centran en transformaciones sintácticas sin generar comentarios en lenguaje natural. Li et al. (2022) desarrollaron un sistema con GPT-2, pero evaluaron solo en proyectos Java de pequeña escala sin estudios de usuario. CodeReviewer (Lu et al., 2022) fine-tunea CodeBERT para revisión, pero trata el problema como clasificación binaria sin distinguir categorías ni generar feedback accionable. Ninguno publica un dataset etiquetado multilingüe con categorías múltiples, lo que dificulta la reproducibilidad y la comparación sistemática.

**4. Idea:**
> Proponemos un sistema que va más allá de la clasificación binaria: dado un pull request, identifica y categoriza los problemas en tres dimensiones (calidad, seguridad y estilo) y genera un comentario en lenguaje natural para cada uno. La clave es un fine-tuning de CodeBERT con una cabeza de clasificación multi-etiqueta, entrenado sobre un dataset de 5.000 pull requests etiquetados manualmente en Python y Java. A diferencia de trabajos previos, el sistema produce feedback accionable y comprensible por desarrolladores.

**5. Contribuciones:**
> 1. Un sistema de revisión de código basado en CodeBERT con clasificación multi-etiqueta en tres categorías, capaz de generar comentarios en lenguaje natural accionables.
> 2. Un dataset público de 5.000 pull requests reales de GitHub etiquetados manualmente en Python y Java, el primero de estas características disponible abiertamente.
> 3. Una evaluación empírica que combina métricas automáticas (F1 por categoría) con un estudio de usuario con 12 desarrolladores profesionales sobre 100 pull requests reales.
> 4. Un análisis de los límites del sistema, identificando vulnerabilidades de seguridad complejas como el principal reto abierto.

**6. Evaluación:**
> La validez se respalda con dos tipos de evaluación complementarios. Por un lado, evaluación automática sobre el conjunto de test (500 pull requests no vistos), midiendo precisión, recall y F1 por categoría. Por otro, un estudio de usuario controlado en el que 12 desarrolladores profesionales evaluaron de forma ciega el feedback del sistema frente al de revisores humanos junior sobre 100 pull requests reales, valorando utilidad, claridad y accionabilidad.

**7. Estructura del documento:**
> El documento se organiza en seis secciones. La Sección 1 es la introducción. La Sección 2 describe el dataset. La Sección 3 detalla la arquitectura del sistema. La Sección 4 presenta la evaluación. La Sección 5 analiza las limitaciones y casos de fallo. La Sección 6 revisa el trabajo relacionado (Tufano et al., Li et al., CodeReviewer). El documento cierra con conclusiones y trabajo futuro.

---

## ESCENARIO D — Introducción interactiva: caso de rechazo (fuerza el rechazo del validador)
*Artículo ficticio sobre un chatbot de atención al cliente. Primera ronda de respuestas vacías de contenido en todos los puntos (fuerza que el validador rechace el informe explícitamente). El agente de adquisición vuelve a preguntar; en esa segunda ronda se aportan datos reales para que el bucle se resuelva y el informe acabe validándose, en vez de que el sistema se rinda por completo. Nota: por diseño (`tarea_validacion_intro` en `tasks.yaml`), la tarea en sí no debe terminar devolviendo "NO VALIDADO" como resultado final — pero el agente de validación sí puede emitir ese veredicto como resultado intermedio de una delegación, que es lo que fuerza este escenario.*

**Primera ronda (respuestas vagas, fuerzan el rechazo):**

**1. Tipo de artículo y ejes de Shaw:**
> No sé, la verdad, no lo tengo claro. Es un trabajo sobre un chatbot, ya está. No sabría decirte qué tipo de pregunta de investigación es ni qué se aporta exactamente. Tampoco sé la revista ni el idioma, ponlo como quieras.

**2. Territorio:**
> Pues de chatbots, que se usan cada vez más. No sabría explicar mucho más sobre el tema en general.

**3. Hueco:**
> No sé qué limitaciones tienen los que ya existen, la verdad no lo he mirado. No me acuerdo de ningún nombre ni estudio.

**4. Idea:**
> Un chatbot mejor que los que hay. No sabría decir en qué consiste exactamente ni qué lo hace diferente.

**5. Contribuciones:**
> No sé, supongo que el chatbot en sí. No tengo claro qué más se podría destacar.

**6. Evaluación:**
> No lo hemos probado todavía, o si se probó no me han pasado los resultados. No tengo datos.

**7. Estructura del documento:**
> No lo sé, no he mirado cómo está organizado el documento.

**Segunda ronda (si el agente repregunta, ahora sí con datos concretos para que el informe se pueda validar):**

**1b. Tipo de artículo y ejes de Shaw:**
> Es un artículo técnico que presenta un sistema nuevo (herramienta). Pregunta de investigación de tipo método: ¿cómo mejorar la comprensión del lenguaje natural en chatbots de atención al cliente? Contribución: un chatbot con un modelo de lenguaje ajustado (fine-tuned) para este dominio. Validación mediante pruebas de usuario controladas. Iría dirigido a una conferencia de interacción persona-ordenador (CHI), en inglés.

**2b. Territorio:**
> Los chatbots basados en modelos de lenguaje se usan cada vez más en atención al cliente porque reducen costes y ofrecen respuesta inmediata las 24 horas. La adopción de grandes modelos de lenguaje preentrenados ha mejorado su fluidez, pero la adaptación a dominios de negocio concretos sigue siendo un reto abierto.

**3b. Hueco:**
> Trabajos como el de Adiwardana et al. (2020) con Meena muestran chatbots de conversación abierta muy fluidos, pero sin especialización en un dominio concreto, lo que provoca respuestas genéricas o incorrectas en consultas reales de atención al cliente.

**4b. Idea:**
> Proponemos afinar (fine-tuning) un modelo de lenguaje preentrenado sobre conversaciones reales de atención al cliente de una empresa de telecomunicaciones, incorporando una base de conocimiento específica del dominio para reducir las respuestas genéricas.

**5b. Contribuciones:**
> 1) Un chatbot especializado en atención al cliente mediante fine-tuning de dominio. 2) Un conjunto de datos etiquetado de conversaciones reales de soporte técnico. 3) Una comparación empírica frente a un chatbot genérico no especializado.

**6b. Evaluación:**
> Evaluamos el sistema con 200 conversaciones reales no vistas, midiendo la tasa de resolución en el primer contacto y la satisfacción del usuario mediante encuesta, comparando frente al chatbot genérico de base.

**7b. Estructura del documento:**
> El documento tiene una introducción, una sección de trabajo relacionado, la descripción del sistema y el proceso de fine-tuning, la evaluación experimental, y termina con conclusiones y trabajo futuro.
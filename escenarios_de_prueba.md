# Batería de Pruebas para el Sistema Multiagente (TFG)

Este documento contiene dos conjuntos de respuestas listas para copiar y pegar en la consola cuando el Agente de Adquisición de Información te haga preguntas. 

El **Escenario A** está diseñado para pasar la validación a la primera. El **Escenario B** está diseñado deliberadamente mal para obligar al Agente de Validación a rechazar el informe, demostrando así que el control de calidad y el bucle de corrección funcionan perfectamente.

---

## ESCENARIO A: Caso de Éxito (Abstract Validado)
*Usa estas respuestas para obtener un abstract perfecto a la primera, con datos empíricos y rigurosidad científica.*

**1. Problema:**
> El problema específico que aborda este artículo es la falta de interpretabilidad en los modelos de aprendizaje profundo (Deep Learning) aplicados al diagnóstico médico por imagen. Aunque las Redes Neuronales Convolucionales (CNN) son muy precisas, su naturaleza de 'caja negra' frena su adopción en entornos clínicos reales, donde los médicos necesitan comprender por qué el modelo toma una decisión. 

**2. Objetivo:**
> El objetivo principal de este trabajo es evaluar y comparar cuantitativamente la efectividad de dos métodos de interpretabilidad post-hoc, específicamente Grad-CAM y LIME, aplicados a una arquitectura ResNet-50. Buscamos determinar cuál de estas técnicas proporciona explicaciones visuales más coherentes y útiles clínicamente para la detección de patologías torácicas.

**3. Metodología:**
> Utilizamos el conjunto de datos público CheXpert, seleccionando 50,000 radiografías de tórax. Entrenamos un modelo ResNet-50 preentrenado en ImageNet, ajustando sus pesos mediante transfer learning durante 30 épocas. Aplicamos Grad-CAM y LIME para generar mapas de calor, y evaluamos su calidad comparándolas con las cajas delimitadoras proporcionadas por radiólogos expertos utilizando la métrica de Intersección sobre Unión (IoU).

**4. Resultados y Datos Estadísticos:**
> El modelo alcanzó un AUC-ROC de 0.94 y una precisión global del 92.4%. Para la interpretabilidad, Grad-CAM logró un IoU promedio de 0.76 frente al 0.68 de LIME (p-valor < 0.01). Además, el tiempo de procesamiento medio fue de 0.2 segundos por imagen para Grad-CAM frente a 1.5 segundos para LIME.

**5. Conclusión:**
> El análisis demuestra que Grad-CAM supera significativamente a LIME tanto en precisión espacial anatómica como en eficiencia computacional. Nuestro estudio aporta un marco cuantitativo robusto que facilita la adopción segura y confiable de la Inteligencia Artificial en entornos de diagnóstico radiológico.

**6. Restricciones:**
> El abstract debe estar redactado estrictamente en INGLÉS. No debe superar bajo ningún concepto las 150 palabras de longitud máxima. Finalmente, la última frase del texto debe ser obligatoria y literalmente la siguiente: "Future clinical validations are necessary."

---
---

## ESCENARIO B: Caso de Rechazo (Forzar el "NO VALIDADO")
*Usa estas respuestas intencionadamente vagas. Al terminar las 6 preguntas, el Agente de Validación se dará cuenta de que no hay datos concretos, rechazará el informe y el Agente de Adquisición volverá a preguntarte.*

**1. Problema:**
> En la medicina hay un problema muy grande con la inteligencia artificial porque a los médicos no les gusta no saber cómo funcionan las cosas por dentro. Pasa mucho con las radiografías.

**2. Objetivo:**
> Pues el objetivo era hacer un programa de ordenador o un modelo que ayudara a los médicos a entender mejor las imágenes. Queríamos ver si funcionaba bien.

**3. Metodología:**
> Usamos un montón de imágenes médicas que sacamos de internet, bastantes miles. Luego usamos un ordenador potente para entrenar una red neuronal durante varios días hasta que pareció que ya funcionaba bien y detectaba las cosas.

**4. Resultados y Datos Estadísticos:**
> Los resultados fueron muy buenos. El modelo acertó casi todas las veces que probamos con pacientes nuevos y se equivocó muy poco. A los médicos que se lo enseñamos les gustó mucho y dijeron que era una buena herramienta. *(Nota: No hay ni un solo número o métrica aquí).*

**5. Conclusión:**
> La conclusión es que la inteligencia artificial es el futuro de la medicina y que nuestro programa funciona estupendamente para ayudar a los hospitales a ir más rápido.

**6. Restricciones:**
> Me da igual el idioma y la longitud, escríbelo como quieras pero que quede bonito.

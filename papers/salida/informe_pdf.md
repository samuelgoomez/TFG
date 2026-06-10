Problema: La Enfermedad de Parkinson (EP) es una afección crónica y progresiva que afecta el movimiento de los pacientes, causando fluctuaciones en los síntomas motores que complican su manejo y seguimiento. La evaluación actual se basa en autoevaluaciones subjetivas, lo que hace necesaria la obtención de información objetiva.

Objetivo: Desarrollar un método que identifique y clasifique las Actividades de la Vida Diaria (AVDs) en pacientes con Parkinson utilizando Redes Neuronales Artificiales (RNA) programadas en Python para enriquecer el seguimiento y apoyo a estos pacientes.

Metodología: Se aplicó Análisis de Componentes Principales (PCA) para reducir la dimensionalidad de una base de datos de 179,755 observaciones y 64 variables, recolectadas a través de sensores inerciales de varios pacientes con Parkinson. Se entrenó un Perceptrón Multicapa (MLP) con los datos obtenidos, normalizando las características y utilizando la función de activación ReLU en la primera capa oculta.

Resultados: El modelo obtuvo un porcentaje de clasificación del 93% en la medida F1-score, evidenciando una alta precisión en la identificación de AVDs a partir de la información proporcionada por los sensores, incluso en un conjunto de datos desbalanceado.

Conclusión: Se demuestra la versatilidad de las RNA, en combinación con la técnica PCA, en la clasificación de actividades en pacientes con EP, mostrando que es posible alcanzar altos niveles de precisión incluso usando una base de datos reducida.

Restricciones: No se especificaron limitaciones de formato en el documento, pero se infiere que el estudio se basa en la implementación técnica y condiciones específicas de los datos utilizados para entrenar el modelo.
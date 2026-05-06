Problema: La investigación aborda el problema del diagnóstico tardío de la enfermedad de Alzheimer en sus fases prodrómicas, concretamente durante el Deterioro Cognitivo Leve (DCL).

Objetivo: El objetivo principal es desarrollar un sistema automatizado mediante Inteligencia Artificial capaz de detectar biomarcadores tempranos en imágenes médicas, antes de que los síntomas clínicos del Alzheimer sean irreversibles.

Metodología: Se entrenó una red neuronal convolucional (arquitectura EfficientNet-B0) con 2.500 resonancias magnéticas estructurales de la iniciativa ADNI. Se aplicaron técnicas de 'skull-stripping' y normalización espacial. Se utilizó el optimizador Adam con una tasa de aprendizaje de 0.001 durante 50 épocas, validando el proceso con 10-fold cross-validation.

Resultados: El modelo logró una precisión global del 91,2% en la distinción entre pacientes sanos y pacientes con DCL. Específicamente, el sistema alcanzó una sensibilidad del 89,5% y una especificidad del 93,1%, con un área bajo la curva (AUC) de 0,94.

Conclusión: La inteligencia artificial se presenta como una herramienta altamente confiable para el diagnóstico precoz de la enfermedad de Alzheimer. La implementación clínica del sistema se realizará mediante un módulo de software integrado en el sistema PACS del hospital, permitiendo iniciar tratamientos farmacológicos preventivos de manera más temprana y efectiva.

Restricciones: La única restricción es que el abstract final no debe superar el límite de 250 palabras y debe estar escrito en un formato completamente académico.
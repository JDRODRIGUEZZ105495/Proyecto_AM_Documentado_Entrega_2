# Ajustes respecto al script inicial

Se conservaron el enfoque, los parámetros físicos y las cinco figuras del código aportado por el grupo. La versión organizada incorpora:

- Conversión del texto pegado en Markdown a Python: eliminación de escapes de formato y entidades HTML.
- Comentarios consistentes con el seno usado y el índice de modulación independiente.
- Uso explícito del mensaje normalizado en la envolvente.
- Semilla 2026 para repetir el ruido.
- Corrección de la escala en la comparación de envolvente sin filtrar: multiplicación por el mismo factor que la señal filtrada.
- Espectro unilateral sin duplicar DC ni Nyquist.
- Etiquetas de amplitud en unidades arbitrarias.
- Visualización del módulo de la envolvente en sobremodulación.
- Guardado de figuras en results y exportación de características, parámetros y métricas.
- Opción de ejecución sin ventanas y manejo de consola compatible con entornos que no exponen stdout.buffer.
- Métricas del registro completo y de un intervalo interior para observar efectos de borde.
- Sustitución de la valoración automática «excelente» por una interpretación cuantitativa.

Las métricas de esta versión pueden diferir de ejecuciones del script inicial, que no fijaba la semilla. No se ha cambiado la normalización por pico del mensaje de referencia; esa dependencia se declara en la documentación.

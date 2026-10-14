# Datos y procedencia

Las señales se generan en `src/sistema_am.py` a partir de expresiones seno y coseno. No se usa base de datos externa, grabación de voz, micrófono ni sensor. No hace falta descargar datos.

El registro tiene 4410 muestras a 44100 Hz. El mensaje es un tono de 440 Hz, de amplitud unitaria; la portadora tiene frecuencia 10000 Hz y amplitud unitaria. El ruido se genera con `numpy.random.default_rng(2026)` y una desviación calculada para SNR objetivo de 20 dB.

Los datos completos se regeneran al ejecutar el programa. `results/caracteristicas.csv` resume cada señal; `parametros.json` registra parámetros y versiones. No se ha generado un archivo de audio ni evaluado perceptualmente su reproducción.

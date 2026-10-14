# Caracterización e interpretación de resultados

Ejecución reproducible con semilla 2026 y parámetros registrados en `results/parametros.json`.

| Señal | Mínimo | Máximo | Media | RMS | Pico a pico |
|---|---:|---:|---:|---:|---:|
| mensaje | -0.99999975 | 0.99999975 | 0.00000000 | 0.70710678 | 1.99999949 |
| portadora | -0.99997463 | 1.00000000 | 0.00000000 | 0.70710678 | 1.99997463 |
| AM | -1.79893128 | 1.79831037 | 0.00000000 | 0.81240384 | 3.59724165 |
| recibida | -1.91938612 | 1.96699070 | -0.00115197 | 0.81643445 | 3.88637682 |
| recuperada | -0.99987929 | 0.99999975 | -0.00054854 | 0.66805524 | 1.99987904 |

Amplitudes en u.a. Todas las señales tienen 4410 muestras y duración N/fs=0.1 s. La media teórica de los tonos es cero; los pequeños residuos numéricos son de precisión flotante. La media de la realización finita del ruido no es exactamente cero.

El RMS del mensaje y la portadora es 0.70710678. La AM tiene RMS=sqrt(0.66)=0.81240384. El ruido aumenta el RMS y altera los extremos. Los picos muestreados no tienen que coincidir exactamente con los extremos continuos.

El RMS recuperado es 0.66805524, inferior al del mensaje a pesar de igualar su pico máximo. Esto ilustra que normalizar por pico no garantiza recuperar toda la amplitud ni elimina distorsión. La correlación alta muestra semejanza temporal en este caso; el MSE cuantifica diferencias después de esa normalización.

Las métricas interior/completa se guardan en metricas.json. Se excluyen 10 ms por extremo para la comparación interior; no se optimiza el intervalo para minimizar el error. La figura temporal muestra el inicio y permite observar el transitorio en lugar de ocultarlo.

La SNR medida es aproximadamente 19.93383 dB. No se fuerza el ruido a tener exactamente 20 dB de SNR en esta realización: se fija su varianza esperada.

Validación analítica del caso sin ruido: la envolvente por Hilbert coincide numéricamente con 1+0.8sin(2π440t); el espectro tiene amplitudes 0.4, 1 y 0.4 en 9560, 10000 y 10440 Hz. La potencia media AM es 0.66 u.a.². Estas comprobaciones validan el transmisor ideal del escenario predeterminado, no todos los usos posibles del receptor.

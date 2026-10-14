# -*- coding: utf-8 -*-

"""

=============================================================================

    TRANSMISOR Y RECEPTOR AM DE AUDIO

    ----------------------------------

    Simulacion completa en Python de un sistema de comunicaciones

    con Modulacion en Amplitud (AM).

    Asignatura: Teoria de Senales - Universidad de Manizales

    Integrantes:

        - Juan David Rodriguez 


    Este script simula:

        1. Generacion de una senal de audio (moduladora)

        2. Generacion de una portadora de alta frecuencia

        3. Modulacion AM (DSB-LC)

        4. Transmision por un canal con ruido

        5. Demodulacion por deteccion de envolvente

        6. Comparacion de senal original vs. recuperada

        7. Analisis en frecuencia (FFT)

=============================================================================

"""

import numpy as np

import matplotlib.pyplot as plt

from scipy.signal import butter, filtfilt, hilbert

import sys

import argparse
import json
import csv
from pathlib import Path
import scipy
import matplotlib
import platform

# Forzar salida UTF-8 en la consola de Windows

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

parser = argparse.ArgumentParser(description='Simulación AM de un tono de audio')
parser.add_argument('--sin-ventanas', action='store_true', help='Guardar figuras sin abrir ventanas')
args = parser.parse_args()
if args.sin_ventanas:
    plt.switch_backend('Agg')
SALIDA = Path(__file__).resolve().parents[1] / 'results'
SALIDA.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------------------

# CONFIGURACION DE MATPLOTLIB (estilo profesional para las graficas)

# ---------------------------------------------------------------------------

plt.rcParams.update({

    'figure.facecolor': '#0d1117',

    'axes.facecolor':   '#161b22',

    'axes.edgecolor':   '#30363d',

    'axes.labelcolor':  '#c9d1d9',

    'text.color':       '#c9d1d9',

    'xtick.color':      '#8b949e',

    'ytick.color':      '#8b949e',

    'grid.color':       '#21262d',

    'grid.alpha':       0.6,

    'font.size':        10,

    'font.family':      'sans-serif',

    'figure.dpi':       120,

})

# Paleta de colores vibrantes

COLOR_MODULADORA = '#58a6ff'   # Azul

COLOR_PORTADORA  = '#f97583'   # Rosa

COLOR_AM         = '#56d364'   # Verde

COLOR_RUIDO      = '#d2a8ff'   # Purpura

COLOR_DEMOD      = '#ff7b72'   # Rojo-naranja

COLOR_COMPARAR   = '#ffa657'   # Naranja

COLOR_FFT        = '#79c0ff'   # Azul claro

# =============================================================================

# 1. PARAMETROS DEL SISTEMA

# =============================================================================

print("=" * 65)

print("   TRANSMISOR Y RECEPTOR AM DE AUDIO")

print("   Teoria de Senales - Universidad de Manizales")

print("=" * 65)

# Parametros de muestreo

fs = 44100          # Frecuencia de muestreo (Hz) - calidad de audio estandar

duracion = 0.1      # Duracion de la senal (segundos) - suficiente para visualizar

t = np.linspace(0, duracion, int(fs * duracion), endpoint=False)

# Parametros de la senal moduladora (audio)

fm = 440            # Frecuencia de la moduladora (Hz) - nota La (A4)

Am = 1.0            # Amplitud de la moduladora

# Parametros de la senal portadora

fc = 10000          # Frecuencia de la portadora (Hz) - 10 kHz

Ac = 1.0            # Amplitud de la portadora

# Indice de modulacion

# m es el índice elegido para el mensaje normalizado x(t)/Am.
# No es Am/Ac en esta implementación; m > 1 produce sobremodulación.

m = 0.8             # Indice de modulacion (80%)

# Nivel de ruido del canal

snr_db = 20         # Relacion senal a ruido en dB

print(f"\n[PARAMETROS] Parametros del sistema:")

print(f"   Frecuencia de muestreo:  {fs:,} Hz")

print(f"   Duracion:                {duracion} s")

print(f"   Frecuencia moduladora:   {fm} Hz (nota La - A4)")

print(f"   Frecuencia portadora:    {fc:,} Hz")

print(f"   Indice de modulacion:    {m} ({m*100:.0f}%)")

print(f"   SNR del canal:           {snr_db} dB")

# =============================================================================

# 2. GENERACION DE SENALES

# =============================================================================

print("\n[AUDIO] Generando senales...")

# -- Senal moduladora (audio) --

# Es la senal que contiene la informacion (audio) que queremos transmitir.

# Usamos una senal senoidal como ejemplo simplificado de audio.

senal_moduladora = Am * np.sin(2 * np.pi * fm * t)

# -- Senal portadora --

# Es la onda de alta frecuencia que sera modulada para transportar la informacion.

senal_portadora = Ac * np.cos(2 * np.pi * fc * t)

print(f"   [OK] Senal moduladora generada: senoidal a {fm} Hz")

print(f"   [OK] Senal portadora generada: cosenoidal a {fc:,} Hz")

# =============================================================================

# 3. MODULACION AM (DSB-LC: Doble Banda Lateral con Portadora)

# =============================================================================

print("\n[AM] Realizando modulacion AM...")

# Formula de modulacion AM:

#   s_AM(t) = Ac * [1 + m * sin(2*pi * fm * t)] * cos(2*pi * fc * t)

#

# Donde:

#   - Ac = amplitud de la portadora

#   - m  = indice de modulacion del mensaje normalizado

#   - fm = frecuencia de la moduladora

#   - fc = frecuencia de la portadora

#

# La envolvente de la senal AM es: E(t) = Ac * [1 + m * sin(2*pi * fm * t)]

envolvente = Ac * (1 + m * senal_moduladora / Am)

senal_am = envolvente * np.cos(2 * np.pi * fc * t)

# Verificar que no haya sobremodulacion

if m > 1:

    print(f"   [ADVERTENCIA] Indice de modulacion m={m} > 1 (sobremodulacion)")

else:

    print(f"   [OK] Modulacion AM correcta (sin sobremodulacion)")

print(f"   [OK] Senal AM generada")

print(f"   [INFO] Amplitud maxima: {np.max(np.abs(senal_am)):.4f}")

print(f"   [INFO] Amplitud minima de envolvente: {np.min(envolvente):.4f}")

# =============================================================================

# 4. SIMULACION DEL CANAL (agregar ruido)

# =============================================================================

print("\n[CANAL] Simulando canal de transmision...")

# Agregar ruido gaussiano blanco al canal

potencia_senal = np.mean(senal_am ** 2)

potencia_ruido = potencia_senal / (10 ** (snr_db / 10))

semilla = 2026
rng = np.random.default_rng(semilla)
ruido = np.sqrt(potencia_ruido) * rng.standard_normal(len(t))

senal_recibida = senal_am + ruido

snr_real = 10 * np.log10(potencia_senal / np.mean(ruido ** 2))

print(f"   [OK] Ruido gaussiano anadido")

print(f"   [INFO] SNR objetivo: {snr_db} dB")

print(f"   [INFO] SNR real:     {snr_real:.2f} dB")

# =============================================================================

# 5. DEMODULACION AM (Deteccion de envolvente)

# =============================================================================

print("\n[RECEPTOR] Demodulando senal AM...")

# Metodo: Deteccion de envolvente usando la transformada de Hilbert

# La envolvente de una senal se obtiene como el modulo de la senal analitica:

#   envolvente = |s(t) + j * H{s(t)}|

# donde H{} es la transformada de Hilbert.

senal_analitica = hilbert(senal_recibida)

envolvente_detectada = np.abs(senal_analitica)

# Eliminar componente DC (la portadora agrega un offset)

envolvente_detectada = envolvente_detectada - np.mean(envolvente_detectada)

# Filtro paso bajo para suavizar la senal recuperada

# Disenamos un filtro Butterworth de orden 4

frecuencia_corte = 2 * fm  # Frecuencia de corte: el doble de la moduladora

nyquist = fs / 2

frecuencia_normalizada = frecuencia_corte / nyquist

b, a = butter(4, frecuencia_normalizada, btype='low')

senal_demodulada = filtfilt(b, a, envolvente_detectada)

# Normalizar para comparar con la senal original

factor_escala = np.max(np.abs(senal_moduladora)) / np.max(np.abs(senal_demodulada))

senal_demodulada = senal_demodulada * factor_escala

print(f"   [OK] Deteccion de envolvente (Hilbert) completada")

print(f"   [OK] Filtro paso bajo aplicado (fc = {frecuencia_corte} Hz)")

print(f"   [OK] Senal demodulada normalizada")

# =============================================================================

# 6. ANALISIS DE CALIDAD

# =============================================================================

print("\n[CALIDAD] Analisis de calidad de la senal recuperada...")

# Calcular el error cuadratico medio (MSE)

mse = np.mean((senal_moduladora - senal_demodulada) ** 2)

# Calcular la correlacion entre senal original y recuperada

correlacion = np.corrcoef(senal_moduladora, senal_demodulada)[0, 1]

print(f"   [INFO] Error cuadratico medio (MSE):  {mse:.6f}")

print(f"   [INFO] Correlacion:                   {correlacion:.6f}")

print('   [INFO] La correlacion mide semejanza; revisar también MSE, ganancia y bordes.')

# =============================================================================

# 7. ANALISIS EN FRECUENCIA (FFT)

# =============================================================================

print("\n[FFT] Calculando espectro en frecuencia (FFT)...")

def calcular_espectro(senal, fs):

    """Calcula el espectro de frecuencia de una senal usando la FFT."""

    N = len(senal)
    fft_magnitud = np.abs(np.fft.rfft(senal)) / N
    if N % 2 == 0:
        fft_magnitud[1:-1] *= 2
    else:
        fft_magnitud[1:] *= 2
    frecuencias = np.fft.rfftfreq(N, 1 / fs)
    return frecuencias, fft_magnitud

freq_mod, fft_mod = calcular_espectro(senal_moduladora, fs)

freq_am, fft_am = calcular_espectro(senal_am, fs)

freq_demod, fft_demod = calcular_espectro(senal_demodulada, fs)

print(f"   [OK] Espectros calculados")

# =============================================================================

# 8. VISUALIZACION - GRAFICAS COMPLETAS

# =============================================================================

print("\n[GRAFICAS] Generando graficas...")

# Rango de visualizacion en el tiempo (mostrar solo unos pocos ciclos)

t_ms = t * 1000  # Convertir a milisegundos

idx_zoom = t_ms <= 10  # Mostrar los primeros 10 ms

# ---------------------------------------------------------------------------

# FIGURA 1: Proceso completo de modulacion AM en el tiempo

# ---------------------------------------------------------------------------

fig1, axes1 = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

fig1.suptitle('TRANSMISOR AM - Proceso de Modulacion', 

              fontsize=16, fontweight='bold', color='white', y=0.98)

# Senal moduladora

axes1[0].plot(t_ms[idx_zoom], senal_moduladora[idx_zoom], 

              color=COLOR_MODULADORA, linewidth=1.5, label='Senal moduladora')

axes1[0].set_ylabel('Amplitud [u.a.]')

axes1[0].set_title(f'Senal Moduladora (Audio) - fm = {fm} Hz', 

                    fontsize=11, color=COLOR_MODULADORA)

axes1[0].legend(loc='upper right')

axes1[0].grid(True, alpha=0.3)

axes1[0].set_ylim([-1.5, 1.5])

# Senal portadora

axes1[1].plot(t_ms[idx_zoom], senal_portadora[idx_zoom], 

              color=COLOR_PORTADORA, linewidth=0.8, label='Senal portadora')

axes1[1].set_ylabel('Amplitud [u.a.]')

axes1[1].set_title(f'Senal Portadora - fc = {fc:,} Hz', 

                    fontsize=11, color=COLOR_PORTADORA)

axes1[1].legend(loc='upper right')

axes1[1].grid(True, alpha=0.3)

axes1[1].set_ylim([-1.5, 1.5])

# Senal AM modulada

axes1[2].plot(t_ms[idx_zoom], senal_am[idx_zoom], 

              color=COLOR_AM, linewidth=0.8, label='Senal AM')

axes1[2].plot(t_ms[idx_zoom], envolvente[idx_zoom], 

              color=COLOR_COMPARAR, linewidth=1.5, linestyle='--', 

              label='Envolvente superior', alpha=0.9)

axes1[2].plot(t_ms[idx_zoom], -envolvente[idx_zoom], 

              color=COLOR_COMPARAR, linewidth=1.5, linestyle='--', 

              label='Envolvente inferior', alpha=0.9)

axes1[2].set_ylabel('Amplitud [u.a.]')

axes1[2].set_title(f'Senal AM Modulada - m = {m} ({m*100:.0f}%)', 

                    fontsize=11, color=COLOR_AM)

axes1[2].legend(loc='upper right', fontsize=8)

axes1[2].grid(True, alpha=0.3)

# Senal recibida con ruido

axes1[3].plot(t_ms[idx_zoom], senal_recibida[idx_zoom], 

              color=COLOR_RUIDO, linewidth=0.6, alpha=0.8, label='Senal recibida')

axes1[3].set_ylabel('Amplitud [u.a.]')

axes1[3].set_xlabel('Tiempo (ms)')

axes1[3].set_title(f'Senal Recibida (con ruido) - SNR = {snr_db} dB', 

                    fontsize=11, color=COLOR_RUIDO)

axes1[3].legend(loc='upper right')

axes1[3].grid(True, alpha=0.3)

fig1.tight_layout(rect=[0, 0, 1, 0.96])

fig1.savefig(SALIDA / 'grafica_01_modulacion_am.png', dpi=150, bbox_inches='tight',

             facecolor=fig1.get_facecolor())

print("   [OK] Figura 1: Proceso de modulacion guardada")

# ---------------------------------------------------------------------------

# FIGURA 2: Proceso de demodulacion

# ---------------------------------------------------------------------------

fig2, axes2 = plt.subplots(3, 1, figsize=(14, 8), sharex=True)

fig2.suptitle('RECEPTOR AM - Proceso de Demodulacion', 

              fontsize=16, fontweight='bold', color='white', y=0.98)

# Senal recibida

axes2[0].plot(t_ms[idx_zoom], senal_recibida[idx_zoom], 

              color=COLOR_RUIDO, linewidth=0.6, alpha=0.8, label='Senal recibida')

axes2[0].set_ylabel('Amplitud [u.a.]')

axes2[0].set_title('Senal Recibida (con ruido del canal)', 

                    fontsize=11, color=COLOR_RUIDO)

axes2[0].legend(loc='upper right')

axes2[0].grid(True, alpha=0.3)

# Envolvente detectada (antes del filtro)

axes2[1].plot(t_ms[idx_zoom], envolvente_detectada[idx_zoom] * factor_escala, 

              color=COLOR_DEMOD, linewidth=1, alpha=0.6, label='Envolvente (sin filtrar)')

axes2[1].plot(t_ms[idx_zoom], senal_demodulada[idx_zoom], 

              color=COLOR_AM, linewidth=2, label='Senal demodulada (filtrada)')

axes2[1].set_ylabel('Amplitud [u.a.]')

axes2[1].set_title('Deteccion de Envolvente + Filtro Paso Bajo', 

                    fontsize=11, color=COLOR_DEMOD)

axes2[1].legend(loc='upper right')

axes2[1].grid(True, alpha=0.3)

# Comparacion original vs recuperada

axes2[2].plot(t_ms[idx_zoom], senal_moduladora[idx_zoom], 

              color=COLOR_MODULADORA, linewidth=2, label='Senal original', alpha=0.8)

axes2[2].plot(t_ms[idx_zoom], senal_demodulada[idx_zoom], 

              color=COLOR_COMPARAR, linewidth=2, linestyle='--', 

              label='Senal recuperada', alpha=0.9)

axes2[2].set_ylabel('Amplitud [u.a.]')

axes2[2].set_xlabel('Tiempo (ms)')

axes2[2].set_title(f'Comparacion: Original vs Recuperada - Correlacion = {correlacion:.4f}', 

                    fontsize=11, color=COLOR_COMPARAR)

axes2[2].legend(loc='upper right')

axes2[2].grid(True, alpha=0.3)

fig2.tight_layout(rect=[0, 0, 1, 0.96])

fig2.savefig(SALIDA / 'grafica_02_demodulacion.png', dpi=150, bbox_inches='tight',

             facecolor=fig2.get_facecolor())

print("   [OK] Figura 2: Proceso de demodulacion guardada")

# ---------------------------------------------------------------------------

# FIGURA 3: Analisis en frecuencia (FFT)

# ---------------------------------------------------------------------------

fig3, axes3 = plt.subplots(3, 1, figsize=(14, 8))

fig3.suptitle('ANALISIS EN FRECUENCIA (FFT)', 

              fontsize=16, fontweight='bold', color='white', y=0.98)

# Espectro de la moduladora

axes3[0].plot(freq_mod, fft_mod, color=COLOR_MODULADORA, linewidth=1.5)

axes3[0].set_ylabel('Amplitud pico [u.a.]')

axes3[0].set_title(f'Espectro de la Senal Moduladora - Pico en {fm} Hz', 

                    fontsize=11, color=COLOR_MODULADORA)

axes3[0].set_xlim([0, 2000])

axes3[0].axvline(x=fm, color=COLOR_COMPARAR, linestyle='--', alpha=0.7, 

                 label=f'fm = {fm} Hz')

axes3[0].legend(loc='upper right')

axes3[0].grid(True, alpha=0.3)

# Espectro de la senal AM

axes3[1].plot(freq_am, fft_am, color=COLOR_AM, linewidth=1.5)

axes3[1].set_ylabel('Amplitud pico [u.a.]')

axes3[1].set_title(f'Espectro de la Senal AM - Portadora: {fc:,} Hz, Bandas: {fc-fm:,} y {fc+fm:,} Hz', 

                    fontsize=11, color=COLOR_AM)

axes3[1].set_xlim([0, 15000])

axes3[1].axvline(x=fc, color=COLOR_PORTADORA, linestyle='--', alpha=0.7, 

                 label=f'fc = {fc:,} Hz')

axes3[1].axvline(x=fc - fm, color=COLOR_COMPARAR, linestyle=':', alpha=0.7, 

                 label=f'fc - fm = {fc-fm:,} Hz')

axes3[1].axvline(x=fc + fm, color=COLOR_COMPARAR, linestyle=':', alpha=0.7, 

                 label=f'fc + fm = {fc+fm:,} Hz')

axes3[1].legend(loc='upper right', fontsize=8)

axes3[1].grid(True, alpha=0.3)

# Espectro de la senal demodulada

axes3[2].plot(freq_demod, fft_demod, color=COLOR_DEMOD, linewidth=1.5)

axes3[2].set_ylabel('Amplitud pico [u.a.]')

axes3[2].set_xlabel('Frecuencia (Hz)')

axes3[2].set_title(f'Espectro de la Senal Demodulada - Pico recuperado en {fm} Hz', 

                    fontsize=11, color=COLOR_DEMOD)

axes3[2].set_xlim([0, 2000])

axes3[2].axvline(x=fm, color=COLOR_COMPARAR, linestyle='--', alpha=0.7, 

                 label=f'fm = {fm} Hz')

axes3[2].legend(loc='upper right')

axes3[2].grid(True, alpha=0.3)

fig3.tight_layout(rect=[0, 0, 1, 0.96])

fig3.savefig(SALIDA / 'grafica_03_espectro_fft.png', dpi=150, bbox_inches='tight',

             facecolor=fig3.get_facecolor())

print("   [OK] Figura 3: Espectros de frecuencia guardada")

# ---------------------------------------------------------------------------

# FIGURA 4: Diagrama resumen del sistema

# ---------------------------------------------------------------------------

fig4, axes4 = plt.subplots(2, 3, figsize=(16, 7))

fig4.suptitle('DIAGRAMA RESUMEN - Sistema Transmisor/Receptor AM', 

              fontsize=16, fontweight='bold', color='white', y=1.02)

# Moduladora

axes4[0, 0].plot(t_ms[idx_zoom], senal_moduladora[idx_zoom], 

                  color=COLOR_MODULADORA, linewidth=1.5)

axes4[0, 0].set_title('(1) Moduladora\n(Audio)', fontsize=10, color=COLOR_MODULADORA)

axes4[0, 0].set_ylabel('Amplitud [u.a.]')

axes4[0, 0].grid(True, alpha=0.3)

# Portadora

axes4[0, 1].plot(t_ms[idx_zoom], senal_portadora[idx_zoom], 

                  color=COLOR_PORTADORA, linewidth=0.8)

axes4[0, 1].set_title('(2) Portadora\n(Alta frecuencia)', fontsize=10, color=COLOR_PORTADORA)

axes4[0, 1].grid(True, alpha=0.3)

# Senal AM

axes4[0, 2].plot(t_ms[idx_zoom], senal_am[idx_zoom], 

                  color=COLOR_AM, linewidth=0.8)

axes4[0, 2].set_title('(3) Senal AM\n(Modulada)', fontsize=10, color=COLOR_AM)

axes4[0, 2].grid(True, alpha=0.3)

# Canal (ruido)

axes4[1, 0].plot(t_ms[idx_zoom], senal_recibida[idx_zoom], 

                  color=COLOR_RUIDO, linewidth=0.6, alpha=0.8)

axes4[1, 0].set_title('(4) Canal\n(Con ruido)', fontsize=10, color=COLOR_RUIDO)

axes4[1, 0].set_ylabel('Amplitud [u.a.]')

axes4[1, 0].set_xlabel('Tiempo (ms)')

axes4[1, 0].grid(True, alpha=0.3)

# Demodulacion

axes4[1, 1].plot(t_ms[idx_zoom], senal_demodulada[idx_zoom], 

                  color=COLOR_DEMOD, linewidth=1.5)

axes4[1, 1].set_title('(5) Demodulada\n(Envolvente)', fontsize=10, color=COLOR_DEMOD)

axes4[1, 1].set_xlabel('Tiempo (ms)')

axes4[1, 1].grid(True, alpha=0.3)

# Comparacion

axes4[1, 2].plot(t_ms[idx_zoom], senal_moduladora[idx_zoom], 

                  color=COLOR_MODULADORA, linewidth=2, alpha=0.7, label='Original')

axes4[1, 2].plot(t_ms[idx_zoom], senal_demodulada[idx_zoom], 

                  color=COLOR_COMPARAR, linewidth=2, linestyle='--', label='Recuperada')

axes4[1, 2].set_title('(6) Comparacion\n(Original vs Recuperada)', 

                        fontsize=10, color=COLOR_COMPARAR)

axes4[1, 2].set_xlabel('Tiempo (ms)')

axes4[1, 2].legend(loc='upper right', fontsize=8)

axes4[1, 2].grid(True, alpha=0.3)

fig4.tight_layout()

fig4.savefig(SALIDA / 'grafica_04_resumen_sistema.png', dpi=150, bbox_inches='tight',

             facecolor=fig4.get_facecolor())

print("   [OK] Figura 4: Diagrama resumen guardada")

# ---------------------------------------------------------------------------

# FIGURA 5: Variacion del indice de modulacion

# ---------------------------------------------------------------------------

fig5, axes5 = plt.subplots(2, 2, figsize=(14, 8))

fig5.suptitle('EFECTO DEL INDICE DE MODULACION', 

              fontsize=16, fontweight='bold', color='white', y=0.98)

indices = [0.3, 0.6, 1.0, 1.5]

colores_m = ['#58a6ff', '#56d364', '#ffa657', '#f97583']

for i, (ax, mi) in enumerate(zip(axes5.flat, indices)):

    env_i = Ac * (1 + mi * np.sin(2 * np.pi * fm * t))

    am_i = env_i * np.cos(2 * np.pi * fc * t)

    ax.plot(t_ms[idx_zoom], am_i[idx_zoom], color=colores_m[i], linewidth=0.7)

    ax.plot(t_ms[idx_zoom], env_i[idx_zoom], color='white', 

            linewidth=1.5, linestyle='--', alpha=0.7)

    ax.plot(t_ms[idx_zoom], -env_i[idx_zoom], color='white', 

            linewidth=1.5, linestyle='--', alpha=0.7)

    if mi > 1:
        ax.plot(t_ms[idx_zoom], np.abs(env_i[idx_zoom]), color='#ffa657',
                linewidth=1.2, label='Envolvente física |E|')
        ax.legend(fontsize=8)
    etiqueta = 'SOBREMODULACION' if mi > 1 else 'SIN SOBREMODULACION'

    ax.set_title(f'm = {mi} ({mi*100:.0f}%) - {etiqueta}', 

                  fontsize=11, color=colores_m[i], fontweight='bold')

    ax.set_xlabel('Tiempo (ms)')

    ax.set_ylabel('Amplitud [u.a.]')

    ax.grid(True, alpha=0.3)

fig5.tight_layout(rect=[0, 0, 1, 0.95])

fig5.savefig(SALIDA / 'grafica_05_indices_modulacion.png', dpi=150, bbox_inches='tight',

             facecolor=fig5.get_facecolor())

print("   [OK] Figura 5: Indices de modulacion guardada")

# =============================================================================

# RESUMEN FINAL

# =============================================================================

print("\n" + "=" * 65)

print("   RESUMEN DEL SISTEMA AM")

print("=" * 65)

print(f"""

   TRANSMISOR:

   +-- Senal moduladora:    senoidal {fm} Hz (audio)

   +-- Senal portadora:     cosenoidal {fc:,} Hz

   +-- Indice de modulacion: m = {m}

   +-- Tipo de AM:          DSB-LC (Doble Banda Lateral con Portadora)

   CANAL:

   +-- Tipo de ruido:       Gaussiano blanco (AWGN)

   +-- SNR:                 {snr_db} dB

   RECEPTOR:

   +-- Metodo:              Deteccion de envolvente (Hilbert)

   +-- Filtro:              Butterworth paso bajo (orden 4, fc={frecuencia_corte} Hz)

   +-- Calidad:

       +-- MSE:             {mse:.6f}

       +-- Correlacion:     {correlacion:.6f}

   ARCHIVOS GENERADOS:

   +-- grafica_01_modulacion_am.png

   +-- grafica_02_demodulacion.png

   +-- grafica_03_espectro_fft.png

   +-- grafica_04_resumen_sistema.png

   +-- grafica_05_indices_modulacion.png

""")

# Mostrar todas las graficas

# Exportar características y métricas; normalización usa el mensaje conocido.
def caracteristicas(nombre, x):
    return dict(senal=nombre, minimo=float(np.min(x)), maximo=float(np.max(x)),
                media=float(np.mean(x)), rms=float(np.sqrt(np.mean(x**2))),
                pico_a_pico=float(np.ptp(x)), muestras=len(x), fs_Hz=fs,
                Ts_s=1/fs, duracion_s=len(x)/fs)

registros = [caracteristicas(nombre, x) for nombre, x in [
    ('mensaje', senal_moduladora), ('portadora', senal_portadora),
    ('AM', senal_am), ('recibida', senal_recibida), ('recuperada', senal_demodulada)]]
with (SALIDA / 'caracteristicas.csv').open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(registros[0]))
    writer.writeheader()
    writer.writerows(registros)
interior = (t >= 0.01) & (t < duracion - 0.01)
metricas = dict(SNR_objetivo_dB=snr_db, SNR_medida_dB=float(snr_real),
    MSE_registro_completo=float(mse), correlacion_registro_completo=float(correlacion),
    MSE_interior=float(np.mean((senal_moduladora[interior]-senal_demodulada[interior])**2)),
    correlacion_interior=float(np.corrcoef(senal_moduladora[interior],senal_demodulada[interior])[0,1]),
    intervalo_interior_s=[0.01, duracion-0.01], factor_normalizacion=float(factor_escala))
(SALIDA / 'metricas.json').write_text(json.dumps(metricas, indent=2), encoding='utf-8')
parametros = dict(fs_Hz=fs, Ts_s=1/fs, N=len(t), duracion_s=duracion,
    fm_Hz=fm, fc_Hz=fc, Am=Am, Ac=Ac, indice_modulacion=m, semilla=semilla,
    filtro_orden_diseno=4, filtro_corte_Hz=frecuencia_corte,
    python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__,
    matplotlib=matplotlib.__version__)
(SALIDA / 'parametros.json').write_text(json.dumps(parametros, indent=2), encoding='utf-8')
print(f'Resultados guardados en {SALIDA}')
if args.sin_ventanas:
    plt.close('all')
else:
    plt.show()

print("[LISTO] Simulacion completada exitosamente.") 

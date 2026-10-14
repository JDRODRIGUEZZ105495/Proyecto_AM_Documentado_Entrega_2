# Fundamentos de la simulación

## Señales y muestreo

Una señal continua x(t) se representa mediante x[n]=x(nTs), Ts=1/fs. Aquí N=4410 y N/fs=0.1 s. Para el tono, Tm=1/440 s; para la portadora, Tc=1/10000 s. La señal AM ideal repite su patrón cada 1/gcd(440,10000)=0.025 s. En tiempo discreto el mensaje tiene período 2205 muestras, la portadora 441 y la AM 2205; la malla no contiene un número entero de muestras por período continuo de AM.

Las amplitudes no tienen calibración física: u.a. significa unidades arbitrarias. La media es sum(x[n])/N, el valor RMS es sqrt(sum(x[n]²)/N) y el pico a pico es max(x)-min(x). Un seno unitario tiene media cero y RMS=1/sqrt(2).

## Modulación

Se normaliza el mensaje como u(t)=x(t)/Am. La AM con portadora es s(t)=Ac[1+μu(t)]cos(2πfc t). El factor 1 conserva la portadora. Con u(t)=sin(2πfm t), la identidad seno por coseno produce una componente en fc y dos bandas laterales en fc±fm. Sus amplitudes pico son Ac y Acμ/2; una de las componentes senoidales lleva signo negativo, que afecta fase, no magnitud espectral.

El ancho de banda ideal es 2fm=880 Hz. La potencia media numérica es Ac²/2·(1+μ²/2)=0.66 u.a.². No se expresa en vatios porque no hay resistencia ni voltaje calibrado.

## Canal

El modelo es r[n]=s[n]+w[n]. Se genera w con distribución normal independiente de media esperada cero y desviación σ=sqrt(Ps/10^(SNR/10)). Para Ps=0.66 y SNR=20 dB, σ≈0.08124038 u.a. La semilla 2026 permite repetir el experimento con el entorno documentado. La SNR se refiere a toda la AM, incluida la portadora; no es una medida directa de calidad del audio recuperado.

## Receptor

SciPy obtiene la señal analítica r_a=r+jH{r}. El módulo |r_a| estima la envolvente. Para la AM limpia de este tono y μ≤1, la separación espectral permite recuperar Ac[1+μu]. Con ruido, el módulo introduce perturbaciones y puede presentar sesgo. Se resta la media de la envolvente, no la media de la portadora oscilante.

Se diseña un Butterworth de cuarto orden a 880 Hz y se aplica mediante filtfilt. El módulo de su respuesta total es |H|², con fase cero y orden combinado ocho. El corte de diseño corresponde a una pasada; no debe describirse como un corte de -3 dB de todo el procesamiento doble. El método trabaja sobre el registro completo y puede introducir efectos de borde.

La salida filtrada y se escala por g=max|x|/max|y|. Este g usa el mensaje original; sirve para comparación de forma, pero no es una estimación autónoma de ganancia. Para un receptor calibrado en el caso ideal puede estudiarse el factor conocido Am/(Acμ), junto con la respuesta del filtro. La correlación sola no detecta errores de escala; por eso también se informa MSE y características RMS.

## Transformada discreta

X[k]=sum_n x[n]exp(-j2πkn/N). Las frecuencias son f[k]=kfs/N. Para señales reales, rfft conserva la mitad no redundante. La amplitud unilateral se calcula con |X|/N y duplicación de bins con pareja negativa. DC y Nyquist no se duplican. La separación de bins es 10 Hz. No se aplica zero-padding ni una ventana de suavizado; se utiliza el registro rectangular coherente con los tonos elegidos.

La FFT representa este registro finito. En ruido, audio real o registros no coherentes las líneas se distribuyen y no se puede interpretar todo pico como la amplitud exacta de un seno aislado.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from scipy.signal import butter, filtfilt

# Початкові параметри
init_amplitude = 1.0
init_frequency = 1.0
init_phase = 0.0
init_noise_mean = 0.0
init_noise_covariance = 0.1
init_show_noise = True
init_filter_order = 4
init_cutoff_frequency = 0.2

# Зберігаю початковий шум для використання, коли параметри шуму не змінюються
current_noise = np.random.normal(init_noise_mean, init_noise_covariance, 500)

# Функція для генерації гармоніки з шумом
def harmonic_with_noise(amplitude, frequency, phase, noise, show_noise):
    t = np.linspace(0, 1, 500)
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        return t, harmonic + noise
    else:
        return t, harmonic

# Функція для фільтрації сигналу
def filter_signal(signal, cutoff_frequency, filter_order):
    b, a = butter(filter_order, cutoff_frequency, btype='low', analog=False)
    return filtfilt(b, a, signal)

# Створення фігури та осей для графіку
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
plt.subplots_adjust(left=0.1, bottom=0.4, right=0.75)
t, y = harmonic_with_noise(init_amplitude, init_frequency, init_phase, current_noise, init_show_noise)
filtered_y = filter_signal(y, init_cutoff_frequency, init_filter_order)
l1, = ax1.plot(t, y, lw=2)
l2, = ax2.plot(t, filtered_y, lw=2, color='orange')

ax1.margins(x=0, y=1)
ax2.margins(x=0, y=1)

ax1.set_title('Гармоніка з шумом')
ax2.set_title('Відфільтрована гармоніка')

# Створюю слайдери для параметрів
axcolor = 'lightgoldenrodyellow'
ax_amp = plt.axes([0.1, 0.3, 0.65, 0.03], facecolor=axcolor)
ax_freq = plt.axes([0.1, 0.25, 0.65, 0.03], facecolor=axcolor)
ax_phase = plt.axes([0.1, 0.2, 0.65, 0.03], facecolor=axcolor)
ax_noise_mean = plt.axes([0.1, 0.15, 0.65, 0.03], facecolor=axcolor)
ax_noise_covariance = plt.axes([0.1, 0.1, 0.65, 0.03], facecolor=axcolor)
ax_cutoff_freq = plt.axes([0.1, 0.05, 0.65, 0.03], facecolor=axcolor)
ax_filter_order = plt.axes([0.1, 0, 0.65, 0.03], facecolor=axcolor)

s_amp = Slider(ax_amp, 'Amplitude', 0.1, 10.0, valinit=init_amplitude)
s_freq = Slider(ax_freq, 'Frequency', 0.1, 10.0, valinit=init_frequency)
s_phase = Slider(ax_phase, 'Phase', 0.0, 2*np.pi, valinit=init_phase)
s_noise_mean = Slider(ax_noise_mean, 'Noise Mean', -1.0, 1.0, valinit=init_noise_mean)
s_noise_covariance = Slider(ax_noise_covariance, 'Noise Cov', 0.01, 1.0, valinit=init_noise_covariance)
s_cutoff_freq = Slider(ax_cutoff_freq, 'Cutoff Freq', 0.01, 0.5, valinit=init_cutoff_frequency)
s_filter_order = Slider(ax_filter_order, 'Filter Order', 1, 10, valinit=init_filter_order, valstep=1)

# Чекбокс для перемикання відображення шуму
rax = plt.axes([0.8, 0.4, 0.15, 0.1], facecolor=axcolor)
check = CheckButtons(rax, ['Show Noise'], [init_show_noise])

# Кнопка для скидання налаштувань
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')

# Кнопка для генерації нового шуму
new_noise_ax = plt.axes([0.8, 0.15, 0.1, 0.04])
button_new_noise = Button(new_noise_ax, 'New Noise', color=axcolor, hovercolor='0.975')

# Оновлюю графік при зміні параметрів
def update(val):
    global current_noise
    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    noise_mean = s_noise_mean.val
    noise_cov = s_noise_covariance.val
    cutoff_frequency = s_cutoff_freq.val
    filter_order = s_filter_order.val
    show_noise = check.get_status()[0]

    # Генерую новий шум при зміні параметрів шуму
    if val in ['Noise Mean', 'Noise Cov', 's_noise_mean, s_noise_covariance']:
        current_noise = np.random.normal(noise_mean, noise_cov, 500)

    t, y = harmonic_with_noise(amp, freq, phase, current_noise, show_noise)
    l1.set_ydata(y)
    
    # Фільтрація сигналу
    filtered_y = filter_signal(y, cutoff_frequency, filter_order)
    l2.set_ydata(filtered_y)
    
    fig.canvas.draw_idle()

# Оновлюю графік при зміні будь-якого параметра
def generic_update(val):
    update(val.label if hasattr(val, 'label') else val)

s_amp.on_changed(generic_update)
s_freq.on_changed(generic_update)
s_phase.on_changed(generic_update)
s_noise_mean.on_changed(lambda val: update('Noise Mean'))
s_noise_covariance.on_changed(lambda val: update('Noise Cov'))
s_cutoff_freq.on_changed(generic_update)
s_filter_order.on_changed(generic_update)
check.on_clicked(generic_update)

# Функція скидання налаштувань
def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_noise_mean.reset()
    s_noise_covariance.reset()
    s_cutoff_freq.reset()
    s_filter_order.reset()
    # початкове значення для show_noise
    if check.get_status()[0] != init_show_noise:
        check.set_active(0)  
    update(None)  

# Функція для генерації нового шуму
def generate_new_noise(event):
    global current_noise
    noise_mean = s_noise_mean.val
    noise_cov = s_noise_covariance.val
    current_noise = np.random.normal(noise_mean, noise_cov, 500)
    update(None)

button_reset.on_clicked(reset)
button_new_noise.on_clicked(generate_new_noise)

plt.show()

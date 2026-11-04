import matplotlib.pyplot as plt
from mplsoccer import Pitch

# Crear un campo de fútbol estilo césped oscuro con líneas blancas
pitch = Pitch(pitch_type='statsbomb', pitch_color='#1b4332', line_color='white')
fig, ax = pitch.draw(figsize=(10, 7))

plt.title("¡Primer campo generado con mplsoccer!", color='black', fontsize=14)
plt.show()
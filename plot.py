import os
import matplotlib.pyplot as plt

# Utwórz katalog, jeśli nie istnieje
os.makedirs('static', exist_ok=True)

# Utwórz wykres
plt.figure(figsize=(10, 5))
plt.plot([1, 2, 3], [4, 5, 6])

# Zapisz wykres do katalogu /static/
plt.savefig('static/plot.png')
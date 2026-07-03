import matplotlib.pyplot as plt
import numpy as np
from matplotlib import rcParams

# Configura il font per supportare LaTeX
rcParams['text.usetex'] = False
rcParams['font.size'] = 10

# Dati Tabella 1: Caso Base
distanze = np.array([10, 30, 50, 70, 100])
rms_mic1 = np.array([0.450, 0.450, 0.450, 0.450, 0.450])
rms_mic2 = np.array([0.448, 0.431, 0.412, 0.395, 0.368])
attenuazione = np.array([-0.04, -0.38, -0.77, -1.14, -1.75])
incertezza = np.array([1.5, 1.5, 1.5, 1.5, 1.5])

# Dati Tabella 2: Confronto materiali
frequenze = np.array([250, 500, 1000, 2000, 4000])
caso_base = np.array([-0.35, -0.77, -1.14, -1.45, -1.75])
schiuma = np.array([-2.1, -5.4, -12.3, -18.8, -24.2])
risonanza = np.array([-0.8, -1.2, -31.4, -4.1, -5.5])
pannelli = np.array([-4.2, -18.5, -3.1, -22.1, -6.8])

# ============ GRAFICO 1: Attenuazione vs Distanza ============
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Sottografico 1a: Attenuazione
ax1.errorbar(distanze, attenuazione, yerr=incertezza, fmt='o-', linewidth=2, 
             markersize=8, capsize=5, capthick=2, color='#1f77b4', 
             ecolor='#1f77b4', label='Attenuazione misurata')
ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.5, label='Riferimento (0 dB)')
ax1.set_xlabel('Distanza Microfono 2 (cm)', fontsize=11, fontweight='bold')
ax1.set_ylabel('Attenuazione Relativa (dB)', fontsize=11, fontweight='bold')
ax1.set_title('Caso Base: Attenuazione vs Distanza\n(Fascio Parallelo - f = 1000 Hz)', 
              fontsize=12, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.legend(fontsize=10)
ax1.set_ylim(-2.5, 0.5)

# Sottografico 1b: RMS dei microfoni
ax2.plot(distanze, rms_mic1, 'o-', linewidth=2, markersize=8, 
         color='#ff7f0e', label='RMS Microfono 1 (riferimento)')
ax2.plot(distanze, rms_mic2, 's-', linewidth=2, markersize=8, 
         color='#2ca02c', label='RMS Microfono 2 (mobile)')
ax2.set_xlabel('Distanza Microfono 2 (cm)', fontsize=11, fontweight='bold')
ax2.set_ylabel('RMS (V)', fontsize=11, fontweight='bold')
ax2.set_title('Pressione Acustica RMS vs Distanza', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.legend(fontsize=10)

plt.tight_layout()
plt.savefig('static/images/grafico_caso_base.png', dpi=300, bbox_inches='tight')
print("✓ Grafico 1 salvato: static/images/grafico_caso_base.png")
plt.close()

# ============ GRAFICO 2: Confronto Materiali ============
fig2, ax = plt.subplots(figsize=(12, 6))

ax.semilogx(frequenze, caso_base, 'o-', linewidth=2.5, markersize=8, 
            label='Caso Base (no materiale)', color='#1f77b4')
ax.semilogx(frequenze, schiuma, 's-', linewidth=2.5, markersize=8, 
            label='Schiuma Acustica', color='#ff7f0e')
ax.semilogx(frequenze, risonanza, '^-', linewidth=2.5, markersize=8, 
            label='Metamateriale (Risonanza Locale)', color='#d62728')
ax.semilogx(frequenze, pannelli, 'd-', linewidth=2.5, markersize=8, 
            label='Pannelli Forati', color='#9467bd')

# Annotare il bandgap risonante
ax.annotate('Bandgap risonante\n-31.4 dB @ 1000 Hz', 
            xy=(1000, -31.4), xytext=(700, -25),
            arrowprops=dict(arrowstyle='->', color='#d62728', lw=2),
            fontsize=10, color='#d62728', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#d62728'))

ax.set_xlabel('Frequenza (Hz)', fontsize=12, fontweight='bold')
ax.set_ylabel('Attenuazione (dB)', fontsize=12, fontweight='bold')
ax.set_title('Confronto Attenuazione Materiali\nAl variare della Frequenza', 
             fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3, which='both')
ax.legend(fontsize=11, loc='lower left')
ax.set_ylim(-35, 1)

plt.tight_layout()
plt.savefig('static/images/grafico_confronto_materiali.png', dpi=300, bbox_inches='tight')
print("✓ Grafico 2 salvato: static/images/grafico_confronto_materiali.png")
plt.close()

# ============ GRAFICO 3: Comportamento Schiuma ============
fig3, ax = plt.subplots(figsize=(10, 6))

ax.plot(frequenze, schiuma, 'o-', linewidth=2.5, markersize=10, 
        color='#ff7f0e', markerfacecolor='#ffbb78', markeredgewidth=2)
ax.fill_between(frequenze, schiuma, alpha=0.3, color='#ff7f0e')

# Aggiungere etichette ai punti
for i, (freq, att) in enumerate(zip(frequenze, schiuma)):
    ax.text(freq, att - 1.5, f'{att} dB', ha='center', fontsize=9, fontweight='bold')

ax.set_xlabel('Frequenza (Hz)', fontsize=12, fontweight='bold')
ax.set_ylabel('Attenuazione (dB)', fontsize=12, fontweight='bold')
ax.set_title('Schiuma Acustica: Assorbimento Progressivo\nAl variare della Frequenza', 
             fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.set_ylim(-27, 1)
ax.set_xscale('log')

plt.tight_layout()
plt.savefig('static/images/grafico_schiuma.png', dpi=300, bbox_inches='tight')
print("✓ Grafico 3 salvato: static/images/grafico_schiuma.png")
plt.close()

print("\n✅ Tutti i grafici sono stati generati con successo!")

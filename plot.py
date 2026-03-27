import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
rho_fe =7000
def radius(mass, rho):
    return  (mass/rho*3/4*1/np.pi)**(1/3)

rcParams['axes.linewidth'] = 1.2
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['xtick.major.size'] = 4
rcParams['ytick.major.size'] = 4
rcParams['xtick.minor.size'] = 2
rcParams['ytick.minor.size'] = 2

files  = ['./PureN2_upper_20', './PureN2_upper_40', './PureN2_upper_60']
labels = ['V in [11.2, 20]', 'V in [11.2, 40]', 'V in [11.2, 60]']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  

fig, ax = plt.subplots(figsize=(4, 4), dpi=300)

for path, lbl, col in zip(files, labels, colors):
    args = pd.read_csv(f'{path}/co2_0/clean_args_array.dat', delimiter=' ')
    mass_in = args.iloc[:, 0].to_numpy()
    results = pd.read_csv(f'{path}/co2_0/clean_results.dat', delimiter=' ')
    r_out = results.iloc[:, 0].to_numpy() * 1e6 * 2
    r_in  = radius(mass_in, rho_fe) * 1e6 * 2
    ax.scatter(r_in, r_out, s=13, c=col, alpha=0.45, label=lbl, edgecolors='none')
    ax.scatter(np.mean(r_in), np.mean(r_out),
           marker='x', s=200, linewidths=2.5,
           color=col, edgecolors='black', zorder=10)

ax.plot([20, 5000], [20, 5000], '--', color='gray', lw=1, alpha=0.6)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(20, 4000)
ax.set_ylim(2, 2000)
ax.set_xlabel('Input equivalent diameter (μm)', fontsize=11)
ax.set_ylabel('After ablation diameter (μm)', fontsize=11)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, alpha=0.5)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)

leg = ax.legend(frameon=True, fontsize=10, loc='upper left')
leg.get_frame().set_facecolor('white')
leg.get_frame().set_alpha(0.8)
leg.get_frame().set_edgecolor('gray')
plt.text(6.5e2,8e2,'1:1 line',rotation = 38)
plt.tight_layout()
#plt.savefig('co2_ablation_comparison.pdf', dpi=600, bbox_inches='tight')
plt.show()

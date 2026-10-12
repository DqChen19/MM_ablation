import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams

rho_fe = 7000

def radius(mass, rho):
    return (3 * mass / (4 * np.pi * rho))**(1/3)

rcParams['axes.linewidth'] = 1.2
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'
rcParams['xtick.major.size'] = 4
rcParams['ytick.major.size'] = 4
rcParams['xtick.minor.size'] = 2
rcParams['ytick.minor.size'] = 2

files = ['./PureN2_upper_20','./PureN2_upper_40','./PureN2_upper_60']
labels = ['V 11.2-20 km/s','V 11.2-40 km/s','V 11.2-60 km/s']
colors = ['#1f77b4', '#ff7f0e', '#2ca02c']

# Store simulation data for the second figure
simulation_data = {}

fig, ax = plt.subplots(figsize=(4, 4), dpi=300)

for path, lbl, col in zip(files, labels, colors):

    args = pd.read_csv(f'{path}/co2_0/clean_args_array.dat',sep=r'\s+')
    results = pd.read_csv(f'{path}/co2_0/clean_results.dat',sep=r'\s+')
    mass_in = args.iloc[:, 0].to_numpy()
    
    r_in = radius(mass_in, rho_fe) * 1e6 * 2
    r_out = results.iloc[:, 0].to_numpy() * 1e6 * 2

    # Remove invalid values and the horizontal floor
    mask = (np.isfinite(r_in) &
        np.isfinite(r_out) &
        (r_in > 0) &
        (r_out > 2.0)
    )

    r_in_clean = r_in[mask]
    r_out_clean = r_out[mask]

    n_total = 1000
    n_survived = np.sum(mask)
    survival_fraction = n_survived / n_total * 100

    print(f'{lbl}: {n_survived}/{n_total} retained ({survival_fraction:.1f}%)')

    simulation_data[lbl] = r_out_clean

    ax.scatter(r_in_clean, r_out_clean, s=10, c=col,
                alpha=0.35, label=f'{lbl} (n={n_survived}/1000)',  edgecolors='none')

    # Mean of retained points
    ax.scatter(np.mean(r_in_clean), np.mean(r_out_clean), marker='x', s=150, linewidths=2.5, color=col, zorder=10)


ax.plot([20, 5000], [20, 5000],'--', color='k', lw=1.5, alpha=0.7)

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(20, 4000)
ax.set_ylim(2, 2000)
ax.set_xlabel('Input equivalent diameter (μm)', fontsize=12)
ax.set_ylabel('After ablation diameter (μm)', fontsize=12)
ax.grid(True, which='major', linestyle=':', linewidth=0.5, alpha=0.5)
ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.3)
ax.legend(frameon=True,fontsize=8,loc='upper left',framealpha=0.85)
ax.text(52, 62, '1:1 line', rotation=38, fontsize=10)
plt.tight_layout()
plt.savefig('co2_ablation_comparison.png', dpi=600, bbox_inches='tight')
plt.show()

# ==========================================
# Figure 2: ECDF comparison
# ==========================================

obs = pd.read_csv('observed_size.csv')

observed_data = {
    'Modern': obs['modern'].dropna().to_numpy(),
    'Helena': obs['helena'].dropna().to_numpy(),
    'Devonian': obs['devonian'].dropna().to_numpy(),
    'Miocene': obs['Miocene'].dropna().to_numpy()
}

observed_colors = {
    'Modern': '#444444',
    'Helena': '#b2182b',
    'Devonian': '#762a83',
    'Miocene':  '#FFA500'
}

def plot_ecdf(ax, values, label, color, **kwargs):

    values = np.asarray(values, dtype=float)
    values = values[np.isfinite(values) & (values > 0)]
    values = np.sort(values)
    n = len(values)
    if n == 0:
        return
    y = np.arange(1, n + 1) / n
    ax.step(values,y,where='post',label=f'{label} (n={n})',color=color,**kwargs)


fig, ax = plt.subplots(figsize=(5, 4), dpi=300)

# ------------------------------------------
# Simulated ECDF
# ------------------------------------------

for lbl, col in zip(labels, colors):

    plot_ecdf(ax, simulation_data[lbl], label=lbl, color=col, linewidth=1.8, alpha=0.9, linestyle='--')

# ------------------------------------------
# Observed ECDF
# ------------------------------------------

for lbl, values in observed_data.items():
    plot_ecdf(ax, values, label=lbl, color=observed_colors[lbl], linewidth=2.2, linestyle='-')

ax.set_xlabel('Spherule diameter (μm)',fontsize=11)
ax.set_ylabel('Cumulative fraction', fontsize=11)
ax.set_xlim(0, 400)
ax.set_ylim(0, 1.02)
ax.set_yticks(np.arange(0, 1.01, 0.2))
ax.grid(True,linestyle=':',linewidth=0.5, alpha=0.4)
ax.legend(fontsize=8,frameon=False,loc='lower right')

plt.tight_layout()
plt.savefig('size_ecdf.png',dpi=600, bbox_inches='tight')
plt.show()
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
    ax.scatter(r_in, r_out, s=10, c=col, alpha=0.35, label=lbl, edgecolors='none')
    ax.scatter(np.mean(r_in), np.mean(r_out),
           marker='x', s=200, linewidths=2.5,
           color=col, edgecolors='black', zorder=10)

ax.plot([20, 5000], [20, 5000], '--', color='k', lw=1.5, alpha=0.7)
ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(20, 4000)
ax.set_ylim(1, 2000)
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
plt.savefig('co2_ablation_comparison.png', dpi=600, bbox_inches='tight')
plt.show()

# ==========================================
# Figure 2: ECDF comparison
# ==========================================

obs = pd.read_csv('observed_sizes.csv')

observed_data = {
    'Modern': obs['modern'].dropna().to_numpy(),
    'Helena': obs['helena'].dropna().to_numpy(),
    'Devonian': obs['devonian'].dropna().to_numpy()
}

observed_colors = {
    'Modern': '#444444',
    'Helena': '#b2182b',
    'Devonian': '#762a83'
}

def plot_ecdf(ax, values, label, color, **kwargs):

    values = np.asarray(values, dtype=float)

    values = values[
        np.isfinite(values) & (values > 0)
    ]

    values = np.sort(values)

    n = len(values)

    if n == 0:
        return

    y = np.arange(1, n + 1) / n

    ax.step(
        values,
        y,
        where='post',
        label=f'{label} (n={n})',
        color=color,
        **kwargs
    )


fig, ax = plt.subplots(figsize=(5, 4), dpi=300)

# ------------------------------------------
# Simulated ECDF
# ------------------------------------------

for lbl, col in zip(labels, colors):

    plot_ecdf(
        ax,
        simulation_data[lbl],
        label=lbl,
        color=col,
        linewidth=1.8,
        alpha=0.9
    )

# ------------------------------------------
# Observed ECDF
# ------------------------------------------

for lbl, values in observed_data.items():

    plot_ecdf(
        ax,
        values,
        label=lbl,
        color=observed_colors[lbl],
        linewidth=2.2,
        linestyle='--'
    )

# ------------------------------------------
# Formatting
# ------------------------------------------

ax.set_xlabel(
    'Spherule diameter (μm)',
    fontsize=11
)

ax.set_ylabel(
    'Cumulative fraction',
    fontsize=11
)

ax.set_xlim(0, 400)
ax.set_ylim(0, 1.02)

ax.set_yticks(np.arange(0, 1.01, 0.2))

ax.grid(
    True,
    linestyle=':',
    linewidth=0.5,
    alpha=0.4
)

ax.legend(
    fontsize=8,
    frameon=False,
    loc='lower right'
)

plt.tight_layout()

plt.savefig(
    'size_ecdf.png',
    dpi=600,
    bbox_inches='tight'
)


plt.show()
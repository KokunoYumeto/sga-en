"""Render a labelled TeX-style phi comparison; this is not source evidence."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams['mathtext.fontset']='cm'
fig,ax=plt.subplots(figsize=(4,2),dpi=200)
ax.set_axis_off()
ax.text(.2,.6,r'$\phi$',fontsize=44,ha='center')
ax.text(.7,.6,r'$\varphi$',fontsize=44,ha='center')
ax.text(.2,.28,r'\phi',fontsize=13,ha='center',fontfamily='monospace')
ax.text(.7,.28,r'\varphi',fontsize=13,ha='center',fontfamily='monospace')
fig.savefig(Path(__file__).resolve().parent/'tex_phi_comparison.png',bbox_inches='tight')

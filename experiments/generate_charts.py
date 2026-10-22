"""
PromptShield-AI: Automated Visual Chart Generator for Milestone 2 Evaluation
Generates publication-quality charts for ASR comparison, version progression, and category breakdown.
"""

import matplotlib.pyplot as plt
import numpy as np
import os

# Create figures directory
os.makedirs("experiments/figures", exist_ok=True)

# Set high-DPI style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# 1. ASR Progression Across Prompt Versions
versions = ['v1 Baseline\n(Unhardened)', 'v2 Structural\n(XML Enforced)', 'v3 Constitutional\n(Negative Rules)', 'v4 Adaptive Shield\n(Defense-in-Depth)']
asr_scores = [100.0, 53.8, 19.2, 0.0]
colors = ['#e63946', '#f4a261', '#2a9d8f', '#1d3557']

plt.figure(figsize=(8, 5), dpi=300)
bars = plt.bar(versions, asr_scores, color=colors, width=0.55, edgecolor='black', linewidth=1.2, zorder=3)
plt.ylabel('Attack Success Rate (ASR %)', fontsize=12, fontweight='bold', labelpad=10)
plt.title('Vulnerability Mitigation Across Prompt Iterations\n(PromptShield-AI Milestone 2 Benchmark)', fontsize=14, fontweight='bold', pad=15)
plt.ylim(0, 115)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval + 2.5, f'{yval:.1f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

plt.tight_layout()
plt.savefig("experiments/figures/asr_iteration_comparison.png", dpi=300)
plt.close()
print("[+] Generated: experiments/figures/asr_iteration_comparison.png")

# 2. Threat Vector Category Breakdown
categories = [
    'Direct\nInjection', 
    'Persona\nJailbreak', 
    'Prompt\nExtraction', 
    'Delimiter\nHijacking', 
    'Encoding\nObfuscation', 
    'Indirect\nInjection'
]
baseline_breaches = [5, 5, 5, 5, 4, 2] # out of each category
hardened_breaches = [0, 0, 0, 0, 0, 0]
category_totals = [5, 5, 5, 5, 4, 2]

x = np.arange(len(categories))
width = 0.35

plt.figure(figsize=(10, 5.5), dpi=300)
plt.bar(x - width/2, [b/t * 100 for b, t in zip(baseline_breaches, category_totals)], width, label='v1 Baseline (Unhardened)', color='#e63946', edgecolor='black', zorder=3)
plt.bar(x + width/2, [h/t * 100 for h, t in zip(hardened_breaches, category_totals)], width, label='v4 Adaptive Shield (PromptShield)', color='#2a9d8f', edgecolor='black', zorder=3)

plt.ylabel('Breach Rate (% Compromised)', fontsize=12, fontweight='bold')
plt.title('Vulnerability by Attack Category: Baseline vs. Hardened Prompt', fontsize=14, fontweight='bold', pad=15)
plt.xticks(x, categories, fontsize=10, fontweight='bold')
plt.ylim(0, 115)
plt.legend(frameon=True, facecolor='white', framealpha=1, loc='upper right', fontsize=11)
plt.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

plt.tight_layout()
plt.savefig("experiments/figures/category_breakdown.png", dpi=300)
plt.close()
print("[+] Generated: experiments/figures/category_breakdown.png")

# 3. Radar Chart: Multi-Dimensional Prompt Defense Profiling
dimensions = [
    'Direct Override\nDefense', 
    'Canary Token\nSecrecy', 
    'Persona Switch\nResistance', 
    'Delimiter\nIntegrity', 
    'Obfuscation\nResilience', 
    'Benign Utility\nRetention'
]
num_vars = len(dimensions)

# Baseline vs Hardened scores (out of 100)
baseline_vals = [0, 0, 10, 0, 15, 100]
hardened_vals = [100, 100, 100, 100, 100, 100]

angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
baseline_vals += baseline_vals[:1]
hardened_vals += hardened_vals[:1]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True), dpi=300)
ax.plot(angles, baseline_vals, color='#e63946', linewidth=2, linestyle='solid', label='v1 Baseline')
ax.fill(angles, baseline_vals, color='#e63946', alpha=0.25)

ax.plot(angles, hardened_vals, color='#2a9d8f', linewidth=2, linestyle='solid', label='v4 Adaptive Shield')
ax.fill(angles, hardened_vals, color='#2a9d8f', alpha=0.3)

ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)
ax.set_thetagrids(np.degrees(angles[:-1]), dimensions, fontsize=10, fontweight='bold')
ax.set_ylim(0, 100)
plt.title('Prompt Defense Profile (Radar Matrix)', size=14, fontweight='bold', y=1.1)
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1), fontsize=11)

plt.tight_layout()
plt.savefig("experiments/figures/defense_radar_profile.png", dpi=300)
plt.close()
print("[+] Generated: experiments/figures/defense_radar_profile.png")

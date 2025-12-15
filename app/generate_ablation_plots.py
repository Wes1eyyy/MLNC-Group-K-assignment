"""
Generate visualizations for ablation study results
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
RESULTS_CSV = "../results/ablation/ablation_results.csv"
OUTPUT_DIR = "../results/ablation/plots"

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load results
print("Loading ablation results...")
df = pd.read_csv(RESULTS_CSV)
print(f"Loaded {len(df)} experiments")

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
colors = plt.cm.Set2(np.linspace(0, 1, 8))

# ============================================================================
# Figure 1: Accuracy Comparison Bar Chart
# ============================================================================
print("\nGenerating Figure 1: Accuracy Comparison...")
fig, ax = plt.subplots(figsize=(14, 8))

# Sort by accuracy
df_sorted = df.sort_values('accuracy', ascending=True)

# Create horizontal bar chart
bars = ax.barh(range(len(df_sorted)), df_sorted['accuracy'], color=colors[2])

# Highlight baseline
baseline_idx = df_sorted[df_sorted['exp_id'] == 'EXP-0'].index[0]
bars[baseline_idx].set_color('red')
bars[baseline_idx].set_alpha(0.8)

# Set labels
ax.set_yticks(range(len(df_sorted)))
ax.set_yticklabels([f"{row['exp_id']}: {row['name'][:40]}"
                     for _, row in df_sorted.iterrows()], fontsize=9)
ax.set_xlabel('Accuracy', fontsize=12, fontweight='bold')
ax.set_title('Ablation Study: Model Accuracy Comparison', fontsize=14, fontweight='bold')
ax.grid(axis='x', alpha=0.3)

# Add value labels
for i, (idx, row) in enumerate(df_sorted.iterrows()):
    ax.text(row['accuracy'] + 0.005, i, f"{row['accuracy']:.4f}",
            va='center', fontsize=8)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/1_accuracy_comparison.png", dpi=300, bbox_inches='tight')
print(f"  Saved to {OUTPUT_DIR}/1_accuracy_comparison.png")
plt.close()

# ============================================================================
# Figure 2: Phase 2 - Feature Group Importance (Ablation)
# ============================================================================
print("\nGenerating Figure 2: Feature Group Importance...")
baseline = df[df['exp_id'] == 'EXP-0'].iloc[0]

ablation_data = {
    'EXP-1': 'Team Form\n(2a+2b)',
    'EXP-2': 'Match\nDynamics (3)',
    'EXP-3': 'Discipline\n(4)',
    'EXP-4': 'Previous\nRank (5a)',
    'EXP-5': 'Squad\nQuality (5b)'
}

groups = []
delta_acc = []
delta_f1 = []

for exp_id, label in ablation_data.items():
    exp = df[df['exp_id'] == exp_id].iloc[0]
    groups.append(label)
    delta_acc.append(baseline['accuracy'] - exp['accuracy'])
    delta_f1.append(baseline['f1_macro'] - exp['f1_macro'])

# Sort by delta_acc
sorted_indices = np.argsort(delta_acc)[::-1]
groups = [groups[i] for i in sorted_indices]
delta_acc = [delta_acc[i] for i in sorted_indices]
delta_f1 = [delta_f1[i] for i in sorted_indices]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Delta Accuracy
bars1 = ax1.barh(range(len(groups)), delta_acc, color=colors[0])
ax1.set_yticks(range(len(groups)))
ax1.set_yticklabels(groups, fontsize=10)
ax1.set_xlabel('ΔAccuracy (Drop when removed)', fontsize=11, fontweight='bold')
ax1.set_title('Feature Group Importance: Accuracy', fontsize=12, fontweight='bold')
ax1.grid(axis='x', alpha=0.3)
ax1.axvline(x=0, color='black', linestyle='--', linewidth=0.8)

for i, val in enumerate(delta_acc):
    ax1.text(val + 0.001, i, f"{val:+.4f}", va='center', fontsize=9)

# Delta F1
bars2 = ax2.barh(range(len(groups)), delta_f1, color=colors[1])
ax2.set_yticks(range(len(groups)))
ax2.set_yticklabels(groups, fontsize=10)
ax2.set_xlabel('ΔF1-Macro (Drop when removed)', fontsize=11, fontweight='bold')
ax2.set_title('Feature Group Importance: F1-Score', fontsize=12, fontweight='bold')
ax2.grid(axis='x', alpha=0.3)
ax2.axvline(x=0, color='black', linestyle='--', linewidth=0.8)

for i, val in enumerate(delta_f1):
    ax2.text(val + 0.001, i, f"{val:+.4f}", va='center', fontsize=9)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/2_feature_importance.png", dpi=300, bbox_inches='tight')
print(f"  Saved to {OUTPUT_DIR}/2_feature_importance.png")
plt.close()

# ============================================================================
# Figure 3: Phase 3 - Progressive Addition Curve
# ============================================================================
print("\nGenerating Figure 3: Progressive Addition Curve...")

progressive_exps = ['EXP-0a', 'EXP-6', 'EXP-7', 'EXP-8', 'EXP-9']
progressive_data = df[df['exp_id'].isin(progressive_exps)]
progressive_data = progressive_data.set_index('exp_id').reindex(progressive_exps).reset_index()

fig, ax = plt.subplots(figsize=(10, 6))

# Plot lines
ax.plot(progressive_data['n_features'], progressive_data['accuracy'],
        marker='o', linewidth=2, markersize=8, label='Accuracy', color=colors[3])
ax.plot(progressive_data['n_features'], progressive_data['f1_macro'],
        marker='s', linewidth=2, markersize=8, label='F1-Macro', color=colors[4])

# Add baseline reference
baseline_acc = df[df['exp_id'] == 'EXP-0']['accuracy'].values[0]
ax.axhline(y=baseline_acc, color='red', linestyle='--', linewidth=1.5,
           label=f'Full Model Baseline ({baseline_acc:.4f})', alpha=0.7)

# Labels and annotations
ax.set_xlabel('Number of Features', fontsize=12, fontweight='bold')
ax.set_ylabel('Score', fontsize=12, fontweight='bold')
ax.set_title('Progressive Feature Addition: Performance vs Feature Count',
             fontsize=13, fontweight='bold')
ax.legend(loc='lower right', fontsize=10)
ax.grid(alpha=0.3)

# Annotate each point with experiment name
for _, row in progressive_data.iterrows():
    ax.annotate(row['exp_id'],
                (row['n_features'], row['accuracy']),
                textcoords="offset points", xytext=(0,10), ha='center',
                fontsize=8, alpha=0.7)

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/3_progressive_addition.png", dpi=300, bbox_inches='tight')
print(f"  Saved to {OUTPUT_DIR}/3_progressive_addition.png")
plt.close()

# ============================================================================
# Figure 4: F1-Score per Class Heatmap
# ============================================================================
print("\nGenerating Figure 4: F1-Score Heatmap...")

f1_data = df[['exp_id', 'f1_H', 'f1_D', 'f1_A']].set_index('exp_id')
f1_matrix = f1_data.values.T  # Transpose to make horizontal

fig, ax = plt.subplots(figsize=(12, 5))

im = ax.imshow(f1_matrix, cmap='RdYlGn', aspect='auto', vmin=0, vmax=0.7)

# Set ticks (swapped x and y)
ax.set_yticks(range(3))
ax.set_yticklabels(['Home Win (H)', 'Draw (D)', 'Away Win (A)'], fontsize=10)
ax.set_xticks(range(len(f1_data)))
ax.set_xticklabels(f1_data.index, fontsize=9, rotation=45, ha='right')

# Add values (swapped i and j for transposed matrix)
for i in range(3):
    for j in range(len(f1_data)):
        text = ax.text(j, i, f'{f1_matrix[i, j]:.3f}',
                      ha="center", va="center", color="black", fontsize=7)

ax.set_title('F1-Score per Class Across Experiments', fontsize=13, fontweight='bold')
plt.colorbar(im, ax=ax, label='F1-Score')

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/4_f1_heatmap.png", dpi=300, bbox_inches='tight')
print(f"  Saved to {OUTPUT_DIR}/4_f1_heatmap.png")
plt.close()

# ============================================================================
# Figure 5: Efficiency Analysis (Accuracy vs Training Time)
# ============================================================================
print("\nGenerating Figure 5: Efficiency Analysis...")

fig, ax = plt.subplots(figsize=(10, 6))

# Scatter plot
scatter = ax.scatter(df['train_time'], df['accuracy'],
                     s=df['n_features']*20, alpha=0.6, c=df['n_features'],
                     cmap='viridis', edgecolors='black', linewidth=0.5)

# Annotate key experiments
key_exps = ['EXP-0', 'EXP-6', 'EXP-10', 'EXP-14']
for exp_id in key_exps:
    row = df[df['exp_id'] == exp_id].iloc[0]
    ax.annotate(exp_id, (row['train_time'], row['accuracy']),
                textcoords="offset points", xytext=(5,5), ha='left',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.3))

ax.set_xlabel('Training Time (seconds)', fontsize=12, fontweight='bold')
ax.set_ylabel('Accuracy', fontsize=12, fontweight='bold')
ax.set_title('Efficiency Analysis: Accuracy vs Training Time',
             fontsize=13, fontweight='bold')
ax.grid(alpha=0.3)

# Colorbar
cbar = plt.colorbar(scatter, ax=ax, label='Number of Features')

plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/5_efficiency_analysis.png", dpi=300, bbox_inches='tight')
print(f"  Saved to {OUTPUT_DIR}/5_efficiency_analysis.png")
plt.close()

print("\n" + "="*70)
print("All visualizations generated successfully!")
print(f"Saved to: {OUTPUT_DIR}")
print("="*70)
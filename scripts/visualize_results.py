#!/usr/bin/env python3
"""
Script de visualisation des résultats.

Ce script génère des graphiques comparatifs pour visualiser les différences
d'utilisation des adpositions entre les auteurs.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path


# Configuration du style des graphiques
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['font.size'] = 10

# Liste des adpositions directionnelles
TARGET_ADPOSITIONS = [
    'across', 'through', 'along', 'past', 'around', 'beyond'
]


def load_data(data_dir):
    """Charge les données nécessaires."""
    comparison_matrix = pd.read_csv(data_dir / 'comparison_matrix.csv', index_col=0)
    frequency_summary = pd.read_csv(data_dir / 'frequency_summary.csv')

    return comparison_matrix, frequency_summary


def plot_comparison_heatmap(comparison_matrix, output_dir):
    """Génère une heatmap comparant tous les auteurs."""
    plt.figure(figsize=(14, 6))

    sns.heatmap(
        comparison_matrix,
        annot=True,
        fmt='.2f',
        cmap='YlOrRd',
        cbar_kws={'label': 'Fréquence (par 10,000 mots)'},
        linewidths=0.5
    )

    plt.title('Fréquence des adpositions directionnelles par auteur (par 10,000 mots)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Adposition', fontsize=12, fontweight='bold')
    plt.ylabel('Auteur', fontsize=12, fontweight='bold')
    plt.tight_layout()

    output_file = output_dir / 'heatmap_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Heatmap sauvegardée : {output_file}")


def plot_author_comparison_bars(comparison_matrix, output_dir):
    """Génère un graphique à barres groupées pour comparer les auteurs."""
    # Transposer pour avoir les adpositions en index
    df_plot = comparison_matrix.T

    # Créer le graphique
    ax = df_plot.plot(kind='bar', width=0.8, figsize=(16, 8))

    plt.title('Comparaison des fréquences d\'adpositions par auteur',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Adposition', fontsize=12, fontweight='bold')
    plt.ylabel('Fréquence (par 10,000 mots)', fontsize=12, fontweight='bold')
    plt.legend(title='Auteur', title_fontsize=11, fontsize=10, loc='upper right')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    output_file = output_dir / 'bars_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Graphique à barres sauvegardé : {output_file}")


def plot_total_frequency_by_author(comparison_matrix, output_dir):
    """Graphique montrant la fréquence totale des adpositions par auteur."""
    # Calculer les totaux
    totals = comparison_matrix.sum(axis=1).sort_values(ascending=True)

    # Créer le graphique
    plt.figure(figsize=(10, 6))
    colors = sns.color_palette('husl', len(totals))

    totals.plot(kind='barh', color=colors)

    plt.title('Fréquence totale des adpositions par auteur (par 10,000 mots)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Fréquence totale (par 10,000 mots)', fontsize=12, fontweight='bold')
    plt.ylabel('Auteur', fontsize=12, fontweight='bold')

    # Ajouter les valeurs sur les barres
    for i, v in enumerate(totals):
        plt.text(v + 0.5, i, f'{v:.2f}', va='center', fontsize=10)

    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    output_file = output_dir / 'total_frequency_by_author.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Graphique des totaux sauvegardé : {output_file}")


def plot_adposition_rankings(comparison_matrix, output_dir):
    """Graphique montrant le classement de chaque auteur pour chaque adposition."""
    # Créer une matrice de rangs
    ranks = comparison_matrix.rank(ascending=False)

    plt.figure(figsize=(14, 6))

    sns.heatmap(
        ranks,
        annot=True,
        fmt='.0f',
        cmap='RdYlGn_r',
        cbar_kws={'label': 'Rang (1 = plus fréquent)'},
        linewidths=0.5,
        vmin=1,
        vmax=len(comparison_matrix)
    )

    plt.title('Classement des auteurs par adposition (1 = utilisation la plus fréquente)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Adposition', fontsize=12, fontweight='bold')
    plt.ylabel('Auteur', fontsize=12, fontweight='bold')
    plt.tight_layout()

    output_file = output_dir / 'rankings_heatmap.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Heatmap des classements sauvegardée : {output_file}")


def plot_hemingway_comparison(comparison_matrix, output_dir):
    """Graphique comparant spécifiquement Hemingway aux autres auteurs."""
    if 'hemingway' not in comparison_matrix.index:
        print("⚠ Hemingway n'est pas dans les données, impossible de créer le graphique de comparaison")
        return

    # Extraire les données de Hemingway
    hemingway_data = comparison_matrix.loc['hemingway']

    # Créer un DataFrame pour le graphique
    plot_data = comparison_matrix.copy()

    # Créer le graphique
    fig, ax = plt.subplots(figsize=(14, 8))

    x = np.arange(len(hemingway_data))
    width = 0.15

    # Tracer Hemingway en premier avec une couleur distinctive
    ax.bar(x - 1.5*width, hemingway_data, width, label='Hemingway',
           color='#e74c3c', alpha=0.8)

    # Tracer les autres auteurs
    colors = ['#3498db', '#2ecc71', '#f39c12']
    other_authors = [auth for auth in plot_data.index if auth != 'hemingway']

    for i, author in enumerate(other_authors):
        offset = (i - 0.5) * width
        ax.bar(x + offset, plot_data.loc[author], width,
               label=author.capitalize(), color=colors[i % len(colors)], alpha=0.8)

    ax.set_xlabel('Adposition', fontsize=12, fontweight='bold')
    ax.set_ylabel('Fréquence (par 10,000 mots)', fontsize=12, fontweight='bold')
    ax.set_title('Comparaison : Hemingway vs autres auteurs',
                 fontsize=14, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(hemingway_data.index, rotation=45, ha='right')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()

    output_file = output_dir / 'hemingway_comparison.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

    print(f"✓ Graphique de comparaison Hemingway sauvegardé : {output_file}")


def plot_individual_adposition_comparison(comparison_matrix, output_dir, adposition):
    """Graphique pour une adposition spécifique."""
    if adposition not in comparison_matrix.columns:
        return

    data = comparison_matrix[adposition].sort_values(ascending=True)

    plt.figure(figsize=(10, 6))
    colors = sns.color_palette('viridis', len(data))

    data.plot(kind='barh', color=colors)

    plt.title(f'Fréquence de "{adposition}" par auteur (par 10,000 mots)',
              fontsize=14, fontweight='bold', pad=20)
    plt.xlabel('Fréquence (par 10,000 mots)', fontsize=12, fontweight='bold')
    plt.ylabel('Auteur', fontsize=12, fontweight='bold')

    # Ajouter les valeurs
    for i, v in enumerate(data):
        plt.text(v + 0.05, i, f'{v:.2f}', va='center', fontsize=10)

    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()

    output_file = output_dir / f'adposition_{adposition}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()


def create_all_individual_plots(comparison_matrix, output_dir):
    """Crée des graphiques individuels pour chaque adposition."""
    adpositions_dir = output_dir / 'by_adposition'
    adpositions_dir.mkdir(exist_ok=True)

    print("\nCréation des graphiques individuels par adposition...")

    for adposition in comparison_matrix.columns:
        plot_individual_adposition_comparison(comparison_matrix, adpositions_dir, adposition)

    print(f"✓ {len(comparison_matrix.columns)} graphiques individuels créés dans {adpositions_dir}")


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'results' / 'data'
    viz_dir = project_root / 'results' / 'visualizations'

    # Créer le dossier de visualisations s'il n'existe pas
    viz_dir.mkdir(parents=True, exist_ok=True)

    print("=== Génération des visualisations ===\n")

    # Charger les données
    print("Chargement des données...")
    comparison_matrix, frequency_summary = load_data(data_dir)
    print("✓ Données chargées\n")

    print("Génération des graphiques...\n")

    # Générer tous les graphiques
    plot_comparison_heatmap(comparison_matrix, viz_dir)
    plot_author_comparison_bars(comparison_matrix, viz_dir)
    plot_total_frequency_by_author(comparison_matrix, viz_dir)
    plot_adposition_rankings(comparison_matrix, viz_dir)
    plot_hemingway_comparison(comparison_matrix, viz_dir)

    # Graphiques individuels
    create_all_individual_plots(comparison_matrix, viz_dir)

    print(f"\n✓ Toutes les visualisations ont été générées dans {viz_dir}")
    print("\nVisualisation terminée !")


if __name__ == '__main__':
    main()

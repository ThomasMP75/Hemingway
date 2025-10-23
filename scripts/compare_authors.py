#!/usr/bin/env python3
"""
Script de comparaison entre auteurs.

Ce script compare les fréquences d'utilisation des adpositions entre
les différents auteurs et génère des rapports comparatifs.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy import stats


# Liste des adpositions directionnelles
TARGET_ADPOSITIONS = [
    'across', 'through', 'along', 'past', 'around', 'beyond'
]


def load_data(data_dir):
    """Charge les données nécessaires."""
    raw_data = pd.read_csv(data_dir / 'adpositions_raw_data.csv')
    author_stats = pd.read_csv(data_dir / 'author_statistics.csv')
    frequency_summary = pd.read_csv(data_dir / 'frequency_summary.csv')

    return raw_data, author_stats, frequency_summary


def create_comparison_matrix(frequency_summary):
    """Crée une matrice de comparaison auteurs x adpositions."""
    # Pivoter pour obtenir une matrice
    matrix = frequency_summary.pivot(
        index='author',
        columns='adposition',
        values='mean_frequency'
    )

    return matrix


def calculate_author_rankings(comparison_matrix):
    """Calcule le classement des auteurs pour chaque adposition."""
    rankings = {}

    for adposition in comparison_matrix.columns:
        sorted_authors = comparison_matrix[adposition].sort_values(ascending=False)
        rankings[adposition] = sorted_authors.to_dict()

    return rankings


def compare_to_hemingway(comparison_matrix):
    """Compare tous les auteurs à Hemingway."""
    if 'hemingway' not in comparison_matrix.index:
        print("Attention: Hemingway n'est pas dans les données")
        return None

    hemingway_row = comparison_matrix.loc['hemingway']
    comparisons = []

    for author in comparison_matrix.index:
        if author == 'hemingway':
            continue

        author_row = comparison_matrix.loc[author]

        for adposition in comparison_matrix.columns:
            hem_freq = hemingway_row[adposition]
            auth_freq = author_row[adposition]

            # Calculer la différence et le ratio
            diff = auth_freq - hem_freq
            ratio = auth_freq / hem_freq if hem_freq > 0 else np.inf

            comparisons.append({
                'author': author,
                'adposition': adposition,
                'hemingway_freq': round(hem_freq, 2),
                'author_freq': round(auth_freq, 2),
                'difference': round(diff, 2),
                'ratio': round(ratio, 2)
            })

    return pd.DataFrame(comparisons)


def identify_distinctive_features(comparison_matrix, threshold=1.5):
    """
    Identifie les adpositions distinctives pour chaque auteur.
    Une adposition est distinctive si sa fréquence est au moins
    threshold fois la moyenne des autres auteurs.
    """
    distinctive_features = []

    for author in comparison_matrix.index:
        for adposition in comparison_matrix.columns:
            author_freq = comparison_matrix.loc[author, adposition]

            # Calculer la moyenne des autres auteurs
            other_authors = comparison_matrix.index[comparison_matrix.index != author]
            other_freq_mean = comparison_matrix.loc[other_authors, adposition].mean()

            if other_freq_mean > 0:
                ratio = author_freq / other_freq_mean

                if ratio >= threshold:
                    distinctive_features.append({
                        'author': author,
                        'adposition': adposition,
                        'author_frequency': round(author_freq, 2),
                        'others_mean_frequency': round(other_freq_mean, 2),
                        'ratio': round(ratio, 2),
                        'distinctive_level': 'high' if ratio >= 2.0 else 'moderate'
                    })

    return pd.DataFrame(distinctive_features)


def generate_summary_report(comparison_matrix, hemingway_comparison, distinctive_features):
    """Génère un rapport textuel de synthèse."""
    lines = []

    lines.append("=" * 80)
    lines.append("RAPPORT COMPARATIF DES ADPOSITIONS DIRECTIONNELLES")
    lines.append("=" * 80)
    lines.append("")

    # Statistiques générales
    lines.append("1. FRÉQUENCES MOYENNES PAR AUTEUR (pour 10,000 mots)")
    lines.append("-" * 80)

    # Calculer le total pour chaque auteur
    total_by_author = comparison_matrix.sum(axis=1).sort_values(ascending=False)

    for author, total in total_by_author.items():
        lines.append(f"  {author:15s}: {total:6.2f}")

    lines.append("")

    # Adpositions les plus fréquentes par auteur
    lines.append("2. ADPOSITION LA PLUS FRÉQUENTE PAR AUTEUR")
    lines.append("-" * 80)

    for author in comparison_matrix.index:
        max_adp = comparison_matrix.loc[author].idxmax()
        max_freq = comparison_matrix.loc[author, max_adp]
        lines.append(f"  {author:15s}: {max_adp:10s} ({max_freq:.2f})")

    lines.append("")

    # Traits distinctifs
    if not distinctive_features.empty:
        lines.append("3. TRAITS DISTINCTIFS (fréquence significativement supérieure)")
        lines.append("-" * 80)

        for author in distinctive_features['author'].unique():
            author_features = distinctive_features[distinctive_features['author'] == author]
            lines.append(f"\n  {author.upper()}:")

            for _, row in author_features.iterrows():
                lines.append(
                    f"    - {row['adposition']:10s}: {row['author_frequency']:5.2f} "
                    f"(×{row['ratio']:.2f} vs autres)"
                )

    lines.append("")

    # Comparaison à Hemingway
    if hemingway_comparison is not None:
        lines.append("4. DIFFÉRENCES PAR RAPPORT À HEMINGWAY")
        lines.append("-" * 80)

        for author in hemingway_comparison['author'].unique():
            author_comp = hemingway_comparison[hemingway_comparison['author'] == author]

            # Trouver les plus grandes différences
            top_diffs = author_comp.nlargest(3, 'difference')

            lines.append(f"\n  {author.upper()}:")
            lines.append("    Adpositions plus fréquentes:")

            for _, row in top_diffs.iterrows():
                if row['difference'] > 0:
                    lines.append(
                        f"      - {row['adposition']:10s}: +{row['difference']:.2f} "
                        f"({row['author_freq']:.2f} vs {row['hemingway_freq']:.2f})"
                    )

    lines.append("")
    lines.append("=" * 80)

    return "\n".join(lines)


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'results' / 'data'

    print("=== Comparaison entre auteurs ===\n")

    # Charger les données
    print("Chargement des données...")
    raw_data, author_stats, frequency_summary = load_data(data_dir)
    print("✓ Données chargées\n")

    # Créer la matrice de comparaison
    print("Création de la matrice de comparaison...")
    comparison_matrix = create_comparison_matrix(frequency_summary)

    # Sauvegarder la matrice
    matrix_file = data_dir / 'comparison_matrix.csv'
    comparison_matrix.to_csv(matrix_file)
    print(f"✓ Matrice de comparaison sauvegardée dans {matrix_file}\n")

    # Comparer à Hemingway
    print("Comparaison à Hemingway...")
    hemingway_comparison = compare_to_hemingway(comparison_matrix)

    if hemingway_comparison is not None:
        hem_comp_file = data_dir / 'hemingway_comparison.csv'
        hemingway_comparison.to_csv(hem_comp_file, index=False)
        print(f"✓ Comparaison à Hemingway sauvegardée dans {hem_comp_file}\n")

    # Identifier les traits distinctifs
    print("Identification des traits distinctifs...")
    distinctive_features = identify_distinctive_features(comparison_matrix)

    if not distinctive_features.empty:
        distinct_file = data_dir / 'distinctive_features.csv'
        distinctive_features.to_csv(distinct_file, index=False)
        print(f"✓ Traits distinctifs sauvegardés dans {distinct_file}\n")

    # Générer le rapport de synthèse
    print("Génération du rapport de synthèse...")
    summary_report = generate_summary_report(
        comparison_matrix,
        hemingway_comparison,
        distinctive_features
    )

    # Sauvegarder le rapport
    report_file = data_dir / 'comparative_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(summary_report)

    print(f"✓ Rapport de synthèse sauvegardé dans {report_file}\n")

    # Afficher le rapport
    print(summary_report)

    print("\nComparaison terminée !")


if __name__ == '__main__':
    main()

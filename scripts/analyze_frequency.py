#!/usr/bin/env python3
"""
Script d'analyse des fréquences des adpositions.

Ce script analyse les données brutes extraites et calcule des statistiques
descriptives pour chaque auteur et chaque adposition.
"""

import pandas as pd
import numpy as np
from pathlib import Path


# Liste des adpositions directionnelles
TARGET_ADPOSITIONS = [
    'across', 'through', 'along', 'past', 'around', 'beyond'
]


def load_raw_data(data_dir):
    """Charge les données brutes extraites."""
    raw_data_file = data_dir / 'adpositions_raw_data.csv'

    if not raw_data_file.exists():
        raise FileNotFoundError(
            f"Le fichier {raw_data_file} n'existe pas. "
            f"Exécutez d'abord extract_prepositions.py"
        )

    return pd.read_csv(raw_data_file)


def calculate_author_statistics(df, target_adpositions):
    """Calcule les statistiques par auteur."""
    stats_list = []

    for author in df['author'].unique():
        author_df = df[df['author'] == author]

        author_stats = {
            'author': author,
            'num_works': len(author_df),
            'total_words': author_df['total_words'].sum(),
            'avg_words_per_work': author_df['total_words'].mean()
        }

        # Calculer les statistiques pour chaque adposition
        for adp in target_adpositions:
            count_col = f'{adp}_count'
            freq_col = f'{adp}_per_10k'

            if count_col in author_df.columns:
                total_count = author_df[count_col].sum()
                avg_freq = author_df[freq_col].mean()
                std_freq = author_df[freq_col].std()

                author_stats[f'{adp}_total_count'] = total_count
                author_stats[f'{adp}_avg_per_10k'] = round(avg_freq, 2)
                author_stats[f'{adp}_std_per_10k'] = round(std_freq, 2)

        stats_list.append(author_stats)

    return pd.DataFrame(stats_list)


def calculate_total_adpositions(df, target_adpositions):
    """Calcule le total de toutes les adpositions pour chaque œuvre."""
    df = df.copy()

    # Total des comptes bruts
    count_cols = [f'{adp}_count' for adp in target_adpositions]
    df['total_adpositions_count'] = df[count_cols].sum(axis=1)

    # Calculer la fréquence normalisée du total
    df['total_adpositions_per_10k'] = (
        df['total_adpositions_count'] / df['total_words']
    ) * 10000

    return df


def create_frequency_summary(df, target_adpositions):
    """Crée un résumé des fréquences moyennes par adposition et par auteur."""
    summary_data = []

    for author in df['author'].unique():
        author_df = df[df['author'] == author]

        for adp in target_adpositions:
            freq_col = f'{adp}_per_10k'

            if freq_col in author_df.columns:
                summary_data.append({
                    'author': author,
                    'adposition': adp,
                    'mean_frequency': round(author_df[freq_col].mean(), 2),
                    'std_frequency': round(author_df[freq_col].std(), 2),
                    'min_frequency': round(author_df[freq_col].min(), 2),
                    'max_frequency': round(author_df[freq_col].max(), 2)
                })

    return pd.DataFrame(summary_data)


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent
    data_dir = project_root / 'results' / 'data'

    print("=== Analyse des fréquences des adpositions ===\n")

    # Charger les données
    print("Chargement des données brutes...")
    df = load_raw_data(data_dir)
    print(f"✓ {len(df)} œuvres chargées\n")

    # Calculer les totaux
    print("Calcul des totaux d'adpositions...")
    df_with_totals = calculate_total_adpositions(df, TARGET_ADPOSITIONS)

    # Sauvegarder les données enrichies
    enriched_file = data_dir / 'adpositions_enriched_data.csv'
    df_with_totals.to_csv(enriched_file, index=False)
    print(f"✓ Données enrichies sauvegardées dans {enriched_file}\n")

    # Calculer les statistiques par auteur
    print("Calcul des statistiques par auteur...")
    author_stats = calculate_author_statistics(df, TARGET_ADPOSITIONS)

    # Sauvegarder les statistiques par auteur
    author_stats_file = data_dir / 'author_statistics.csv'
    author_stats.to_csv(author_stats_file, index=False)
    print(f"✓ Statistiques par auteur sauvegardées dans {author_stats_file}\n")

    # Créer un résumé des fréquences
    print("Création du résumé des fréquences...")
    frequency_summary = create_frequency_summary(df, TARGET_ADPOSITIONS)

    # Sauvegarder le résumé
    summary_file = data_dir / 'frequency_summary.csv'
    frequency_summary.to_csv(summary_file, index=False)
    print(f"✓ Résumé des fréquences sauvegardé dans {summary_file}\n")

    # Afficher un aperçu des résultats
    print("=== Aperçu des statistiques par auteur ===")
    print("\nNombre d'œuvres et mots totaux par auteur:")
    print(author_stats[['author', 'num_works', 'total_words', 'avg_words_per_work']])

    print("\n=== Fréquence totale moyenne des adpositions (par 10k mots) ===")
    total_freq_by_author = df_with_totals.groupby('author')['total_adpositions_per_10k'].mean()
    for author, freq in total_freq_by_author.items():
        print(f"{author:15s}: {freq:6.2f}")

    print("\nAnalyse terminée !")


if __name__ == '__main__':
    main()

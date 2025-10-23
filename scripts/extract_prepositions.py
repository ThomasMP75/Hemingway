#!/usr/bin/env python3
"""
Script d'extraction et de comptage des adpositions directionnelles.

Ce script lit les fichiers texte du corpus, tokenise le texte,
compte les adpositions ciblées et normalise les résultats par 10,000 mots.
"""

import os
import glob
from pathlib import Path
import pandas as pd
import nltk
from collections import Counter

# Télécharger les ressources NLTK nécessaires
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# Liste des adpositions directionnelles à analyser
TARGET_ADPOSITIONS = [
    'across', 'through', 'along', 'past', 'around', 'beyond'
]


def read_text_file(filepath):
    """Lit un fichier texte et retourne son contenu."""
    encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']

    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Impossible de lire le fichier {filepath} avec les encodages testés")


def tokenize_text(text):
    """Tokenise le texte et retourne une liste de tokens en minuscules."""
    tokens = nltk.word_tokenize(text.lower())
    return tokens


def count_adpositions(tokens, target_adpositions):
    """Compte les occurrences de chaque adposition dans la liste de tokens."""
    counter = Counter(tokens)
    adposition_counts = {adp: counter.get(adp, 0) for adp in target_adpositions}
    return adposition_counts


def normalize_frequency(counts, total_words, per_n_words=10000):
    """Normalise les fréquences pour N mots."""
    if total_words == 0:
        return {adp: 0 for adp in counts}

    normalized = {
        adp: (count / total_words) * per_n_words
        for adp, count in counts.items()
    }
    return normalized


def process_corpus_file(filepath, author):
    """Traite un fichier du corpus et retourne les statistiques."""
    text = read_text_file(filepath)
    tokens = tokenize_text(text)
    total_words = len(tokens)

    # Compter les adpositions
    adp_counts = count_adpositions(tokens, TARGET_ADPOSITIONS)

    # Normaliser par 10,000 mots
    normalized_freq = normalize_frequency(adp_counts, total_words)

    # Préparer les résultats
    filename = Path(filepath).stem
    results = {
        'author': author,
        'work': filename,
        'total_words': total_words,
    }

    # Ajouter les comptes bruts
    for adp, count in adp_counts.items():
        results[f'{adp}_count'] = count

    # Ajouter les fréquences normalisées
    for adp, freq in normalized_freq.items():
        results[f'{adp}_per_10k'] = round(freq, 2)

    return results


def get_author_from_filename(filename):
    """Détermine l'auteur à partir du nom de fichier pour les comparables."""
    author_mapping = {
        'Winesburg, Ohio': 'Sherwood Anderson',
        'The Great Gatsby': 'F. Scott Fitzgerald',
        'Manhattan Transfer': 'John Dos Passos',
        'As I Lay Dying': 'William Faulkner',
        '1919': 'John Dos Passos',
        'Of Mice and Men': 'John Steinbeck'
    }

    for work_title, author in author_mapping.items():
        if work_title in filename:
            return author

    return 'Unknown Author'


def process_author_corpus(corpus_dir, author_name):
    """Traite tous les fichiers .txt d'un auteur."""
    author_dir = os.path.join(corpus_dir, author_name)

    if not os.path.exists(author_dir):
        print(f"Attention: Le dossier {author_dir} n'existe pas")
        return []

    txt_files = glob.glob(os.path.join(author_dir, '*.txt'))

    if not txt_files:
        print(f"Attention: Aucun fichier .txt trouvé dans {author_dir}")
        return []

    results = []
    for filepath in txt_files:
        print(f"Traitement de {filepath}...")
        try:
            # Pour les comparables, déterminer l'auteur à partir du nom de fichier
            if author_name == 'comparables':
                filename = Path(filepath).stem
                actual_author = get_author_from_filename(filename)
            else:
                actual_author = author_name

            result = process_corpus_file(filepath, actual_author)
            results.append(result)
        except Exception as e:
            print(f"Erreur lors du traitement de {filepath}: {e}")

    return results


def main():
    """Fonction principale."""
    # Définir les chemins
    project_root = Path(__file__).parent.parent
    corpus_dir = project_root / 'corpus'
    results_dir = project_root / 'results' / 'data'

    # Créer le dossier de résultats s'il n'existe pas
    results_dir.mkdir(parents=True, exist_ok=True)

    # Liste des dossiers de corpus (structure actuelle)
    corpus_folders = ['hemingway', 'comparables']

    # Traiter tous les dossiers
    all_results = []
    for folder in corpus_folders:
        print(f"\n=== Traitement de {folder.upper()} ===")
        folder_results = process_author_corpus(corpus_dir, folder)
        all_results.extend(folder_results)

    # Créer un DataFrame et sauvegarder
    if all_results:
        df = pd.DataFrame(all_results)
        output_file = results_dir / 'adpositions_raw_data.csv'
        df.to_csv(output_file, index=False)
        print(f"\n✓ Résultats sauvegardés dans {output_file}")
        print(f"\nNombre total d'œuvres analysées : {len(df)}")
        print(f"Auteurs : {df['author'].unique().tolist()}")
    else:
        print("\nAucune donnée à sauvegarder. Vérifiez que les fichiers .txt sont présents dans les dossiers du corpus.")


if __name__ == '__main__':
    main()

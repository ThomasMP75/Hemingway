#!/usr/bin/env python3
"""
Script de conversion des fichiers RTF en TXT.

Ce script convertit tous les fichiers .rtf du dossier corpus en fichiers .txt.
"""

import os
import glob
from pathlib import Path
from striprtf.striprtf import rtf_to_text


def convert_rtf_to_txt(rtf_filepath):
    """Convertit un fichier RTF en TXT."""
    try:
        # Lire le fichier RTF
        with open(rtf_filepath, 'r', encoding='utf-8', errors='ignore') as f:
            rtf_content = f.read()

        # Convertir RTF en texte brut
        text_content = rtf_to_text(rtf_content)

        # Créer le nom du fichier TXT
        txt_filepath = rtf_filepath.replace('.rtf', '.txt')

        # Sauvegarder le fichier TXT
        with open(txt_filepath, 'w', encoding='utf-8') as f:
            f.write(text_content)

        print(f"✓ Converti: {Path(rtf_filepath).name} → {Path(txt_filepath).name}")
        return txt_filepath

    except Exception as e:
        print(f"✗ Erreur lors de la conversion de {rtf_filepath}: {e}")
        return None


def main():
    """Fonction principale."""
    # Définir le chemin du corpus
    project_root = Path(__file__).parent.parent
    corpus_dir = project_root / 'corpus'

    # Trouver tous les fichiers RTF
    rtf_files = list(corpus_dir.rglob('*.rtf'))

    if not rtf_files:
        print("Aucun fichier RTF trouvé dans le corpus.")
        return

    print(f"Fichiers RTF trouvés: {len(rtf_files)}\n")

    # Convertir tous les fichiers
    converted_count = 0
    for rtf_file in rtf_files:
        result = convert_rtf_to_txt(str(rtf_file))
        if result:
            converted_count += 1

    print(f"\n{'='*50}")
    print(f"Conversion terminée: {converted_count}/{len(rtf_files)} fichiers convertis")


if __name__ == '__main__':
    main()

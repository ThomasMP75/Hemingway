# Hemingway and the Grammar of Motion

A stylometric analysis of directional adpositions in Hemingway's prose compared to his contemporaries.

## Summary

This project measures the frequency of spatial adpositions (across, through, along, past, around, beyond) in four Hemingway works from the 1920s and compares them with four contemporary American authors: Sherwood Anderson, F. Scott Fitzgerald, John Dos Passos, and Sinclair Lewis.

**Key finding:** Hemingway uses 39% more directional adpositions than his contemporaries (43.25 vs 31.04 per 10,000 words).

## Corpus

**Hemingway (254,139 words)**
- A Farewell to Arms (1929)
- The Sun Also Rises (1926)
- Men Without Women (1927)
- In Our Time (1925)

**Contemporaries (497,964 words)**
- Sherwood Anderson - Winesburg, Ohio (1919)
- F. Scott Fitzgerald - The Great Gatsby (1925)
- John Dos Passos - Manhattan Transfer (1925)
- Sinclair Lewis - Main Street (1920)

## Results

Full analysis available in `/memos/Resultats_Analyse.md`

**Distinctive adpositions in Hemingway:**
- **around**: 2.92× more frequent than contemporaries
- **across**: 2.14× more frequent
- **along**: 1.34× more frequent

See `/results/` for detailed data and visualizations.

## Project Structure

```
/corpus           # Text files (.txt)
/scripts          # Python analysis scripts
/results
  /data           # CSV output files
  /visualizations # Charts and graphs
/memos            # Analysis reports
```

## Usage

```bash
# Install dependencies
pip install -r requirements.txt

# Run analysis pipeline
python scripts/extract_prepositions.py
python scripts/analyze_frequency.py
python scripts/compare_authors.py
python scripts/visualize_results.py
```

## Methodology

- **Normalization:** Frequency per 10,000 words
- **Adpositions analyzed:** across, through, along, past, around, beyond
- **Focus:** Pure spatial adpositions (avoiding metaphorical usage)

## Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## Author

**Thomas Oriol** (2025)

## Citation

If you use this work in academic research, please cite:

```
Thomas Oriol (2025). "Hemingway and the Grammar of Motion: A Stylometric Analysis
of Directional Adpositions in 1920s American Literature." GitHub repository.
```

## License

This work is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](LICENSE).

You are free to share and adapt this work for any purpose, including commercially, as long as you provide appropriate attribution to Thomas Oriol.

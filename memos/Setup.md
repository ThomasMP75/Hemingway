# Project Setup

## Requirements

- Python 3.8 or higher
- Text files (.txt format) in `/corpus` directory

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Download NLTK data (if needed)

```python
import nltk
nltk.download('punkt')
```

## Dependencies

- **nltk** (≥3.8): Text tokenization
- **pandas** (≥2.0.0): Data manipulation and CSV handling
- **matplotlib** (≥3.7.0): Basic visualizations
- **seaborn** (≥0.12.0): Advanced statistical visualizations
- **numpy** (≥1.24.0): Numerical computations

## Project Structure

```
/corpus               # Text corpus (.txt files)
/scripts              # Python analysis scripts
  - extract_prepositions.py
  - analyze_frequency.py
  - compare_authors.py
  - visualize_results.py
/results
  /data               # CSV output files
  /visualizations     # Charts and graphs
/memos                # Documentation and analysis notes
README.md
requirements.txt
```

## Running the Analysis

### Complete pipeline

```bash
# 1. Extract adpositions from texts
python scripts/extract_prepositions.py

# 2. Analyze frequencies
python scripts/analyze_frequency.py

# 3. Compare authors
python scripts/compare_authors.py

# 4. Generate visualizations
python scripts/visualize_results.py
```

### Individual scripts

Each script can be run independently if you have the necessary input data from previous steps.

## Output

- **CSV files** in `/results/data/`: Raw counts, normalized frequencies, statistical comparisons
- **Visualizations** in `/results/visualizations/`: Bar charts, heatmaps, comparative graphs
- **Text reports** in `/results/data/`: Summary statistics and comparative reports

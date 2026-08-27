# Sifat Notes

An interactive study site built from [CampusX](https://www.youtube.com/@campusx-official)'s YouTube playlists — **100 Days of Machine Learning**, **100 Days of Deep Learning**, and its companion **NLP** lecture series — turned into properly formatted, richer web notes instead of a flat document.

**Live structure:** three self-contained tracks, each with its own sidebar, math rendering (KaTeX), syntax-highlighted code, interactive widgets (Chart.js), inline architecture diagrams, and a 5-question quiz at the end of every topic.

- **Machine Learning** (`ml/`, 40 topics) — ML fundamentals through regression, classical algorithms, ensembles, and unsupervised learning.
- **Deep Learning** (`dl/`, 18 topics) — perceptrons through Transformers: MLPs, CNNs, RNNs, LSTMs, attention, BERT & GPT.
- **NLP** (`nlp/`, 7 topics) — the NLP pipeline, text representation, Word2Vec, classification, POS tagging, NER, and topic modeling.

Where a playlist's own notes ran out before the videos did, the remaining topics were written from scratch to keep each track complete — always disclosed inline on the page, never presented as if it were the original source.

## Structure

```
index.html              Home page (course picker)
ml/, dl/, nlp/           Built pages, one per topic, grouped by track
content/                 Source HTML fragments (one per page) — edit these
partials/                Shared header, footer, and per-track sidebars
assets/                  Shared CSS/JS (theme, Tailwind config, app behavior)
sources/                 Original source PDFs the notes were built from
build.py                 Static site builder — stitches partials + content into pages
page_template.html       Page shell for topic pages
home_template.html       Page shell for the home page
```

## Building

Pure static HTML, no dependencies beyond Python's standard library:

```
python3 build.py
```

Regenerates every page in `ml/`, `dl/`, `nlp/`, and `index.html` from the templates and content fragments. Open `index.html` directly in a browser — no server required.

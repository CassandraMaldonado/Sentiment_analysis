# AI Industry Impact: NLP-Powered Labor Risk Analysis

This project investigates how AI is affecting different industries and job types using custom NLP techniques applied to 180,000+ news articles.


## Project Overview

With increasing concern over AI’s impact on the workforce, this project aims to:
- Identify which industries and roles are most vulnerable to automation or augmentation.
- Track how sentiment toward AI shifts over time and by sector.
- Detect key technologies, entities, and narratives influencing public perception.


## Methodology

- **Data**: 180K AI-related news articles (2022–2025), filtered for labor relevance.
- **Cleaning**: Regex-based filtering removed around 20K off-topic or noisy entries.
- **Topic Modeling**: Used LDA to extract latent themes and map them to industries.
- **NER**: Named entity recognition for people, organizations and places.
- **Sentiment Analysis**: Custom scoring pipeline focused on labor and industry tone.
- **Temporal Analysis**: Visualized sentiment shifts following major events like GPT-4 and AI Act.
- **Tools Used**: `spaCy`, `TextBlob`, `Gensim`, `Pandas`, `Matplotlib`, `Seaborn`, `Streamlit`.


## Key Findings

- Office, legal, and service jobs show the highest automation risk
- Healthcare and education are cautiously embracing AI for augmentation
- Sentiment dropped sharply after major regulatory events and policy debates
- Trust depends heavily on **how** AI tools are framed (e.g. “assistant” vs “replacement”)

## Author

Cassandra M. Sullivan 
📧 cassandra@email.com | 🐦 @cassandra_ds | 🌐 cassandraprojects.dev



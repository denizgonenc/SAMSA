# SAMSA - BBM479-BBM480 Project

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Description

This is a sentiment analysis project conducted in the field of Natural Language Processing (NLP) and speech recognition. The objective of this project was to predict the sentiment of lines spoken by characters in movies and visualize the results. The lines were obtained through speech-to-text conversion of sound files. To calculate sentiment scores, we employed the NRC emotion lexicon.
You can visit [here](http://34.78.112.214/).

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributors](#contributors)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [References](#references)

## Installation

To install and run this software project locally, please follow these steps:

1. Clone the repository:  
`git clone https://github.com/atayalin/SAMSA`
2. Create virtual environment:  
`python -m venv env `
4. Install requirements:  
`pip install -r requirements.in`
5. Download and save executable ffmpeg file in /Interface

## Usage
`uvicorn Interface.main:app --reload`

## Contributors
- Ata Yalın Başaran
- Erkin Deniz Kasaplı
- Deniz Gönenç
- Murat İleri

## License
This software project is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

This software project was made possible thanks to the following resources:

- [NRC Lexicon](https://saifmohammad.com/WebPages/NRC-Emotion-Lexicon.htm) [1][2]:
  Provided us with a word-sentiment lexicon to calculate sentiment scores.
- [SemEval-2018  E-c Dataset](https://competitions.codalab.org/competitions/17751#learn_the_details-overview) [3]:
  Used in testing our model.

## References

- [1] Mohammad, S. M., & Turney, P. D. (2013). Crowdsourcing a Word-Emotion Association Lexicon. *Computational Intelligence*, 29(3), 436-465.
- [2] Mohammad, Saif, and Peter Turney. "Emotions Evoked by Common Words and Phrases: Using Mechanical Turk to Create an Emotion Lexicon." In *Proceedings of the NAACL HLT 2010 Workshop on Computational Approaches to Analysis and Generation of Emotion in Text*, June 2010, Los Angeles, CA. Association for Computational Linguistics, pp. 26-34. Available online: [link](https://aclanthology.org/W10-0204).
- [3] Mohammad, S. M., Bravo-Marquez, F., Salameh, M., & Kiritchenko, S. (2018). SemEval-2018 Task 1: Affect in Tweets. In Proceedings of International Workshop on Semantic Evaluation (SemEval-2018), New Orleans, LA, USA.
- [Star Wars Movie Scripts](https://www.kaggle.com/datasets/xvivancos/star-wars-movie-scripts)
- [Sentiment Analysis: Rick and Morty Scripts](https://www.kaggle.com/code/andradaolteanu/sentiment-analysis-rick-and-morty-scripts#10.-Bigram-Network)
- [Generate Domain Specific Sentiment Lexicon](https://www.mathworks.com/help/textanalytics/ug/generate-domain-specific-sentiment-lexicon.html)




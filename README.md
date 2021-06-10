# Progrution &copy;

### Your programming solution

This is a universal solution for frustrated developers around the world. 

The main features of this project are:

- It detects the programming language or the technology stack you are complaining about.
- It detects your emotional state and assigns a score to it.
- Searches your favourite sites **github** and **stackoverflow** for answers to your existential questions.
- Tries to make you a happier person by sending memes when you are most likely to need them.

The project includes the following modules:

- **bot.py** the file that glues all of the magic from the other modules.
- **telebot.py** the file that contains the implementation of the main features of our **telegram** bot.
- **norm.py** this file contains all the modules for the **nlp** pipeline modules.
- **database.py** the file that contains the implementation of the **database manager**.
- **tech_clsf_v2.pkl** pipeline that classifies the technology that the user writes about.
- **Sentyment_analysis.pkl** pipeline that assigns a score to how the user feels when writing a particular message.
- **Tech-Nontech.pkl** pipeline that classifies every message in two classes **tech** and **not-tech**.

The data used when training the **nlp** models:

- [IMDB dataset (Sentiment analysis)](https://www.kaggle.com/columbine/imdb-dataset-sentiment-analysis-in-csv-format?select=Train.csv)
- [Stack Overflow Questions](https://www.kaggle.com/imoore/60k-stack-overflow-questions-with-quality-rate)
- [SMS Spam Collection Dataset](https://www.kaggle.com/uciml/sms-spam-collection-dataset)

To run this project, you first should install the following dependencies by running the following command:

```
pip install requests scikit-learn nltk 
```

and then start it, by running this command:

```
python bot.py
```

and access the following [link](https://t.me/myFucking234bOT).

Authors:

- Fișer Răzvan (the great)
- Spînu Lavinia
- Basoc Nicoleta-Nina
- Purici Marius
- **Păpăluță Vasile** (our beloved **jedi**)

from django.apps import AppConfig
from transformers import AutoTokenizer,AutoModelForTokenClassification,pipeline
import joblib
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer, TextClassificationPipeline
import os

class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    tokenizer = AutoTokenizer.from_pretrained("d4data/biomedical-ner-all")
    model = AutoModelForTokenClassification.from_pretrained("d4data/biomedical-ner-all")
    pipe=pipeline('ner',model=model,tokenizer=tokenizer,aggregation_strategy='simple')
    #print current working directory
    model_langid = joblib.load(
        os.path.join(os.path.dirname(__file__), 'diagnosis_bert/language_classifier_ngram_2_6.joblib')
    )
    vectorizer_langid = joblib.load(
        os.path.join(os.path.dirname(__file__), 'diagnosis_bert/vectorizer.joblib')
    )
    pipeline_trans = Pipeline([
        ('vectorizer', vectorizer_langid),
        ('classifier', model_langid)
    ])
    model_diagnosis = TFAutoModelForSequenceClassification.from_pretrained(
        os.path.join(os.path.dirname(__file__), 'diagnosis_bert/')
    )

    # Load the tokenizer
    tokenizer_diagnosis = AutoTokenizer.from_pretrained(
        os.path.join(os.path.dirname(__file__), 'diagnosis_bert/')
    )
    
    pipe_diagnosis = TextClassificationPipeline(model=model_diagnosis, tokenizer=tokenizer_diagnosis, top_k = 24)

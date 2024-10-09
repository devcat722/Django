from rest_framework.response import Response
from rest_framework.decorators import api_view
from googletrans import Translator  # Assuming you're using googletrans for translation
from .apps import ApiConfig
from translate import Translator
from indic_transliteration import sanscript

# test_api method
@api_view(["GET"])
def test_api(request):
    data = {"message": "Hello from Django!"}
    return Response(data)


# actual API methods below
def identify_language(word):
    print(word)
    prediction=ApiConfig.pipeline_trans.predict([word])
    if prediction[0]==0:
        return 'en'
    else:
        return 'hi'

def translate_to_hindi(word):
    print("A: ",word)
    translator = Translator(from_lang="en",to_lang="hi")
    translation = translator.translate(word)
    return translation

def transliterate_to_devanagari(word):
    transliterated_word = sanscript.transliterate(word, sanscript.ITRANS, sanscript.DEVANAGARI)
    return transliterated_word

def translate_to_english(sentence):
    print(sentence)
    translator = Translator(from_lang="hi",to_lang="en")
    translation = translator.translate(sentence)
    print(translation)
    return translation

def translate_hinglish_2(sentences):
    translated_sentences = []
    for sentence in sentences:
        sentence=sentence.lower()
        nwords = sentence.split()
        words=[]
        for i, w in enumerate(nwords):
            try:
                if w in hindi_dictionary:
                    words.append((hindi_dictionary[w],"en"))
                else:
                     words.append((w,identify_language(w)))
            except KeyError:
                pass
        output = ""
        start = 0
        end = 0

        while start < len(words):

            current_language = words[start][1]
            end = start + 1
            while end < len(words) and (words[end][1]) == current_language:
                end += 1
            current_sequence = ' '.join(word[0] for word in words[start:end])

            if current_language == 'en':
                translated_sequence = translate_to_hindi(current_sequence)
            else:
                translated_sequence = transliterate_to_devanagari(current_sequence)

            output += translated_sequence + " "
            start = end

        translated_sentence = translate_to_english(output.strip())
        translated_sentences.append(translated_sentence)

    return translated_sentences
hindi_dictionary = {
    'bukhar':'fever',
    'khansi': 'Cough',
    'daura': 'Attack',
    'kaf': 'Phlegm',
    'tanav': 'Stress',
    'krodh': 'Anger',
    'bhay': 'Fear',
    'jukam': 'Cold',
    'najla': 'Runny nose',
    'jalan': 'Burning sensation',
    'allergy': 'Allergy',
    'gard': 'Filth',
    'gandagi': 'Dirtiness',
    'sardi': 'Cold',
    'flu': 'Flu',
    'garam': 'fever',
    'thandi': 'cold',
    'pyaas': 'Thirst',
    'jakhm': 'Wound',
    'sankraman': 'Infection',
    'thakan': 'Fatigue',
    'jodo': 'joints',
    'dard': 'Pain',
    'sir': 'Head',
    'sar' : 'Head',
    'cheenkne': 'Sneezing',
    'gala': 'throat',
    'kharaab':'bad',
    'laali': 'Redness',
    'laal':'Redness',
    'aankh':'eye',
    'khujli': 'Itching',
    'naak': 'nose',
    'tootne': 'Breaking',
    'thanda': 'Cold',
    'chehra': 'face',
    'pet': 'Stomach',
    'saans': 'Breath',
    'chaati': 'Chest',
    'ulti': 'Vomiting',
    'dakar': 'Burping',
    'matli': 'Nausea',
    'bechaini': 'Restlessness',
    'jalan':'burning',
    'chaati':'chest',
    'seena':'chest',
}


def process_text(text):
  translated_text = translate_hinglish_2([text])[0]
  ner_output = ApiConfig.pipe(translated_text)
  print(ner_output)
  symptoms = []
  biological_structure = None
  combined_symptoms = []
  for entity in ner_output:
      if entity['entity_group'] == 'Biological_structure':
          biological_structure = entity['word']
      elif entity['entity_group'] == 'Sign_symptom':
          symptom = entity['word']
          if biological_structure:
              symptoms.append(f'"{biological_structure} {symptom}"')
              biological_structure = None
          else:
              symptoms.append(f'"{symptom}"')

  # Join symptoms into a single string
  symptoms_str = ', '.join(symptoms)
  print(symptoms_str)
  diagnosis = ApiConfig.pipe_diagnosis(symptoms_str)
  return diagnosis[0][0]['label'],translated_text

# 3. API for Symptom Diagnosis (Top 3 Probabilities)
@api_view(["POST"])
def diagnose_symptoms(request):
    input_text = request.data["prompt"]
    diagnosis,translated_text = process_text(input_text)
    print(diagnosis)
    return Response({"message": "Diagnosis successful! "+diagnosis + " is the most probable diagnosis.", "translated_text": translated_text})

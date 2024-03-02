from django.shortcuts import render
import nltk
from nltk.corpus import wordnet

# Create your views here.
def index(request):
    return render(request, 'word.html')

def word(request):
    search = request.GET.get('search')

    # Use WordNet for meanings
    meanings = []
    if search:
        for synset in wordnet.synsets(search):
            meanings.extend([synset.definition() for synset in wordnet.synsets(search)])

    # Use WordNet for synonyms and antonyms
    synonyms = []
    antonyms = []
    if search:
        for synset in wordnet.synsets(search):
            # Get synonyms
            synonyms.extend([word.name() for word in synset.lemmas()])
            # Get antonyms (if available)
            for lemma in synset.lemmas():
                antonyms.extend([antonym.name() for antonym in lemma.antonyms()])

    # Remove duplicates
    meanings = list(set(meanings))
    synonyms = list(set(synonyms))
    try:
        synonyms.remove(search)
    except ValueError:
        print("Word not found in the list.")
    synonyms = list(set(synonyms))
    synonyms = [word.replace("_", " ") for word in synonyms]
    antonyms = list(set(antonyms))
    antonyms = [word.replace("_", " ") for word in antonyms]

    context = { 'search': search,
                'meanings': meanings,
                'synonyms': synonyms,
                'antonyms': antonyms
            }
    return render(request, 'word.html', context )

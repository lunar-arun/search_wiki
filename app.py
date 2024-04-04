import streamlit as st
import wikipedia
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")

pos_colors = {
        "ADJ": "#FF5733",  # Adjective
        "ADP": "#FFD700",  # Adposition
        "ADV": "#00FFFF",  # Adverb
        "AUX": "#FF6347",  # Auxiliary verb
        "CONJ": "#FF00FF",  # Coordinating conjunction
        "CCONJ": "#FF00FF",  # Coordinating conjunction (alternative)
        "DET": "#32CD32",  # Determiner
        "INTJ": "#00FF7F",  # Interjection
        "NOUN": "#1E90FF",  # Noun
        "NUM": "#FF8C00",  # Numeral
        "PART": "#FFA500",  # Particle
        "PRON": "#9370DB",  # Pronoun
        "PROPN": "#FF1493",  # Proper noun
        "PUNCT": "#696969",  # Punctuation
        "SCONJ": "#000080",  # Subordinating conjunction
        "SYM": "#8B008B",  # Symbol
        "VERB": "#800080",  # Verb
        "Other": "#708090"  # Other
    }

def visualize_entities(text, entity_types):
    
    doc = nlp(text)
    
    print(entity_types)
    
    if not entity_types:
        output = displacy.render([doc], style="ent")
        st.write(output, unsafe_allow_html=True)
    elif entity_types == ["ALL"]:
        output = displacy.render([doc], style="ent")
        st.write(output, unsafe_allow_html=True)
    else:
        output = displacy.render([doc], style="ent", options = {"ents": entity_types})
        st.write(output, unsafe_allow_html=True)
    
def pos_tagging(text, pos_tags):
    # Load the English language model    
    # Process the text with SpaCy
    doc = nlp(text)
    
    for pos, color in pos_colors.items():
        st.sidebar.markdown(f'<div style="display:flex; align-items: center;"><div style="background-color:{color}; width:20px; height:20px; margin-right:10px; border-radius: 5px;"></div><div>{pos}</div></div>', unsafe_allow_html=True)
    
    if pos_tags[0] == "ALL":
        # Generate HTML markup to highlight each word with its POS tag using colors
        html = "<div>"
        for token in doc:
            # Get the color for the POS tag, default to white if not found
            color = pos_colors.get(token.pos_, "#FFFFFF")
            html += f"<span style='background-color: {color}; color: white; padding: 2px; margin: 3px; border-radius: 0.3em;'>{token.text} </span>"
        html += "</div>"
    else:
        # Generate HTML markup to highlight each word with its POS tag using colors
        html = "<div>"
        for token in doc:
            if token.pos_ in pos_tags:
            # Get the color for the POS tag, default to white if not found
                color = pos_colors.get(token.pos_, "#FFFFFF")
                html += f"<span style='background-color: {color}; color: white; padding: 2px; margin: 3px; border-radius: 0.3em;'>{token.text} </span>"
            else:
                html += f"<span>{token.text} </span>"
        html += "</div>"

    st.write(html, unsafe_allow_html=True)

#def dropdown(text):
    
def RadioButton(text, ner_types, pos_types):
    if text:
        option = st.radio("Select Visualization", ("Entity Recognizer", "Part of Speech Tagging"),horizontal=True)
        if option == "Entity Recognizer":
            entity_type = st.multiselect("Select Entity Type", ("ALL",) + ner_types,("ALL"))
            visualize_entities(text,entity_type)
        else :
            pos_tags = st.multiselect("Select Part of Speech Tags", ("ALL",) + pos_types,("ALL"))
            pos_tagging(text, pos_tags)
        
def search(search_text):
    try:
        if search_text:
            results = wikipedia.summary(search_text, sentences = 4)
            doc = nlp(results) 
            ner_types = {ent.label_ for ent in doc.ents}
            pos_types = {word.pos_ for word in doc}
            RadioButton(results, tuple(ner_types), tuple(pos_types))
    except wikipedia.exceptions.DisambiguationError:
        return None 

def main():
    st.title("Wikipedia Search App")
    search(st.text_input("Enter text:"))
        

if __name__ == '__main__':
    main()
import streamlit as st
import wikipedia
import spacy
from spacy import displacy

# Define colors for each POS tag
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
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        #st.error(f"Error loading SpaCy model: {e}")
        return

    try:
        doc = nlp(text)
    except Exception as e:
        #st.error(f"Error processing text with SpaCy: {e}")
        return
    
    if entity_types == "ALL":
        output = displacy.render([doc], style="ent")
    else:
        entity_types_list = entity_types.split(",")
        valid_entity_types = {"ORG", "GPE", "LOC", "DATE", "MONEY", "PERCENT", "QUANTITY", "TIME", "CARDINAL", "EVENT", "FAC", "LANGUAGE", "NORP", "PERSON", "PRODUCT", "WORK_OF_ART"}
        if all(entity_type.strip() in valid_entity_types for entity_type in entity_types_list):
            selected_entities = [(ent.text, ent.start_char, ent.end_char, ent.label_) for ent in doc.ents if ent.label_ in entity_types_list]
            selected_spans = {}
            for ent_type in entity_types_list:
                selected_spans[ent_type.strip()] = [(start, end, label) for text, start, end, label in selected_entities if label == ent_type.strip()]
            output = displacy.render([doc], style="ent", options={"ents": selected_spans})
        else:
            st.error("Invalid entity type")
            return
       
    st.write(output, unsafe_allow_html=True)    
        
def pos_tagging(text, pos_tags):
    # Load the English language model
    nlp = spacy.load("en_core_web_sm")
    
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

def search():
    st.title('Wiki Search')
    search_text = st.text_input('Enter search word:')
    try:
        if search_text:
            results = wikipedia.summary(search_text, sentences = 4)
            return results
    except wikipedia.exceptions.DisambiguationError as e:
        return None

def main():
    results = search()
    
    option = st.radio("Select Visualization", ("Entity Recognizer", "Part of Speech Tagging"))
    if option == "Entity Recognizer":
        entity_type = st.multiselect("Select Entity Type", ("ALL","ORG", "GPE", "LOC", "DATE", "MONEY", "PERCENT", "QUANTITY", "TIME", "CARDINAL", "EVENT", "FAC", "LANGUAGE", "NORP", "PERSON", "PRODUCT", "WORK_OF_ART"),("ALL"))
        selected_entities = ", ".join(entity_type)
        visualize_entities(results, selected_entities)
        
    else:        
        pos_tags = st.multiselect("Select Part of Speech Tags", ("ALL", "ADJ", "ADP", "ADV", "AUX", "CONJ", "CCONJ", "DET", "INTJ", "NOUN", "NUM", "PART", "PRON", "PROPN", "PUNCT", "SCONJ", "SYM", "VERB", "X"),("ALL"))
        pos_tagging(results, pos_tags)
            

if __name__ == '__main__':
    main()
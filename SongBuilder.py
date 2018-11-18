
from __future__ import print_function
import random

CardTitlePrefix = "Song Builder"

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    """
    Build a speechlet JSON representation of the title, output text, 
    reprompt text & end of session
    """
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': CardTitlePrefix + " - " + title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
def build_response(session_attributes, speechlet_response):
    """
    Build the full response JSON from the speechlet response
    """
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# --------------- General Python Logic Functions ------------------------ #
def random_dict_keys(dictionary):
    key_list = []
    i = 0
    while i < len(dictionary):
        key_list.append(dictionary[i].keys())
        i += 1
    random_key = random.choice(key_list)
    key_to_give = random_key[0]
    return key_to_give
    
    
def remove_period(string):
  string_list = list(string)
  i = 0
  while i < len(string_list):
    if string_list[i] == ".":
      string_list[i] = ""
    i += 1
    
  string = "".join(string_list)
  return string.lower()
  
def translate_to_seventh(string):
    return string.replace('7th', 'seventh')

# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    session_attributes = {}
    card_title = "Hello"
    speech_output = "Welcome to song builder... Ask me for a random chord to get started!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry - I didn't understand. Please ask for a random chord"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
    
    
def random_chord():
    card_title = "Here's your random chord"
    chord_to_give = random.choice(CHORD_DICT.keys())
    speech_output = chord_to_give
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))
        
def random_scale():
    card_title = "Here's your random scale"
    scale_class = random.choice(DICT_OF_SCALES.keys())
    scale = random.choice(scale_class.keys())
    scale_notes = scale_class[scale]
    speech_output = "You should play the {0} scale. The notes are {1}".format(scale + " " + DICT_OF_KEYS[scale_class], scale_notes)
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_chord_attributes(chord_to_explain):
    return {"explainChord": chord_to_explain}
      
        
def explain_chord(intent, session):
    """ Sets the chord in the session and prepares the speech to reply to the
    user.
    """

    card_title = "Here's how to play your chord."
    session_attributes = {""}
    should_end_session = True

    if 'chord' in intent['slots']:
        if '7th' in intent['slots']['chord']['value']:
            intent['slots']['chord']['value'] = translate_to_seventh(intent['slots']['chord']['value'])
        chord_to_explain = remove_period(intent['slots']['chord']['value'])
        notes_to_chord = CHORD_DICT[chord_to_explain]
        session_attributes = create_chord_attributes(chord_to_explain)
        speech_output = "The notes are " + notes_to_chord
        reprompt_text = ""
    else:
        speech_output = "Please try again"
        reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def explain_scale(intent):
    
    card_title = "Here's how to play your scale."
    session_attributes = {""}
    should_end_session = True
    
    scale_class = intent['slots']['scale_class']['value']
    note = remove_period(intent['slots']['note']['value'])
    if scale_class == 'major':
        scale_dictionary = MAJOR_SCALE
    
    session_attributes = create_chord_attributes(note)
    speech_output = "The notes to your scale are " + scale_dictionary[note]
    reprompt_text = ""
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


    
# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """
    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they want """
    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()

def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """
    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    # Dispatch to your skill's intent handlers
    if intent_name == "greeting":
        return say_hello()
    elif intent_name == "GiveChord":
        return random_chord()
    elif intent_name == "ExplainChord":
        return explain_chord(intent, session)
    elif intent_name == "RandomScale":
        return random_scale()
    elif intent_name == "ListScale":
        return explain_scale(intent)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session. Is not called when the skill returns should_end_session=true """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])

# --------------- Lists containing chords ------------------

# -- http://www.piano-keyboard-guide.com/keyboard-chords.html -- #

CHORD_DICT = {
                  'a flat major': 'a flat, c, e flat', 'a major': 'a, c sharp, e', 'b flat major': 'b flat, d, f', 'b major': 'b, d sharp, f sharp', 'c major': 'c, e, g', 'c sharp major': 'c sharp, e sharp, g sharp',
                  'd major': 'd, f sharp, a', 'e flat major': 'e flat, g, b flat', 'e major': 'e, g sharp, b', 'f major': 'f, a, c', 'f sharp major': 'f sharp, a sharp, c sharp', 'g major': 'g, b, d',
                  'a flat minor': 'a flat, b, e flat', 'a minor': 'a, c, e', 'b flat minor': 'b flat, d flat, f', 'b minor': 'b, d, f sharp', 'c minor': 'c, e flat, g', 'c sharp minor': 'c sharp, e, g sharp',
                  'd minor': 'd, f, a', 'e flat minor': 'e flat, g flat, b flat', 'e minor': 'e, g, b', 'f minor': 'f, a flat, c', 'f sharp minor': 'f sharp, a, c sharp', 'g minor': 'g, b flat, d',
                  'a flat diminished': 'a flat, c flat, d', 'a diminished': 'a, c, e flat', 'b flat diminished': 'b flat, d flat, e', 'b diminished': 'b, d, f',
                  'c sharp diminished': 'c sharp, e, g', 'c diminished': 'c, e flat, g flat', 'd diminished': 'd, f, a flat', 'e flat diminished': 'e flat, g flat, a', 'e diminished': 'e, g, b flat',
                  'f diminished': 'f, a flat, b', 'f sharp diminished': 'f sharp, a, c', 'g diminished': 'g, b flat, d flat',
                  'a flat major 7th': 'a flat, c, e flat, g', 'a major 7th': 'a, c sharp, e, g sharp', 'b flat major 7th': 'b flat, d, f, a', 'b major 7th': 'b, d sharp, f sharp, a sharp',
                  'c major 7th': 'c, e, g, b', 'c sharp major 7th': 'c sharp, f, g sharp, c', 'd major 7th': 'd, f sharp, a, c sharp', 'e flat major 7th': 'e flat, g, b flat, d', 'e major 7th': 'e, g sharp, b, d sharp',
                  'f major 7th': 'f, a, c, e', 'f sharp major 7th': 'f sharp, a sharp, c sharp, f', 'g major 7th': 'g, b, d, f sharp',
                  'a flat dominant seventh': 'a flat, c, e flat, g flat', 'a dominant seventh': 'a, c sharp, e, g', 'b flat dominant seventh': 'b flat, d, f, a flat', 'b dominant seventh': 'b, d sharp, f sharp, a',
                  'c dominant seventh': 'c, e, g, b flat', 'c sharp dominant seventh': 'c sharp, e sharp, g sharp, b', 'd dominant seventh': 'd, f sharp, a, c', 'e flat dominant seventh': 'e flat, g, b flat, d flat',
                  'e dominant seventh': 'e, g sharp, b, d', 'f dominant seventh': 'f, a, c, e flat', 'f sharp dominant seventh': 'f sharp, a sharp, c sharp, e', 'g dominant seventh': 'g, b, d, f',
                  'a flat minor seventh': 'a flat, c flat, e flat, g flat', 'a minor seventh': 'a, c, e, g', 'b flat minor seventh': 'b flat, d flat, f, a flat', 'b minor seventh': 'b, d, f sharp, a', 'c minor seventh': 'c, e flat, g, b flat',
                  'c sharp minor seventh': 'c sharp, e, g sharp, b', 'd minor seventh': 'd, f, a, c', 'e flat minor seventh': 'e flat, g flat, b flat, d flat', 'e minor seventh': 'e, g, b, d',
                  'f minor seventh': 'f, a flat, c, e flat', 'f sharp minor seventh': 'f sharp, a, c sharp, e', 'g minor seventh': 'g, b flat, d, f',
                  'a flat minor seventh flat five': 'a flat, c flat, e double flat, g flat', 'a minor seventh flat five': 'a, c, e flat, g', 'b flat minor seventh flat five': 'b flat, d flat, f flat, a flat',
                  'b minor seventh flat five': 'b, d, f, a', 'c minor seventh flat five': 'c, e flat, g flat, b flat', 'c sharp minor seventh flat five': 'c sharp, e, g, b',
                  'd minor seventh flat five': 'd, f, a flat, c', 'e flat minor seventh flat five': 'e flat, g flat, b double flat, d flat', 'e minor seventh flat five': 'e, g, b flat, d',
                  'f minor seventh flat five': 'f, a flat, c flat, e flat', 'f sharp minor seventh flat five': 'f sharp, a, c, e', 'g minor seventh flat five': 'g, b flat, d flat, f'
                  }
                         
# --------------- Lists containing standard scale dictionaries -------------------- #
# - https://www.pianoscales.org/major.html - #
sharp_notes = ['c', 'c sharp', 'd', 'd sharp', 'e', 'f', 'f sharp', 'g', 'g sharp', 'a', 'a sharp', 'b']
flat_notes = ['c', 'd flat', 'd', 'e flat', 'e', 'f', 'g flat', 'g', 'a flat', 'a', 'b flat', 'b']

"""
                    {'c': '',
                     'c sharp': '',
                     'd flat': '',
                     'd': '',
                     'd sharp': '',
                     'e flat': '',
                     'e': '',
                     'f': '',
                     'f sharp': '',
                     'g': '',
                     'a flat': '',
                     'a': '',
                     'b flat': '',
                     'b': ''
                    }"""
                    
# This was turned into a dictionary to store the "speech" version of the scale class
DICT_OF_SCALES = {MAJOR_SCALE: "Major", MINOR_SCALE: "Minor", MINOR_BLUES_SCALE: "Minor Blues"}

MAJOR_SCALE = {'c': 'C, D, E, F, G, A, B, C',
               'c sharp': 'C sharp, D sharp, F, F sharp, G sharp, A sharp, B sharp, C sharp',
               'd flat': 'D flat, E flat, F, G flat, A flat, B flat, C, D flat',
               'd': 'D, E, F sharp, G, A, B, C sharp',
               'd sharp': 'D sharp, E sharp, F double sharp, G sharp, A sharp, B sharp, C double sharp',
               'e flat': 'E flat, F, G, A flat, B flat, C, D',
               'e': 'E, F sharp, G sharp, A, B, C sharp, D sharp',
               'f': 'F, G, A, B flat, C, D, E',
               'f sharp': 'F sharp, G sharp, A sharp, B, C sharp, D sharp, F',
               'g flat': 'Gb, Ab, Bb, Cb, Db, Eb, F, Gb',
               'g': 'G, A, B, C, D, E, F sharp',
               'g sharp': 'G sharp, A sharp, B sharp, C sharp, D sharp, E sharp, F double sharp, G sharp',
               'a flat': 'A flat, B flat, C, D flat, E flat, F, G',
               'a': 'A, B, C sharp, D, E, F sharp, G sharp',
               'a sharp': 'A sharp, B sharp, C double sharp, D sharp, E sharp, F double sharp, G doubel sharp, A sharp',
               'b flat': 'B flat, C, D, E flat, F, G, A',
               'b': 'B, C sharp, D sharp, E, F sharp, G sharp, A sharp'
                }

MINOR_SCALE = {'c': 'C, D, E flat, F, G, A flat, B flat, C',
               'c sharp': 'C sharp, D sharp, E, F sharp, G sharp, A, B, C sharp',
               'd flat': 'D flat, E flat, F flat, G flat, A flat, A, B, D flat',
               'd': 'D, E, F, G, A, B flat, C, D',
               'd sharp': 'D sharp, E sharp, F sharp, G sharp, A sharp, B, C sharp, D sharp',
               'e flat': 'E flat, F, G flat, A flat, B flat, C flat, D flat, E flat',
               'e': 'E, F sharp, G, A, B, C, D, E',
               'f': 'F, G, A flat, B flat, C, D flat, E flat, F',
               'f sharp': 'F sharp, G sharp, A, B, C sharp, D, E, F sharp',
               'g flat': 'G flat, A flat, B double flat, C flat, D flat, E double flat, F flat, G flat',
               'g': 'G, A, B flat, C, D, Eb, F, G',
               'g sharp': 'G sharp, A sharp, B, C sharp, D sharp, E, F sharp, G sharp',
               'a flat': 'A flat, B flat, C flat, D flat, E flat, F flat, G flat, A flat',
               'a': 'A, B, C, D, E, F, G, A',
               'a sharp': 'A sharp, B sharp, C sharp, D sharp, F, F sharp, G sharp, A sharp',
               'b flat': 'B flat, C, D flat, E flat, F, G flat, A flat, B flat',
               'b': 'B, C sharp, D, E, F sharp, G, A, B'
                }

MINOR_BLUES_SCALE = {'c': '',
                     'c sharp': '',
                     'd flat': '',
                     'd': '',
                     'd sharp': '',
                     'e flat': '',
                     'e': '',
                     'f': '',
                     'f sharp': '',
                     'g': '',
                     'a flat': '',
                     'a': '',
                     'b flat': '',
                     'b': ''
                    }

MAJOR_BLUES_SCALE = {'c': '',
                     'c sharp': '',
                     'd flat': '',
                     'd': '',
                     'd sharp': '',
                     'e flat': '',
                     'e': '',
                     'f': '',
                     'f sharp': '',
                     'g': '',
                     'a flat': '',
                     'a': '',
                     'b flat': '',
                     'b': ''
                    }

JAZZ_SCALE = {}

PENTATONIC_SCALE = {}

# --------------- Lists containing exotic scale dictionaries -------------------- #

ALGARIAN_SCALE = [] 

ARABIC_SCALE = []

BYZANTINE_SCALE = []

CHINESE_SCALE = []

DIMINISHED_SCALE = []

DOMINANT_DIMINISHED_SCALE = []

EGYPTIAN_SCALE = []

EIGHT_TONE_SPANISH_SCALE = []

ENIGMATIC_SCALE = []

GEEZ_SCALE = []

HINDU_SCALE = []

HIRAJOSHI_SCALE = []

HUNGARIAN_SCALE = []

JAPANESE_SCALE = []

ORIENTAL_SCALE = []

WHOLE_TONE_SCALE = []

ROMANIAN_MINOR_SCALE = []

SPANISH_GYPSY_SCALE = []

SUPER_LOCRIAN_SCALE = []

MAGAM_SCALE = []



# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])
    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])
    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

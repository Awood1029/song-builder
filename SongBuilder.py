
from __future__ import print_function
import random
# We'll start with a couple of globals...

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

# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    session_attributes = {}
    card_title = "Hello"
    speech_output = "Welcome to song builder... Ask me for a random chord to get started!"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "I'm sorry - I didn't understand. Please ask for a random card"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))

def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

def say_hello():
    """
    Return a suitable greeting...
    """
    card_title = "Greeting Message"
    greeting_string = "Hello, how are you?"
    return build_response({}, build_speechlet_response(card_title, greeting_string, "Ask me to say hello...", True))
    
def random_chord():
    card_title = "Here's your random chord"
    chord_to_give = random.choice(CHORD_DICT.keys())
    speech_output = chord_to_give
    # Setting this to true ends the session and exits the skill.
    should_end_session = False
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
    should_end_session = False

    if 'chord' in intent['slots']:
        chord_to_explain = intent['slots']['chord']['value']
        notes_to_chord = CHORD_DICT[chord_to_explain]
        session_attributes = create_chord_attributes(chord_to_explain)
        speech_output = "The notes are " + notes_to_chord
        reprompt_text = ""
    else:
        speech_output = "Please try again"
        reprompt_text = ""
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def blah():
    print "Delete this"

    
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
                  'a flat minor': '', 'a minor': '', 'b flat minor': '', 'b minor': '', 'c minor': '', 'c sharp minor': '',
                  'd minor': '', 'e flat minor': '', 'e minor': '', 'f minor': '', 'f sharp minor': '', 'g minor': '',
                  'a flat diminished': '', 'a diminished': '', 'b flat diminished': '', 'b diminished': '',
                  'c sharp diminished': '', 'c diminished': '', 'd diminished': '', 'e flat diminished': '', 'e diminished': '',
                  'f diminished': '', 'f sharp diminished': '', 'g diminished': '',
                  'a flat major seventh': '', 'a major seventh': '', 'b flat major seventh': '', 'b major seventh': '',
                  'c major seventh': '', 'c sharp major seventh': '', 'd major seventh': '', 'e flat major seventh': '', 'e major seventh': '',
                  'f major seventh': '', 'f sharp major seventh': '', 'g major seventh': '',
                  'a flat dominant seventh': '', 'a dominant seventh': '', 'b flat dominant seventh': '', 'b dominant seventh': '',
                  'c dominant seventh': '', 'c sharp dominant seventh': '', 'd dominant seventh': '', 'e flat dominant seventh': '',
                  'e dominant seventh': '', 'f dominant seventh': '', 'f sharp dominant seventh': '', 'g dominant seventh': '',
                  'a flat minor seventh': '', 'a minor seventh': '', 'b flat minor seventh': '', 'b minor seventh': '', 'c minor seventh': '',
                  'c sharp minor seventh': '', 'd minor seventh': '', 'e flat minor seventh': '', 'e minor seventh': '',
                  'f minor seventh': '', 'f sharp minor seventh': '', 'g minor seventh': '',
                  'a flat minor seventh flat five': '', 'a minor seventh flat five': '', 'b flat minor seventh flat five': '',
                  'b minor seventh flat five': '', 'c minor seventh flat five': '', 'c sharp minor seventh flat five': '',
                  'd minor seventh flat five': '', 'e flat minor seventh flat five': '', 'e minor seventh flat five': '',
                  'f minor seventh flat five': '', 'f sharp minor seventh flat five': '', 'g minor seventh flat five': ''
                  }
                  
                  
CHORD_NOTE_DICTIONARY = {"a": "a, c sharp, and e", "b": "b, d sharp, and f sharp", \
                         "c": "c, e, and g"}
                         
# --------------- Lists containing standard scale dictionaries -------------------- #
# - https://www.pianoscales.org/major.html - #

MAJOR_SCALE = []

MINOR_SCALE = []

BLUES_SCALE = []

JAZZ_SCALE = []

PENTATONIC_SCALE = []

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

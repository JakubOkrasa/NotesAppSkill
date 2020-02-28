import logging
import ask_sdk_core.utils as ask_utils
import json
import requests
import os, sys
file_path = 'lib/'
sys.path.append(os.path.dirname(file_path))

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
from urllib.request import urlopen

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class GetNotesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("GetNotesIntent")(handler_input)

    def get_notes(self):
        notes_speech = "Your notes are: "
        notes_response = requests.get('http://one-user-notes.herokuapp.com/api/v1/dto/notes')
        notes_obj = notes_response.json()
        for note in notes_obj:
            notes_speech += note["noteTitle"] + ", "
        return notes_speech[:len(notes_speech)-2]
        

    def handle(self, handler_input):
        speak_output = self.get_notes()
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
    
class AddNoteIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AddNoteIntent")(handler_input)
        
    def handle(self, handler_input):
        url = 'https://one-user-notes.herokuapp.com/api/v1/dto/notes'
        slots = handler_input.request_envelope.request.intent.slots
        title=slots['noteTitle']
        content=slots['noteContent']
        noteTitleAnswer=title.value
        noteContentAnswer=content.value
        
        if noteContentAnswer is null:
            noteContentAnswer = ""
        note = {
            "noteContent": noteContentAnswer,
            "noteTitle": noteTitleAnswer
        }
        requests.post(url, data=json.dumps(note), headers={"Content-Type": "application/json"})
        #self.add_note(handler_input)
        speak_output = "note created"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )
        
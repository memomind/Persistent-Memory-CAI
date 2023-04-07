from flask import Flask, render_template
from flask_dialogflow.agent import DialogflowAgent
from flask_dialogflow.conversation import V2beta1DialogflowConversation
from DM.utils import normalize_date

import DM

app = Flask(__name__)
agent = DialogflowAgent(app, templates_file='templates/templates.yaml')

@app.route("/")
def agent_template():
    return render_template('frontend.html')


def conversation_tell(conv:V2beta1DialogflowConversation, msg) -> None:
    """
    triggers the dialogflow tell commend
    @param conv: the conversation object
    @param msg: the message to tell
    """
    conv.tell(msg)
    conv.google.tell(msg)

def conversation_dummy(conv):
    conversation_tell(conv,'dummy msg')


def conversation_ask(conv:V2beta1DialogflowConversation, msg) -> None:
    """
    triggers the dialogflow ask commend
    @param conv: the conversation object
    @param msg: the questionto ask
    """

    conv.ask(msg)
    conv.google.ask(msg)


@agent.handle(intent='search_date')
def search_date_handler(conv:V2beta1DialogflowConversation):
    date = conv.parameters['date']
    date = normalize_date(date)
    kg_results =  DM.kg_query(f'''MATCH (e:Event {{Date: "{date}"}}) RETURN e''')
    list_str = [i['e']['Description'] for i in kg_results]

    conversation_tell(conv,f'''On {date}, many things happened: {', '.join(list_str)}.''')
    return conv

@agent.handle(intent='search_person')
def search_person_handler(conv:V2beta1DialogflowConversation):
    person_name = conv.parameters['person']['name']
    kg_results = DM.kg_query(f'''
MATCH (o:Object)
WHERE toLower(o.Name) = toLower('{person_name}')
RETURN o''')
    if len(kg_results)> 0:
        list_str = kg_results[0]['o']['Interests']
        conversation_tell(conv, f'''Yes, {person_name} likes {', '.join(list_str)}.''')
    else:
        conversation_tell(conv, "Oh I don't know her/him so well.")
    return conv

@agent.handle(intent='search_event')
def search_event_handler(conv:V2beta1DialogflowConversation):
    event_name = conv.parameters['event']
    kg_results = DM.kg_query(f'''
    MATCH (o:Event)
    WHERE toLower(o.Description) = toLower('{event_name}')
    RETURN o''')
    if len(kg_results) > 0:
        str = kg_results[0]['o']['Date']
        conversation_tell(conv, f'''Yes, the {event_name} happened on {str}.''')
    else:
        conversation_tell(conv, "Oh I don't know it so well.")
    return conv



@agent.handle(intent="search_person_in_event")
def search_person_in_event_handler(conv:V2beta1DialogflowConversation):
    event_name = conv.parameters['event']
    kg_results = DM.kg_query(f'''
MATCH (o:Object)-[:ParticipatedIn]->(e:Event)
WHERE toLower(e.Description) = toLower("{event_name}")
RETURN o
''')

    list_str = [i['o']['Name'] for i in kg_results]

    conversation_tell(conv,f"{', '.join(list_str)} were in the {event_name}.")
    return conv

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
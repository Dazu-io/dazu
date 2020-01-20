import json

class GoogleWebHook:

    def __init__(self, assistant):
        self.assistant = assistant

    def handle(self, data):
        print("Google WebHook !!!")
        print json.dumps(data, sort_keys=True, indent=4)
        input = data['queryResult']['queryText']
        print("input", input)
        response = self.assistant.respond(input)
        print("output", response['output']['text'])
        return {
            "fulfillmentText" : response['output']['text']
        }

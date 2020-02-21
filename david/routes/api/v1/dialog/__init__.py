from sanic import Blueprint
from sanic.exceptions import abort
from sanic.response import json
from sanic_openapi import doc

from david.registry import Registry

dialog = Blueprint("dialog", url_prefix="/dialog")


@dialog.post("/")
def dialogDefault(request):
    requestData = request.json
    return process_dialog(requestData)


@dialog.post("/<adapter_name:path>")
def dialogAdopted(request, adapter_name):
    requestData = request.json
    return process_dialog(requestData, adapter_name)


def process_dialog(requestData, adapter_name=None):
    from david.server import Server

    adapter = Registry.getAdapter(Server.config, adapter_name)

    if not adapter:
        abort(404, "Invalid adapter")

    if not adapter.validate_data(requestData):
        abort(400, "Invalid input")

    messageIn = adapter.input(requestData)
    messageOut = Server.engine.respond(messageIn)
    responseData = adapter.output(messageOut)
    return json(responseData)

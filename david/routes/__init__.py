from sanic import Blueprint
from sanic.response import text
from sanic_openapi import doc, swagger_blueprint

from david import version

from .api import api

index = Blueprint("index", url_prefix="/")
router = Blueprint.group([index, api, swagger_blueprint])


@index.route("/")
@doc.exclude(True)
def hi(request):
    return text("Hi, am i David: " + version.__version__)

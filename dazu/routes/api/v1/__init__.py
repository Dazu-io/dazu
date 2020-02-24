from sanic import Blueprint

from .dialog import dialog

v1 = Blueprint.group([dialog], url_prefix="/v1")

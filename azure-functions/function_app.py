import azure.functions as func

# world/src/app.py is copied to app.py (this directory) as a build step
# before publishing/testing - see deploy.sh/test-local.sh. Azure's remote
# build only packages this directory, not sibling repo folders, so the
# source of truth stays in world/src/app.py but the deployed/tested
# artifact needs its own local copy.
from app import app as flask_app  # the Flask() instance from world/src/app.py

func_app = func.FunctionApp()


@func_app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS)
def world(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(flask_app.wsgi_app).handle(req, context)

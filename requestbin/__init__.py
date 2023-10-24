import os

from flask import Flask
from flask_cors import CORS

from .models.configs import GlobalConfigs

cfg = GlobalConfigs()

class WSGIRawBody(object):
    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        length = environ.get("CONTENT_LENGTH", "0")
        length = 0 if length == "" else int(length)

        body = environ["wsgi.input"].read(length)
        environ["raw"] = body
        environ["wsgi.input"] = StringIO(body)

        # Call the wrapped application
        app_iter = self.application(environ, self._sr_callback(start_response))

        # Return modified response
        return app_iter

    def _sr_callback(self, start_response):
        def callback(status, headers, exc_info=None):
            # Call upstream start_response
            start_response(status, headers, exc_info)

        return callback


app = Flask(__name__)

if os.environ.get("ENABLE_CORS", cfg.enable_cors):
    cors = CORS(
        app,
        resources={
            r"*": {"origins": os.environ.get("CORS_ORIGINS", cfg.cors_origins)}
        },
    )  # noqa: E501

# from werkzeug.contrib.fixers import ProxyFix  # noqa: E402

# app.wsgi_app = WSGIRawBody(ProxyFix(app.wsgi_app))

app.debug = cfg.debug
app.secret_key = cfg.flask_session_secret_key.get_secret_value()
app.root_path = os.path.abspath(os.path.dirname(__file__))

if cfg.bugsnag_key:
    import bugsnag
    from bugsnag.flask import handle_exceptions

    bugsnag.configure(
        api_key=cfg.bugsnag_key,
        project_root=app.root_path,
        # 'production' is a magic string for bugsnag, rest are arbitrary
        release_stage=cfg.realm.replace("prod", "production"),  # noqa: E251,E501
        notify_release_stages=["production", "test"],
        use_ssl=True,  # noqa: E251
    )
    handle_exceptions(app)

from .filters import *  # noqa: E402,F403

app.jinja_env.filters["status_class"] = status_class  # noqa: F405
app.jinja_env.filters["friendly_time"] = friendly_time  # noqa: F405
app.jinja_env.filters["friendly_size"] = friendly_size  # noqa: F405
app.jinja_env.filters["to_qs"] = to_qs  # noqa: F405
app.jinja_env.filters["approximate_time"] = approximate_time  # noqa: F405
app.jinja_env.filters["exact_time"] = exact_time  # noqa: F405
app.jinja_env.filters["short_date"] = short_date  # noqa: F405

app.add_url_rule("/", "views.home")
app.add_url_rule(
    "/<path:name>",
    "views.bin",
    methods=["GET", "POST", "DELETE", "PUT", "OPTIONS", "HEAD", "PATCH", "TRACE"],
)  # noqa: 501

app.add_url_rule("/docs/<name>", "views.docs")
app.add_url_rule("/api/v1/bins", "api.bins", methods=["POST"])
app.add_url_rule("/api/v1/bins/<name>", "api.bin", methods=["GET"])
app.add_url_rule(
    "/api/v1/bins/<bin>/requests", "api.requests", methods=["GET"]
)  # noqa: E501
app.add_url_rule(
    "/api/v1/bins/<bin>/requests/<name>", "api.request", methods=["GET"]
)  # noqa: E501

app.add_url_rule("/api/v1/stats", "api.stats")

# app.add_url_rule('/robots.txt', redirect_to=url_for('static', filename='robots.txt'))  # noqa: E501

from requestbin import api, views  # noqa: F401,E402

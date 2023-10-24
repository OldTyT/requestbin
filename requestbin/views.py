import urllib  # noqa: F401
from datetime import datetime, timedelta

from flask import (
    #escape,
    make_response,
    redirect,  # noqa: E501,F401
    render_template,
    request,
    session,
    url_for,
)

from requestbin import app, cfg, db


def update_recent_bins(name):
    if "recent" not in session:
        session["recent"] = []
    if name in session["recent"]:
        session["recent"].remove(name)
    session["recent"].insert(0, name)
    if len(session["recent"]) > 10:
        session["recent"] = session["recent"][:10]
    session.modified = True


def expand_recent_bins():
    if "recent" not in session:
        session["recent"] = []
    recent = []
    for name in session["recent"]:
        try:
            recent.append(db.lookup_bin(name))
        except KeyError:
            session["recent"].remove(name)
            session.modified = True
    return recent


@app.endpoint("views.home")
def home():
    return render_template("home.html", recent=expand_recent_bins())


@app.endpoint("views.bin")
def bin(name):
    try:
        bin = db.lookup_bin(name)
    except KeyError:
        return "Not found\n", 404
    if request.query_string == b"inspect":
        if bin.private and session.get(bin.name) != bin.secret_key:
            return "Private bin\n", 403
        update_recent_bins(name)
        return render_template(
            "bin.html",
            bin=bin,  # noqa: E128
            base_url=request.scheme + "://" + request.host,
            max_requests=cfg.max_requests,
            request_expiry=(
                datetime.utcnow() + timedelta(seconds=db.expiry_time(name))
            ).strftime("%Y/%m/%d, %H:%M:%S"),
        )  # noqa: E128,,E501
    else:
        db.create_request(bin, request)
        resp = make_response("ok\n")
        resp.headers["Sponsored-By"] = "https://www.runscope.com"
        return resp


@app.endpoint("views.docs")
def docs(name):
    doc = db.lookup_doc(name)
    if doc:
        return render_template(
            "doc.html",
            content=doc["content"],  # noqa: E128
            title=doc["title"],
            recent=expand_recent_bins(),
        )
    else:
        return "Not found", 404

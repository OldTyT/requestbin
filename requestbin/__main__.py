import os

from requestbin import app, config

if __name__ == "__main__":
    port = int(os.environ.get("PORT", config.port_number))
    app.run(host="0.0.0.0", port=port, debug=config.debug)

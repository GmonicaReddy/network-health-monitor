from flask import Flask, render_template
from pathlib import Path
import json

LOG_FILE = Path(__file__).parent / "logs" / "monitor.log"

app = Flask(__name__)

def read_latest(n=20):
    if not LOG_FILE.exists():
        return []
    lines = LOG_FILE.read_text().strip().splitlines()
    # take last n lines
    data = []
    for line in lines[-n:]:
        try:
            data.append(json.loads(line))
        except:
            pass
    # show newest first
    return list(reversed(data))

@app.route("/")
def index():
    entries = read_latest(30)
    return render_template("index.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True, port=5001)

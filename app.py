from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def skill():
    message = "Hello {name}! How you doing"
    
    return message.format(name=os.getenv("NAME", "BNT"))
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)

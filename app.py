from flask import Flask

app = Flask(__name__)

@app.route("/greet")
def greet():
    name = request.args.get("name")
    if name:
        return f"Hello, {name}!"
    else:
        return "Please provide a name."

if __name__ == "__main__":
    app.run(port=8080)

# When you run this script and navigate to http://localhost:8080/greet?name=John in your web browser, you should see the message "Hello, John!" displayed on the page. 
#
# If you navigate to http://localhost:8080/greet without providing a name parameter, you should see the message "Please provide a name.".    
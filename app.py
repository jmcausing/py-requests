# Python app that accepts string request
# Author: John Mark Causing
# Date: April 7, 2023
# Example usage:
# curl https://py-requests-optgf.kinsta.app/greet?name=john
# Hello, john!


from flask import Flask, request

app = Flask(__name__)

@app.route("/greet")

def greet():
    name = request.args.get("name")
    if name:
        return f"Hello, {name}!"
    else:
        return "Please provide a name."
    

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
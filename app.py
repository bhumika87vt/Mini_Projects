from flask import Flask, render_template, request

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route("/calculate",methods=["GET","POST"])
def calculate():

    if request.method == "GET":
        return render_template("method_not_allowed.html"), 405

    num1=float(request.form["number1"])
    num2=float(request.form["number2"])
    operation=request.form["operation"]
    result=0

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 != 0:
            result = num1 / num2
        else:
            result = "Cannot divide by zero"

    return render_template("results.html",
                           num1=num1,
                           num2=num2,
                           operation=operation,
                           result=result)

@app.route("/greet/<username>")
def greet(username):
    return render_template("greet.html",username=username)

if __name__=="__main__":
    app.run(debug=True)
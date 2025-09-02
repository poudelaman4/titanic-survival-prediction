from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load trained model
model = pickle.load(open("model.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    user_data = None  # Add this variable to store user input
    if request.method == "POST":
        pclass = int(request.form["pclass"])
        sex = int(request.form["sex"])
        age = float(request.form["age"])
        sibsp = int(request.form["sibsp"])
        parch = int(request.form["parch"])
        fare = float(request.form["fare"])
        embarked = int(request.form["embarked"])

        data = pd.DataFrame([[pclass, sex, age, sibsp, parch, fare, embarked]],
                            columns=["Pclass","Sex","Age","SibSp","Parch","Fare","Embarked"])
        prediction = model.predict(data)[0]

        # Store user input to display on the page
        user_data = {
            'Pclass': pclass,
            'Sex': 'Male' if sex == 0 else 'Female',
            'Age': age,
            'SibSp': sibsp,
            'Parch': parch,
            'Fare': fare,
            'Embarked': 'Southampton' if embarked == 0 else 'Cherbourg' if embarked == 1 else 'Queenstown'
        }

    return render_template("index.html", prediction=prediction, user_data=user_data)

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, request
import hostcalculator


a = hostcalculator.hosts(verbose=False)

app = Flask(__name__)

# Route with URL parameters
@app.route('/calc')
def calc():
    try:
        xip = request.args.get('ip')
        xcidr = request.args.get('cidr')

        a.calculate_nflb(str(xip), int(xcidr))
        return "{0}".format(a.calculate_nflb(str(xip), int(xcidr)))
    except ValueError:
        return 'Age must be a number.'

# Route with two query parameters (for addition)
@app.route('/add/<int:a>/<int:b>')
def add(a, b):
    return f'The sum of {a} and {b} is {a + b}.'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
from flask import Flask, jsonify, request
import json
app = Flask(__name__)

# Sample initial list of books


@app.route('/get_wallet', methods=['GET'])
def get_wallet():
    with open('wallet.json', mode='r') as file:
        data = json.load(file)


@app.route('/write_wallet', methods=['POST'])
def write_wallet():
    new_book = request.json['wallet'],
    with open('wallet.json', 'w') as file:
        # Write the data to the file
        json.dump(new_book, file)

if __name__ == '__main__':
    app.run()
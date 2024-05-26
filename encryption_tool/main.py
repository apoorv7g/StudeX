from flask import Flask, render_template, request, send_file
import io

app = Flask(__name__)


def custom_encrypt(data):
    return data[::-1]


def custom_decrypt(data):
    return data[::-1]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/encrypt', methods=['POST'])
def encrypt():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            data = file.read()
            encrypted_data = custom_encrypt(data)
            encrypted_file = io.BytesIO(encrypted_data)
            encrypted_file.seek(0)
            encrypted_filename = 'encrypted_' + file.filename
            return send_file(encrypted_file, as_attachment=True, download_name=encrypted_filename)


@app.route('/decrypt', methods=['POST'])
def decrypt():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            encrypted_data = file.read()
            decrypted_data = custom_decrypt(encrypted_data)
            decrypted_file = io.BytesIO(decrypted_data)
            decrypted_file.seek(0)
            decrypted_filename = 'decrypted_' + file.filename
            return send_file(decrypted_file, as_attachment=True, download_name=decrypted_filename)


if __name__ == '__main__':
    app.run(debug=False)

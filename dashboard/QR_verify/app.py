from flask import Flask, request, render_template
import qrcode
import io
import base64

app = Flask(__name__)
@app.route('/verify/<id_value>')
def verify(id_value):
    # 🔒 Optional: check against a database here for validation
    return render_template('verified.html', id_value=id_value)
@app.route('/', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        id_value = request.form['id']

        # Generate QR code
        qr = qrcode.make(id_value)
        buf = io.BytesIO()
        qr.save(buf, format='PNG')
        img_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        
        return render_template('display.html', qr_code=img_data, id_value=id_value)
    
    return render_template('form.html')
# Removed invalid usage of id_value outside of request context
if __name__ == '__main__':
    app.run(debug=True)
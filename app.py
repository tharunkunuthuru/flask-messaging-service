from flask import Flask, request, render_template
import boto3
import json

app = Flask(__name__)

sqs_client = boto3.client('sqs', region_name='us-east-1')
QUEUE_URL = 'https://sqs.us-east-1.amazonaws.com/905418149763/my-queue-1595'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not all([name, age, phone, email]):
            return "Please fill all the fields."

        message = {
            'name': name,
            'age': age,
            'phone': phone,
            'email': email
        }

        try:
            sqs_client.send_message(
                QueueUrl=QUEUE_URL,
                MessageBody=json.dumps(message)
            )
        except Exception as e:
            return f"Error sending to SQS: {e}"

        return f"Acknowledgement request submitted for {email}. You will receive a copy shortly."

    return render_template('form.html')

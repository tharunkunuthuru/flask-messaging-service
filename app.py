from flask import Flask, request, render_template_string
import boto3
import json

app = Flask(__name__)

# AWS clients
sqs_client = boto3.client('sqs', region_name='ap-south-1')

# Your SQS Queue URL
QUEUE_URL = 'https://sqs.ap-south-1.amazonaws.com/123456789012/YourQueueName'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        phone = request.form.get('phone')
        email = request.form.get('email')

        if not all([name, age, phone, email]):
            return "Please fill all the fields."

        # Message to be sent to SQS
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

    # HTML form
    return render_template_string('''
        <form method="post">
          Name: <input name="name" type="text" required><br>
          Age: <input name="age" type="number" required><br>
          Phone: <input name="phone" type="text" placeholder="+911234567890" required><br>
          Email: <input name="email" type="email" required><br>
          <input type="submit" value="Submit">
        </form>
    ''')

from flask import Flask, render_template, request, jsonify
from watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = Flask(__name__)

# IBM Watson credentials
api_key = 'your-api-key'
url = 'your-api-url'
assistant_id = 'your-assistant-id'

# Authenticator setup
authenticator = IAMAuthenticator(api_key)
assistant = AssistantV2(
    version='2021-06-14',
    authenticator=authenticator
)
assistant.set_service_url(url)

# Create session
session_id = assistant.create_session(assistant_id=assistant_id).get_result()['session_id']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['message']
    response = assistant.message(
        assistant_id=assistant_id,
        session_id=session_id,
        input={'message_type': 'text', 'text': user_input}
    ).get_result()
    reply = response['output']['generic'][0]['text']
    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)

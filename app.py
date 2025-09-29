# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory
import requests
# from openai import OpenAI
import pyttsx3  # optional if you want backend TTS, but better do TTS in browser
import os



app = Flask(__name__, static_url_path='/static')

newsapi = "pub_d52d5cec0a0a46e48284c7964a2d4050"
@app.route('/style')
def style():
    return '<link rel="stylesheet" href="/static/style.css">'

# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                 'favicon.png', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.json
    command = data.get('command', '').lower()

    if "google" in command:
        return jsonify({"action": "open_url", "url": "https://www.google.com"})
    elif "facebook" in command:
        return jsonify({"action": "open_url", "url": "https://www.facebook.com"})
    elif "github" in command:
        return jsonify({"action": "open_url", "url": "https://www.github.com"})
    elif "youtube" in command:
        return jsonify({"action": "open_url", "url": "https://www.youtube.com"})
    elif "instagram" in command:
        return jsonify({"action": "open_url", "url": "https://www.instagram.com/fr_o_lic/"})
    elif "news" in command:
        try:
            response = requests.get(f"https://newsdata.io/api/1/news?apikey={newsapi}&language=en")
            if response.status_code == 200:
                data = response.json()
                articles = data.get('results', [])
                headlines = [a['title'] for a in articles[:5] if 'title' in a]
                return jsonify({"action": "speak", "text": "Here are the top headlines: " + ". ".join(headlines)})
            else:
                return jsonify({"action": "speak", "text": "Failed to fetch news."})
        except Exception as e:
            return jsonify({"action": "speak", "text": "Sorry, I couldn't fetch the news right now."})

    # Fallback response if no conditions matched
    return jsonify({"action": "speak", "text": "Sorry, I didn't understand your command."})

    # else:
    #     client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        # Call OpenAI if command is not a direct action
        # try:
        #     client = OpenAI(api_key="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")
        #     completion = client.chat.completions.create(
        #         model="gpt-3.5-turbo",
        #         messages=[
        #             {"role": "system", "content": "You are a virtual assistant named Jarvis."},
        #             {"role": "user", "content": command}
        #         ]
        #     )
        #     answer = completion.choices[0].message.content
        #     return jsonify({"action": "speak", "text": answer})
        # except Exception as e:
        #     return jsonify({"action": "speak", "text": "Sorry, I had trouble processing your request."})

if __name__ == '__main__':
    app.run(debug=True, port=5000)

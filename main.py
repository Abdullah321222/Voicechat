import speech_recognition as sr
import pyttsx3
import wikipediaapi
from flask import Flask, request, jsonify
from flask_cors import CORS
import wikipedia


app = Flask(__name__)
CORS(app)

recognizer = sr.Recognizer()
engine = pyttsx3.init()


user_agent = "YourAppName/1.0 (YourContactInfo)"
wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent=user_agent
)


wikipedia.set_user_agent(user_agent)


def speak(text):
    """
    Convert text to speech.
    """
    engine.say(text)
    engine.runAndWait()


def listen():
    """
    Convert speech to text.
    """
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."


def fetch_wikipedia_data(query):
    """
    Fetch data from Wikipedia.
    """
    try:
        page = wiki_wiki.page(query)
        if page.exists():
            return page.summary[:1000]  
        else:
            return "Sorry, I could not find any information on that topic."
    except Exception as e:
        return f"An error occurred while fetching data from Wikipedia: {e}"


def fetch_wikipedia_summary(query):
    """
    Fetch summary from Wikipedia using the `wikipedia` library.
    """
    try:
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Disambiguation Error: {e.options}"
    except wikipedia.exceptions.PageError:
        return "Sorry, the page does not exist."
    except Exception as e:
        return f"An error occurred: {e}"


def process_text(text):
    """
    Process the text input and generate a response.
    """
    if 'hello' in text.lower():
        return "Hello! How can I assist you today?"
    elif 'bye' in text.lower():
        return "Goodbye! Have a great day!"
    elif 'name' in text.lower():
        return "I don't have a name, but you can call me Chatbot."
    elif 'how are you' in text.lower():
        return "I'm just a bot, but I'm doing well. How about you?"
    else:
        return fetch_wikipedia_summary(text)


@app.route('/chat', methods=['POST'])
def chat():
    """
    Flask route to handle chat requests.
    """
    user_input = request.json.get('message')
    response = process_text(user_input)
    speak(response)  
    return jsonify({'response': response})


if __name__ == "__main__":
    def main():
        """
        Main interactive loop for voice-based interaction.
        """
        print("Say 'quit' to exit the program.")
        while True:
            print("Speak now...")
            user_text = listen()
            if user_text.lower() == 'quit':
                print("Goodbye!")
                speak("Goodbye!")
                break
            response_text = process_text(user_text)
            print("Chatbot:", response_text)
            speak(response_text)

    main()
    app.run(debug=True)

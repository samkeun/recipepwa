from flask import Flask, render_template, request
import openai
import os
from dotenv import load_dotenv
# from flask_cors import CORS

app = Flask(__name__)

# Securely fetch the API key using the dotenv library
load_dotenv()
key = os.getenv("OPENAI_API_KEY")
openai.api_key = key

dietary_restrictions = [
    "Gluten-Free",
    "Dairy-Free",
    "Vegan",
    "Pescatarian",
    "Nut-Free",
    "Kosher",
    "Halal",
    "Low-Carb",
    "Organic",
    "Locally Sourced",
]

cuisines = [
    "",
    "Korean",
    "Italian",
    "Mexican",
    "Chinese",
    "Indian",
    "Japanese",
    "Thai",
    "French",
    "Mediterranean",
    "American",
    "Greek",
]

# create a dictionary to store the languages and their corresponding codes
languages = {
    'English': 'en',
    'Spanish': 'es',
    'French': 'fr',
    'German': 'de',
    'Russian': 'ru',
    'Chinese (Simplified)': 'zh-CN',
    'Chinese (Traditional)': 'zh-TW',
    'Japanese': 'ja',
    'Korean': 'ko',
    'Italian': 'it',
    'Portuguese': 'pt',
    'Arabic': 'ar',
    'Dutch': 'nl',
    'Swedish': 'sv',
    'Turkish': 'tr',
    'Greek': 'el',
    'Hebrew': 'he',
    'Hindi': 'hi',
    'Indonesian': 'id',
    'Thai': 'th',
    'Filipino': 'tl',
    'Vietnamese': 'vi'
    # ... potentially more based on actual Whisper support
}

@app.route('/')
def index():
    # Display the main ingredient input page
    return render_template('index.html', 
                           cuisines=cuisines, 
                           dietary_restrictions=dietary_restrictions, 
                           languages=languages)

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    # Extract the three ingredients from the user's input
    ingredients = request.form.getlist('ingredient')

    # Extract cuisine, restrictions, and language
    selected_cuisine = request.form.get('cuisine')
    selected_restrictions = request.form.getlist('restrictions')
    selected_language = request.form.get('language')

    print('selected_cuisine: ' + selected_cuisine)
    print('selected_restrictions: ' + str(selected_restrictions))
    print('selected_language: ' + selected_language)

    if len(ingredients) != 3:
        return "Kindly provide exactly 3 ingredients."

    # Craft a conversational prompt for ChatGPT, specifying our needs
    prompt = f"Craft a recipe in HTML in {selected_language} using \
        {', '.join(ingredients)}. It's okay to use some other necessary ingredients. \
        Ensure the recipe ingredients appear at the top, \
        followed by the step-by-step instructions."

    if selected_cuisine:
        prompt += f" The cuisine should be {selected_cuisine}."

    if selected_restrictions and len(selected_restrictions) > 0:
        prompt += f" The recipe should have the following restrictions: {', '.join(selected_restrictions)}."

    print('prompt: ' + prompt)

    messages = [{'role': 'user', 'content': prompt}]

    # Engage ChatGPT to receive the desired recipe
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.8,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    )

    # Extract the recipe from ChatGPT's response
    recipe = response["choices"][0]["message"]["content"]

    # Showcase the recipe on a new page
    return render_template('recipe.html', recipe=recipe)

if __name__ == '__main__':
    app.run(debug=True) #, ssl_context='adhoc')  # SSL Context 추가

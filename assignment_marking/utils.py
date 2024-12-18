import PyPDF2
import requests
import google.generativeai as genai
from decouple import config

def extract_text_from_pdf(pdf_file):
    # Handles file-like object (from Django request.FILES)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n" if page.extract_text() else ''
    return text


def compare_assignments(student_text, teacher_text):
    # Replace with actual API endpoint and credentials
    genai.configure(api_key=config('GEMINI_API_KEY'))
    generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
    }
    model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
    )
    # url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBSuTtIwJIIsaJp5BcPvoySfdTsFn-0BMk'
    # headers = {
    #     'Content-Type': 'application/json',
    # }
    
    # Prepare the data for comparison
    data = {
        'text': student_text,
        'text': teacher_text
    }
    
    chat_session = model.start_chat(
    history=[
    ]
    )

    prompt = "Please compare the first document to the provided answer key in the second document. Grade the document based on accuracy, completeness, structure, and clarity. Use a scale of 0-100, where 100 is a perfect match with the answer keyand return only the score please"
    response = model.generate_content([prompt, teacher_text, student_text])
    grade = int(response.text.split('.')[0])
    if ( grade < 66 ) :
        grade = f"{grade - 50}"
    return grade
    # try:
        
    #     # Post data to Gemini or any AI service
    #     response = requests.post(url, headers=headers, json=data)
    #     response.raise_for_status()  # Handle 4xx/5xx errors
    #     return response.json()  # Assuming JSON response
    # except requests.exceptions.RequestException as e:
    #     return {'error': str(e)}

def analyze_submission(submission_text):
    # Replace with actual Gemini API details
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=AIzaSyBSuTtIwJIIsaJp5BcPvoySfdTsFn-0BMk'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'text': submission_text,  # Adjust this to match the API's expected input format
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
        return response.json()  # Ensure the response is in JSON format
    except requests.exceptions.RequestException as e:
        # Handle any API request errors
        return {'error': str(e)}



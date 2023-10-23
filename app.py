from flask import Flask, render_template, request, jsonify
import PyPDF2
import openai

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    pdf_file = request.files['pdf_file']
    if pdf_file:
        try:
            pdf_text = extract_text_from_pdf(pdf_file)
            return jsonify({'message': 'PDF uploaded successfully', 'pdf_text': pdf_text})
        except Exception as e:
            return jsonify({'error': str(e)})

    return jsonify({'error': 'No file uploaded'})

@app.route('/ask', methods=['POST'])
def ask_question():
    question = request.form.get('question')
    pdf_text = request.form.get('pdf_text')

    # Use OpenAI's API to answer the question
    # Replace 'YOUR_API_KEY' with your OpenAI API key
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Question: {question}\nAnswer:",
        max_tokens=50
    )

    answer = response.choices[0].text.strip()

    return jsonify({'answer': answer})

def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page in range(len(pdf_reader.pages)):
        pdf_text += pdf_reader.pages[page].extract_text()
    return render_template('index.html', pdf_text=pdf_text)

if __name__ == '__main__':
    app.run(debug=True)

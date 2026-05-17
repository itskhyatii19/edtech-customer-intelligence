from transformers import pipeline

summarizer = None
generator = None
classifier = None


def load_models():
    global summarizer, generator, classifier

    if summarizer is None:
        print("🔄 Loading models...")

        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        generator = pipeline("text2text-generation", model="google/flan-t5-base")
        classifier = pipeline(
            "text-classification",
            model="distilbert-base-uncased-finetuned-sst-2-english"
        )

def generate_summary(text):
    load_models()
    text = text[:800]

    prompt = f"""
Summarize student reviews.

Give:
- summary
- 2 problems
- 2 positives

Reviews:
{text}
"""

    result = summarizer(prompt, max_length=300)
    return result[0]['generated_text']

def generate_qa(text, num_questions=5):
    load_models()
    text = text[:800]

    prompt = f"Generate {num_questions} question answer pairs from:\n{text}"
    result = generator(prompt, max_length=256)

    return result[0]['generated_text']


def extract_insights(text):
    load_models()
    text = text[:800]

    prompt = f"""
From these reviews, list:

- main problems
- improvements

Reviews:
{text}
"""

    result = generator(prompt, max_length=300)
    return result[0]['generated_text']

def evaluate_output(original, generated):
    load_models()

    combined = f"{original} {generated}"
    return classifier(combined)

def get_sentiment(text):
    load_models()
    text = text[:512]

    result = classifier(text)
    return result
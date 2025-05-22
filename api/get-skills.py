import json
import re
from collections import Counter

# Skill pattern
skill_patterns = re.compile(
    r"\b(java|python|kotlin|flutter|react|angular|node|swift|ruby|php|c\+\+|c#|go|docker|kubernetes|aws|azure|gcp|restful|graphql|ai|ml|dl|cv|nlp|cloud|devops|agile|ci/cd|sql|nosql|mongodb|firebase|redux|git|jira|confluence|trello|testing|tdd|bdd|scrum|microservices|big data|data science|machine learning|deep learning|nlp|cloud computing|containerization|orchestration|api|mvc|mvvm|mvp|.net|spring|django|express|flask|ios|android|dart|objective-c|cybersecurity|penetration testing|firewalls|siem|threat intelligence|data analysis|pandas|numpy|matplotlib|seaborn|scikit-learn|tensorflow|keras|pytorch)\b",
    re.IGNORECASE
)

# Text cleaner
def clean_text(text):
    text = re.sub(r"\n|<.*?>|\t|\r", " ", str(text))
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()

# Extract skills
def extract_skills(descriptions):
    all_text = ' '.join([clean_text(desc) for desc in descriptions])
    matches = skill_patterns.findall(all_text)
    counts = Counter([m.lower() for m in matches])
    return [skill for skill, _ in counts.most_common()]

# Mock job data
def get_mocked_job_summaries(job, location):
    return [
        f"We are looking for a {job} developer with experience in .NET, C#, Azure, and Agile methodologies.",
        "The candidate must have skills in SQL, RESTful APIs, and CI/CD pipelines.",
        "Experience with Docker, Kubernetes, and cloud computing is a plus.",
        "Strong knowledge of Git, Jira, and software testing is required."
    ]

# Vercel-compatible handler
def handler(event, context):
    try:
        # Get query params
        query = event.get("queryStringParameters") or {}
        job = query.get("job", "developer")
        location = query.get("location", "remote")

        descriptions = get_mocked_job_summaries(job, location)
        skills = extract_skills(descriptions)

        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "job": job,
                "location": location,
                "skills": skills
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({ "error": str(e) })
        }

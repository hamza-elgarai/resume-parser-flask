from pathlib import Path
import re
from fuzzywuzzy import process
from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import Matcher


def get_filename_without_extension(file_path):

    # Convert the file path to a Path object and get the filename without the extension
    filename_without_extension = Path(file_path).stem
    return filename_without_extension


def clean_filename(text):
    text = text.replace('CV','').replace('cv','')
    # Replace dashes and underscores with spaces
    text = text.replace("-", " ").replace("_", " ")

    # Remove parentheses and square brackets
    text = re.sub(r"[()\[\]]", "", text)

    # Remove numbers
    text = re.sub(r"\d", "", text)

    # Optionally, trim multiple spaces to a single space
    text = re.sub(r"\s+", " ", text).strip()

    return text


def find_similar_strings_in_document(document_text, filename, top_n=5, similarity_threshold=80):
    filename = clean_filename(filename)
    # Split the document text into words
    words = set(re.findall(r'\b\w+\b', document_text))

    # Find the top N matches for the filename from the words in the document
    best_matches = process.extract(filename, list(words), limit=top_n)

    # Filter matches based on a similarity threshold
    filtered_matches = [
        match for match in best_matches if match[1] >= similarity_threshold
    ]
    print('filtered matches : ')
    print(filtered_matches)
    return filtered_matches


def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)

def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"(\+?\d{0,3}\s*(?:\d{2}\s*){4}\d{2}\d?)"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number

def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email

def extract_skills_from_resume(text, skills_list):
    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills

def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(faculté|école|université|institut|grande école|bachelor|master|doctorat|ensa|fst|ensam|ehtp)\b\s*(.*?)(?=\.|\n|;|,|$)"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match[0] + " " + match[1].strip())

    return education

 
def extract_name(resume_text):
    nlp = spacy.load('fr_core_news_sm')
    matcher = Matcher(nlp.vocab)
 
    # Define name patterns
    patterns = [
        [{'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}],  # First name and Last name
        [{'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}],  # First name, Middle name, and Last name
        [{'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}, {'IS_ALPHA': True, 'OP': '+'}]  # First name, Middle name, Middle name, and Last name
    ]
 
    for pattern in patterns:
        matcher.add('NAME', patterns=[pattern])
 
    doc = nlp(resume_text)
    matches = matcher(doc)
 
    for match_id, start, end in matches:
        span = doc[start:end]
        return span.text
 
    return None

def extract_all_data(path):
    resume_paths = [path]

    for resume_path in resume_paths:
        text = extract_text_from_pdf(resume_path)
        filename = get_filename_without_extension(resume_path)
        similar_strings = find_similar_strings_in_document(text,filename)
        print(similar_strings)

        print("Resume:", resume_path)
        response = dict()


        name = extract_name(text)
        response['name'] = name
        if name:
            print("Name:", name)
        else:
            print("Name not found")

        contact_number = extract_contact_number_from_resume(text)
        if contact_number:
            response['contact_number'] = contact_number
            print("Contact Number:", contact_number.replace('\n',''))
        else:
            print("Contact Number not found")

        email = extract_email_from_resume(text)
        if email:
            response['email'] = email
            print("Email:", email)
        else:
            print("Email not found")

        skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'LWC','Keycloak','Laravel','HTML','CSS','JS','Java','JavaScript']
        extracted_skills = extract_skills_from_resume(text, skills_list)
        if extracted_skills:
            response['extracted_skills'] = extracted_skills
            print("Skills:", extracted_skills)
        else:
            print("No skills found")

        extracted_education = extract_education_from_resume(text)
        if extracted_education:
            response['education'] = extracted_education
            print("Education:", extracted_education)
        else:
            print("No education information found")
        return response


if __name__ == '__main__':
    resume_paths = [r"CV-Hamza-ELGARAI (1).pdf"]

    for resume_path in resume_paths:
        text = extract_text_from_pdf(resume_path)
        filename = get_filename_without_extension(resume_path)
        similar_strings = find_similar_strings_in_document(text,filename)
        print(similar_strings)

        print("Resume:", resume_path)


        name = extract_name(text)
        if name:
            print("Name:", name)
        else:
            print("Name not found")

        contact_number = extract_contact_number_from_resume(text)
        if contact_number:
            print("Contact Number:", contact_number.replace('\n',''))
        else:
            print("Contact Number not found")

        email = extract_email_from_resume(text)
        if email:
            print("Email:", email)
        else:
            print("Email not found")

        skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication', 'Project Management', 'Deep Learning', 'SQL', 'Tableau', 'LWC','Keycloak','Laravel','HTML','CSS','JS','Java','JavaScript']
        extracted_skills = extract_skills_from_resume(text, skills_list)
        if extracted_skills:
            print("Skills:", extracted_skills)
        else:
            print("No skills found")

        extracted_education = extract_education_from_resume(text)
        if extracted_education:
            print("Education:", extracted_education)
        else:
            print("No education information found")

        print()


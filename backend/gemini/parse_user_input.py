import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel('gemini-2.5-pro')

def parse_product_description(user_input: str) -> dict:
    prompt = f"""
    Aşağıdaki ürün açıklamasını incele ve JSON formatında geri dön:
    {{
        "category":"", 
        "color":"", 
        "size":"", 
        "gender":"", 
        "features":"" 
    }}

    Ürün açıklaması: "{user_input}"

    Sadece JSON olarak cevap ver.
    """
    response = model.generate_content(prompt)
    return extract_json_from_response(response.text)

def extract_json_from_response(text):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        json_text = match.group()
        try:
            data = json.loads(json_text)
            return data
        except json.JSONDecodeError:
            print("JSON parse error.")
            return None
    else:
        print("JSON part not found in response.")
        return None


def get_product_details(text):
    prompt = f"""
Aşağıdaki ürün açıklamasından kategoriyi, rengi, bedeni, cinsiyeti ve ürünün belirgin bir özelliğini JSON formatında çıkar.

Ürün Açıklaması: "{text}"

Sadece JSON olarak cevap ver:

Örnek çıktı:
{{
    "category": "Etek",
    "color": "Siyah",
    "size": "Medium",
    "gender": "Kadın",
    "features": "Pileli"
}}
"""
    response = model.generate_content(prompt)
    return extract_json_from_response(response.text)
import sys
import json
from services.file_extractor import extract_text_from_file
from services.groq_merchant_analysis import analyze_bank_statement

def run():
    file_path = "uploads/20260314_072423_satyam.pdf"
    with open(file_path, "rb") as f:
        content = f.read()

    print("Extracting text...")
    text = extract_text_from_file(content, "satyam.pdf")
    
    print("Running Groq analysis on Satyam's actual data...")
    result = analyze_bank_statement(text, "Satyam")
    
    with open("satyam_real_result.json", "w", encoding="utf-8") as fw:
        json.dump(result, fw, indent=4)
    print("Done! Saved to satyam_real_result.json")

if __name__ == "__main__":
    run()

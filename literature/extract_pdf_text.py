import pdfplumber
import os

# Directory containing the papers
papers_dir = os.path.join(os.path.dirname(__file__), 'papers')
output_dir = os.path.dirname(__file__)

# List of PDF files to extract (add more if needed)
papers = [
    "CloudEx-A_Fair_Access_Financial_Exchange_in_the_Cloud.pdf",
    "Jasper-Scalable_and_Fair_Multicast_for_Financial_Exchanges_in_the_Cloud.pdf",
    "DBO-Fairness_for_Cloud_Hosted_Financial_Exchanges.pdf"
]

def extract_text(pdf_path, out_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                all_text += page_text + "\n\n"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(all_text)
    print(f"Extracted text from {os.path.basename(pdf_path)} to {os.path.basename(out_path)}")

if __name__ == "__main__":
    for paper in papers:
        pdf_path = os.path.join(papers_dir, paper)
        out_name = paper.replace(".pdf", ".txt")
        out_path = os.path.join(output_dir, out_name)
        if os.path.exists(pdf_path):
            extract_text(pdf_path, out_path)
        else:
            print(f"File not found: {pdf_path}")

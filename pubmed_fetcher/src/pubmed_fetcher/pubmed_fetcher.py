import requests
import csv
import xml.etree.ElementTree as ET
import re

# 🔹 Add your PubMed API Key here
PUBMED_API_KEY = "d9d0d751b28c5ea0ca7437a150e0d5a33e08"

# 🔹 Search for PubMed articles
def search_pubmed(query, debug=False):
    """Searches PubMed and returns a list of article IDs."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": 5,  # Limit to 5 results for testing
        "api_key": PUBMED_API_KEY,
        "format": "json"
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if debug:
        print("🔍 PubMed API Response:", data)

    return data.get("esearchresult", {}).get("idlist", [])

# 🔹 Extract email from text
def extract_email(text):
    """Extract email addresses from text."""
    if not text:
        return "N/A"
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    return "; ".join(emails) if emails else "N/A"

# 🔹 Fetch article details using EFetch (full metadata)
def get_paper_details(pubmed_id, debug=False):
    """Fetches details for a given PubMed article ID."""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": pubmed_id,
        "api_key": PUBMED_API_KEY,
        "retmode": "xml"
    }

    response = requests.get(base_url, params=params)
    root = ET.fromstring(response.content)

    # Extracting the article title
    title = root.find(".//ArticleTitle")
    title = title.text if title is not None else "N/A"

    # Extracting the publication date
    pub_date = root.find(".//PubDate/Year")
    pub_date = pub_date.text if pub_date is not None else "N/A"

    # Extracting author details
    authors = []
    affiliations = []
    emails = []

    for author in root.findall(".//Author"):
        last_name = author.find("LastName")
        fore_name = author.find("ForeName")

        name = f"{fore_name.text} {last_name.text}" if fore_name is not None and last_name is not None else "N/A"
        authors.append(name)

        aff_element = author.find("AffiliationInfo/Affiliation")
        if aff_element is not None:
            affiliations.append(aff_element.text)
            emails.append(extract_email(aff_element.text))  # Extract email from affiliation

    return {
        "PubMed ID": pubmed_id,
        "Title": title,
        "Publication Date": pub_date,
        "All Authors": ", ".join(authors) if authors else "N/A",
        "All Affiliations": "; ".join(affiliations) if affiliations else "N/A",
        "Authors Emails": "; ".join(filter(lambda x: x != "N/A", emails)) or "N/A"
    }

# 🔹 Main function to fetch and save data
def fetch_and_save_pubmed_data(query, filename=None, debug=False):
    """Fetch PubMed papers and save to CSV if filename is given."""
    pubmed_ids = search_pubmed(query, debug)
    
    if not pubmed_ids:
        print("❌ No results found.")
        return

    papers = [get_paper_details(pubmed_id, debug) for pubmed_id in pubmed_ids]
    papers = [paper for paper in papers if paper]

    if not papers:
        print("❌ No detailed data found for the results.")
        return

    # ✅ Only save CSV if -f is given
    if filename:
        save_to_csv(papers, filename)
        print(f"\n✅ Results saved to {filename}")
    else:
        print("\n🔹 PubMed Results (Console Output):\n")
        for paper in papers:
            print(f"🆔 PubMed ID: {paper['PubMed ID']}")
            print(f"📖 Title: {paper['Title']}")
            print(f"📅 Publication Date: {paper['Publication Date']}")
            print(f"👥 Authors: {paper['All Authors']}")
            print(f"🏢 Affiliations: {paper['All Affiliations']}")
            print(f"📧 Emails: {paper['Authors Emails']}")
            print("=" * 60)    

# 🔹 Save data to CSV
def save_to_csv(papers, filename):
    """Saves the research papers to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=papers[0].keys())
        writer.writeheader()
        writer.writerows(papers)

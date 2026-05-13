# Certification and Commendation Extractor Skill

## Overview
This skill automates the extraction of detailed information from certification and written commendation PDF documents, organizing the data into an AI-optimized Excel workbook. The extracted data includes exact certificate names, course names, course numbers, dates, organizations, credits/hours earned, names on certificates, sponsoring organizations, instructor names, and relevance assessments for various investigative roles.

## Purpose
The primary purpose of this skill is to streamline the process of compiling professional credentials and commendations into a structured, machine-readable format. This enables efficient utilization by various AI platforms (e.g., Manus, Claude.ai, ChatGPT, Perplexity, Gemini, CoPilot, Notion) for tasks such as:
- Tailoring resumes and cover letters to specific job descriptions (e.g., Fraud Investigator, Digital Forensic Analyst, Fraud Analyst).
- Populating investigative portfolios with relevant experience.
- Analyzing career progression and skill development.
- Generating customized content for LinkedIn profiles or other professional platforms.

## Usage
To use this skill, provide a collection of PDF documents containing certifications and written commendations. The skill will perform the following steps:

1.  **PDF to Image Conversion**: Each page of the provided PDF documents will be converted into a high-resolution image for optimal OCR processing.
2.  **OCR and Data Extraction**: Optical Character Recognition (OCR) will be performed on each image to extract raw text. This text will then be parsed by an AI model to identify and extract specific fields such as:
    *   `source_document`: Original PDF filename.
    *   `page_number`: Page number within the original PDF.
    *   `record_type`: (e.g., Certificate/Training, Commendation, Continuation, Blank/Unreadable).
    *   `document_title`: Exact title of the certificate or document.
    *   `course_name`: Exact course, training, or seminar name.
    *   `course_number`: Course ID, certificate number, or POST number.
    *   `date`: Exact completion or issue date.
    *   `hours_credits`: Hours, credits, or CEU/POST values.
    *   `name_on_document`: Name of the individual on the document.
    *   `issuing_org`: Organization that issued the document.
    *   `sponsoring_org`: Sponsoring organization (if different).
    *   `instructor_names`: Semicolon-separated list of instructor names.
    *   `signatory_names`: Semicolon-separated list of signatory names.
    *   `summary`: A one-sentence summary of the achievement.
    *   `relevance_fraud_financial_crimes`: Relevance to Fraud/Financial Crimes roles (High, Medium, Low, Not applicable).
    *   `relevance_cybersecurity_digital_forensics`: Relevance to Cybersecurity/Digital Forensics roles (High, Medium, Low, Not applicable).
    *   `relevance_osint`: Relevance to OSINT roles (High, Medium, Low, Not applicable).
    *   `relevance_investigative_interviewing`: Relevance to Investigative Interviewing roles (High, Medium, Low, Not applicable).
    *   `relevance_workflow_automation_ai_productivity`: Relevance to Workflow Automation/AI Productivity roles (High, Medium, Low, Not applicable).
    *   `relevance_evidence_organization_analysis`: Relevance to Evidence Organization/Structured Analysis roles (High, Medium, Low, Not applicable).
    *   `relevance_supervision_leadership`: Relevance to Supervision/Leadership roles (High, Medium, Low, Not applicable).
    *   `relevance_general_law_enforcement`: Relevance to General Law Enforcement roles (High, Medium, Low, Not applicable).
    *   `confidence`: A numerical score (0.00-1.00) indicating the confidence level of the extraction.
    *   `extraction_notes`: Any notes regarding unreadable text, issues, or context.

3.  **Excel Workbook Generation**: The extracted and structured data will be compiled into a single Excel workbook (`.xlsx` format). This workbook will feature:
    *   A primary sheet containing all extracted data with clearly labeled columns.
    *   Auto-adjusted column widths for readability.
    *   Pre-defined relevance categories to facilitate AI-driven content generation for specific job roles.

## Integration with GitHub
This skill is designed to integrate with your GitHub repository (`hokster-4849/investigative-portfolio` and `troyhokanson/troy-hokanson-resume-cover-cv`) to support automated document generation. Once the Excel workbook is created, it can be committed to your repository. You can then configure GitHub Actions or similar automation workflows to:

*   **Trigger Document Generation**: Automatically generate tailored resumes, cover letters, or portfolio sections when specific keywords (e.g., "build resume for fraud investigator") are detected in issues, pull requests, or other repository events.
*   **AI Platform Integration**: Utilize the structured data in the Excel workbook as a source for various AI platforms to generate highly customized content based on job descriptions and desired role relevance.

## Future Enhancements
*   **Automated Relevance Scoring**: Further refine AI models for more precise and automated relevance scoring across a broader range of job roles.
*   **Direct GitHub Commit**: Implement direct commit functionality for the generated Excel workbook to a specified GitHub repository.
*   **Dynamic Document Generation Templates**: Develop templates within the skill to generate various document types (resumes, cover letters, LinkedIn summaries) directly from the Excel data based on user-defined parameters.

## Dependencies
*   `pandas`
*   `openpyxl`
*   `xlsxwriter`
*   `openai`
*   `Pillow` (PIL Fork)
*   `poppler-utils` (for `pdftoppm`)
*   `tesseract-ocr` and `tesseract-ocr-eng`

## Example Workflow
1.  Upload PDF documents to the sandbox.
2.  Run the skill, providing the paths to the PDF documents.
3.  The skill processes the PDFs, extracts data, and generates an Excel workbook.
4.  The Excel workbook is saved to `/home/ubuntu/cert_comm_project/certifications_commendations.xlsx`.
5.  Commit the Excel workbook to your GitHub repository.
6.  Utilize the structured data in the Excel workbook with your preferred AI platform for tailored content generation.

# SAP CPI Interface Design Document Generator

An AI-powered documentation generator for **SAP Integration Suite (Cloud Integration)** that automatically analyzes SAP CPI Integration Flow (iFlow) packages and generates professional Solution Design Documents in Microsoft Word format.

---

## Overview

Creating Interface Design Documents for SAP CPI interfaces is a repetitive and time-consuming task. This project automates the documentation process by parsing exported SAP CPI iFlow ZIP packages, analyzing their structure, and generating comprehensive technical documentation using Google's Gemini AI.

The generated document follows a professional consulting-style format and includes interface details, architecture overview, process flow, security considerations, monitoring, business benefits, and more.

---

## Features

- Parse SAP CPI iFlow ZIP packages
- Extract Interface Metadata
- Parse BPMN Components and Integration Flow
- Analyze Adapters, Connections, and Properties
- AI-generated Interface Design Documentation using Gemini AI
- Automatically Generate Process Flow Diagrams using Graphviz
- Professional Microsoft Word Document Generation
- Branded Cover Page
- Interface Summary
- Dynamic Page Numbering
- Professional Headers & Footers
- Clean Consultant-style Formatting

---

## Generated Documentation Includes

- Cover Page
- Interface Summary
- Introduction
- Business Context
- Business Challenges
- Proposed Solution
- Solution Architecture
- End-to-End Integration Flow
- Process Flow Diagram
- Security Design
- Monitoring & Error Handling
- Business Benefits
- Assumptions
- Limitations
- Recommendations
- Conclusion

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| Python | Core Development |
| SAP Integration Suite | Source iFlow Packages |
| Google Gemini 2.5 Flash | AI Documentation Generation |
| Graphviz | Process Flow Diagram Generation |
| python-docx | Microsoft Word Document Generation |
| lxml | XML Parsing |
| Pydantic | Data Models |
| Pillow | Image Processing |

---

## Project Structure

```
SAP_CPI_Doc_Generator/
│
├── ai/
├── analyzer/
├── builder/
├── generator/
│   ├── sections/
│   └── diagram_generator.py
├── models/
├── parser/
├── utils/
├── output/
├── config.py
├── main.py
└── requirements.txt
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/DarkKing-Lab/SAP_CPI_Doc_Generator.git
```

Navigate to the project

```bash
cd SAP_CPI_Doc_Generator
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Update your Gemini API Key inside `config.py`

```python
GEMINI_API_KEY = "YOUR_API_KEY"
```

---

## Usage

Run the application

```bash
python main.py
```

Provide the exported SAP CPI iFlow ZIP package when prompted.

The generated documentation will be available in:

```
output/
```

---

## Workflow

```
SAP CPI ZIP
      │
      ▼
Read ZIP Package
      │
      ▼
Parse XML & BPMN
      │
      ▼
Analyze Interface
      │
      ▼
Generate JSON
      │
      ▼
Generate Process Flow Diagram
      │
      ▼
Generate AI Documentation
      │
      ▼
Generate Microsoft Word Solution Design Document
```

---

## Sample Output

The generated document contains:

- Professional Cover Page
- Interface Summary
- AI-generated Technical Documentation
- Process Flow Diagram
- Consultant-style Formatting

---

## Future Enhancements

- AI-generated Process Flow Images
- PDF Export
- Web-based User Interface
- Batch Processing of Multiple Interfaces
- Custom Document Templates
- Support for Additional SAP Integration Artifacts

---

## Requirements

- Python 3.11+
- Graphviz
- Google Gemini API Key

---

## Author

**Srivastav Cheekoti**

---

## License

This project is intended for educational, learning, and demonstration purposes.

import json
import re

from ai.document_context import build_document_context


class DocumentGenerator:

    def __init__(self, llm):

        self.llm = llm

    # =====================================================
    # Generate AI Documentation
    # =====================================================

    def generate(self, interface):

        # print("\n========== AI Documentation ==========\n")

        # Build structured context
        context = build_document_context(interface)

        print("Preparing AI prompt...")

        prompt = self._build_prompt(context)

        print("Calling Gemini...\n")

        response = self.llm.generate(prompt)

        print("AI response received.\n")

        return self._parse_json(response)
    
    # =====================================================
    # Prompt Builder
    # =====================================================

    def _build_prompt(self, context):

        interface = context.get("interface", {})
        document = context.get("document", {})

        return f"""
You are a Senior SAP Integration Suite (SAP CPI) Solution Architect with more than 15 years of enterprise consulting experience.

You are preparing a customer-facing Solution Design Document (SDD).

The document should look like it was written by an SAP consulting company.

===========================================================
DOCUMENT INFORMATION
===========================================================

Title:
{document.get("title", interface.get("name", "Unknown Interface"))}

Document Type:
SAP Integration Suite Solution Design Document

Version:
{document.get("version", "1.0")}

===========================================================
IMPORTANT RULES
===========================================================

1. Use the Interface Name exactly as provided.

2. Never refer to the interface as:
   - Integration Process
   - Process
   - iFlow

3. Never invent information.

Only use information explicitly available in the parsed interface.

Do NOT invent:

• API names

• Endpoint URLs

• Authentication methods

• Adapter names

• External systems

• Business processes

If information is unavailable, write "Not Available".

4. Keep the document concise.

5. Avoid repeating information between sections.

6. Use professional SAP consulting language.

7. Paragraphs should not exceed four sentences.

8. Prefer bullet points wherever appropriate.

9. Do not mention AI, LLM, Gemini, ChatGPT or automation.

10. Return ONLY valid JSON.

===========================================================
GENERATE THE FOLLOWING SECTIONS
===========================================================

Return EXACTLY this JSON structure.

{{
    "purpose": "",
    "scope": "",
    "business_context": "",
    "business_challenges": [],
    "solution_summary": "",
    "architecture_overview": "",
    "process_description": "",
    "security_design": "",
    "monitoring": "",
    "error_handling": "",
    "business_benefits": [],
    "assumptions": [],
    "limitations": [],
    "recommendations": [],
    "conclusion": ""
}}

===========================================================
SECTION GUIDELINES
===========================================================

Purpose

Explain the objective of the interface in one concise paragraph.

-----------------------------------------------------------

Scope

Describe what the interface covers and what is outside its scope.

Maximum two short paragraphs.

-----------------------------------------------------------

Business Context

Explain

• Why the interface exists

• Which business process it supports

• What business problem it solves

Maximum two paragraphs.

-----------------------------------------------------------

Business Challenges

Return 4–6 concise bullet points.

-----------------------------------------------------------

Solution Summary

Describe the proposed SAP Integration Suite solution.

Focus on the overall integration rather than implementation details.

-----------------------------------------------------------

Architecture Overview

Explain the architecture at a high level.

Mention only components explicitly present in the parsed context.

-----------------------------------------------------------

Process Flow

Return ONLY a JSON array.

Each element must follow this structure:

{{
    "title": "",
    "description": ""
}}

Example:

[
    {{
        "title": "Receive Source Data",
        "description": "The integration begins when the sender system transmits the business payload through the configured sender adapter."
    }},
    {{
        "title": "Message Preparation",
        "description": "The payload is validated and enriched using Content Modifier components before proceeding to the transformation stage."
    }},
    {{
        "title": "Data Transformation",
        "description": "The payload is transformed into the required target structure using mapping logic and custom processing where applicable."
    }}
]

Requirements:

• Generate between 6 and 10 steps.

• Each step must contain a meaningful business-oriented title.

• Each description should be between 2 and 4 sentences.

• Explain what happens during that stage of the integration.

• Follow the actual execution order of the iFlow.

• Do NOT simply list CPI component names.

• Use professional SAP consulting language.

Security Design

Describe only observable security mechanisms.

If unavailable, write "Not Available".

-----------------------------------------------------------

Monitoring

Describe logging, monitoring and operational visibility only if evident.

-----------------------------------------------------------

Error Handling

Describe exception handling only if it exists in the parsed interface.

-----------------------------------------------------------

Business Benefits

Return 4–6 concise bullet points.

-----------------------------------------------------------

Assumptions

Return 3–5 concise bullet points.

-----------------------------------------------------------

Limitations

Return 3–5 concise bullet points.

-----------------------------------------------------------

Recommendations

Return 4–6 practical recommendations focusing on:

• Monitoring

• Performance

• Maintainability

• Scalability

-----------------------------------------------------------

Conclusion

Provide a professional conclusion in one short paragraph.

===========================================================
PARSED INTERFACE
===========================================================

{json.dumps(context, indent=2)}

"""
    
    # =====================================================
    # Parse AI Response
    # =====================================================

    def _parse_json(self, response):

        if not response:

            print("No response received from AI.")

            return self._empty_document()

        response = response.strip()

        # -------------------------------------------------
        # Remove Markdown code blocks
        # -------------------------------------------------

        response = re.sub(
            r"```json",
            "",
            response,
            flags=re.IGNORECASE
        )

        response = re.sub(
            r"```",
            "",
            response
        )

        response = response.strip()

        # -------------------------------------------------
        # Extract JSON
        # -------------------------------------------------

        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:

            response = response[start:end + 1]

        else:

            # print("No JSON object found in AI response.")

            return self._empty_document()

        # -------------------------------------------------
        # Parse JSON
        # -------------------------------------------------

        try:

            data = json.loads(response)

            # print("AI JSON parsed successfully.\n")

            return data

        except json.JSONDecodeError as ex:

            print("Failed to parse AI JSON.")
            print(ex)

            print("\nRaw AI Response:\n")
            print(response)

            return self._empty_document()

        except Exception as ex:

            # print("Unexpected AI parsing error.")
            # print(ex)

            return self._empty_document()
        
    # =====================================================
    # Empty AI Document
    # =====================================================

    def _empty_document(self):

        # print("Using empty AI document template.\n")

        return {

            "purpose": "Not Available",

            "scope": "Not Available",

            "business_context": "Not Available",

            "business_challenges": [],

            "solution_summary": "Not Available",

            "architecture_overview": "Not Available",

            "process_flow": [],

            "security_design": "Not Available",

            "monitoring": "Not Available",

            "error_handling": "Not Available",

            "business_benefits": [],

            "assumptions": [],

            "limitations": [],

            "recommendations": [],

            "conclusion": "Not Available"

        }
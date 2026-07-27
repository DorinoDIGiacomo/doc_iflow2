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
===========================================================
ROLE
===========================================================

You are a Senior SAP Integration Suite (SAP Cloud Integration)
Solution Architect with over 15 years of experience delivering
enterprise integration solutions for SAP and heterogeneous system
landscapes.

You are preparing a customer-facing Interface Design Document (IDD)
that should resemble documentation produced by a leading SAP
consulting organization.

The document must be technically accurate, professionally written,
easy to understand, and suitable for:

• Solution Architects
• Integration Developers
• Functional Consultants
• Technical Consultants
• Test Engineers
• Support Teams
• Project Stakeholders

===========================================================
DOCUMENT INFORMATION
===========================================================

Title:
{document.get("title", interface.get("name", "Unknown Interface"))}

Document Type:
SAP Integration Suite Interface Design Document

Version:
{document.get("version", "1.0")}

===========================================================
OBJECTIVE
===========================================================

Generate a comprehensive Interface Design Document based ONLY on
the parsed SAP Integration Suite interface metadata supplied at
the end of this prompt.

The documentation should explain both the business purpose and
technical implementation of the interface in a consulting style.

The output should read as if it were prepared by an experienced
SAP Integration Architect.

===========================================================
GLOBAL RULES
===========================================================

1. Use the Interface Name exactly as supplied.

2. Never refer to the interface as:
   • Integration Process
   • Process
   • iFlow

3. Never mention:
   • AI
   • LLM
   • Gemini
   • ChatGPT
   • Machine-generated documentation

4. Never fabricate technical information including:

   • Endpoint URLs
   • Host names
   • Credentials
   • Authentication mechanisms
   • API Names
   • Adapter Types that are not present
   • External systems not present in the parsed metadata

5. Avoid generic statements.

Every paragraph should be specific to this interface.

6. Avoid repeating the same explanation across multiple sections.

7. Use professional SAP terminology.

8. Write detailed documentation instead of short summaries.

9. Prefer complete paragraphs over single sentences.

10. Return ONLY valid JSON.

===========================================================
INFERENCE POLICY
===========================================================

The parsed interface may not explicitly contain all business
information.

Apply the following decision process.

LEVEL 1 — Explicit Information

If information exists in the parsed interface,
use it exactly as provided.

LEVEL 2 — Reasonable Technical Inference

If information is not explicitly available but can be
reasonably concluded from the integration design,
provide a professional explanation.

Examples include:

• Overall integration objective

• Data movement direction

• Transformation purpose

• Routing behaviour

• Monitoring considerations

• High-level architecture

• Business value

These should be described using neutral SAP consulting language.

LEVEL 3 — Unknown

Return "Not Available" ONLY when absolutely no
reasonable conclusion can be drawn without inventing facts.

Never infer:

• URLs

• Credentials

• Authentication methods

• Company-specific business processes

• External applications not present in the metadata

• Adapter types that are not parsed

===========================================================
OUTPUT FORMAT
===========================================================

Return EXACTLY one JSON object using the following schema.

{{
    "purpose": "",
    "scope": "",
    "business_context": "",
    "business_challenges": [],
    "solution_summary": "",
    "architecture_overview": "",
    "process_flow": [],
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

PURPOSE

Describe the primary objective of the interface.

Include:

• Why the interface exists.
• What business data is exchanged.
• The overall business objective.
• The value delivered by the integration.

Write 1–2 detailed paragraphs using SAP consulting terminology.

-----------------------------------------------------------

SCOPE

Describe:

• What the integration covers.
• The source and target communication.
• Major processing activities.
• What is intentionally outside the scope of this interface.

Avoid generic wording.

Maximum two paragraphs.

-----------------------------------------------------------

BUSINESS CONTEXT

Based on the parsed interface, explain the operational scenario
supported by this integration.

If the exact business process is unknown, describe it using
neutral terminology such as:

• business transaction
• master data synchronization
• transactional data exchange
• business document processing
• enterprise integration

Do NOT invent company-specific processes.

Maximum two paragraphs.

-----------------------------------------------------------

BUSINESS CHALLENGES

Return between 4 and 6 concise bullet points describing
typical integration challenges addressed by this interface.

Examples include:

• Manual processing
• Duplicate data
• Delayed synchronization
• Lack of automation
• Data consistency
• Process visibility

Do not invent company-specific challenges.

-----------------------------------------------------------

SOLUTION SUMMARY

Describe the complete SAP Integration Suite solution.

Explain:

• Sender
• Receiver
• Message flow
• Integration approach
• Processing logic
• Transformation
• Routing
• Overall design philosophy

Write 2–3 paragraphs.

-----------------------------------------------------------

ARCHITECTURE OVERVIEW

Describe how the components collaborate.

When present, explain:

• Sender Adapter
• Receiver Adapter
• Request Reply
• Router
• Content Modifier
• Groovy Script
• Message Mapping
• XSLT Mapping
• Splitter
• Aggregator
• Multicast
• Exception Subprocess
• Data Store
• Value Mapping

Do NOT list components.

Explain their interaction.

Write 2–3 paragraphs.

-----------------------------------------------------------

PROCESS FLOW

Return a JSON array.

Each object must contain:

{{
    "title": "",
    "description": ""
}}

Generate between 6 and 10 sequential processing steps.

Each title should represent a business activity rather than a CPI
component.

Examples:

Receive Business Request

Retrieve Business Data

Validate Incoming Payload

Enrich Business Information

Transform Message Structure

Determine Processing Route

Invoke Target System

Handle Response

Update Processing Status

Complete Integration

Each description should contain between 2 and 4 complete
sentences explaining:

• What happens.
• Why it happens.
• Expected outcome.

Never simply list CPI components.

Always describe the business purpose of each stage.

-----------------------------------------------------------

SECURITY DESIGN

Describe observable security mechanisms only.

If authentication is visible in the metadata,
explain it.

Otherwise provide a neutral statement such as:

"The parsed interface does not explicitly expose the security
configuration. Standard SAP Integration Suite security mechanisms
are expected to be applied."

-----------------------------------------------------------

MONITORING

Describe operational monitoring.

Mention only capabilities evident from the interface such as:

• Logging
• Exception subprocess
• Data Store
• JMS
• Status updates
• Message persistence
• Operational traceability

If none are evident,
provide a neutral monitoring statement.

-----------------------------------------------------------

ERROR HANDLING

Describe the exception handling strategy.

Mention:

• Exception Subprocess
• Retry logic
• Logging
• Error persistence
• Notifications

Only when present.

Otherwise state that explicit exception handling
could not be identified.

-----------------------------------------------------------

BUSINESS BENEFITS

Return between 5 and 7 concise bullet points.

Focus on:

• Automation

• Faster processing

• Reduced manual effort

• Better integration

• Improved data consistency

• Operational efficiency

-----------------------------------------------------------

ASSUMPTIONS

Return between 4 and 6 concise bullet points.

Include only reasonable assumptions based on the parsed
interface.

-----------------------------------------------------------

LIMITATIONS

Return between 4 and 6 concise bullet points.

Mention only realistic technical limitations that can reasonably
apply to the integration design.

-----------------------------------------------------------

RECOMMENDATIONS

Return between 5 and 8 practical recommendations.

Focus on:

• Performance

• Monitoring

• Maintainability

• Scalability

• Security

• Reusability

Recommendations should be actionable.

-----------------------------------------------------------

CONCLUSION

Provide a professional closing summary.

Explain:

• Overall solution value.

• Integration quality.

• Business contribution.

Write one well-structured paragraph.

===========================================================
WRITING STYLE
===========================================================

Follow these writing principles throughout the document.

• Write like an experienced SAP Integration Architect.

• Maintain a professional consulting tone.

• Avoid repetitive explanations.

• Ensure every section contributes unique information.

• Prefer complete paragraphs over isolated sentences.

• Use bullet points where they improve readability.

• Do not include placeholder text.

• Do not mention missing information unless absolutely necessary.

• Never mention AI, LLMs, prompts, or generated content.

• The document should be suitable for customer delivery.

===========================================================
QUALITY CHECKS
===========================================================

Before generating the response, ensure that:

✓ Every section contains meaningful content.

✓ Purpose, Scope and Business Context are distinct.

✓ Solution Summary and Architecture Overview are not duplicates.

✓ Recommendations are practical and actionable.

✓ Business Benefits focus on business value rather than technical implementation.

✓ Process Flow follows the execution sequence of the integration.

✓ All output is valid JSON.

===========================================================
PARSED INTERFACE CONTEXT
===========================================================

The following JSON represents the parsed SAP Integration Suite
interface.

Use it as the primary source of truth.

Reasonable technical inference is allowed according to the
Inference Policy defined above.

{json.dumps(context, indent=2)}

===========================================================
FINAL INSTRUCTIONS
===========================================================

Generate exactly one JSON object.

Do not wrap the response in Markdown.

Do not include explanations.

Do not include comments.

Do not include headings outside the JSON.

Return only the JSON object.
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
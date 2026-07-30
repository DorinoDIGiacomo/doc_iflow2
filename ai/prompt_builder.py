import json

from models import interface


def build_process_prompt(interface):

    # Build a lookup of BPMN ID -> Component
    
    component_lookup = {
        component.id: component
        for component in interface.components
    }

    previous_lookup = {}
    next_lookup = {}

    for connection in interface.connections:
        source_component = component_lookup.get(connection.source)
        target_component = component_lookup.get(connection.target)

        if source_component and target_component:
            
            next_lookup[source_component.id] = target_component.name
            previous_lookup[target_component.id] = source_component.name

    components = []

    for index, component in enumerate(interface.components, start=1):

        component_type = component.category

        # Replace generic callActivity with its actual activity type
        if component_type == "callActivity":
            component_type = component.properties.get(
                "activityType",
                component.category
            )

        components.append({
            "step": index,
            "component_type": component_type,
            "component_name": component.name,
            "previous_component": previous_lookup.get(component.id),
            "next_component": next_lookup.get(component.id),
            "properties": component.properties,
            "analysis": component.analysis
        })

    return f"""
You are an SAP Integration Suite Solution Architect.

Based on the list of SAP CPI components below, generate a JSON array.

Each JSON object must contain EXACTLY these fields:

[
  {{
    "step": 1,
    "component_type": "",
    "component_name": "",
    "title": "",
    "description": "",
    "icon": ""
  }}
]

Rules:

Rules:

1. Generate ONLY 6 to 10 sequential business process steps.

2. DO NOT create one step for every SAP CPI component.

3. Instead, analyze the complete integration flow and group related technical components into one meaningful business stage.

4. The output should explain the integration from start to finish as an end-to-end business process.

5. Each JSON object must contain:

[
  {{
    "step": 1,
    "component_type": "",
    "component_name": "",
    "title": "",
    "description": "",
    "icon": ""
  }}
]

6. The fields component_type and component_name are required only for internal traceability.

Choose the highest-level logical activity instead of technical SAP CPI components.

Avoid values such as:

- Content Modifier
- Groovy Script
- Message Mapping
- XML to JSON Converter
- JSON to XML Converter
- ProcessCallElement
- General Splitter
- Gather
- Router
- Request Reply

Instead prefer logical business activities such as:

- Source Reception
- Data Validation
- Data Transformation
- Business Processing
- SAP Communication
- Response Processing
- Result Aggregation
- Output Delivery

7. The title must contain between 3 and 7 words.

Examples:

Receive Source Request

Validate and Prepare Data

Transform Business Payload

Process Business Records

Invoke Target System

Handle System Response

Generate Processing Result

Complete Integration

8. Each description must:

• Contain exactly ONE sentence.
• Be between 15 and 25 words.
• Describe only the business activity.
• Explain WHAT happens, not HOW it is implemented.
• Be suitable for displaying inside a process flow diagram.

9. Never mention SAP CPI components in either the title or the description.

Do NOT use titles like:

- Content Modifier
- Groovy Script
- Router
- Splitter
- Message Mapping
- XML Converter
- JSON Converter
- Request Reply

Instead describe the business activity.

10. Merge related technical components into one business stage whenever appropriate.

11. Think like an SAP Functional Consultant, not a CPI Developer.

Describe business activities and business outcomes rather than middleware implementation details.

12. Return ONLY valid JSON.

13. Do NOT wrap the response in Markdown.

Components:

{json.dumps(components, indent=2)}
"""
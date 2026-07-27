import os


class SystemLandscapeGenerator:

    def __init__(self, llm):
        self.llm = llm

    def generate(self, interface):

        sender = interface.sender_systems[0] if interface.sender_systems else "Source System"

        receiver = interface.receiver_systems[0] if interface.receiver_systems else "Target System"

        prompt = f"""
Create a professional SAP Integration Suite system landscape diagram.

Style:
- Flat vector
- Enterprise architecture
- SAP blue theme
- White background
- Clean labels
- High quality
- Technical documentation style

Interface:
{interface.name}

Sender System:
{", ".join(interface.sender_systems) if interface.sender_systems else "Unknown"}

Sender Adapter:
{", ".join(interface.sender_adapters) if interface.sender_adapters else "Unknown"}

Integration Platform:
SAP Integration Suite

Receiver System:
{", ".join(interface.receiver_systems) if interface.receiver_systems else "Unknown"}

Receiver Adapter:
{", ".join(interface.receiver_adapters) if interface.receiver_adapters else "Unknown"}

Protocols:
{", ".join(interface.protocols)}

Authentication:
{", ".join(interface.authentication)}

Message Format:
{", ".join(interface.message_formats)}

Show message flow with arrows.
Use SAP architecture icons.
Professional solution design documentation style.
"""

        output = os.path.join(
            "output",
            "system_landscape.png"
        )

        return self.llm.generate_image(
            prompt,
            output
        )
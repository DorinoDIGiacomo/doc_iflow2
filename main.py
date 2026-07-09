from pathlib import Path
from docx import document
from parser.zip_reader import read_zip
from parser.xml_reader import parse_iflow
from parser.bpmn_parser import parse_bpmn
from parser.metadata_parser import parse_metadata
from parser.flow_parser import parse_flows
from parser.property_parser import parse_properties
from analyzer.interface_analyzer import analyze_interface
from analyzer.adapter_analyzer import analyze_adapters
from analyzer.flow_analyzer import analyze_connections
from builder.interface_builder import build_json
from generator.word_generator import generate_word
from ai.gemini_client import GeminiClient
from ai.generate_document import DocumentGenerator
from config import GEMINI_API_KEY, MODEL
from generator.diagram_generator import generate_process_flow

def main():

    print("======================================")
    print(" SAP CPI Solution Design Generator")
    print("======================================\n")

    zip_path = input("Enter ZIP file path: ")

    # ==========================================================
    # Read ZIP
    # ==========================================================

    interface = read_zip(zip_path)

    # ==========================================================
    # Interface Name from ZIP File
    # ==========================================================

    interface.name = Path(zip_path).stem

    print("\nInterface Name :", interface.name)

    # ==========================================================
    # Interface Summary
    # ==========================================================

    # print("\n========== Interface Summary ==========\n")

    # print("iFlow XML       :", interface.iflow_xml != "")
    # print("Groovy Scripts  :", len(interface.resources["groovy"]))
    # print("Mappings        :", len(interface.resources["mapping"]))
    # print("XSD Files       :", len(interface.resources["xsd"]))
    # print("WSDL Files      :", len(interface.resources["wsdl"]))
    # print("EDMX Files      :", len(interface.resources["edmx"]))
    # print("Properties      :", len(interface.resources["properties"]))
    # print("Other Files     :", len(interface.resources["other"]))

    # ==========================================================
    # Parse XML
    # ==========================================================

    # print("\n========== XML Parser ==========\n")

    root = parse_iflow(interface)

    parse_metadata(root, interface)

    parse_flows(root, interface)

    # print("XML Loaded Successfully")

    # ==========================================================
    # Parse BPMN
    # ==========================================================

    parse_bpmn(root, interface)

    # ==========================================================
    # Parse Properties
    # ==========================================================

    parse_properties(root, interface)

    # ==========================================================
    # Analyze Interface
    # ==========================================================

    analyze_interface(interface)

    analyze_adapters(interface)

    analyze_connections(interface)

    # ==========================================================
    # Export JSON
    # ==========================================================

    build_json(interface)

    # ==========================================================
    # Generate Process Flow Diagram
    # ==========================================================

    generate_process_flow(
        interface,
        "output/process_flow"
    )

    # ==========================================================
    # AI Documentation
    # ==========================================================

    # print("\n========== AI Documentation ==========\n")

    llm = GeminiClient(
        api_key=GEMINI_API_KEY,
        model=MODEL
    )

    document_generator = DocumentGenerator(
        llm
    )

    ai_data = document_generator.generate(interface)

    # print("\n========== AI DATA ==========\n")
    # print(ai_data)

    # ==========================================================
    # Generate Word Document
    # ==========================================================

    generate_word(
        interface=interface,
        output_path="output/SAP_CPI_Solution_Design_Document.docx",
        ai_data=ai_data
    )

    # ==========================================================
    # Final Statistics
    # ==========================================================

    # print("\n========== Final Statistics ==========\n")

    # print("Total Components  :", len(interface.components))
    # print("Total Connections :", len(interface.connections))

    print("\nCompleted Successfully.")


if __name__ == "__main__":
    main()
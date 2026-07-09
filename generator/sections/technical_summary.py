def add_technical_summary(document, interface):

    document.add_heading(
        "Technical Summary",
        level=1
    )

    # =====================================================
    # Count Technical Components
    # =====================================================

    request_reply = 0
    splitters = 0
    routers = 0
    multicasts = 0
    content_modifiers = 0
    mappings = 0
    groovy = 0
    converters = 0
    exception_subprocess = 0

    adapters = set()

    for component in interface.components:

        category = component.category.lower()

        if "request reply" in category:
            request_reply += 1

        elif "splitter" in category:
            splitters += 1

        elif "router" in category:
            routers += 1

        elif "multicast" in category:
            multicasts += 1

        elif "content modifier" in category:
            content_modifiers += 1

        elif "mapping" in category:
            mappings += 1

        elif "groovy" in category:
            groovy += 1

        elif "converter" in category:
            converters += 1

        if "exception" in category:
            exception_subprocess += 1

        direction = component.analysis.get(
            "direction",
            ""
        )

        if direction:
            adapters.add(direction)

    # =====================================================
    # Technical Summary Table
    # =====================================================

    table = document.add_table(
        rows=0,
        cols=2
    )

    table.style = "Table Grid"

    def add_row(key, value):

        row = table.add_row().cells

        row[0].text = key

        row[1].text = str(value)

    add_row(
        "Primary Process",
        interface.analysis.get(
            "primary_process",
            "Not Available"
        )
    )

    add_row(
        "Integration Pattern",
        "Synchronous" if request_reply else "Asynchronous"
    )

    add_row(
        "Total Components",
        len(interface.components)
    )

    add_row(
        "Total Connections",
        len(interface.connections)
    )

    add_row(
        "Adapters",
        ", ".join(sorted(adapters)) if adapters else "-"
    )

    add_row(
        "Request Reply Steps",
        request_reply
    )

    add_row(
        "Splitters",
        splitters
    )

    add_row(
        "Routers",
        routers
    )

    add_row(
        "Multicast",
        multicasts
    )

    add_row(
        "Content Modifiers",
        content_modifiers
    )

    add_row(
        "Message Mappings",
        mappings
    )

    add_row(
        "Groovy Scripts",
        groovy
    )

    add_row(
        "Converters",
        converters
    )

    add_row(
        "Exception Subprocess",
        "Yes" if exception_subprocess else "No"
    )

    add_row(
        "External Resources",
        f"XSD={len(interface.resources.get('xsd', []))}, "
        f"WSDL={len(interface.resources.get('wsdl', []))}, "
        f"EDMX={len(interface.resources.get('edmx', []))}"
    )
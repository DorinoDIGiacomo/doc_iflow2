import re


def create_process_summary(description):
    """
    Converts a long AI-generated process description into
    2-3 concise bullet points for the process flow diagram.
    """

    if not description:
        return []

    # Remove line breaks
    description = description.replace("\n", " ")

    # Split into sentences
    sentences = re.split(r'(?<=[.!?])\s+', description)

    bullets = []

    for sentence in sentences:

        sentence = sentence.strip()

        if not sentence:
            continue

        # Remove ending punctuation
        sentence = sentence.rstrip(".!?")

        bullets.append(sentence)

        if len(bullets) == 3:
            break

    return bullets
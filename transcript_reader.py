import os
from docx import Document

try:
    from pypdf import PdfReader
except:
    PdfReader = None


def read_transcript(uploaded_file):

    filename = uploaded_file.filename.lower()

    if filename.endswith(".txt"):

        return uploaded_file.read().decode("utf-8")

    elif filename.endswith(".docx"):

        temp_file = "temp.docx"

        uploaded_file.save(temp_file)

        doc = Document(temp_file)

        text = "\n".join(
            para.text
            for para in doc.paragraphs
        )

        os.remove(temp_file)

        return text

    elif filename.endswith(".pdf"):

        if PdfReader is None:
            raise Exception(
                "PDF support not installed"
            )

        temp_file = "temp.pdf"

        uploaded_file.save(temp_file)

        reader = PdfReader(temp_file)

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        os.remove(temp_file)

        return text

    else:

        raise Exception(
            "Unsupported file type"
        )
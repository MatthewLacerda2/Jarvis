from googlenewsdecoder import gnewsdecoder

def decode(source_url: str):
    interval_time = 1  # interval is optional, default is None

    try:
        decoded_url = gnewsdecoder(source_url, interval=interval_time)

        if decoded_url.get("status"):
            print("Decoded URL:", decoded_url["decoded_url"])
            
            from docling.document_converter import DocumentConverter
            converter = DocumentConverter()
            doc = converter.convert(decoded_url["decoded_url"])
            print(doc.document.export_to_markdown())
            
        else:
            print("Error:", decoded_url["message"])
    except Exception as e:
        print(f"Error occurred: {e}")
import os
import re
import json
import base64
from jinja2 import Environment, FileSystemLoader
from pikepdf import Pdf
from htmlmin import minify

PDF_FOLDER = "pdfs"             # Folder where PDF files are stored
SERIES_DATA_FILE = "series.json"  # Series data file (contains nodes, edges, subseries_colors)
TEMPLATE_FILE = "template.html"
OUTPUT_FILE = "compiled_series.html"

# pdfStore will map node id to its PDF data (as a base64 string)
pdfStore = {}

def compress_and_encode_pdf(pdf_path):
    temp_file = "temp_compressed.pdf"
    with Pdf.open(pdf_path) as pdf:
        pdf.remove_unreferenced_resources()
        pdf.flatten_annotations('screen')
        pdf.save(temp_file, linearize=False, compress_streams=True)
    with open(temp_file, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode("utf-8")
    return f"data:application/pdf;base64,{encoded}"

def load_series_data():
    with open(SERIES_DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def embed_pdfs_and_assign_colors(seriesData):
    # Expecting seriesData to have keys: "nodes", "edges", and "subseries_colors"
    subseries_colors = seriesData.get("subseries_colors", {})
    for node in seriesData["nodes"]:
        sub = node.get("subseries", "").lower()
        node["color"] = subseries_colors.get(sub, "#999999")
        # Build regex pattern that matches the prefix: "<id>-" (with optional spaces)
        pattern = re.compile(r"^" + re.escape(str(node['id'])) + r"-\s*", re.IGNORECASE)
        found = False
        for fname in os.listdir(PDF_FOLDER):
            if pattern.match(fname):
                pdf_path = os.path.join(PDF_FOLDER, fname)
                print(f"Embedding PDF for {node['title']} from file: {fname}")
                pdfStore[node["id"]] = compress_and_encode_pdf(pdf_path)
                found = True
                break
        if not found:
            print(f"No PDF found for {node['title']} => using placeholder.")
            # Use a placeholder PDF (could also be a Base64 string directly)
            with open("placeholderpdf.txt", "r", encoding="utf-8") as f:
                pdfStore[node["id"]] = f.read()
        # Remove the pdf field from node data to keep graphData lean.
        node["pdf"] = None

def main():
    seriesData = load_series_data()
    embed_pdfs_and_assign_colors(seriesData)

    # Prepare Jinja2 environment and template
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template(TEMPLATE_FILE)

    # Convert series data and pdfStore to JSON strings
    graph_json = json.dumps(seriesData, ensure_ascii=False)
    pdf_store_json = json.dumps(pdfStore, ensure_ascii=False)

    rendered = template.render(graph_json=graph_json, pdf_store_json=pdf_store_json)
    minified = minify(rendered, remove_comments=True, remove_all_empty_space=True, reduce_boolean_attributes=True, remove_optional_attribute_quotes=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(minified)
    print(f"Created {OUTPUT_FILE}")

if __name__ == "__main__":
    main()

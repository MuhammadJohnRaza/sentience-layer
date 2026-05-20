"""
Parser Wrapper: Layout-Aware PDF Parser and Table Extractor.
Extracts structural blocks, sorted columns, headers, and markdown tables.
"""
import os
import io
import sys
import json
import argparse
from typing import Dict, Any, List

class LayoutAwarePDFParser:
    """
    Parses complex multi-column PDFs, extracting structural headers,
    body text block-by-block (sorted top-to-bottom, left-to-right),
    page ranges, and tables converted to clean GFM markdown.
    """
    def __init__(self, file_path_or_bytes: Any, filename: str = ""):
        self.file_path_or_bytes = file_path_or_bytes
        self.filename = filename or (file_path_or_bytes if isinstance(file_path_or_bytes, str) else "uploaded_document.pdf")
        self.doc = None

    def _open_document(self):
        try:
            import fitz  # PyMuPDF
            if isinstance(self.file_path_or_bytes, str):
                self.doc = fitz.open(self.file_path_or_bytes)
            else:
                self.doc = fitz.open(stream=self.file_path_or_bytes, filetype="pdf")
            return "fitz"
        except ImportError:
            # Fallback to pypdf
            try:
                from pypdf import PdfReader
                if isinstance(self.file_path_or_bytes, str):
                    self.doc = PdfReader(self.file_path_or_bytes)
                else:
                    self.doc = PdfReader(io.BytesIO(self.file_path_or_bytes))
                return "pypdf"
            except ImportError:
                return "none"

    def parse(self) -> Dict[str, Any]:
        engine = self._open_document()
        
        document_metadata = {
            "title": os.path.basename(self.filename),
            "author": "Unknown",
            "pages": 0,
            "engine": engine
        }
        
        if engine == "none":
            return {
                "metadata": document_metadata,
                "sections": [{"title": "Content", "text": "PDF parser dependencies (PyMuPDF or pypdf) not installed.", "pages": [1]}],
                "tables": [],
                "error": "Missing PDF dependencies"
            }

        if engine == "fitz":
            document_metadata["author"] = self.doc.metadata.get("author", "Unknown")
            document_metadata["pages"] = len(self.doc)
            
            parsed_sections = []
            current_section = {"title": "Introduction", "text": "", "pages": [1]}
            tables = []

            for page_num in range(len(self.doc)):
                page = self.doc[page_num]
                
                # Table Extraction
                try:
                    tab_finder = page.find_tables()
                    for idx, table in enumerate(tab_finder):
                        raw_headers = table.header.names
                        rows = table.extract()
                        if not rows:
                            continue
                        
                        # Generate Markdown
                        headers = [h or f"Column_{i}" for i, h in enumerate(raw_headers)]
                        md_table = f"\n| {' | '.join(headers)} |\n"
                        md_table += f"| {' | '.join(['---'] * len(headers))} |\n"
                        for row in rows:
                            if row == raw_headers:
                                continue
                            cells = [cell.replace('\n', ' ').strip() if cell else '' for cell in row]
                            md_table += f"| {' | '.join(cells)} |\n"
                        
                        tables.append({
                            "page": page_num + 1,
                            "table_index": idx,
                            "markdown": md_table
                        })
                except Exception:
                    pass

                # Text Extraction (Layout-Aware)
                text_page = page.get_text("blocks")
                # Sort blocks by vertical position first (top-to-bottom), then horizontal (left-to-right)
                sorted_blocks = sorted(text_page, key=lambda b: (b[1], b[0]))
                
                for block in sorted_blocks:
                    block_text = block[4].strip()
                    if not block_text:
                        continue
                    
                    lines = block_text.split("\n")
                    first_line = lines[0].strip()
                    
                    # Detect potential structural headers
                    is_header = False
                    if len(first_line) < 120:
                        if (first_line.isupper() and len(first_line) > 3) or first_line.startswith(("1.", "2.", "3.", "4.", "5.", "6.", "7.", "8.", "9.", "I.", "II.", "III.", "IV.", "V.")):
                            is_header = True
                    
                    if is_header:
                        if current_section["text"].strip():
                            parsed_sections.append(current_section)
                        current_section = {
                            "title": block_text.replace("\n", " ").strip(),
                            "text": "",
                            "pages": [page_num + 1]
                        }
                    else:
                        # Standardize lists in Markdown
                        cleaned_lines = []
                        for line in lines:
                            cleaned = line.strip()
                            if cleaned.startswith(("•", "*", "-")) and not cleaned.startswith("- "):
                                cleaned = f"- {cleaned[1:].strip()}"
                            cleaned_lines.append(cleaned)
                        
                        current_section["text"] += "\n".join(cleaned_lines) + "\n\n"
                        if (page_num + 1) not in current_section["pages"]:
                            current_section["pages"].append(page_num + 1)

            if current_section["text"].strip():
                parsed_sections.append(current_section)
                
            # Interleave extracted tables into the sections mapping to their page
            for tab in tables:
                page_tab = tab["page"]
                for sec in parsed_sections:
                    if page_tab in sec["pages"] and tab["markdown"] not in sec["text"]:
                        sec["text"] += f"\n\n*Table Extracted from Page {page_tab}:*\n{tab['markdown']}\n"

            return {
                "metadata": document_metadata,
                "sections": parsed_sections,
                "tables": tables
            }

        else:  # pypdf fallback
            document_metadata["pages"] = len(self.doc.pages)
            extracted_text = ""
            for idx, page in enumerate(self.doc.pages):
                page_text = page.extract_text()
                if page_text:
                    extracted_text += f"\n\n--- PAGE {idx+1} ---\n\n" + page_text

            # Create simple structure
            return {
                "metadata": document_metadata,
                "sections": [{
                    "title": "Document Content",
                    "text": extracted_text,
                    "pages": list(range(1, len(self.doc.pages) + 1))
                }],
                "tables": []
            }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Layout-aware PDF extractor wrapper.")
    parser.add_argument("--file-path", required=True, help="Absolute path to target PDF document.")
    args = parser.parse_args()
    
    if not os.path.exists(args.file_path):
        print(json.dumps({"error": f"File not found: {args.file_path}"}))
        sys.exit(1)
        
    pdf_parser = LayoutAwarePDFParser(args.file_path)
    print(json.dumps(pdf_parser.parse(), indent=2))

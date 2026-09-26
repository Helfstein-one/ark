"""
title: Advanced Document Ingestion Skill
author: ark-core
version: 1.0.0
description: Skill for extracting text from PDF and text documents and splitting into semantic chunks.
"""

import os
from typing import Dict, Any, List
import PyPDF2


class DocumentIngester:
    def __init__(self):
        pass

    def sanitize_text(self, text: str) -> str:
        """
        Sanitizes text by removing null bytes, non-printable control characters,
        and handling malformed encodings or invalid characters.
        :param text: Input raw text to sanitize.
        :return: Cleaned string.
        """
        if not text or not isinstance(text, str):
            return ""

        # Remove null bytes
        cleaned = text.replace("\x00", "")

        # Handle surrogate / malformed character encoding issues safely
        cleaned = cleaned.encode("utf-8", "ignore").decode("utf-8", "ignore")

        # Filter non-printable control characters, preserving standard whitespace (\n, \r, \t)
        sanitized_chars = []
        for char in cleaned:
            if char in ("\n", "\r", "\t"):
                sanitized_chars.append(char)
            elif char.isprintable():
                sanitized_chars.append(char)

        return "".join(sanitized_chars)

    def extract_text(self, file_path: str) -> str:
        """
        Extracts raw text from a PDF or plain text file.
        :param file_path: Path to the target document.
        :return: Extracted string content.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext == ".pdf":
            text_content = []
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(page_text)
            return "\n\n".join(text_content)
        else:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()

    def chunk_text(
        self, text: str, chunk_size: int = 500, chunk_overlap: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Splits text into chunks of specified maximum character length with overlap.
        Attempts to make semantic cuts on sentence/paragraph boundaries when possible.
        :param text: Raw text to be chunked.
        :param chunk_size: Target size of each chunk in characters.
        :param chunk_overlap: Overlap size between adjacent chunks in characters.
        :return: List of dicts containing chunk metadata and content.
        """
        sanitized_text = self.sanitize_text(text)
        if not sanitized_text or not sanitized_text.strip():
            return []

        if chunk_overlap >= chunk_size:
            chunk_overlap = max(0, chunk_size - 1)

        cleaned_text = sanitized_text.strip()
        text_length = len(cleaned_text)

        chunks = []
        start = 0
        chunk_index = 0

        while start < text_length:
            end = start + chunk_size

            if end < text_length:
                # Try to break at paragraph boundary first, then sentence boundary, then space
                cut_point = -1
                for delimiter in ["\n\n", "\n", ". ", " "]:
                    pos = cleaned_text.rfind(delimiter, start, end)
                    if pos > start:
                        cut_point = pos + len(delimiter) if delimiter in [". ", " "] else pos
                        break

                if cut_point > start:
                    end = cut_point

            chunk_str = cleaned_text[start:end].strip()
            if chunk_str:
                chunks.append(
                    {
                        "chunk_index": chunk_index,
                        "text": chunk_str,
                        "start_char": start,
                        "end_char": end,
                        "char_count": len(chunk_str),
                    }
                )
                chunk_index += 1

            if end >= text_length:
                break

            start = max(start + 1, end - chunk_overlap)

        return chunks

    def ingest_document(
        self, file_path: str, chunk_size: int = 500, chunk_overlap: int = 50
    ) -> Dict[str, Any]:
        """
        Ingests a document from path, extracts text, and returns semantic chunks.
        :param file_path: Path to the document.
        :param chunk_size: Chunk size in characters.
        :param chunk_overlap: Overlap between chunks in characters.
        :return: Dict containing status, document metadata, total chunks, and chunk list.
        """
        try:
            raw_text = self.extract_text(file_path)
            sanitized_text = self.sanitize_text(raw_text)
            chunks = self.chunk_text(sanitized_text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
            return {
                "status": "SUCCESS",
                "file_path": file_path,
                "total_characters": len(sanitized_text),
                "total_chunks": len(chunks),
                "chunks": chunks,
            }
        except Exception as e:
            return {
                "status": "ERROR",
                "file_path": file_path,
                "error_message": str(e),
            }


class Tools:
    def __init__(self):
        self.ingester = DocumentIngester()

    def ingest_document(
        self, file_path: str, chunk_size: int = 500, chunk_overlap: int = 50
    ) -> Dict[str, Any]:
        return self.ingester.ingest_document(
            file_path=file_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap
        )

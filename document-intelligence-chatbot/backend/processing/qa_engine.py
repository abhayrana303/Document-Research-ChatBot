import os
import re
import requests
from typing import List, Dict
from utils.vector_store import vector_store  # Fixed: correct module path


class QAEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

    # Current Groq model — llama3-8b-8192 was decommissioned.
    # See https://console.groq.com/docs/models for the latest list.
    GROQ_MODEL = "llama-3.1-8b-instant"

    def _call_groq(self, system_prompt: str, user_prompt: str, max_tokens: int = 512, temperature: float = 0.2) -> str:
        """Helper to call Groq API and return response text, or raise on failure."""
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": self.GROQ_MODEL,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                "max_tokens": max_tokens,
                "temperature": temperature,
            },
            timeout=30,
        )
        # Log Groq's error body before raising so the full message is visible in server logs
        if not response.ok:
            print(f"Groq API error {response.status_code}: {response.text}")
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def _extract_citation(self, answer_text: str) -> tuple:
        """Extract citation from answer text and clean up the answer."""
        citation = "Page 1, Paragraph 1"  # Default citation

        patterns = [
            r"(?i)(page\s+\d+,?\s*(?:paragraph|para|p)\s*\d+)",
            r"(?i)(p\.\s*\d+,?\s*(?:paragraph|para|p)\s*\d+)",
            r"(?i)(section\s+[\d.]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, answer_text)
            if match:
                citation = match.group(1)
                answer_text = re.sub(pattern, "", answer_text).strip()
                break

        answer_text = answer_text.rstrip("., ")
        return answer_text, citation

    def process_question(self, question: str, documents: List[Dict]) -> tuple:
        """Process a question against the uploaded documents using RAG."""
        # Use ChromaDB to retrieve relevant chunks for the question
        relevant_chunks = vector_store.query_similar_chunks(question, top_k=5)

        if not relevant_chunks:
            return [{"docId": "N/A", "answer": "No relevant content found in the uploaded documents.", "citation": "N/A"}], []

        context = "\n".join([chunk["text"] for chunk in relevant_chunks])
        prompt = f"""Based on the following context from uploaded documents, answer the question.
Include a citation in the format 'Page X, Paragraph Y' at the end of your answer.

Context:
{context[:3000]}

Question: {question}

Format: Provide a direct answer followed by a citation in parentheses.
Example: The company's revenue grew by 25% in Q2. (Page 3, Paragraph 2)"""

        answers = []
        try:
            answer_text = self._call_groq(
                system_prompt="You are a precise document analysis assistant. Always provide answers with specific citations from the provided context.",
                user_prompt=prompt,
            )
            answer_text, citation = self._extract_citation(answer_text)
            answers.append({
                "docId": relevant_chunks[0]["doc_id"] if relevant_chunks else "N/A",
                "answer": answer_text,
                "citation": citation,
            })
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            answers.append({"docId": "ERROR", "answer": f"Failed to get answer: {str(e)}", "citation": "N/A"})

        # Generate themes — now works correctly since we pass all answers
        themes = []
        if answers and answers[0].get("docId") != "ERROR":
            themes_prompt = f"""Analyze the following answer and the original question, then identify 2-3 key themes.

Question: {question}
Answer: {answers[0]['answer']}

List each theme on a new line as: "Theme: <title> - <brief description>"
"""
            try:
                theme_text = self._call_groq(
                    system_prompt="You are a theme analysis expert. Create concise, clear themes from the given Q&A.",
                    user_prompt=themes_prompt,
                    max_tokens=256,
                    temperature=0.3,
                )
                for i, line in enumerate(theme_text.strip().split("\n")):
                    line = line.strip()
                    if not line:
                        continue
                    # Parse "Theme: title - description" or just use the line as summary
                    if " - " in line:
                        parts = line.split(" - ", 1)
                        title = parts[0].replace("Theme:", "").strip()
                        summary = parts[1].strip()
                    else:
                        title = f"Theme {i + 1}"
                        summary = line
                    themes.append({"title": title, "summary": summary})
            except Exception as e:
                print(f"Error generating themes: {str(e)}")

        return answers, themes
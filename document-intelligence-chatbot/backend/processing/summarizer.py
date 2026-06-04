import os
import requests


class Summarizer:
    """Summarizes a collection of documents using the Groq LLM API."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")

    def summarize(self, docs: list) -> str:
        """Generate an AI-powered summary of all document contents."""
        if not docs:
            return "No documents to summarize."

        # Build combined context from all document texts (cap at 4000 chars to stay within token limits)
        combined_text = ""
        for doc in docs:
            snippet = doc.get("text", "")[:500]
            combined_text += f"\n\n--- Document: {doc['filename']} ---\n{snippet}"
        combined_text = combined_text[:4000]

        prompt = f"""You are given excerpts from the following documents. Write a concise summary (3-5 sentences) covering the main topics and key findings across all documents.

Documents:
{combined_text}

Summary:"""

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    # llama3-8b-8192 was decommissioned — use llama-3.1-8b-instant
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are an expert document summarizer. Provide clear, concise summaries.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 300,
                    "temperature": 0.3,
                },
                timeout=30,
            )
            if not response.ok:
                print(f"Groq API error {response.status_code}: {response.text}")
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            # Fallback: return a simple listing if the API call fails
            filenames = ", ".join([doc["filename"] for doc in docs])
            return f"Uploaded documents: {filenames}. (AI summary unavailable: {str(e)})"
// ── API Response Types — aligned with FastAPI backend ──────────────────────

/** A single uploaded document as returned by GET /documents/ */
interface Document {
    id: string;        // e.g. "DOC001"
    filename: string;  // e.g. "report.pdf"
}

/** A single answer row returned by POST /ask/ */
interface Answer {
    docId: string;     // The source document ID, e.g. "DOC001"
    answer: string;    // The LLM-generated answer text
    citation: string;  // e.g. "Page 3, Paragraph 2"
}

/** A theme identified from the answer by POST /ask/ */
interface Theme {
    title: string;    // e.g. "Revenue Growth"
    summary: string;  // Brief description of the theme
}

/** Full response from POST /ask/ */
interface QAResponse {
    answers: Answer[];
    themes: Theme[];
}

/** Response from GET /summarize/ */
interface SummarizeResponse {
    summary: string;
}

/** Response from POST /upload/ */
interface UploadResponse {
    message: string;  // "Documents uploaded successfully."
    ids: string[];    // ["DOC001", "DOC002"]
}

/** Generic error response */
interface ErrorResponse {
    error: string;
}
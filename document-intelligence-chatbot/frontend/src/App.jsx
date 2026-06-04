import React, { useState, useCallback, useEffect } from 'react';
import ChatWindow from './components/ChatWindow';
import DocumentUploader from './components/DocumentUploader';
import './styles/main.css';

const App = () => {
    const [documents, setDocuments] = useState([]);
    const [questions, setQuestions] = useState([]);
    const [responses, setResponses] = useState([]);
    const [isAsking, setIsAsking] = useState(false);
    const [inputValue, setInputValue] = useState('');

    // useCallback prevents fetchDocuments from being recreated every render
    const fetchDocuments = useCallback(async () => {
        try {
            const res = await fetch('/documents/');
            const data = await res.json();
            setDocuments(data);
        } catch (error) {
            console.error('Error fetching documents:', error);
        }
    }, []);

    useEffect(() => {
        fetchDocuments();
    }, [fetchDocuments]);

    const handleDocumentUpload = () => {
        fetchDocuments();
    };

    const handleQuestionSubmit = async (question) => {
        if (!question.trim() || isAsking) return;
        setIsAsking(true);

        // Add question immediately so the loading skeleton appears in the chat
        setQuestions(prev => [...prev, question]);

        try {
            const formData = new FormData();
            formData.append('question', question);
            documents.forEach(doc => formData.append('documentIds', doc.id));

            const response = await fetch('/ask/', {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();

            // Atomically update responses to match the already-pushed question
            setResponses(prev => [...prev, response.ok
                ? data
                : { answers: [{ docId: 'ERROR', answer: data.error || 'Failed to get answer.', citation: 'N/A' }], themes: [] }
            ]);
        } catch (error) {
            console.error('Error asking question:', error);
            setResponses(prev => [...prev, {
                answers: [{ docId: 'ERROR', answer: 'Failed to connect to server. Is the backend running?', citation: 'N/A' }],
                themes: [],
            }]);
        } finally {
            setIsAsking(false);
        }
    };

    const handleClearChat = () => {
        setQuestions([]);
        setResponses([]);
    };

    return (
        <div className="app">
            <header className="app-header">
                <h1>📄 Document Intelligence Chatbot</h1>
                <div className="header-actions">
                    {documents.length > 0 && (
                        <span className="doc-count">
                            {documents.length} doc{documents.length !== 1 ? 's' : ''} loaded
                        </span>
                    )}
                    {questions.length > 0 && (
                        <button className="btn btn-ghost" onClick={handleClearChat} title="Clear chat history">
                            🗑 Clear Chat
                        </button>
                    )}
                </div>
            </header>

            <main className="app-main">
                {/* Document Uploader */}
                <DocumentUploader onUpload={handleDocumentUpload} />

                {/* Loaded Documents List */}
                {documents.length > 0 && (
                    <section className="document-list-section">
                        <h2 className="section-title">Loaded Documents</h2>
                        <ul className="document-list">
                            {documents.map(doc => (
                                <li key={doc.id} className="document-item">
                                    <span className="doc-id-badge">{doc.id}</span>
                                    <span className="doc-filename">{doc.filename}</span>
                                </li>
                            ))}
                        </ul>
                    </section>
                )}

                {/* Chat Window */}
                <ChatWindow
                    questions={questions}
                    responses={responses}
                    isAsking={isAsking}
                />

                {/* Question Input Row */}
                <div className="question-input">
                    <input
                        type="text"
                        id="question-input"
                        placeholder={
                            documents.length === 0
                                ? 'Upload documents first...'
                                : 'Ask a question about your documents...'
                        }
                        value={inputValue}
                        disabled={isAsking || documents.length === 0}
                        onChange={(e) => setInputValue(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter' && inputValue.trim() && !isAsking) {
                                handleQuestionSubmit(inputValue.trim());
                                setInputValue('');
                            }
                        }}
                        aria-label="Ask a question about your uploaded documents"
                    />
                    <button
                        className="btn btn-primary"
                        onClick={() => {
                            if (inputValue.trim()) {
                                handleQuestionSubmit(inputValue.trim());
                                setInputValue('');
                            }
                        }}
                        disabled={isAsking || !inputValue.trim() || documents.length === 0}
                        aria-label="Submit question"
                    >
                        {isAsking ? '⏳ Thinking...' : '➤ Ask'}
                    </button>
                </div>
            </main>
        </div>
    );
};

export default App;
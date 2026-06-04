import React, { useEffect, useRef } from 'react';

/**
 * ChatWindow — displays the conversation history.
 * Props:
 *   questions  : string[]  — list of asked questions
 *   responses  : object[]  — matching API responses { answers, themes }
 *   isAsking   : boolean   — true while waiting for LLM response
 */
const ChatWindow = ({ questions, responses, isAsking }) => {
  const bottomRef = useRef(null);

  // Auto-scroll to the latest message whenever questions, responses, or loading state changes
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [questions, responses, isAsking]);

  return (
    <div className="chat-window">
      <div className="messages">

        {/* Empty state — shown only when no questions have been asked */}
        {questions.length === 0 && !isAsking && (
          <div className="empty-state">
            <div className="empty-state-icon">📄</div>
            <p>Upload documents above, then ask a question to get started.</p>
          </div>
        )}

        {/* Render each Q&A pair */}
        {questions.map((question, idx) => (
          // Use a composite key (not just idx) to avoid rendering bugs on list mutation
          <div key={`qa-${idx}-${question.slice(0, 20)}`} className="qa-section">

            <div className="question">
              <strong>{question}</strong>
            </div>

            {/* Answer table — shown once response is available */}
            {responses[idx] ? (
              <table className="answer-table">
                <thead>
                  <tr>
                    <th>Document ID</th>
                    <th>Answer</th>
                    <th>Citation</th>
                  </tr>
                </thead>
                <tbody>
                  {responses[idx]?.answers?.map((answer, ansIdx) => (
                    <tr key={`ans-${idx}-${ansIdx}`}>
                      <td>{answer.docId}</td>
                      <td>{answer.answer}</td>
                      <td>{answer.citation}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            ) : (
              /* Skeleton loader for the current question's answer */
              <div className="answer-skeleton">
                <div className="skeleton-line wide"></div>
                <div className="skeleton-line medium"></div>
                <div className="skeleton-line narrow"></div>
              </div>
            )}

            {/* Themes section — only shown when themes are present */}
            {responses[idx]?.themes?.length > 0 && (
              <div className="themes-container">
                <h4 className="themes-title">Key Themes</h4>
                {responses[idx].themes.map((theme, themeIdx) => (
                  <div key={`theme-${idx}-${themeIdx}`} className="theme-section">
                    <h5>{theme.title}</h5>
                    <p>{theme.summary}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {/* Loading indicator while waiting for LLM response */}
        {isAsking && (
          <div className="qa-section loading-qa">
            <div className="question">
              <strong>Analyzing documents...</strong>
            </div>
            <div className="typing-indicator">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>
        )}

        {/* Invisible anchor element — scrollIntoView targets this to reach the bottom */}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};

export default ChatWindow;
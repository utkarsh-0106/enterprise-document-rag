import { useState } from "react";
import { Link } from "react-router-dom";
import api from "../api/axios";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleAsk(event) {
    event.preventDefault();

    const trimmedQuestion = question.trim();

    if (!trimmedQuestion || loading) return;

    setError("");

    const userMessage = {
      role: "user",
      content: trimmedQuestion,
    };

    setMessages((current) => [...current, userMessage]);
    setQuestion("");
    setLoading(true);

    try {
      const response = await api.post("/api/rag/query", {
        question: trimmedQuestion,
        top_k: 5,
      });

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: response.data.answer,
          sources: response.data.sources || [],
        },
      ]);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to get an answer. Please try again."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="chat-page">
      <nav className="navbar">
        <div className="brand">JANGO RAG</div>

        <Link to="/dashboard" className="back-button">
          ← Dashboard
        </Link>
      </nav>

      <main className="chat-content">
        <header className="chat-header">
          <p className="eyebrow">PRIVATE KNOWLEDGE ASSISTANT</p>

          <h1>Ask Jango</h1>

          <p>
            Ask questions about your uploaded documents and get
            answers grounded in their content.
          </p>
        </header>

        <section className="chat-container">
          {messages.length === 0 && (
            <div className="chat-empty">
              <div className="chat-empty-icon">✦</div>

              <h2>What would you like to know?</h2>

              <p>
                Ask something about your uploaded documents.
              </p>

              <div className="suggested-questions">
                <button
                  onClick={() =>
                    setQuestion(
                      "What programming languages and technical skills does this person have?"
                    )
                  }
                >
                  What are the technical skills?
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "What projects has this person worked on?"
                    )
                  }
                >
                  What projects are mentioned?
                </button>

                <button
                  onClick={() =>
                    setQuestion(
                      "Summarize this person's experience."
                    )
                  }
                >
                  Summarize the experience
                </button>
              </div>
            </div>
          )}

          <div className="messages">
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message-row ${message.role}`}
              >
                <div className="message-avatar">
                  {message.role === "user" ? "U" : "J"}
                </div>

                <div className="message-body">
                  <span className="message-role">
                    {message.role === "user" ? "You" : "Jango"}
                  </span>

                  <div className="message-content">
                    {message.content}
                  </div>

                  {message.role === "assistant" &&
                    message.sources?.length > 0 && (
                      <div className="sources">
                        <h3>Sources</h3>

                        {message.sources.map((source, sourceIndex) => (
                          <div
                            className="source-card"
                            key={sourceIndex}
                          >
                            <div className="source-number">
                              {sourceIndex + 1}
                            </div>

                            <div>
                              <strong>
                                {source.filename ||
                                  "Document"}
                              </strong>

                              <span>
                                Page{" "}
                                {source.page_number || "—"}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                </div>
              </div>
            ))}

            {loading && (
              <div className="message-row assistant">
                <div className="message-avatar">J</div>

                <div className="message-body">
                  <span className="message-role">Jango</span>

                  <div className="typing-indicator">
                    <span />
                    <span />
                    <span />
                    <em>Searching your knowledge base...</em>
                  </div>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="alert alert-error chat-error">
              <span>⚠</span>
              {error}
            </div>
          )}

          <form
            className="chat-input-area"
            onSubmit={handleAsk}
          >
            <textarea
              value={question}
              onChange={(event) =>
                setQuestion(event.target.value)
              }
              placeholder="Ask something about your documents..."
              rows="1"
              disabled={loading}
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {
                  event.preventDefault();
                  event.currentTarget.form.requestSubmit();
                }
              }}
            />

            <button
              type="submit"
              disabled={loading || !question.trim()}
            >
              {loading ? "Thinking..." : "Ask Jango ↑"}
            </button>
          </form>

          <p className="chat-disclaimer">
            Jango answers using your private document knowledge
            base. Sources are shown with each answer.
          </p>
        </section>
      </main>
    </div>
  );
}

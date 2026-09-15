import { useState } from "react";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  // Document summarization states
  const [summary, setSummary] = useState("");
  const [summaryLoading, setSummaryLoading] = useState(false);

  // =========================
  // ASK QUESTION
  // =========================

  const askQuestion = async () => {
    if (!question.trim() || loading) return;

    const userQuestion = question.trim();

    setMessages((prev) => [
      ...prev,
      {
        type: "user",
        text: userQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question: userQuestion,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessages((prev) => [
          ...prev,
          {
            type: "assistant",
            text: data.answer,
            sources: data.sources || [],
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            type: "assistant",
            text: "Something went wrong. Please try again.",
            sources: [],
          },
        ]);
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          type: "assistant",
          text:
            "Unable to connect to the backend. Please make sure FastAPI and Ollama are running.",
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };


  // =========================
  // SUMMARIZE DOCUMENT
  // =========================

  const summarizeDocument = async () => {
    if (summaryLoading) return;

    setSummaryLoading(true);
    setSummary("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/summarize",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();

      if (response.ok) {
        setSummary(data.summary);
      } else {
        setSummary(
          "Unable to generate the document summary. Please try again."
        );
      }
    } catch (error) {
      console.error(error);

      setSummary(
        "Unable to connect to the backend. Please make sure FastAPI and Ollama are running."
      );
    } finally {
      setSummaryLoading(false);
    }
  };


  // =========================
  // NEW CHAT
  // =========================

  const startNewChat = () => {
    setMessages([]);
    setSummary("");
    setQuestion("");
  };


  return (
    <div className="app">

      {/* =========================
          SIDEBAR
      ========================= */}

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-icon">
            🎓
          </div>

          <div>
            <h2>University AI</h2>
            <span>Knowledge Assistant</span>
          </div>

        </div>


        {/* New Chat */}

        <button
          className="new-chat"
          onClick={startNewChat}
        >
          <span>＋</span>
          New Chat
        </button>


        {/* Documents */}

        <div className="sidebar-section">

          <p>DOCUMENTS</p>

          <div className="document-item">

            <span className="document-icon">
              📄
            </span>

            <div>
              <strong>University Syllabus</strong>
              <small>Knowledge source</small>
            </div>

          </div>


          {/* Summarize Button */}

          <button
            className="summarize-button"
            onClick={summarizeDocument}
            disabled={summaryLoading}
          >

            <div className="summarize-icon">
              📋
            </div>

            <div className="summarize-text">

              <strong>
                {summaryLoading
                  ? "Generating Summary..."
                  : "Summarize Document"}
              </strong>

              <small>
                Generate overview
              </small>

            </div>

          </button>

        </div>


        {/* Sidebar Status */}

        <div className="sidebar-bottom">

          <div className="status-dot"></div>

          <span>
            AI system online
          </span>

        </div>

      </aside>


      {/* =========================
          MAIN
      ========================= */}

      <main className="main">


        {/* =========================
            TOP BAR
        ========================= */}

        <header className="topbar">

          <div>
            <h1>
              University Knowledge Assistant
            </h1>
          </div>

          <div className="online-badge">

            <span></span>

            Online

          </div>

        </header>


        {/* =========================
            CHAT AREA
        ========================= */}

        <section className="chat-area">


          {/* =========================
              WELCOME SCREEN
          ========================= */}

          {messages.length === 0 &&
            !summary && (
              <div className="welcome">

                <div className="welcome-icon">
                  🎓
                </div>

                <h2>
                  How can I help you?
                </h2>

                <p>
                  Ask questions about your university syllabus
                  and other available documents.
                </p>


                {/* Sample Questions */}

                <div className="suggestions">

                  <button
                    onClick={() =>
                      setQuestion(
                        "What subjects are included in the CSE syllabus?"
                      )
                    }
                  >
                    📚 CSE syllabus subjects
                  </button>


                  <button
                    onClick={() =>
                      setQuestion(
                        "What are the courses in the first year?"
                      )
                    }
                  >
                    📝 First year courses
                  </button>


                  <button
                    onClick={() =>
                      setQuestion(
                        "What is Data Structures using C?"
                      )
                    }
                  >
                    💻 Data Structures
                  </button>

                </div>

              </div>
            )}


          {/* =========================
              DOCUMENT SUMMARY
          ========================= */}

          {summary && (

            <div className="summary-box">

              <div className="summary-header">

                <div className="summary-header-icon">
                  📋
                </div>

                <div>

                  <h2>
                    Document Summary
                  </h2>

                  <p>
                    AI-generated overview of the university syllabus
                  </p>

                </div>

              </div>


              <div className="summary-content">
                {summary}
              </div>

            </div>

          )}


          {/* =========================
              MESSAGES
          ========================= */}

          {messages.map((message, index) => (

            <div
              className={`message-row ${message.type}`}
              key={index}
            >

              {/* Assistant Avatar */}

              {message.type === "assistant" && (

                <div className="avatar assistant-avatar">
                  AI
                </div>

              )}


              <div className="message-content">


                {/* User Message */}

                {message.type === "user" ? (

                  <div className="user-message">
                    {message.text}
                  </div>

                ) : (

                  <>

                    {/* Assistant Answer */}

                    <div className="assistant-message">

                      <div className="answer-label">
                        Assistant
                      </div>

                      <div className="answer-text">
                        {message.text}
                      </div>

                    </div>


                    {/* Sources */}

                    {message.sources &&
                      message.sources.length > 0 && (

                        <div className="source-box">

                          <div className="source-title">

                            <span>
                              📚
                            </span>

                            Sources

                          </div>


                          <div className="source-list">

                            {message.sources.map(
                              (source) => (

                                <div
                                  className="source-card"
                                  key={source.chunk_id}
                                >

                                  <span>
                                    Chunk {source.chunk_id}
                                  </span>

                                  <span>
                                    {source.score}
                                  </span>

                                </div>

                              )
                            )}

                          </div>

                        </div>

                      )}

                  </>

                )}

              </div>

            </div>

          ))}


          {/* =========================
              QUESTION LOADING
          ========================= */}

          {loading && (

            <div className="message-row assistant">

              <div className="avatar assistant-avatar">
                AI
              </div>


              <div className="message-content">

                <div className="assistant-message loading-box">

                  <div className="answer-label">
                    Assistant
                  </div>


                  <div className="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>


                  <p>
                    Searching the university documents...
                  </p>

                </div>

              </div>

            </div>

          )}


          {/* =========================
              SUMMARY LOADING
          ========================= */}

          {summaryLoading && (

            <div className="message-row assistant">

              <div className="avatar assistant-avatar">
                AI
              </div>


              <div className="message-content">

                <div className="assistant-message loading-box">

                  <div className="answer-label">
                    Assistant
                  </div>


                  <div className="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                  </div>


                  <p>
                    Reading the document and generating a summary...
                  </p>

                </div>

              </div>

            </div>

          )}

        </section>


        {/* =========================
            INPUT
        ========================= */}

        <div className="input-wrapper">

          <div className="input-box">

            <input
              type="text"
              placeholder="Ask anything about the university documents..."
              value={question}
              onChange={(e) =>
                setQuestion(e.target.value)
              }
              onKeyDown={(e) => {

                if (e.key === "Enter") {
                  askQuestion();
                }

              }}
              disabled={loading || summaryLoading}
            />


            <button
              className="send-button"
              onClick={askQuestion}
              disabled={
                loading ||
                summaryLoading ||
                !question.trim()
              }
            >
              ↑
            </button>

          </div>


          <p className="input-note">
            Answers are generated using information from the provided documents.
          </p>

        </div>

      </main>

    </div>
  );
}

export default App;

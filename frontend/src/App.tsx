import { useCallback, useEffect, useState } from "react";
import { fetchHealth, fetchLesson, fetchLessons, runQuery } from "./api";
import { Feedback } from "./components/Feedback";
import { LessonPanel } from "./components/LessonPanel";
import { SqlEditor } from "./components/Editor";
import { ResultsTable } from "./components/ResultsTable";
import type { Lesson, LessonSummary, RunResponse, SqlError } from "./types";
import "./index.css";

const STORAGE_KEY = "sql-healthcare-progress";

function loadProgress(): { lessonId: string; dialect: "postgres" | "mysql" } {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) return JSON.parse(raw);
  } catch {
    /* ignore */
  }
  return { lessonId: "01-01-hello-select", dialect: "postgres" };
}

function saveProgress(lessonId: string, dialect: "postgres" | "mysql") {
  localStorage.setItem(STORAGE_KEY, JSON.stringify({ lessonId, dialect }));
}

export default function App() {
  const [lessons, setLessons] = useState<LessonSummary[]>([]);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [lessonId, setLessonId] = useState(loadProgress().lessonId);
  const [dialect, setDialect] = useState<"postgres" | "mysql">(loadProgress().dialect);
  const [sql, setSql] = useState("");
  const [running, setRunning] = useState(false);
  const [result, setResult] = useState<RunResponse | null>(null);
  const [error, setError] = useState<SqlError | null>(null);
  const [dbHealth, setDbHealth] = useState({ postgres: false, mysql: false });

  useEffect(() => {
    fetchLessons().then(setLessons).catch(console.error);
    fetchHealth().then(setDbHealth).catch(console.error);
  }, []);

  useEffect(() => {
    fetchLesson(lessonId)
      .then((l) => {
        setLesson(l);
        setSql(l.starterSql);
        setResult(null);
        setError(null);
      })
      .catch(console.error);
    saveProgress(lessonId, dialect);
  }, [lessonId, dialect]);

  const handleSqlChange = useCallback((nextSql: string) => {
    setSql(nextSql);
    setError(null);
    setResult(null);
  }, []);

  const handleRun = useCallback(async () => {
    setRunning(true);
    setError(null);
    setResult(null);
    try {
      const res = await runQuery(sql, dialect, lessonId);
      setResult(res);
      if (!res.ok && res.error) setError(res.error);
    } catch (e) {
      console.error(e);
      setError({
        line: 1,
        column: null,
        severity: "error",
        title: "Could not reach the server",
        why: "The app could not talk to the backend API.",
        fix: "Start the backend on port 8000, then run your query again.",
        suggestions: [],
        source: "client",
        rawMessage: e instanceof Error ? e.message : "Network error",
      });
    } finally {
      setRunning(false);
    }
  }, [sql, dialect, lessonId]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
        e.preventDefault();
        handleRun();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [handleRun]);

  const currentIndex = lessons.findIndex((l) => l.id === lessonId);
  const nextLesson = lessons[currentIndex + 1];

  return (
    <div className="app">
      <header className="header">
        <h1>SQL Healthcare Practice</h1>
        <div className="header-controls">
          <label>
            Dialect{" "}
            <select
              value={dialect}
              onChange={(e) => setDialect(e.target.value as "postgres" | "mysql")}
              data-testid="dialect-select"
            >
              <option value="postgres">PostgreSQL</option>
              <option value="mysql">MySQL</option>
            </select>
          </label>
          <span className={`db-dot ${dbHealth[dialect] ? "ok" : "bad"}`}>
            DB {dbHealth[dialect] ? "connected" : "offline"}
          </span>
          <label>
            Lesson{" "}
            <select
              value={lessonId}
              onChange={(e) => setLessonId(e.target.value)}
              data-testid="lesson-select"
            >
              {lessons.map((l) => (
                <option key={l.id} value={l.id}>
                  {l.title}
                </option>
              ))}
            </select>
          </label>
        </div>
      </header>

      <main className="main">
        {lesson && <LessonPanel lesson={lesson} dialect={dialect} />}
        <section className="workspace">
          <SqlEditor value={sql} onChange={handleSqlChange} errorLine={error?.line} />
          <div className="toolbar">
            <button onClick={handleRun} disabled={running} data-testid="run-button">
              {running ? "Running…" : "Run (Ctrl+Enter)"}
            </button>
            {result?.ok && result.passed && nextLesson && (
              <button
                className="btn-next"
                onClick={() => setLessonId(nextLesson.id)}
                data-testid="next-lesson"
              >
                Next lesson →
              </button>
            )}
            {nextLesson && !(result?.ok && result.passed) && (
              <button
                className="btn-skip"
                onClick={() => setLessonId(nextLesson.id)}
                data-testid="skip-lesson"
              >
                Skip for now
              </button>
            )}
          </div>
          <Feedback
            error={error}
            success={result?.ok}
            passed={result?.passed}
            feedback={result?.feedback}
          />
          {result?.ok && result.columns && result.rows && (
            <ResultsTable columns={result.columns} rows={result.rows} />
          )}
        </section>
      </main>
    </div>
  );
}

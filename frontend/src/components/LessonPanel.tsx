import type { Lesson } from "../types";

interface Props {
  lesson: Lesson;
  dialect: "postgres" | "mysql";
}

export function LessonPanel({ lesson, dialect }: Props) {
  const note = lesson.dialectNotes[dialect];
  return (
    <aside className="lesson-panel">
      <p className="lesson-module">{lesson.module}</p>
      <h2>{lesson.title}</h2>
      <p className="lesson-prompt">{lesson.prompt}</p>
      {note && <p className="dialect-note">{note}</p>}
      <section>
        <h3>Tables used</h3>
        <ul className="schema-list">
          {lesson.schemaTables.map((t) => (
            <li key={t}>
              <code>{t}</code>
              <span className="schema-cols">{lesson.schemaSnippet[t]}</span>
            </li>
          ))}
        </ul>
      </section>
      <section>
        <h3>Hints</h3>
        <ul>
          {lesson.hints.map((h) => (
            <li key={h}>{h}</li>
          ))}
        </ul>
      </section>
    </aside>
  );
}

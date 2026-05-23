import type { SqlError } from "../types";

interface Props {
  error: SqlError | null;
  success?: boolean;
  passed?: boolean;
  feedback?: string | null;
}

export function Feedback({ error, success, passed, feedback }: Props) {
  if (error) {
    return (
      <div className="feedback feedback-error" data-testid="feedback-error">
        <h3>{error.title}</h3>
        <p className="feedback-line">
          <strong>Line {error.line}</strong>
          {error.column != null && ` · column ${error.column}`}
        </p>
        <section>
          <h4>Why</h4>
          <p>{error.why}</p>
        </section>
        <section>
          <h4>Try this</h4>
          <p>{error.fix}</p>
        </section>
        {error.suggestions.length > 0 && (
          <details>
            <summary>Learn more</summary>
            <ul>
              {error.suggestions.map((s) => (
                <li key={s}>{s}</li>
              ))}
            </ul>
          </details>
        )}
      </div>
    );
  }

  if (success) {
    return (
      <div className="feedback feedback-success" data-testid="feedback-success">
        <p>Query ran successfully — {passed ? "lesson complete!" : "check your results below."}</p>
        {!passed && feedback && <p className="feedback-hint">{feedback}</p>}
      </div>
    );
  }

  return null;
}

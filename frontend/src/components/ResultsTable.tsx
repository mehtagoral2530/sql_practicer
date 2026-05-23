interface Props {
  columns: string[];
  rows: unknown[][];
}

export function ResultsTable({ columns, rows }: Props) {
  if (columns.length === 0) return null;
  return (
    <div className="results" data-testid="results-table">
      <p className="results-meta">
        {rows.length} row{rows.length !== 1 ? "s" : ""}
      </p>
      <div className="results-scroll">
        <table>
          <thead>
            <tr>
              {columns.map((c) => (
                <th key={c}>{c}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>
                {row.map((cell, j) => (
                  <td key={j}>{cell == null ? "NULL" : String(cell)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

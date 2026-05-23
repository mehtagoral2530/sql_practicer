export interface SqlError {
  line: number;
  column: number | null;
  severity: string;
  title: string;
  why: string;
  fix: string;
  suggestions: string[];
  source: string;
  rawMessage: string;
}

export interface RunResponse {
  ok: boolean;
  error?: SqlError;
  passed?: boolean;
  feedback?: string | null;
  columns?: string[];
  rows?: unknown[][];
  rowCount?: number;
  sql?: string;
}

export interface LessonSummary {
  id: string;
  title: string;
  module: string;
}

export interface Lesson extends LessonSummary {
  dialectNotes: { postgres: string | null; mysql: string | null };
  prompt: string;
  schemaTables: string[];
  schemaSnippet: Record<string, string>;
  starterSql: string;
  hints: string[];
  hasValidation?: boolean;
}

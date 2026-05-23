import type { Lesson, LessonSummary, RunResponse } from "./types";

export async function fetchLessons(): Promise<LessonSummary[]> {
  const res = await fetch("/api/lessons");
  if (!res.ok) throw new Error("Failed to load lessons");
  return res.json();
}

export async function fetchLesson(id: string): Promise<Lesson> {
  const res = await fetch(`/api/lessons/${id}`);
  if (!res.ok) throw new Error("Lesson not found");
  return res.json();
}

export async function runQuery(
  sql: string,
  dialect: "postgres" | "mysql",
  lessonId: string
): Promise<RunResponse> {
  const res = await fetch("/api/run", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sql, dialect, lessonId }),
  });
  return res.json();
}

export async function fetchHealth(): Promise<{ postgres: boolean; mysql: boolean }> {
  const res = await fetch("/api/health");
  return res.json();
}

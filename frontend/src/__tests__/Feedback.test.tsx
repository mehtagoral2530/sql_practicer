import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { Feedback } from "../components/Feedback";

describe("Feedback", () => {
  it("renders error line, why, and fix", () => {
    render(
      <Feedback
        error={{
          line: 3,
          column: 12,
          severity: "error",
          title: "Syntax error near FROM",
          why: "FRMO is not a valid keyword.",
          fix: "Change FRMO to FROM on line 3.",
          suggestions: ["Pattern: SELECT columns FROM table_name;"],
          source: "parser",
          rawMessage: "syntax error",
        }}
      />
    );
    expect(screen.getByTestId("feedback-error")).toBeInTheDocument();
    expect(screen.getByText(/Line 3/)).toBeInTheDocument();
    expect(screen.getByText(/FRMO is not a valid keyword/)).toBeInTheDocument();
    expect(screen.getByText(/Change FRMO to FROM/)).toBeInTheDocument();
  });

  it("renders success when lesson passed", () => {
    render(<Feedback success passed />);
    expect(screen.getByTestId("feedback-success")).toHaveTextContent("lesson complete");
  });
});

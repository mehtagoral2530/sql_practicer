import { render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { SqlEditor } from "../components/Editor";

describe("SqlEditor", () => {
  it("renders sql content in the editor", () => {
    render(
      <SqlEditor
        value={"SELECT name\nFROM hospitals"}
        onChange={vi.fn()}
        errorLine={2}
      />
    );

    expect(screen.getByRole("textbox")).toBeInTheDocument();
    expect(document.querySelector(".cm-error-line")).toBeInTheDocument();
  });

  it("updates when errorLine changes", () => {
    const { rerender } = render(
      <SqlEditor value={"SELECT name\nFRMO hospitals"} onChange={vi.fn()} errorLine={2} />
    );

    rerender(
      <SqlEditor value={"SELECT name\nFRMO hospitals"} onChange={vi.fn()} errorLine={null} />
    );

    expect(screen.getByRole("textbox")).toBeInTheDocument();
  });
});

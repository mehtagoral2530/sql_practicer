import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ResultsTable } from "../components/ResultsTable";

describe("ResultsTable", () => {
  it("renders columns and rows with null as NULL", () => {
    render(
      <ResultsTable
        columns={["name", "city"]}
        rows={[
          ["General Hospital", "Boston"],
          [null, "NYC"],
        ]}
      />
    );

    expect(screen.getByTestId("results-table")).toBeInTheDocument();
    expect(screen.getByText("General Hospital")).toBeInTheDocument();
    expect(screen.getByText("NULL")).toBeInTheDocument();
    expect(screen.getByText("2 rows")).toBeInTheDocument();
  });

  it("returns null when there are no columns", () => {
    const { container } = render(<ResultsTable columns={[]} rows={[]} />);
    expect(container.firstChild).toBeNull();
  });
});

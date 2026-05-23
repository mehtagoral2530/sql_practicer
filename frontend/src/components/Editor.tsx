import { Decoration, EditorView, ViewPlugin } from "@codemirror/view";
import CodeMirror from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";
import { useMemo } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  errorLine?: number | null;
}

function errorLineHighlight(line: number | null | undefined) {
  return ViewPlugin.fromClass(
    class {
      decorations;
      constructor(view: EditorView) {
        this.decorations = this.build(view);
      }
      update(update: import("@codemirror/view").ViewUpdate) {
        if (update.docChanged || update.viewportChanged) {
          this.decorations = this.build(update.view);
        }
      }
      build(view: EditorView) {
        if (!line) return Decoration.none;
        const l = Math.min(Math.max(1, line), view.state.doc.lines);
        const info = view.state.doc.line(l);
        return Decoration.set([
          Decoration.line({ class: "cm-error-line" }).range(info.from),
        ]);
      }
    },
    { decorations: (v) => v.decorations }
  );
}

export function SqlEditor({ value, onChange, errorLine }: Props) {
  const extensions = useMemo(() => {
    const exts = [sql(), errorLineHighlight(errorLine)];
    return exts;
  }, [errorLine]);

  return (
    <CodeMirror
      value={value}
      height="220px"
      extensions={extensions}
      onChange={onChange}
      basicSetup={{ lineNumbers: true }}
    />
  );
}

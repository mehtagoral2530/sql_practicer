import { Decoration, EditorView } from "@codemirror/view";
import CodeMirror, { type ReactCodeMirrorRef } from "@uiw/react-codemirror";
import { sql } from "@codemirror/lang-sql";
import { StateEffect, StateField, type EditorState } from "@codemirror/state";
import { useCallback, useEffect, useMemo, useRef } from "react";

interface Props {
  value: string;
  onChange: (value: string) => void;
  errorLine?: number | null;
}

const setErrorLine = StateEffect.define<number | null>();

function buildErrorLineDecorations(state: EditorState, line: number | null) {
  if (line == null) return Decoration.none;
  const clamped = Math.min(Math.max(1, line), state.doc.lines);
  const info = state.doc.line(clamped);
  return Decoration.set([
    Decoration.line({ class: "cm-error-line" }).range(info.from),
  ]);
}

const errorLineMetaField = StateField.define<number | null>({
  create: () => null,
  update(value, tr) {
    for (const effect of tr.effects) {
      if (effect.is(setErrorLine)) return effect.value;
    }
    return value;
  },
});

const errorLineDecorationsField = StateField.define({
  create(state) {
    return buildErrorLineDecorations(state, state.field(errorLineMetaField));
  },
  update(deco, tr) {
    const lineChanged = tr.effects.some((effect) => effect.is(setErrorLine));
    if (lineChanged || tr.docChanged) {
      return buildErrorLineDecorations(tr.state, tr.state.field(errorLineMetaField));
    }
    return deco.map(tr.changes);
  },
  provide: (field) => EditorView.decorations.from(field),
});

export function SqlEditor({ value, onChange, errorLine }: Props) {
  const editorRef = useRef<ReactCodeMirrorRef>(null);
  const extensions = useMemo(
    () => [sql(), errorLineMetaField, errorLineDecorationsField],
    []
  );

  const applyErrorLine = useCallback(
    (view: EditorView) => {
      view.dispatch({ effects: setErrorLine.of(errorLine ?? null) });
    },
    [errorLine]
  );

  useEffect(() => {
    const view = editorRef.current?.view;
    if (view) applyErrorLine(view);
  }, [applyErrorLine]);

  return (
    <CodeMirror
      ref={editorRef}
      value={value}
      height="220px"
      extensions={extensions}
      onChange={onChange}
      onCreateEditor={applyErrorLine}
      basicSetup={{ lineNumbers: true }}
    />
  );
}

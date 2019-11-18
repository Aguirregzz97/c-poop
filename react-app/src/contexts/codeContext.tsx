import React, { createContext, useState, createRef } from "react";

import { EMOJI_HASH } from "../constants/emoji-categories";

const initialState: any = {
  code: "console.log('C💩 Rocks!');",
  translatedCode: "console.log('C; Rocks!');"
};

const CodeContext = createContext(initialState);

const CodeProvider = ({ children }: { children: React.ReactNode }) => {
  const [code, setCode] = useState(initialState.code);
  const [translatedCode, setTranslatedCode] = useState(
    initialState.translatedCode
  );

  const ref: any = createRef();

  const addEmoji = (emoji: string) => {
    const { editor } = ref.current;
    editor.session.insert(editor.getCursorPosition(), emoji);
    editor.focus();
  };

  const regex = new RegExp(Object.keys(EMOJI_HASH).join("|"), "gi");

  const handleTranslation = (newCode: string) => {
    const aux = newCode.replace(regex, matched => {
      return EMOJI_HASH[matched];
    });
    setTranslatedCode(aux);
  };

  return (
    <CodeContext.Provider
      value={{
        code,
        setCode,
        ref,
        addEmoji,
        translatedCode,
        setTranslatedCode,
        handleTranslation
      }}
    >
      {children}
    </CodeContext.Provider>
  );
};

export { CodeProvider, CodeContext };

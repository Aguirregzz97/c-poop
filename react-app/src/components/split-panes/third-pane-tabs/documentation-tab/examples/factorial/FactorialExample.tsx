import React, { useContext } from "react";

import { Theme, useTheme } from "@material-ui/core/styles";

import { IconButton } from "@material-ui/core";
import CodeIcon from "@material-ui/icons/Code";
import Tooltip from "@material-ui/core/Tooltip";
import AceEditor from "react-ace";
import { CodeContext } from "../../../../../../contexts/codeContext";
import factorialCode from "./factorialCode";

import useStyles from "../documentation-example.jss";

const FactorialExample: React.FC = () => {
  const { setValue } = useContext(CodeContext);
  const theme: Theme = useTheme();
  const classes = useStyles();

  const { fontSize } = theme.typography;
  return (
    <>
      <div className={classes.div}>
        <h4 className={classes.h4}> 1) Factorial</h4>
        <Tooltip title="Copy code" placement="top">
          <IconButton
            aria-label="code"
            size="medium"
            onClick={() => setValue(factorialCode)}
            className={classes.codeIcon}
          >
            <CodeIcon />
          </IconButton>
        </Tooltip>
      </div>

      <AceEditor
        mode="python"
        theme="monokai"
        value={factorialCode}
        editorProps={{ $blockScrolling: true }}
        fontSize={fontSize - 2}
        readOnly
        style={{ height: "270px", width: "100%" }}
      />
    </>
  );
};

export default FactorialExample;

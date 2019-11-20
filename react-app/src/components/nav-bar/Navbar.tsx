import React, { useContext } from "react";

import { TranslatedContext } from "../../contexts/";

import { AppBar, Button, Toolbar, Typography } from "@material-ui/core/";

import useStyles from "./navbar.jss";

const Navbar: React.FC = () => {
  const classes = useStyles();

  const { handleTranslation } = useContext(TranslatedContext);

  return (
    <div className={classes.root}>
      <AppBar position="static" elevation={2}>
        <Toolbar>
          <Typography variant="h5" className={classes.title}>
            {"C"}
            <span role="img" aria-label="title-poop-emoji">
              {"💩 "}
            </span>
            {"Compiler"}
          </Typography>
          <Button variant="contained" onClick={() => handleTranslation()}>
            Translate
          </Button>
          <Button variant="contained" color="primary">
            Run
          </Button>
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default Navbar;

import React from "react";
import SplitPane from "react-split-pane";

const SplitPanes: React.FC = () => (
  <SplitPane
    split="vertical"
    defaultSize="20%"
    minSize={200}
    maxSize={400}
    className="pane-parent"
  >
    <div className="pane pane-1">pane 1 size: 20%</div>
    <SplitPane split="vertical" defaultSize="50%">
      <div className="pane pane-2">pane 2 size: 40%</div>
      <SplitPane split="vertical" defaultSize="100%">
        <div className="pane pane-3">pane 3 size: 40%</div>
      </SplitPane>
    </SplitPane>
  </SplitPane>
);

export default SplitPanes;
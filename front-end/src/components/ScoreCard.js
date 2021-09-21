import { Card } from "antd";

function ScoreCard({ color, children, bodyStyle, style }) {
  let localBodyStyle = {
    padding: "24px 0px",
    textAlign: "center",
  };

  let localStyle = {
    borderRadius: "10px",
    paddingRight: "8px",
  };

  if (bodyStyle !== undefined && bodyStyle !== null) {
    for (const property in bodyStyle) {
      localBodyStyle[property] = bodyStyle[property];
    }
  }

  if (style !== undefined && style !== null) {
    for (const property in style) {
      localStyle[property] = style[property];
    }
  }

  return (
    <Card style={localStyle} bodyStyle={localBodyStyle}>
      {children}
    </Card>
  );
}
export default ScoreCard;

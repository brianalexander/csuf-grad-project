import { Card, Tag, Row, Col } from "antd";

function SimilarItemCard({ color, children, style, tags }) {
  let localStyle = {
    borderRadius: "10px",
    fontSize: "10px",
    width: "auto",
    height: "auto",
  };

  const tagColors = {
    "Hate Speech": "magenta",
    Toxic: "gold",
    Misinformation: "red",
    Offensive: "green",
    Add: "purple",
  };

  let localBodyStyle = { padding: "4px 8px 4px 8px", margin: "0px" };

  let localTagStyle = {
    fontSize: "8px",
    padding: "2px 8px",
    lineHeight: "8px",
  };

  if (color === "green") {
    localStyle.color = "#389e0d";
    localStyle.background = "#f6ffed";
    localStyle.borderColor = "#b7eb8f";
  } else if (color === "red") {
    localStyle.color = "#cf1322";
    localStyle.background = "#fff1f0";
    localStyle.borderColor = "#ffa39e";
  }

  if (style !== undefined && style !== null) {
    for (const property in style) {
      localStyle[property] = style[property];
    }
  }

  // if (tags === undefined) {
  //   tags = [
  //     { text: "tag1", color: "magenta" },
  //     { text: "tag2", color: "gold" },
  //   ];
  // }

  return (
    <Card style={localStyle} bodyStyle={localBodyStyle}>
      <Row gutter={[0, 4]}>
        <Col span={24}>{children}</Col>
        <Col span={24}>
          {tags.map((tag) => {
            return (
              <Tag color={tagColors[tag]} style={localTagStyle}>
                {tag}
              </Tag>
            );
          })}
        </Col>
      </Row>
    </Card>
  );
}

export default SimilarItemCard;

import { Button, Tag } from "antd";

function TagButton({ onClick, color, icon, children, buttonStyle, tagStyle }) {
  let localButtonStyle = {
    padding: "0px",
    height: "auto",
    border: "none",
    fontSize: "0px",
  };

  let localTagStyle = { margin: "0px" };

  if (buttonStyle !== undefined && buttonStyle !== null) {
    for (const property in buttonStyle) {
      localButtonStyle[property] = buttonStyle[property];
    }
  }

  if (tagStyle !== undefined && tagStyle !== null) {
    for (const property in tagStyle) {
      localTagStyle[property] = tagStyle[property];
    }
  }

  return (
    <Button style={localButtonStyle} onClick={onClick}>
      <Tag color={color} icon={icon} style={localTagStyle}>
        {children}
      </Tag>
    </Button>
  );
}

export default TagButton;

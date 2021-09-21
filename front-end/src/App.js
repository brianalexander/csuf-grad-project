// import logo from "./logo.svg";
// import "./App.css";

import "antd/dist/antd.css";
import "react-toastify/dist/ReactToastify.css";
import "./demo.css";

import { ToastContainer } from "react-toastify";
import { toast } from "react-toastify";

import { connect, useDispatch } from "react-redux";
import {
  removeItem,
  fetchBatchForModerator,
  returnResultForItemByModerator,
} from "./redux/batchSlice";

import React, { useState, useEffect } from "react";

// import { socket } from "./websockets";

import { Layout, Menu, Space } from "antd";
import { Row, Col } from "antd";
import { Card, Input } from "antd";
import { Button } from "antd";
import { Modal } from "antd";

import TagButton from "./components/TagButton";
import SimilarItemCard from "./components/SimilarItemCard";
import ScoreCard from "./components/ScoreCard";

import {
  // DesktopOutlined,
  // PieChartOutlined,
  // FileOutlined,
  // TeamOutlined,
  UserOutlined,
  PlusOutlined,
  MinusOutlined,
  RedoOutlined,
  CheckSquareOutlined,
  CloseSquareOutlined,
} from "@ant-design/icons";

const { Header, Content, Footer, Sider } = Layout;
// const { SubMenu } = Menu;

function App(props) {
  // const [collapsed, setCollapsed] = useState(true);
  const [isModalVisible, setIsModalVisible] = useState(false);
  // const [size, setSize] = useState("large");
  const [moderatorId, setModeratorId] = useState("");
  const [newTagText, setNewTagText] = useState("");
  const [tags, setTags] = useState([]);
  const dispatch = useDispatch();

  const tagColors = {
    "Hate Speech": "magenta",
    Toxic: "gold",
    Misinformation: "red",
    Offensive: "green",
    Add: "purple",
  };

  useEffect(() => {
    let delayDebounceFn = setTimeout(() => {}, 1000);

    if (moderatorId.length >= 5) {
      delayDebounceFn = setTimeout(() => {
        toast.info(`Requesting items as ${moderatorId}`);
        dispatch(fetchBatchForModerator("test_moderator"));
      }, 3000);
    }

    return () => clearTimeout(delayDebounceFn);
  }, [moderatorId]);

  // useEffect(() => {
  //   setTags(props.item.tags);
  // }, [props.item]);

  // const similarItemTags = props.item.similarItems[0].tags.map((tag) => {
  //   return { text: tag, color: tagColors[tag] };
  // });

  // const getBatch = (evt) => {
  //   console.log("requesting batch");
  //   socket.send(
  //     JSON.stringify({ type: "getBatchRequest", payload: { user: "user" } })
  //   );
  // };
  const addTagButtonHandler = (evt) => {
    setNewTagText("");
    setIsModalVisible(true);
  };

  const modalOkHandler = () => {
    setTags([...tags, newTagText]);
    setIsModalVisible(false);
  };

  const modalCancelHandler = () => {
    setIsModalVisible(false);
  };

  const tagTextOnChangeHandler = (evt) => {
    setNewTagText(evt.target.value);
  };
  const moderatorIdChangedHandler = (evt) => {
    setModeratorId(evt.target.value);
  };

  const rejectItemHandler = (evt) => {
    if (moderatorId.length === 0) {
      toast.warn("Please set your moderator ID first!");
      return;
    }

    dispatch(
      returnResultForItemByModerator({
        itemId: props.item.id,
        moderatorId,
        flagged: false,
        tags,
      })
    );
    setTags([]);
    dispatch(removeItem({ id: props.item.id }));

    if (props.batchLength <= 5) {
      dispatch(fetchBatchForModerator(moderatorId));
    }
  };

  const acceptItemHandler = (evt) => {
    if (moderatorId.length === 0) {
      toast.warn("Please set your moderator Id first!");
      return;
    }

    dispatch(
      returnResultForItemByModerator({
        itemId: props.item.id,
        moderatorId,
        flagged: true,
        tags,
      })
    );

    setTags([]);
    dispatch(removeItem({ id: props.item.id }));

    if (props.batchLength <= 5) {
      dispatch(fetchBatchForModerator("test_moderator"));
    }
  };

  const skipItemHandler = (evt) => {
    dispatch(removeItem({ id: props.item.id }));
    if (props.batchLength <= 5) {
      dispatch(fetchBatchForModerator("test_moderator"));
    }
  };

  // const addTagButtonHandler = (evt) => {
  //   setTags([...tags, "newTag"]);
  // };

  const removeTagButtonHandler = (removedTag) => {
    const newTags = [...tags].filter((tag) => tag !== removedTag);
    setTags(newTags);
  };

  return (
    <Layout style={{ minHeight: "100vh" }}>
      {/* <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(collapsed) => {
          setCollapsed(collapsed);
        }}
      >
        <div className="logo" />
        <Menu theme="dark" defaultSelectedKeys={["1"]} mode="inline">
          <Menu.Item key="1" icon={<PieChartOutlined />}>
            Option 1
          </Menu.Item>
          <Menu.Item key="2" icon={<DesktopOutlined />}>
            Option 2
          </Menu.Item>
          <SubMenu key="sub1" icon={<UserOutlined />} title="User">
            <Menu.Item key="3">Tom</Menu.Item>
            <Menu.Item key="4">Bill</Menu.Item>
            <Menu.Item key="5">Alex</Menu.Item>
          </SubMenu>
          <SubMenu key="sub2" icon={<TeamOutlined />} title="Team">
            <Menu.Item key="6">Team 1</Menu.Item>
            <Menu.Item key="8">Team 2</Menu.Item>
          </SubMenu>
          <Menu.Item key="9" icon={<FileOutlined />}>
            Files
          </Menu.Item>
        </Menu>
      </Sider> */}
      <Layout className="site-layout">
        {/* <Header
          className="site-layout-background"
          style={{ padding: "0 16px" }}
        ></Header> */}
        <Content style={{ margin: "16px 16px 0px 16px" }}>
          <div
            className="site-layout-background"
            style={{ padding: 24, minHeight: 360, height: "100%" }}
          >
            <Row style={{ height: "100%" }}>
              <Col span={18}>
                <Row
                  wrap={false}
                  style={{
                    flexDirection: "column",
                    height: "100%",
                    padding: "12px",
                  }}
                >
                  <Col flex="none">
                    <Row>
                      <Col span={24}>
                        <Card
                          bodyStyle={{
                            justifyContent: "space-around",
                            padding: "8px 8px",
                          }}
                          style={{
                            width: "100%",
                            borderRadius: "10px",
                          }}
                        >
                          <Row gutter={[16, 8]} style={{ textAlign: "center" }}>
                            {/* <Col flex="auto" style={{}}>
                              <TagButton color="magenta">Recommended</TagButton>
                            </Col> */}
                            <Col flex="auto" style={{}}>
                              <TagButton color="green">Low</TagButton>
                            </Col>
                            <Col flex="auto" style={{}}>
                              <TagButton color="gold">Medium</TagButton>
                            </Col>
                            <Col flex="auto" style={{}}>
                              <TagButton color="red">High</TagButton>
                            </Col>
                          </Row>
                        </Card>
                      </Col>
                    </Row>
                  </Col>
                  <Col flex="auto">
                    <Row
                      gutter={[0, 8]}
                      justify="center"
                      style={{ flexDirection: "column", height: "100%" }}
                    >
                      <Col>
                        <Row
                          gutter={16}
                          // justify="space-around"
                          align="middle"
                          style={{
                            padding: "24px 24px 0px 24px",
                            height: "100%",
                          }}
                        >
                          <Col span={8}>
                            <ScoreCard>
                              {props.item
                                ? props.item.scores[0].text +
                                  ": " +
                                  parseFloat(
                                    props.item.scores[0].value * 100
                                  ).toFixed(0) +
                                  "%"
                                : "Loading..."}
                            </ScoreCard>
                          </Col>
                          <Col span={8}>
                            <ScoreCard>
                              {props.item
                                ? props.item.scores[1].text +
                                  ": " +
                                  parseFloat(
                                    props.item.scores[1].value * 100
                                  ).toFixed(0) +
                                  "%"
                                : "Loading..."}
                            </ScoreCard>
                          </Col>
                          <Col span={8}>
                            <ScoreCard>
                              {props.item
                                ? props.item.scores[2].text +
                                  ": " +
                                  parseFloat(
                                    props.item.scores[2].value * 100
                                  ).toFixed(0) +
                                  "%"
                                : "Loading..."}
                            </ScoreCard>
                          </Col>
                        </Row>
                      </Col>
                      <Col>
                        <Row style={{ padding: "12px 24px" }}>
                          <Col span={24}>
                            <Card
                              style={{
                                width: "100%",
                                minHeight: 200,
                                borderRadius: "10px",
                              }}
                            >
                              <div style={{}}>
                                {props.item !== undefined
                                  ? props.item.text
                                  : ""}
                              </div>
                            </Card>
                          </Col>
                        </Row>
                      </Col>
                      <Col>
                        <Row style={{ padding: 12 }}>
                          <Col span={24}>
                            <Card
                              bodyStyle={{ padding: "8px 8px" }}
                              style={{
                                borderRadius: "10px",
                              }}
                            >
                              <Row gutter={[16, 8]} justify="start">
                                {props.item
                                  ? props.item.tags.map((tag, index) => {
                                      return (
                                        <Col>
                                          <TagButton color={tagColors[tag]}>
                                            {tag}
                                          </TagButton>
                                        </Col>
                                      );
                                    })
                                  : ""}
                                {props.item
                                  ? tags.map((tag, index) => {
                                      return (
                                        <Col>
                                          <TagButton
                                            color={tagColors[tag]}
                                            icon={<MinusOutlined />}
                                            onClick={(e) => {
                                              e.preventDefault();
                                              removeTagButtonHandler(tag);
                                            }}
                                          >
                                            {tag}
                                          </TagButton>
                                        </Col>
                                      );
                                    })
                                  : "Loading..."}
                                <Col>
                                  <TagButton
                                    color="purple"
                                    icon={<PlusOutlined />}
                                    onClick={addTagButtonHandler}
                                  >
                                    Add
                                  </TagButton>
                                </Col>
                              </Row>
                            </Card>
                          </Col>
                        </Row>
                      </Col>
                      <Col>
                        <Row gutter={16}>
                          <Col
                            className="gutter-row"
                            style={{ textAlign: "center" }}
                            flex="auto"
                          >
                            <Button
                              type="danger"
                              shape="round"
                              icon={<CloseSquareOutlined />}
                              size="large"
                              onClick={rejectItemHandler}
                            >
                              Reject
                            </Button>
                          </Col>
                          <Col
                            className="gutter-row"
                            style={{ textAlign: "center" }}
                            flex="auto"
                          >
                            <Button
                              shape="round"
                              icon={<RedoOutlined />}
                              size="large"
                              onClick={skipItemHandler}
                            >
                              Skip
                            </Button>
                          </Col>
                          <Col
                            className="gutter-row"
                            style={{ textAlign: "center" }}
                            flex="auto"
                          >
                            <Button
                              type="primary"
                              shape="round"
                              icon={<CheckSquareOutlined />}
                              size="large"
                              onClick={acceptItemHandler}
                            >
                              Accept
                            </Button>
                          </Col>
                        </Row>
                      </Col>
                    </Row>
                  </Col>
                </Row>
              </Col>
              <Col span={6} style={{}}>
                <Row
                  wrap={false}
                  style={{
                    flexDirection: "column",
                    height: "100%",
                    padding: "12px",
                  }}
                >
                  <Col flex="none">
                    <Input
                      onChange={moderatorIdChangedHandler}
                      style={{ borderRadius: "10px" }}
                      size="large"
                      placeholder="Enter Moderator ID..."
                      prefix={<UserOutlined />}
                    />
                  </Col>
                  <Col flex="auto">
                    <Row
                      gutter={[0, 16]}
                      justify="center"
                      style={{ flexDirection: "column", height: "100%" }}
                    >
                      {props.item
                        ? props.item.similarItems.map((post, index) => {
                            return (
                              <Col>
                                <SimilarItemCard
                                  color={post.flagged ? "red" : "green"}
                                  tags={post.tags}
                                >
                                  {post.text}
                                </SimilarItemCard>
                              </Col>
                            );
                          })
                        : "Loading..."}
                      {/* <Col>
                        <SimilarItemCard
                          color={
                            props.item.similarItems[0].flagged ? "red" : "green"
                          }
                          tags={similarItemTags}
                        >
                          {props.item.similarItems[0].text}
                        </SimilarItemCard>
                      </Col>
                      <Col>
                        <SimilarItemCard color="red">
                          Similar Item 2
                        </SimilarItemCard>
                      </Col>
                      <Col>
                        <SimilarItemCard color="green">
                          Similar Item 3
                        </SimilarItemCard>
                      </Col>
                      <Col>
                        <SimilarItemCard color="red">
                          Similar Item 4
                        </SimilarItemCard>
                      </Col> */}
                    </Row>
                  </Col>
                </Row>
              </Col>
            </Row>
          </div>
        </Content>
        <Footer style={{ textAlign: "center" }}>
          Content Moderation ©2021 Created by Brian Alexander
        </Footer>
      </Layout>
      <ToastContainer
        position="top-right"
        autoClose={2000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
      <Modal
        // title="Enter Tag Text"
        visible={isModalVisible}
        onOk={modalOkHandler}
        onCancel={modalCancelHandler}
        closable={false}
      >
        <Input
          placeholder="Enter tag text..."
          onChange={tagTextOnChangeHandler}
          value={newTagText}
          onPressEnter={modalOkHandler}
        />
      </Modal>
    </Layout>
  );
}

const mapStateToProps = (state, ownProps) => {
  return {
    item: state.batch.batch[0],
    batchLength: state.batch.batch.length,
  };
};

const mapDispatchToProps = {};

export default connect(mapStateToProps, mapDispatchToProps)(App);

export const getBatchForModerator = async (moderatorId) => {
  const response = await fetch(
    `http://localhost/moderator/${moderatorId}/item`,
    { method: "GET" }
  );

  return response.json();
};

export const sendResultForItemByModerator = async (
  itemId,
  moderatorId,
  flagged,
  tags
) => {
  const response = await fetch(`http://localhost/result`, {
    method: "POST", // or 'PUT'
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      id: itemId,
      moderator: moderatorId,
      flagged,
      tags,
    }),
  });

  return response.status;
};

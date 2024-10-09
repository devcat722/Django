import React, { useEffect, useState } from "react";
import DjangoUrl from "../constants";

const ApiPage = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch(`${DjangoUrl}/api/test`)
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((error) => console.error("Error Fetching Data:", error));
  }, []);

  return (
    <div className="flex justify-center items-center h-screen">
      <h1 className="text-4xl font-bold">{message}</h1>
    </div>
  );
};

export default ApiPage;
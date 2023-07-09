import Link from "next/link";
import { useState } from "react";

// Pass config to React Context Provider
export default function QuestsButton() {
  const [isOrgsVisible, setIsOrgsVisible] = useState(false);

  return (
    <button className="btn btn-primary btn-sm" onClick={() => setIsOrgsVisible(true)}>
      Quests
    </button>
  );
}

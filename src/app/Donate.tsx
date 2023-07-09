import Link from "next/link";
import { useState } from "react";

// Pass config to React Context Provider
export default function Donate() {
  const [isOrgsVisible, setIsOrgsVisible] = useState(false);

  return (
    <button className="btn btn-primary" onClick={() => setIsOrgsVisible(true)}>
      Donate
    </button>
  );
}

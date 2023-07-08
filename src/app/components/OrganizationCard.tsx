import React from "react";

export default function OrganizationCard(
  id: String,
  name: String,
  contractAddress: String
) {
  return (
    <div>
      <p>Organization ID: {id}</p>
      <p>Name: {name}</p>
      <p>Contract Address: {contractAddress}</p>
    </div>
  );
}

"use client";

import React, { useEffect, useState } from "react";
import { EndaomentSdkApi } from "@endaoment/sdk";
import Image from "next/image";
import OrganizationCard from "./components/OrganizationCard";
import App from "./App";
const endaomentApi = new EndaomentSdkApi();

async function fetchOrgs(): Promise<any> {
  try {
    const response = await endaomentApi.getDeployedOrgs();
    return response;
  } catch (error) {
    console.error("Error fetching organizations:", error);
    throw error;
  }
}

export default function Home() {
  const [orgs, setOrgs] = useState<any[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const orgsData = await fetchOrgs();
        setOrgs(orgsData);
      } catch (error) {
        console.error("Error in Home component:", error);
      }
    };

    fetchData();
  }, []);

  if (typeof window === "undefined") {
    return null; // Render nothing on the server side
  }

  return (
    // <div>
    //   <h1 className="text-xl">Organizations</h1>
    //   {orgs.length > 0 ? (
    //     <ul>
    //       {orgs.map((org: any) => (
    //         <li key={org.id} className="mb-6">
    //           <p>Organization ID: {org.id}</p>
    //           <p>Name: {org.name}</p>
    //           <p>Contract Address: {org.contractAddress}</p>
    //           {/* <Image src={org.logoUrl} alt="" width={100} height={100} /> */}
    //         </li>
    //       ))}
    //     </ul>
    //   ) : (
    //     <p>No organizations found.</p>
    //   )}
    // </div>
    <div className="flex justify-center items-center">
      <App />
    </div>
  );
}

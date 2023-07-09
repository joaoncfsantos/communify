"use client";

import React, { useEffect, useState } from "react";
import { EndaomentSdkApi } from "@endaoment/sdk";
import Image from "next/image";
import ConnectWallet from "./ConnectWallet";
import Donate from "./Donate";
import OrganizationCard from "./components/OrganizationCard";
import QuestsButton from "./QuestsButton";
import Link from "next/link";
import QuestCard from "./components/QuestCard";
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
  const [showMain, setShowMain] = useState<boolean>(true);
  const [showQuests, setShowQuests] = useState<boolean>(false);

  const handleShowQuests = () => {
    setShowMain(false);
    setShowQuests(true);
  };

  const handleShowMain = () => {
    setShowMain(true);
    setShowQuests(false);
  };

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
    <div className="py-8 px-20">
      <div className="flex justify-between gap-5">
        <h1
          className="text-3xl font-medium text-[#4ECCA3] cursor-pointer"
          onClick={handleShowMain}
        >
          Communify
        </h1>
        <div className="flex gap-8">
          {/* <Link href="/questspage">
            <QuestsButton />
          </Link> */}
          <div onClick={handleShowQuests}>
            <QuestsButton />
          </div>

          <Donate />
          <ConnectWallet />
        </div>
      </div>
      {/* -------------------------------------------------------------------------------------------- */}
      {showQuests && (
        <div>
          <div className="flex justify-center">
            <div className="flex flex-col text-center justify-center gap-6 mt-36">
              <h2 className="text-6xl">Available Quests</h2>
              <h3 className="text-xl font-medium">
                Here you can find all the quests
              </h3>
            </div>
          </div>
          <div className="flex flex-col p-12 gap-8 justify-center items-center">
            <div className="flex flex-col gap-12">
              <QuestCard
                title="Barcelona Quest 1"
                creator="@BernardoReiis"
                description="This is a quest about Barcelona"
                group="Hackathon BCN"
                isCompleted={true}
              />
              <QuestCard
                title="Barcelona Quest 2"
                creator="@GugaRodri"
                description="This is another quest about Barcelona"
                group="Hackathon BCN"
                isCompleted={false}
              />
              <QuestCard
                title="Barcelona Quest 3"
                creator="@BernardoReiis"
                description="This is the last quest about Barcelona"
                group="Hackathon BCN"
                isCompleted={false}
              />
            </div>
          </div>
        </div>
      )}

      {showMain && (
        <div>
          <div className="flex justify-center">
            <div className="flex flex-col text-center justify-center gap-6 mt-36">
              <h2 className="text-6xl">
                Communifying your donations and impact!
              </h2>
              <h3 className="text-xl font-medium">
                Why donate alone when you can do it with your community?
              </h3>
            </div>
          </div>
          <div className="flex flex-col p-12 gap-8 justify-center items-center">
            <div className="flex gap-12">
              <OrganizationCard
                name={orgs[2]?.name}
                description={orgs[2]?.description}
                contractAddress={orgs[2]?.contractAddress}
              />
              <OrganizationCard
                name={orgs[13]?.name}
                description={orgs[13]?.description}
                contractAddress={orgs[13]?.contractAddress}
              />
              <OrganizationCard
                name={orgs[14]?.name}
                description={orgs[14]?.description}
                contractAddress={orgs[14]?.contractAddress}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

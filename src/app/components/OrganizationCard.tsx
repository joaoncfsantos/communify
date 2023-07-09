import React, { useState } from "react";

// import { useDebounce } from "use-debounce";
import { usePrepareSendTransaction } from "wagmi";

interface Props {
  name: string;
  description: string;
  contractAddress: string;
}

const OrganizationCard: React.FC<Props> = (props) => {
  const [donationAmount, setDonationAmount] = useState<string>("");
  const [buttonText, setButtonText] = useState<string>("Donate Now");

  const handleDonate = () => {
    setButtonText("Donated!");
    setDonationAmount("");
  };

  return (
    <div>
      <div className="card w-96 bg-base-100 shadow-xl">
        <figure>{/* <Image src={} /> */}</figure>
        <div className="card-body">
          <h2 className="card-title">{props.name}</h2>
          <p className="line-clamp-4">{props.description}</p>
          <div className="card-actions justify-between mt-4">
            <div>
              <input
                id="input"
                type="text"
                placeholder="USDC"
                className="input input-bordered w-32 max-w-xs"
                value={donationAmount}
                onChange={(e) => setDonationAmount(e.target.value)}
              />
            </div>
            <button className="btn btn-primary" onClick={handleDonate}>
              {buttonText}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrganizationCard;

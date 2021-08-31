import { SearchResponse, SearchResponseItem } from "./models";

import Offer from "./Offer";

interface OffersProps {
  offers: SearchResponse | null;
}

export default function Offers({ offers }: OffersProps): JSX.Element {
  if (offers == null) {
    return <div>"Nothing there yet"</div>;
  }

  const elements = offers.journeys.map((offer: SearchResponseItem) => (
    <Offer offer={offer} />
  ));

  return <div>{elements}</div>;
}

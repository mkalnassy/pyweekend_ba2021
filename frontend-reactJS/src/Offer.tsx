import { SearchResponseItem } from "./models";

interface OfferProps {
  offer: SearchResponseItem;
}

export default function Offer({ offer }: OfferProps) {
  return (
    <li>
      (destination) {offer.origin} - (origin) {offer.destination}, ({offer.departure} - {offer.arrival})
    </li>
  );
}

import { useState } from "react";

import "./App.css";

import { Container } from "react-bootstrap";

import { SearchResponse } from "./models";

import { search } from "./api";

import SearchForm from "./SearchForm";
import Offers from "./Offers";

function App() {
  const [offers, setOffers] = useState<null | SearchResponse>(null);

  const [origin, setOrigin] = useState<string>("");
  const [destination, setDestination] = useState<string>("");
  const [timeFrom, setTimeFrom] = useState<string>("");
  const [timeTo, setTimeTo] = useState<string>("");

  const [fetchInProgress, setFetchInProgress] = useState(false);

  const onSubmit = (
    origin: string,
    destination: string,
    timeFrom: string,
    timeTo: string
  ): void => {
    setFetchInProgress(true);
    search(origin, destination, timeFrom, timeTo, (offers) => {
      setOffers(offers);
      setFetchInProgress(false);
    });
  };

  if (fetchInProgress) {
    return <div>Searching...</div>;
  }

  return (
    <Container>
      <h1>Hyper ultra something-like-a-kiwi search</h1>
      <SearchForm
        onSubmit={onSubmit}
        origin={origin}
        setOrigin={setOrigin}
        destination={destination}
        setDestination={setDestination}
        timeTo={timeTo}
        setTimeTo={setTimeTo}
        timeFrom={timeFrom}
        setTimeFrom={setTimeFrom}
      />
      <Offers offers={offers} />
    </Container>
  );
}

export default App;

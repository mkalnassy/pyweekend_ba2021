import { useState } from "react";
import { Form, Button } from "react-bootstrap";

interface SearchFormProps {
  onSubmit: (
    origin: string,
    destination: string,
    timeFrom: string,
    timeTo: string
  ) => void;
  origin: string;
  setOrigin: (_: string) => void;
  destination: string;
  setDestination: (_: string) => void;
  timeFrom: string;
  setTimeFrom: (_: string) => void;
  timeTo: string;
  setTimeTo: (_: string) => void;
}

export default function SearchForm({ onSubmit,
  origin,
  setOrigin,
  destination,
  setDestination,
  timeFrom,
  setTimeFrom,
  timeTo,
  setTimeTo
}: SearchFormProps): JSX.Element {
  return (
    <Form>
      <Form.Group className="mb-3" controlId="origin">
        <Form.Label>Origin</Form.Label>
        <Form.Control
          type="text"
          placeholder="Origin"
          value={origin}
          onChange={(e) => setOrigin(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="destination">
        <Form.Label>Destination</Form.Label>
        <Form.Control
          type="text"
          placeholder="Destination"
          value={destination}
          onChange={(e) => setDestination(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="timeFrom">
        <Form.Label>From</Form.Label>
        <Form.Control
          type="datetime-local"
          placeholder="From"
          value={timeFrom}
          onChange={(e) => setTimeFrom(e.target.value)}
        />
      </Form.Group>

      <Form.Group className="mb-3" controlId="timeTo">
        <Form.Label>To</Form.Label>
        <Form.Control
          type="datetime-local"
          placeholder="To"
          value={timeTo}
          onChange={(e) => setTimeTo(e.target.value)}
        />
      </Form.Group>

      <Button variant="primary" type="button" onClick={() => onSubmit(origin, destination, timeFrom, timeTo)}>
        Search
      </Button>
    </Form>
  );
}

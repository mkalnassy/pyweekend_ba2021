export interface SearchResponse {
  journeys: SearchResponseItem[];
  origin: string;
  destination: string;
  time_from: string;
  time_to: string;
};

export interface SearchResponseItem {
  carrier: string;
  origin: string;
  destination: string;
  departure: string;
  arrival: string;
}

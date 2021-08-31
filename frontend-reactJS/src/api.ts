import { SearchResponse } from "./models";
import axios from "axios";

const API_URL = "http://localhost:8000";

export function search(
  origin: string,
  destination: string,
  timeFrom: string,
  timeTo: string,
  onSuccess: (response: SearchResponse) => void
): void {
  let formData = new FormData();
  formData.append("origin", origin);
  formData.append("destination", destination);
  formData.append("time_to", timeTo);
  formData.append("time_from", timeFrom);

  axios
    .post(`${API_URL}/search`, formData, {
      method: "post",
      headers: { "accept": "application/json" },
    })
    .then((res) => onSuccess(res.data));
}

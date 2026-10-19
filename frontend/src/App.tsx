import { useEffect, useState } from "react";
import PlacesMap from "./components/PlacesMap";

const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

type Place = {
  id: string;
  name: string;
  municipality: string;
  category: string;
  description: string;
  latitude: number;
  longitude: number;
};

function App() {
  const [status, setStatus] = useState("checking...");
  const [places, setPlaces] = useState<Place[]>([]);
  const [placesError, setPlacesError] = useState("");

  useEffect(() => {
    fetch(`${API_URL}/health`)
      .then((res) => res.json())
      .then((data) => setStatus(data.status))
      .catch(() => setStatus("backend unreachable"));
  }, []);

  useEffect(() => {
    fetch(`${API_URL}/places`)
      .then((res) => {
        if (!res.ok) throw new Error("bad response");
        return res.json();
      })
      .then((data: Place[]) => setPlaces(data))
      .catch(() => setPlacesError("Could not load places."));
  }, []);

  return (
    <main>
      <h1>Catanduanes Planner</h1>
      <p>Backend status: {status}</p>
      <PlacesMap places={places} />
      <h2>Places</h2>
      {placesError && <p>{placesError}</p>}
      <ul>
        {places.map((place) => (
          <li key={place.id}>
            <strong>{place.name}</strong> ({place.municipality},{" "}
            {place.category})
          </li>
        ))}
      </ul>
    </main>
  );
}

export default App;

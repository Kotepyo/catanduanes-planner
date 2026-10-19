import { useEffect, useRef } from "react";
import { Map as MapLibreMap, Marker, Popup, setWorkerUrl } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import workerUrl from "maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url";

setWorkerUrl(workerUrl);

export type MapPlace = {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
};

type Props = {
  places: MapPlace[];
};

function PlacesMap({ places }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const mapRef = useRef<MapLibreMap | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const map = new MapLibreMap({
      container: containerRef.current,
      style: {
        version: 8,
        sources: {
          osm: {
            type: "raster",
            tiles: ["https://tile.openstreetmap.org/{z}/{x}/{y}.png"],
            tileSize: 256,
            attribution: "© OpenStreetMap contributors",
            maxzoom: 19,
          },
        },
        layers: [{ id: "osm", type: "raster", source: "osm" }],
      },
      center: [124.25, 13.75],
      zoom: 9,
    });
    mapRef.current = map;

    return () => {
      map.remove();
      mapRef.current = null;
    };
  }, []);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    const markers = places.map((place) =>
      new Marker()
        .setLngLat([place.longitude, place.latitude])
        .setPopup(new Popup({ offset: 25 }).setText(place.name))
        .addTo(map)
    );

    return () => {
      markers.forEach((marker) => marker.remove());
    };
  }, [places]);

  return <div ref={containerRef} style={{ width: "100%", height: "400px" }} />;
}

export default PlacesMap;
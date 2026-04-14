"use client";

import { useEffect, useState } from "react";
import { MapKey } from "./Types";

const MAP_CONFIG: Record<
  MapKey,
  { src: string; label: string; sublabel: string }
> = {
  haram: {
    src: "/maps/Haram-map.png",
    label: "المسجد الحرام",
    sublabel: "الخريطة الرئيسية",
  },
  doors: {
    src: "/maps/Haram-map-doors.png",
    label: "أبواب الحرم",
    sublabel: "المداخل والبوابات",
  },
  bathrooms: {
    src: "/maps/Haram-map-bathrooms.png",
    label: "دورات المياه",
    sublabel: "المرافق القريبة",
  },
  cars: {
    src: "/maps/Haram-map-cars.png",
    label: "المواقف",
    sublabel: "السيارات والتنقل",
  },
  clock: {
    src: "/maps/Haram-map-clock.png",
    label: "برج الساعة",
    sublabel: "المعلم القريب",
  },
};

interface MapDisplayProps {
  currentMap: MapKey;
}

export default function MapDisplay({ currentMap }: MapDisplayProps) {
  const [displayedMap, setDisplayedMap] = useState<MapKey>(currentMap);
  const [transitioning, setTransitioning] = useState(false);

  useEffect(() => {
    if (currentMap !== displayedMap) {
      setTransitioning(true);

      const timer = setTimeout(() => {
        setDisplayedMap(currentMap);
        setTransitioning(false);
      }, 200);

      return () => clearTimeout(timer);
    }
  }, [currentMap, displayedMap]);

  const config = MAP_CONFIG[displayedMap];

  return (
    <div
      className="relative flex-shrink-0 overflow-hidden"
      style={{
        height: "38vh",
        minHeight: "220px",
        maxHeight: "360px",
        marginTop: "-1px",
     }}
    >
      <img
        key={displayedMap}
        src={config.src}
        alt={config.label}
        className="w-full h-full object-cover"
        style={{
          opacity: transitioning ? 0 : 1,
          transform: transitioning ? "scale(1.01)" : "scale(1)",
          transition: "opacity 0.28s ease, transform 0.28s ease",
        }}
      />

      <div
        className="absolute inset-0 pointer-events-none"
        style={{
          background:
            "linear-gradient(to bottom, rgba(0,0,0,0.06), transparent 28%, transparent 72%, rgba(0,0,0,0.12))",
        }}
      />

      <div
        className="absolute bottom-3 right-3 px-3 py-1.5 rounded-xl z-10"
        style={{
          background: "rgba(23,50,11,0.88)",
          backdropFilter: "blur(8px)",
          border: "1px solid rgba(255,255,246,0.22)",
        }}
      >
        <p className="text-xs font-bold leading-none" style={{ color: "#fffff6" }}>
          {config.label}
        </p>
        <p
          className="text-[9px] mt-0.5"
          style={{ color: "rgba(255,255,246,0.78)" }}
        >
          {config.sublabel}
        </p>
      </div>

      <div
        className="absolute bottom-3 left-3 flex flex-col gap-1 z-10"
        style={{
          background: "rgba(255,255,246,0.92)",
          backdropFilter: "blur(8px)",
          borderRadius: "10px",
          border: "1px solid rgba(23,50,11,0.12)",
        }}
      >
        <button className="w-8 h-8 flex items-center justify-center rounded-t-[9px] transition-colors text-lg font-light active:scale-95 text-[#17320b] hover:bg-[#f3f3ea]">
          +
        </button>
        <div className="h-px bg-[rgba(23,50,11,0.12)]" />
        <button className="w-8 h-8 flex items-center justify-center rounded-b-[9px] transition-colors text-lg font-light active:scale-95 text-[#17320b] hover:bg-[#f3f3ea]">
          −
        </button>
      </div>

      <button
        className="absolute top-3 left-3 w-9 h-9 flex items-center justify-center z-10 rounded-full active:scale-95 transition-all"
        style={{
          background: "rgba(255,255,246,0.92)",
          backdropFilter: "blur(8px)",
          border: "1px solid rgba(23,50,11,0.12)",
        }}
      >
        <svg
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="#17320b"
          strokeWidth="2.2"
          strokeLinecap="round"
          strokeLinejoin="round"
        >
          <circle cx="12" cy="12" r="3" />
          <path d="M12 2v3M12 19v3M2 12h3M19 12h3" />
        </svg>
      </button>
    </div>
  );
}

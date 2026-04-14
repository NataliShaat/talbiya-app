"use client";

import { useState, useEffect } from "react";
import SplashScreen from "./components/SplashScreen";
import MainScreen from "./components/MainScreen";

export default function Home() {
  const [showSplash, setShowSplash] = useState(true);
  const [fadeOut, setFadeOut] = useState(false);
  const [mainVisible, setMainVisible] = useState(false);

  useEffect(() => {
    const fadeTimer = setTimeout(() => setFadeOut(true), 2000);
    const mainTimer = setTimeout(() => setMainVisible(true), 2100);
    const hideTimer = setTimeout(() => setShowSplash(false), 2900);

    return () => {
      clearTimeout(fadeTimer);
      clearTimeout(mainTimer);
      clearTimeout(hideTimer);
    };
  }, []);

  return (
    <div className="min-h-screen w-full bg-[#17320b] md:flex md:items-center md:justify-center md:overflow-hidden">
      <div
        className="relative w-full min-h-screen bg-[#fffff6] overflow-hidden md:w-[390px] md:h-[844px] md:min-h-0 md:rounded-[48px] md:shadow-2xl md:border md:border-[rgba(255,255,246,0.35)]"
        style={{
          boxShadow:
            "0 30px 80px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.08)",
        }}
      >
        {/* Desktop-only fake iPhone chrome */}
        <div className="hidden md:block absolute top-0 left-0 right-0 h-[44px] bg-[#17320b] z-40" />

        <div className="hidden md:block absolute top-0 left-1/2 -translate-x-1/2 w-[120px] h-[34px] bg-black rounded-b-2xl z-50" />

        <div className="hidden md:flex absolute top-0 left-0 right-0 h-[44px] z-50 items-start pt-2 px-6 justify-between">
          <span className="text-[11px] font-semibold text-[#fffff6] mt-1">9:41</span>

          <div className="flex items-center gap-1 mt-1">
            <svg width="17" height="12" viewBox="0 0 17 12" fill="#fffff6">
              <rect x="0" y="3" width="3" height="9" rx="1" />
              <rect x="4.5" y="2" width="3" height="10" rx="1" />
              <rect x="9" y="0.5" width="3" height="11.5" rx="1" />
              <rect x="13.5" y="0" width="3" height="12" rx="1" opacity="0.45" />
            </svg>

            <svg width="16" height="12" viewBox="0 0 16 12" fill="#fffff6">
              <path d="M8 2.4C10.8 2.4 13.3 3.6 15 5.6L16 4.4C14 2 11.1 0.6 8 0.6C4.9 0.6 2 2 0 4.4L1 5.6C2.7 3.6 5.2 2.4 8 2.4Z" />
              <path d="M8 5.2C10 5.2 11.8 6.1 13 7.6L14 6.4C12.5 4.6 10.4 3.4 8 3.4C5.6 3.4 3.5 4.6 2 6.4L3 7.6C4.2 6.1 6 5.2 8 5.2Z" />
              <circle cx="8" cy="10" r="1.8" />
            </svg>

            <svg width="25" height="12" viewBox="0 0 25 12" fill="none">
              <rect
                x="0.5"
                y="0.5"
                width="21"
                height="11"
                rx="3.5"
                stroke="#fffff6"
                strokeOpacity="0.45"
              />
              <rect x="2" y="2" width="17" height="8" rx="2" fill="#fffff6" />
              <path
                d="M23 4.5V7.5C23.8 7.2 24.5 6.7 24.5 6C24.5 5.3 23.8 4.8 23 4.5Z"
                fill="#fffff6"
                fillOpacity="0.45"
              />
            </svg>
          </div>
        </div>

        <div className="absolute inset-0 bg-[#17320b]">
          <div
            style={{
              position: "absolute",
              inset: 0,
              opacity: mainVisible ? 1 : 0,
              transition: "opacity 0.6s ease",
            }}
            className="pt-0 md:pt-[44px]"
          >
            <MainScreen />
          </div>

          {showSplash && <SplashScreen fadeOut={fadeOut} />}
        </div>
      </div>
    </div>
  );
}

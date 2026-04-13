"use client";

interface SplashScreenProps {
  fadeOut: boolean;
}

export default function SplashScreen({ fadeOut }: SplashScreenProps) {
  return (
    <div
      className="absolute inset-0 overflow-hidden"
      style={{
        transition: "opacity 0.8s cubic-bezier(0.4, 0, 0.2, 1)",
        opacity: fadeOut ? 0 : 1,
        pointerEvents: fadeOut ? "none" : "auto",
        zIndex: 50,
        background: "#17320b",
      }}
    >
      <img
        src="/brand/splashscreen.png"
        alt="تلبية"
        className="absolute inset-0 w-full h-full object-cover object-center"
      />

      <div className="absolute bottom-16 left-0 right-0 flex justify-center gap-2">
        {[0, 1, 2].map((i) => (
          <div
            key={i}
            className="w-2.5 h-2.5 rounded-full"
            style={{
              background: "#fffff6",
              animation: `dot-bounce 1.2s ease-in-out ${i * 0.18}s infinite`,
              opacity: 0.9,
            }}
          />
        ))}
      </div>
    </div>
  );
}
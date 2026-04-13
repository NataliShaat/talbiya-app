"use client";

export default function Header() {
  return (
    <div
      className="flex items-center justify-between px-5 py-3 relative z-10"
      style={{
        background: "#17320b",
      }}
    >
      <button className="w-9 h-9 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors active:scale-95">
        <img
          src="/icons/options.png"
          alt="خيارات"
          className="w-5 h-5 object-contain"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = "none";
            const parent = target.parentElement!;
            parent.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fffff6" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/></svg>`;
          }}
        />
      </button>

      <div className="flex flex-col items-center">
        <h1
          className="text-2xl font-bold leading-none font-scheherazade"
          style={{
            color: "#fffff6",
            letterSpacing: "0.04em",
          }}
        >
          تَلبيَة
        </h1>
        <span
          className="text-[9px] opacity-90 mt-0.5 tracking-wider"
          style={{ color: "#fffff6" }}
        >
          مساعدك الذكي في الحرم
        </span>
      </div>

      <button className="w-9 h-9 flex items-center justify-center rounded-full hover:bg-white/10 transition-colors active:scale-95">
        <img
          src="/icons/profile.png"
          alt="الحساب"
          className="w-6 h-6 object-contain"
          onError={(e) => {
            const target = e.target as HTMLImageElement;
            target.style.display = "none";
            const parent = target.parentElement!;
            parent.innerHTML = `<svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fffff6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>`;
          }}
        />
      </button>
    </div>
  );
}
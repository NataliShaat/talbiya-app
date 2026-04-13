"use client";

import { useEffect, useRef, useState } from "react";
import { Message } from "./Types";

interface ChatAreaProps {
  messages: Message[];
  isTyping: boolean;
  onSend: (text: string) => void;
}

function StarAvatar({ size = 18 }: { size?: number }) {
  return (
    <img
      src="/icons/star.png"
      alt="AI"
      width={size}
      height={size}
      style={{ objectFit: "contain" }}
      onError={(e) => {
        const target = e.target as HTMLImageElement;
        target.style.display = "none";
        const parent = target.parentElement!;
        parent.innerHTML += `<svg width="${size}" height="${size}" viewBox="0 0 24 24" fill="#fffff6"><path d="M12 2c0 0 1.2 6.8 4 10 2.8 3.2 6 0 6 0s-6.8 1.2-10 4C8.8 19.2 12 22 12 22s-1.2-6.8-4-10C5.2 8.8 2 12 2 12s6.8-1.2 10-4C15.2 6.8 12 2 12 2Z"/></svg>`;
      }}
    />
  );
}

export default function ChatArea({
  messages,
  isTyping,
  onSend,
}: ChatAreaProps) {
  const [inputText, setInputText] = useState("");
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const handleSend = () => {
    if (!inputText.trim()) return;
    onSend(inputText.trim());
    setInputText("");
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") handleSend();
  };

  const handleMicClick = () => {
    setIsRecording((prev) => !prev);

    if (!isRecording) {
      setTimeout(() => {
        setIsRecording(false);
        onSend("أين أقرب باب؟");
      }, 1800);
    }
  };

  return (
    <div
      className="flex flex-col flex-1 min-h-0"
      style={{
        background: "#fffff6",
        marginTop: "-2px",
        borderTopLeftRadius: "32px",
        borderTopRightRadius: "32px",
        boxShadow: "0 -8px 30px rgba(0,0,0,0.04)",
        position: "relative",
        zIndex: 5,
        borderTop: "2px solid #17320b",
      }}
    >
      <div className="flex justify-center pt-3 pb-1">
        <div
          style={{
            width: 58,
            height: 5,
            borderRadius: 999,
            background: "rgba(23,50,11,0.16)",
          }}
        />
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-3 min-h-0">
        {messages.length === 0 ? (
          <div className="flex flex-col items-center justify-center h-full gap-4 pb-6">
            <div
              className="w-16 h-16 rounded-full flex items-center justify-center"
              style={{
                background: "#17320b",
                boxShadow: "0 12px 24px rgba(23,50,11,0.10)",
              }}
            >
              <StarAvatar size={24} />
            </div>

            <p
              className="text-lg text-center font-medium"
              style={{ color: "#17320b" }}
            >
              أنا معك في الحرم...كيف اقدر اساعدك؟     
            </p>

            <div className="flex flex-wrap gap-2 justify-center mt-1 px-1">
               {["أقرب بوابة", "أقرب دورات المياه", "حالة طارئة", "متى أتحرك؟"].map( (suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => onSend(suggestion)}
                    className="px-4 py-2 rounded-full text-sm font-medium transition-all active:scale-95"
                    style={{
                      background: "#fffff6",
                      color: "#17320b",
                      border: "1px solid rgba(23,50,11,0.22)",
                    }}
                  >
                    {suggestion}
                  </button>
                )
              )}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg, index) => (
              <div
                key={msg.id}
                className={`flex ${
                  msg.role === "user" ? "justify-start" : "justify-end"
                }`}
                style={{
                  animation: "fadeIn 0.3s ease forwards",
                  animationDelay: `${index * 0.04}s`,
                  opacity: 0,
                  animationFillMode: "forwards",
                }}
              >
                {msg.role === "assistant" && (
                  <div
                    className="w-7 h-7 rounded-full flex items-center justify-center ml-2 flex-shrink-0 self-end mb-0.5"
                    style={{ background: "#17320b" }}
                  >
                    <StarAvatar size={15} />
                  </div>
                )}

                <div
                  className={`max-w-[90%] px-4 py-3 text-sm leading-relaxed ${
                    msg.role === "user" ? "bubble-user" : "bubble-assistant"
                  }`}
                  style={{ direction: "rtl" }}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {isTyping && (
              <div
                className="flex justify-end"
                style={{ animation: "fadeIn 0.3s ease forwards" }}
              >
                <div
                  className="w-7 h-7 rounded-full flex items-center justify-center ml-2 flex-shrink-0 self-end mb-0.5"
                  style={{ background: "#17320b" }}
                >
                  <StarAvatar size={15} />
                </div>

                <div className="bubble-assistant px-4 py-3 flex gap-1.5 items-center">
                  {[0, 1, 2].map((i) => (
                    <div
                      key={i}
                      className="w-1.5 h-1.5 rounded-full"
                      style={{
                        background: "#17320b",
                        animation: `pulse-soft 1s ease-in-out ${i * 0.15}s infinite`,
                        opacity: 0.5,
                      }}
                    />
                  ))}
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      <div
        className="px-3 py-3 flex items-center gap-2"
        style={{
          background: "#fffff6",
          borderTop: "2px solid #17320b",
          boxShadow: "0 -2px 12px rgba(0,0,0,0.02)",
        }}
      >
        <button
          onClick={handleMicClick}
          className="w-10 h-10 flex items-center justify-center rounded-full flex-shrink-0 transition-all active:scale-90"
          style={{
            background: isRecording ? "#17320b" : "rgba(23,50,11,0.08)",
            boxShadow: isRecording ? "0 0 12px rgba(23,50,11,0.18)" : "none",
            border: "1px solid rgba(23,50,11,0.12)",
          }}
        >
          <img
            src="/icons/mic.png"
            alt="تسجيل صوتي"
            className="w-5 h-5 object-contain"
            style={{ filter: isRecording ? "brightness(0) invert(1)" : "none" }}
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = "none";
              const parent = target.parentElement!;
              parent.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="${
                isRecording ? "#fffff6" : "#17320b"
              }" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 10c0 3.9 3.1 7 7 7s7-3.1 7-7"/><line x1="12" y1="17" x2="12" y2="21"/><line x1="8" y1="21" x2="16" y2="21"/></svg>`;
            }}
          />
        </button>

        <div className="flex-1 relative">
          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="بماذا يمكنني مساعدتك؟"
            className="w-full text-sm outline-none"
            dir="rtl"
            style={{
              background: "#fffff6",
              borderRadius: "24px",
              padding: "13px 18px",
              border: "1.5px solid rgba(23,50,11,0.22)",
              color: "#17320b",
              fontFamily: '"Scheherazade New", serif',
              transition: "border-color 0.2s ease, box-shadow 0.2s ease",
            }}
            onFocus={(e) => {
              e.target.style.borderColor = "#17320b";
              e.target.style.boxShadow = "0 0 0 3px rgba(23,50,11,0.08)";
            }}
            onBlur={(e) => {
              e.target.style.borderColor = "rgba(23,50,11,0.22)";
              e.target.style.boxShadow = "none";
            }}
          />
        </div>

        <button
          onClick={handleSend}
          disabled={!inputText.trim()}
          className="w-10 h-10 flex items-center justify-center rounded-full flex-shrink-0 transition-all active:scale-90"
          style={{
            background: inputText.trim() ? "#17320b" : "rgba(23,50,11,0.08)",
            boxShadow: inputText.trim()
              ? "0 2px 8px rgba(23,50,11,0.16)"
              : "none",
            border: "1px solid rgba(23,50,11,0.12)",
          }}
        >
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            stroke={inputText.trim() ? "#fffff6" : "#17320b"}
            strokeWidth="2.2"
            strokeLinecap="round"
            strokeLinejoin="round"
            style={{
              transform: "rotate(180deg)",
              opacity: inputText.trim() ? 1 : 0.45,
            }}
          >
            <line x1="22" y1="2" x2="11" y2="13" />
            <polygon points="22 2 15 22 11 13 2 9 22 2" />
          </svg>
        </button>
      </div>
    </div>
  );
}
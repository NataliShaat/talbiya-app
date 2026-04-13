"use client";

import { useState } from "react";
import Header from "./Header";
import MapDisplay from "./MapDisplay";
import ChatArea from "./ChatArea";
import { BackendChatResponse, MapKey, Message } from "./Types";

export type { MapKey, Message };

function mapBackendImageToMapKey(mapImage?: string): MapKey {
  switch (mapImage) {
    case "Haram-map-doors.png":
      return "doors";
    case "Haram-map-bathrooms.png":
      return "bathrooms";
    case "Haram-map-cars.png":
      return "cars";
    case "Haram-map-clock.png":
      return "clock";
    case "Haram-map.png":
    default:
      return "haram";
  }
}

async function sendMessageToBackend(text: string): Promise<BackendChatResponse> {
  const response = await fetch("http://127.0.0.1:8000/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message: text }),
  });

  if (!response.ok) {
    throw new Error("Backend request failed");
  }

  return response.json();
}

export default function MainScreen() {
  const [currentMap, setCurrentMap] = useState<MapKey>("haram");
  const [messages, setMessages] = useState<Message[]>([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (text: string) => {
    if (!text.trim()) return;

    const userMsg: Message = {
      id: crypto.randomUUID(),
      role: "user",
      text,
    };

    setMessages((prev) => [...prev, userMsg]);
    setIsTyping(true);

    try {
      const result = await sendMessageToBackend(text);

      const reply =
        result?.data?.reply?.trim() ||
        "صار خلل بسيط، جرّب مرة ثانية.";

      const nextMap = mapBackendImageToMapKey(result?.data?.map_image);

      setCurrentMap(nextMap);

      const assistantMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: reply,
        map: nextMap,
      };

      setMessages((prev) => [...prev, assistantMsg]);
    } catch (error) {
      const fallbackMsg: Message = {
        id: crypto.randomUUID(),
        role: "assistant",
        text: "صار خطأ في الاتصال بالنظام. حاول مرة ثانية.",
        map: "haram",
      };

      setMessages((prev) => [...prev, fallbackMsg]);
      setCurrentMap("haram");
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-[#F8F7F4]">
      <Header />
      <MapDisplay currentMap={currentMap} />
      <ChatArea messages={messages} isTyping={isTyping} onSend={handleSend} />
    </div>
  );
}
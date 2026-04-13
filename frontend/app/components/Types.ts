export type MapKey = "haram" | "doors" | "bathrooms" | "cars" | "clock";

export interface Message {
  id: string;
  role: "user" | "assistant";
  text: string;
  map?: MapKey;
}

export interface BackendChatResponse {
  user_message: string;
  data: {
    map_type: string;
    map_image: string;
    intent?: string;
    emotion?: string;
    dialect?: string;
    reply: string;
  };
}
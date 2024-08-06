import { FieldValue } from "firebase/firestore";

export interface ChatBody {
  query: string;
  model: "Mistral" | "Llama2";
}

export type ChatResponse = { response: string } | { error: string };

export enum Role {
  AI = "ai",
  HUMAN = "human",
}

export interface ChatMessage {
  role: Role;
  content: string;
}

export interface Conversation {
  human: string;
  ai: string;
  createdAt?: FieldValue;
}

export interface ChatHistory {
  [key: string]: ChatMessage[];
}

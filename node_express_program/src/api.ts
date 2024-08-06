import { axiosInstance } from "./config";
import { ChatResponse } from "./types";

export const sendChat = async (
  model: string,
  query: string
): Promise<ChatResponse> => {
  try {
    const { data } = await axiosInstance.post("/chat", { model, query });
    return data;
  } catch (error) {
    console.error("Error in sendChat:", error);
    return { error: "Failed to send chat request." };
  }
};

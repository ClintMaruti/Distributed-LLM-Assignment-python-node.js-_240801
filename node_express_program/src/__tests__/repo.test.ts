import { addChatToDb, getMessages, getAllChats } from "../repo";
import { db } from "../../firebaseConfig";
import {
  collection,
  addDoc,
  getDocs,
  serverTimestamp,
} from "firebase/firestore";
import { ChatMessage, Conversation } from "../types";

jest.mock("../firebaseConfig", () => ({
  db: {},
}));

jest.mock("firebase/firestore", () => ({
  collection: jest.fn(),
  addDoc: jest.fn(),
  getDocs: jest.fn(),
  serverTimestamp: jest.fn(),
  query: jest.fn(),
  orderBy: jest.fn(),
}));

describe("Firebase Repository Functions", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("should add chat to the database", async () => {
    (addDoc as jest.Mock).mockResolvedValueOnce(undefined);

    await addChatToDb("test@example.com", { human: "Hello", ai: "Hi!" });

    expect(addDoc).toHaveBeenCalledWith(expect.anything(), {
      human: "Hello",
      ai: "Hi!",
      createdAt: serverTimestamp(),
    });
  });

  it("should fetch messages for a user", async () => {
    (getDocs as jest.Mock).mockResolvedValueOnce({
      docs: [{ data: () => ({ role: "ai", content: "Hi!" }) }],
    });

    const messages = await getMessages("test@example.com");
    expect(messages).toEqual([{ role: "ai", content: "Hi!" }]);
  });

  it("should fetch all chats", async () => {
    (getDocs as jest.Mock).mockResolvedValueOnce({
      docs: [
        {
          id: "test@example.com",
          ref: { collection: jest.fn().mockResolvedValueOnce({ docs: [] }) },
        },
      ],
    });

    const allChats = await getAllChats();
    expect(allChats).toEqual({});
  });
});

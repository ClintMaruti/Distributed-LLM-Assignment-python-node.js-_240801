import {
  collection,
  addDoc,
  getDocs,
  doc,
  serverTimestamp,
  query,
  orderBy,
} from "firebase/firestore";
import { db } from "../firebaseConfig";
import { ChatMessage, Conversation } from "./types";

export async function addChatToDb(user_email: string, message: Conversation) {
  try {
    const chatDocRef = doc(db, "chats", user_email);
    const messagesCollectionRef = collection(chatDocRef, "messages");
    await addDoc(messagesCollectionRef, {
      ...message,
      createdAt: serverTimestamp(),
    });
    console.log("Message added successfully");
  } catch (e) {
    console.error("Error adding document: ", e);
  }
}

export async function getMessages(email: string): Promise<ChatMessage[]> {
  const messages: ChatMessage[] = [];
  try {
    const chatDocRef = doc(db, "chats", email);
    const messagesCollectionRef = collection(chatDocRef, "messages");

    const messagesQuery = query(
      messagesCollectionRef,
      orderBy("createdAt", "desc")
    );

    const querySnapshot = await getDocs(messagesQuery);
    querySnapshot.forEach((doc) => {
      messages.push(doc.data() as ChatMessage);
    });
  } catch (error) {
    console.error("Error getting messages: ", error);
  }
  return messages;
}

export async function getAllChats(): Promise<Record<string, Conversation[]>> {
  try {
    const chatsCollectionRef = collection(db, "chats");
    const chatsSnapshot = await getDocs(chatsCollectionRef);
    const allChats: Record<string, Conversation[]> = {};

    for (const chatDoc of chatsSnapshot.docs) {
      const userEmail = chatDoc.id;
      const messagesCollectionRef = collection(chatDoc.ref, "messages");
      const messagesQuery = query(messagesCollectionRef, orderBy("createdAt"));
      const messagesSnapshot = await getDocs(messagesQuery);

      const messages: Conversation[] = messagesSnapshot.docs.map(
        (doc) => doc.data() as Conversation
      );

      allChats[userEmail] = messages;
    }

    return allChats;
  } catch (e) {
    console.error("Error fetching documents: ", e);
    throw e;
  }
}

import express, { Request, Response } from "express";
import { sendChat } from "./api";
import { addChatToDb, getAllChats, getMessages } from "./repo";
import { ChatResponse, Conversation } from "./types";

const router = express.Router();

router.get("/", (req: Request, res: Response) => res.send("Health check 100%"));

router.post("/chat", async (req: Request, res: Response) => {
  try {
    const { model, query, user_email } = req.body;

    if (!model || !query || !user_email) {
      return res
        .status(400)
        .json({ error: "'model', 'query', and 'user_email' are required!" });
    }

    const response = await sendChat(model, query);

    if ("response" in response) {
      const convo: Conversation = { human: query, ai: response.response };
      await addChatToDb(user_email, convo);
      return res.status(201).json(response);
    }

    res.status(400).json(response);
  } catch (error) {
    console.error("Error in /chat route:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

router.get("/conversation-history", async (req: Request, res: Response) => {
  try {
    const messages = await getAllChats();
    res.status(200).json(messages);
  } catch (error) {
    console.error("Error in /conversation-history route:", error);
    res.status(500).json({ error: "Internal server error" });
  }
});

router.get(
  "/conversation-history/:email",
  async (req: Request, res: Response) => {
    try {
      const { email } = req.params;
      if (!email) {
        return res.status(400).json({ error: "'email' cannot be empty!" });
      }
      const messages = await getMessages(email);
      res.status(200).json(messages);
    } catch (error) {
      console.error("Error in /conversation-history/:email route:", error);
      res.status(500).json({ error: "Internal server error" });
    }
  }
);

export default router;

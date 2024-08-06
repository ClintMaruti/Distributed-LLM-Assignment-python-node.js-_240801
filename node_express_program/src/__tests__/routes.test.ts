import request from "supertest";
import express from "express";
import router from "../routes";

const app = express();
app.use(express.json());
app.use(router);

describe("API Routes", () => {
  it("should return health check message", async () => {
    const response = await request(app).get("/");
    expect(response.status).toBe(200);
    expect(response.text).toBe("Health check 100%");
  });

  it("should handle POST /chat with valid data", async () => {
    const response = await request(app)
      .post("/chat")
      .send({
        model: "Mistral",
        query: "Hello",
        user_email: "test@example.com",
      });

    expect(response.status).toBe(201);
    expect(response.body).toHaveProperty("response");
  });

  it("should return 400 for missing parameters in POST /chat", async () => {
    const response = await request(app).post("/chat").send({});
    expect(response.status).toBe(400);
    expect(response.body).toHaveProperty("error");
  });
});

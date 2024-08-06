import { sendChat } from "../api";
import axios from "axios";
import MockAdapter from "axios-mock-adapter";

const mock = new MockAdapter(axios);

describe("sendChat", () => {
  it("should return chat response for successful API call", async () => {
    const mockResponse = { response: "Hello!" };
    mock.onPost("/chat").reply(200, mockResponse);

    const result = await sendChat("Mistral", "Hello");
    expect(result).toEqual(mockResponse);
  });

  it("should handle errors gracefully", async () => {
    mock.onPost("/chat").reply(500);

    const result = await sendChat("Mistral", "Hello");
    expect(result).toEqual({ error: "Failed to send chat request." });
  });
});

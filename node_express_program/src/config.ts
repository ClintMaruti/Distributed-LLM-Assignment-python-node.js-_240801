import dotenv from "dotenv";
import axios, { AxiosInstance } from "axios";

dotenv.config();

export const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.BASE_URL,
});

// src/firebaseConfig.ts

import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAULjhGtyofASM3rLpo31_auXdTVf7LRt8",
  authDomain: "hyperhire-2d88d.firebaseapp.com",
  projectId: "hyperhire-2d88d",
  storageBucket: "hyperhire-2d88d.appspot.com",
  messagingSenderId: "1095391667296",
  appId: "1:1095391667296:web:0acf4306284b1d7c428f05",
  measurementId: "G-FVV6HR4YLJ",
};

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };

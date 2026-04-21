import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyAkr7Aovna9Kq3a9uXlNzydpPecTa6xzvM",
  authDomain: "ak-analysis-system-umair.firebaseapp.com",
  projectId: "ak-analysis-system-umair",
  storageBucket: "ak-analysis-system-umair.firebasestorage.app",
  messagingSenderId: "877794258923",
  appId: "1:877794258923:web:a3f6df0f05e587093473ae"
};

const app = initializeApp(firebaseConfig);
export const db = getFirestore(app);

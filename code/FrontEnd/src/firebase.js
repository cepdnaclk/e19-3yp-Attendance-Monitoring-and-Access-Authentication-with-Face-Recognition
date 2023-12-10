// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import { getAuth } from "firebase/auth";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyCnopQGNISC5gMZTdNe9aubYCTby0xRuVo",
  authDomain: "ypproject-5b928.firebaseapp.com",
  projectId: "ypproject-5b928",
  storageBucket: "ypproject-5b928.appspot.com",
  messagingSenderId: "1094734042705",
  appId: "1:1094734042705:web:b1e014a28c4bee00ddca70",
  measurementId: "G-2QMZKVTVV8"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Initialize Firebase Authentication and get a reference to the service
const auth = getAuth(app);

export { auth };

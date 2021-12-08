
// Import the functions you need from the SDKs you need   
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.6.0/firebase-analytics.js";

// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional

const firebaseConfig = {
  apiKey: "AIzaSyAa83ZWl-i_3pWpsMncl9G1553oXSuPD0s",
  authDomain: "icu-diary.firebaseapp.com",
  projectId: "icu-diary",
  storageBucket: "icu-diary.appspot.com",
  messagingSenderId: "353609023120",
  appId: "1:353609023120:web:8556c4b6583b6a6a6fa215",
  measurementId: "G-Z3SGGCH5QY"
};


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Get a reference to the storage service, which is used to create references in your storage bucket
const storage = getStorage(firebaseApp);

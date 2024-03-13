import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signInWithPopup,
  signOut,
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCx8npTDa3pF5_K0Tc1B6DezRHC4oKbXhM",
  authDomain: "test-aa16b.firebaseapp.com",
  projectId: "test-aa16b",
  storageBucket: "test-aa16b.appspot.com",
  messagingSenderId: "479276953122",
  appId: "1:479276953122:web:e4ac18271b48282ac7a47b",
};

const app = initializeApp(firebaseConfig);

const provider_google = new GoogleAuthProvider();
const auth = getAuth(app);
auth.languageCode = "en";

const googleLogin = document.getElementById("login-google");
googleLogin?.addEventListener("click", function () {
  signInWithPopup(auth, provider_google)
    .then((result) => {
      const credential = GoogleAuthProvider.credentialFromResult(result);
      const token = credential.accessToken;
      const user = result.user;
      const dataToPython = { User: user, Token: token };

      fetch("/toMyMap", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToPython),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Data from Python:", data);
          window.location.href = "/toMyMap";
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

const LoginEmail = document.getElementById("LoginEmail");
const LoginPass = document.getElementById("LoginPass");
const emailpassLogin = document.getElementById("login-emailpass");
emailpassLogin?.addEventListener("click", function () {
  signInWithEmailAndPassword(auth, LoginEmail.value, LoginPass.value)
    .then((userCredential) => {
      const user = userCredential.user;
      const token = userCredential.accessToken;
      const dataToPython = { User: user, Token: token };

      fetch("/toMyMap", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dataToPython),
      })
        .then((response) => response.json())
        .then((data) => {
          console.log("Data from Python:", data);
          window.location.href = "/toMyMap";
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});

const inputEmail = document.getElementById("inputEmail");
const inputPass = document.getElementById("inputPass");
const CreateAccount = document.getElementById("CreateAccount");
CreateAccount?.addEventListener("click", function () {
  if (!inputEmail.value || !inputPass.value) {
    alert("空文字またはnullです");
  } else {
    createUserWithEmailAndPassword(auth, inputEmail.value, inputPass.value)
      .then((userCredential) => {
        // Signed in
        const user = userCredential.user;
        // ...
        alert("アカウント作成が完了しました");
      })
      .catch((error) => {
        alert("存在しないメールアドレスです");
      });
  }
});

const Logout = document.getElementById("logout-btn");
Logout?.addEventListener("click", function () {
  signOut(auth)
    .then(() => {
      window.location.href = "/";
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
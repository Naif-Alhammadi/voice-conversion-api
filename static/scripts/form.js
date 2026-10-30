'use strict'

const haveAnAccount = document.querySelector("#have-question");
const donotHave = document.querySelector("#donotHave");

const register = document.querySelector(".register");
const login = document.querySelector(".login");

const loginForm = document.querySelector("#login-form");

const loginName = document.querySelector("#name");
const loginPassword = document.querySelector("#password");
const loginVerifyPassword = document.querySelector("#verifypassword");
const loginEmail = document.querySelector("#email");

const errorText = document.querySelector(".error-text");


haveAnAccount.addEventListener("click", function(){
    login.style.transform = "translateX(-260px)";
    register.style.transform = "translateX(0px)";
});

donotHave.addEventListener("click", function() {
    login.style.transform = "translateX(0px)";
    register.style.transform = "translateX(260px)";
});


loginForm.addEventListener("submit", event => {
    event.preventDefault();

    fetch("/login", {
    method:"POST",
    headers: {
        "Content-Type": "application/json"
    },
    body: JSON.stringify({
        "name": loginName.value,
        "email": loginEmail.value,
        "password": loginPassword.value,
        "verifypassword": loginVerifyPassword.value
    }),
}).then(response => response.json()).then(data => {
    if (data["redirect"])
    {
        window.location.href = data["location"];
    }
    else
    {
        errorText.innerHTML = data["message"];
    }
}).catch (error => {
    console.error(error);
});
});


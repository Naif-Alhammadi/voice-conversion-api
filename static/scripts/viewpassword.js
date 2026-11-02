'use strict'

const viewPassword = document.querySelector("#password");
const iconPassword = document.querySelector("#password-icon");

const verifyPassword = document.querySelector("#verifypassword");
const verifyIconPassword = document.querySelector("#verifypassword-icon");

const viewRegisterPassword = document.querySelector("#register-password");
const iconPasswordRegister = document.querySelector("#password-icon-register");


// return the type of the input
const passwordType = function(type)
{
    if (type === "password")
    {
        type = "text";
        return type
    }

    else
        type = "password";
        return type
}

// icon check
const checkEye = function(icon)
{
    const iconContainClass = icon.classList.contains("fa-eye");
    if (!iconContainClass)
    {
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
    }

    else 
    {
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
    }
}

// inspact passwrod
iconPassword.addEventListener("click", function(){
    viewPassword.type = passwordType(viewPassword.type);

    checkEye(iconPassword);
});


// inspact verify password
verifyIconPassword.addEventListener("click", function(){
    verifyPassword.type = passwordType(verifyPassword.type);

    checkEye(verifyIconPassword);
});


// inspact register password
iconPasswordRegister.addEventListener("click", function(){
    viewRegisterPassword.type = passwordType(viewRegisterPassword.type);

    checkEye(iconPasswordRegister);
});
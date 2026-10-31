'use strict'


// ===== light mode package =====
// --ice-silver: #DDE3E8;
// --deep-aubergine: #3A0F34;
// --marigold: #EAAA00;
// --linerar-1: #dde3e87e;
// --linear-2: #3a0f347d;
// --image: url(../images/light-background.jpg);



// ===== dark mode package =====
// --jet-black: #0A0A0A;
// --cerulean-blue: #007BA7;
// --neon-rose: #FF2D95;
// --linerar-1: #0a0a0a7b;
// --linear-2: #007aa774;
// --image: url(../images/dark-background.jpg);
// document.querySelector(".img").src = "../static/images/light-mic.png"


// the mode that being selected
let mode = document.querySelector("#mode");


// query if user is already changed the default preferred mode
fetch('/preferred-mode').then(response => response.json()).then(data => {

    // if mode was dark
    if(data["mode"] === "dark")
    {
        // update the value of the mdoe
        mode.value = data["mode"]
        document.documentElement.style.setProperty("--primary", "#0A0A0A");
        document.documentElement.style.setProperty("--secondary", "#007BA7");
        document.documentElement.style.setProperty("--third", "#FF2D95");
        document.documentElement.style.setProperty("--text", "#FFF");
            
        const img = document.querySelector(".img");
        
        // if the image does exist (The page that contains the picture)
        if (img !== null)
        {
            document.querySelector(".img").src = "../static/images/dark-mic.png";
        }
        
        // update the value of the mdoe
        document.documentElement.style.setProperty("--linerar-1", "#0a0a0a7b");
        document.documentElement.style.setProperty("--linerar-2", "#007aa774");
        document.documentElement.style.setProperty("--image", "url(../images/dark-background.jpg)");
                  
    }
          
    // if mode was light
    else if(data["mode"] === "light")
    {
        // update the value of the mdoe
        mode.value = data["mode"]
        document.documentElement.style.setProperty("--primary", "#DDE3E8");
        document.documentElement.style.setProperty("--secondary", "#3A0F34");
        document.documentElement.style.setProperty("--third", "#EAAA00");
        document.documentElement.style.setProperty("--text", "#000");

        // if the image does exist (The page that contains the picture)
        const img = document.querySelector(".img");

        if (img !== null)
        {
            document.querySelector(".img").src = "../static/images/light-mic.png";
        }

        // update the value of the mdoe
        document.documentElement.style.setProperty("--linerar-1", "#dde3e87e");
        document.documentElement.style.setProperty("--linerar-2", "#3a0f347d");
        document.documentElement.style.setProperty("--image", "url(../images/light-background.jpg)");
    
        // check if page is conversion or log in make the --text property white
        const loginPage = String(window.location.href);
        const loginWordLength = 5;
        const isLogin = loginPage.slice(loginWordLength * -1);
    
        const conversionPage = String(window.location.href);
        const conversionWordLength = 10;
        const isConversion = conversionPage.slice(conversionWordLength * -1);
        if(isConversion === "conversion" || isLogin === "login")
        {
            document.documentElement.style.setProperty("--text", "#FFF");
        }
    } 
});


// if user change the current selected value
mode.addEventListener("change", function(){
    fetch('/preferred-mode', {
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({"mode": mode.value})
    }).then(response => response.json()).then(data => {
        
        // if mode is dark
        if(data["mode"] === "dark")
        {
            // update the value of the mdoe
            document.documentElement.style.setProperty("--primary", "#0A0A0A");
            document.documentElement.style.setProperty("--secondary", "#007BA7");
            document.documentElement.style.setProperty("--third", "#FF2D95");
            document.documentElement.style.setProperty("--text", "#FFF");

            // if the image does exist (The page that contains the picture)
            const img = document.querySelector(".img");

            if (img !== null)
            {
                document.querySelector(".img").src = "../static/images/dark-mic.png";
            }

            // update the value of the mdoe
            document.documentElement.style.setProperty("--linerar-1", "#0a0a0a7b");
            document.documentElement.style.setProperty("--linerar-2", "#007aa774");
            document.documentElement.style.setProperty("--image", "url(../images/dark-background.jpg)");
        }

        // if mode is light
        else if(data["mode"] === "light")
        {
            // update the value of the mdoe
            document.documentElement.style.setProperty("--primary", "#DDE3E8");
            document.documentElement.style.setProperty("--secondary", "#3A0F34");
            document.documentElement.style.setProperty("--third", "#EAAA00");
            document.documentElement.style.setProperty("--text", "#000");


            // if the image does exist (The page that contains the picture)
            const img = document.querySelector(".img");

            if (img !== null)
            {
                document.querySelector(".img").src = "../static/images/light-mic.png";
            }
            
            // update the value of the mdoe
            document.documentElement.style.setProperty("--linerar-1", "#dde3e87e");
            document.documentElement.style.setProperty("--linerar-2", "#3a0f347d");
            document.documentElement.style.setProperty("--image", "url(../images/light-background.jpg)");


            // check if page is conversion or log in make the --text property white
            const loginPage = String(window.location.href);
            const loginWordLength = 5;
            const isLogin = loginPage.slice(loginWordLength * -1);

            const conversionPage = String(window.location.href);
            const conversionWordLength = 10;
            const isConversion = conversionPage.slice(conversionWordLength * -1);
            if(isConversion === "conversion" || isLogin === "login")
            {
                document.documentElement.style.setProperty("--text", "#FFF");
            }
        }
    });
});
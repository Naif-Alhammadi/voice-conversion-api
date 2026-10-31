'use strict'

const activeList = document.querySelectorAll('.specific-list-choice');


// weather queries info
let weather;
let dayOrNight;
let userCity;
let localTime = document.querySelector('#time');
let morOrNight = document.querySelector('#mor-or-night');

// responsive nav
const nav = document.querySelector(".responsive-nav");
const tag = document.querySelector("#nav-toggle");

activeList[0].classList.add('active-list');


for (let list of activeList)
{
    list.addEventListener('click', function() {
    if(!list.classList.contains('active-list'))
    {
        for (let i = 0; i < activeList.length; i++)
        {
            activeList[i].classList.remove('active-list');
        }
    }
        list.classList.add('active-list');
    });
}

// get user location for the weather display
navigator.geolocation.getCurrentPosition(position => {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    
    fetch("/weather").then(response => 
        {
            if(!response.ok)
            {
                throw new Error(`HTTP Error ${response.status}`);
            }
            return response.json();
        }).then(data => {
            fetch(`https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lon}&appid=${data["weatherAPI"]}`).then(response => response.json()).then(data => {

                weather = data.weather[0]['main'];
                dayOrNight = data.weather[0]['icon'];
                userCity = data.name
                if(dayOrNight.slice(-1) === 'n')
                {
                    morOrNight.innerHTML = "🎑";
                }
        
                else {
                    morOrNight.innerHTML = "🌅"
                }
            }).catch(error => {
                console.log(error);
            });

    }).catch(error => {
        console.log(error);
    })},
(error) => {
    console.log("something went wronge");
    }
);

function time()
{
    const now = new Date();
    localTime.innerHTML = now.toLocaleString(undefined, {
        weekday: "long",
        year: "numeric",
        day:"numeric",
        hour:"2-digit",
        minute: "2-digit",
        second: "2-digit"
    });
}

setInterval(time, 1000);


// responsive nav
tag.addEventListener("click", function(){
    nav.classList.toggle("active-res-nav");
});
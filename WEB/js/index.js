let bChoosedCity = false;

let city_pick = document.getElementsByClassName('city-img');
let choosedCity = null;

let choosedCityStr = null;

for(i = 0; i < city_pick.length; i++) {
    city_pick[i].addEventListener('click', (e) => {
        if(!bChoosedCity) {
            choosedCity = e.target;
            choosedCityStr = e.target.firstElementChild.innerText.toLowerCase().replace("'", "");
            e.target.style = "background-size: 100% 100%;";
            e.target.lastElementChild.style = "font-size: 60px;"
            bChoosedCity = true;
        }
        else {
            choosedCity.style = "background-size: 100% 0px;";
            choosedCity.lastElementChild.style = ""
            choosedCity = e.target;
            choosedCityStr = e.target.firstElementChild.innerText.toLowerCase().replace("'", "");
            e.target.style = "background-size: 100% 100%;";
            e.target.lastElementChild.style = "font-size: 60px;"
        }
    })
}
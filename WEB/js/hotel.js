var url = document.location.toString();
var urlParmStr = url.slice(url.indexOf('?')+1);//获取问号后所有的字符串
//console.log(urlParmStr);
var default_url = "http://127.0.0.1:5000";

if(urlParmStr) urlParmStr = "/" + urlParmStr;

let selectedFlightID = null;

function getbus() {
    fetch(default_url + '/hotels' + urlParmStr , {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('获取航班信息失败:', data.error);
        } else {
            //console.log(data);
            for (i = 0; i < Object.keys(data).length; i++) {
                //console.log(i);
                let newFlightlistInfo = document.createElement('div');
                newFlightlistInfo.setAttribute("class", "flightlist-info flightlist-bottom");
                newFlightlistInfo.setAttribute("id", data[i].location);
                let newFlightfrom = document.createElement('div');
                newFlightfrom.setAttribute("class", "flightlist-item flightfrom");
                newFlightfrom.innerText = data[i].location;
                let newFlightarrive = document.createElement('div');
                newFlightarrive.setAttribute("class", "flightlist-item flightarrive");
                newFlightarrive.innerText = data[i].num_rooms;
                let newFlightseat = document.createElement('div');
                newFlightseat.setAttribute("class", "flightlist-item flightseat");
                newFlightseat.innerText = data[i].num_avail;
                let newFlightprice = document.createElement('div');
                newFlightprice.setAttribute("class", "flightlist-item flightprice");
                newFlightprice.innerText = data[i].price;

                newFlightlistInfo.appendChild(newFlightfrom);
                newFlightlistInfo.appendChild(newFlightarrive);
                newFlightlistInfo.appendChild(newFlightseat);
                newFlightlistInfo.appendChild(newFlightprice);

                document.getElementById('fl').appendChild(newFlightlistInfo);
            }
            addEvent();
        }
    })
}

getbus();

function reservation() {
    let inputname = document.getElementsByClassName('userName')[0].value;
    fetch(default_url + '/hotels', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            custname : inputname,
            hotel_location : selectedFlightID
        })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('提交失败');
            } else {
                console.log('提交成功');
                document.getElementById('fl').innerHTML="<div class='flightlist-info flightlist-top'><div class='flightlist-topitem'>所在城市</div><div class='flightlist-topitem'>房间数量</div><div class='flightlist-topitem'>空房间数量</div><div class='flightlist-topitem'>价格</div></div>";
                getbus();
            }
        })
}

function addEvent() {
    let fl_items = document.getElementsByClassName("flightlist-bottom");
    for(i = 0; i < fl_items.length; i++) {
        fl_items[i].addEventListener("click", (e) => {
            e.target.style = "background-color: #536976AA; color: white;";
            if(selectedFlightID) {
                if(selectedFlightID != e.target.id) {
                    document.getElementById(selectedFlightID).style = "";
                }
            }
            selectedFlightID = e.target.id;
        })
    }
}

document.getElementsByClassName('checkBTN')[0].addEventListener('click', (e) => {
    if(document.getElementsByClassName('userName')[0].value != ""&&selectedFlightID) {
        reservation();
        console.log(document.getElementsByClassName('userName')[0].value + " | " + selectedFlightID);
        e.target.style = "background: green;"
        e.target.innerText = "预定成功"
    }
    else if(!selectedFlightID) {
        console.log(selectedFlightID);
        e.target.style = "background: red;"
        e.target.innerText = "请选择宾馆"
    }
    else if(document.getElementsByClassName('userName')[0].value == "") {
        e.target.style = "background: red;"
        e.target.innerText = "请输入乘客名"
    }
})
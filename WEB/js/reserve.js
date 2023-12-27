var default_url = "http://127.0.0.1:5000";

function getreserve(username) {
    fetch(default_url + '/reserve', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({ custname: username }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error('获取信息失败:', data.error);
        } else {
            document.getElementById('fl').innerHTML = "<div class='flightlist-info flightlist-top'><div class='flightlist-topitem'>预定乘客名</div><div class='flightlist-topitem'>预定场景</div><div class='flightlist-topitem'>位置/出发地</div><div class='flightlist-topitem'>操作</div></div>";
            //console.log(data);
            for (i = 0; i < Object.keys(data).length - 1; i++) {
                //console.log(i);
                console.log(data);
                let newFlightlistInfo = document.createElement('div');
                newFlightlistInfo.setAttribute("class", "flightlist-info flightlist-bottom");
                newFlightlistInfo.setAttribute("id", "i" + data[i].id);
                
                let newFlightfrom = document.createElement('div');
                newFlightfrom.setAttribute("class", "flightlist-item flightfrom");
                newFlightfrom.innerText = data[i].passenger_name;
                
                let newFlightseat = document.createElement('div');
                newFlightseat.setAttribute("class", "flightlist-item flightseat");
                newFlightseat.innerText = data[i].reservation_type;
                
                let newFlightprice = document.createElement('div');
                newFlightprice.setAttribute("class", "flightlist-item flightprice");
                newFlightprice.innerText = data[i].value;

                let newCtrlContainer = document.createElement('div');
                newCtrlContainer.setAttribute("class", "flightlist-item");

                let newCtrl_del = document.createElement('button');
                newCtrl_del.setAttribute("class", "flightlist-btns");
                newCtrl_del.innerText = "删除";
                newCtrl_del.setAttribute("id", data[i].id);

                newCtrlContainer.appendChild(newCtrl_del);

                newFlightlistInfo.appendChild(newFlightfrom);
                newFlightlistInfo.appendChild(newFlightseat);
                newFlightlistInfo.appendChild(newFlightprice);
                newFlightlistInfo.appendChild(newCtrlContainer);

                document.getElementById('fl').appendChild(newFlightlistInfo);
            }
            if(data[Object.keys(data).length - 1].is_route_complete) {
                document.getElementById('good').innerText = "合理的路线";
            }
            else {
                document.getElementById('good').innerText = "不合理的路线";
            }
            addEvents();
        }
    })
}

function deleteResv(resv_id) {
    fetch(default_url + '/reservations/' + resv_id, {
    method: 'DELETE',
    headers: {
        'Content-Type': 'application/json',
    },
    })
    .then(response => response.json())
}

function addEvents() {
    let btns = document.getElementsByClassName('flightlist-btns');
    for(i = 0; i < btns.length; i++) {
        btns[i].addEventListener('click', (e) => {
            document.getElementById('fl').removeChild(document.getElementById('i' + e.target.id));
            deleteResv(e.target.id);
        })
    }
}

document.getElementsByClassName('checkBTN')[0].addEventListener('click', (e) => {
    if(document.getElementsByClassName("userName")[0].value != "") {
        getreserve(document.getElementsByClassName("userName")[0].value);
    }
})
// add or modify stock 
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "account_type": 1,
  "account_number": "123456",
  "stock_data": {
    "stock_symbol": "AAL",
    "owning_price": 150,
    "t0_volume": 500,
    "t1_volume": 300,
    "t2_volume": 200,
    "other_volume": 700,
    "having_volume": 8000,
    "reward_volume": 0,
    "FS_volume": 0,
    "Outroom_volume": 0
  }
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("https://magnetic-eminent-bass.ngrok-free.app/stock/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));



// delete a stock 
var requestOptions = {
    method: 'DELETE',
    redirect: 'follow'
  };
  
  fetch("https://magnetic-eminent-bass.ngrok-free.app/stock/123456/1/AAL/", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));


// get account summary 
var requestOptions = {
    method: 'GET',
    redirect: 'follow'
  };
  
  fetch("https://magnetic-eminent-bass.ngrok-free.app/account-summary/123456/1/", requestOptions)
    .then(response => response.text())
    .then(result => console.log(result))
    .catch(error => console.log('error', error));


// modify account summary 
var myHeaders = new Headers();
myHeaders.append("Content-Type", "application/json");

var raw = JSON.stringify({
  "account_type": 3,
  "account_number": "123456",
  "total_asset": 150000,
  "total_cash": 50000,
  "margin_ratio": 50
});

var requestOptions = {
  method: 'POST',
  headers: myHeaders,
  body: raw,
  redirect: 'follow'
};

fetch("https://magnetic-eminent-bass.ngrok-free.app/add-or-modify-summary/", requestOptions)
  .then(response => response.text())
  .then(result => console.log(result))
  .catch(error => console.log('error', error));

let url = 'http://127.0.0.1:5000/data'

function getData(){
    fetch(url).then((response)=>{
        return response.json();
    }).then((data)=>{
        console.log(data);
    })
}

let values = getData()

console.log(values)
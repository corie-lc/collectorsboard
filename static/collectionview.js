// scrolling systems for collectionview.html


counter = 0;
var id="#observer"
list_p = []


const numSteps = 20.0;

let boxElement = document.querySelector(id)
let prevRatio = 0.0;
let increasingColor = "rgba(40, 40, 190, ratio)";
let decreasingColor = "rgba(190, 40, 40, ratio)";

// Set things up
window.addEventListener(
    "DOMContentLoaded",
    (event) => {
    boxElement = document.querySelector(id);

    createObserver();
    },
    false
);

function createObserver() {
    let observer;

    let options = {
        root: null,
        rootMargin: "0px",
        threshold: buildThresholdList(),
    };

    observer = new IntersectionObserver(handleIntersect, options);
    observer.observe(boxElement);
}

function buildThresholdList() {
    let thresholds = [];
    let numSteps = 0.5;

     for (let i = 0.5; i <= numSteps; i++) {
        let ratio = i / numSteps;
        thresholds.push(ratio);
    }

    thresholds.push(0);
    return thresholds;
}

function handleStuff(observer){
    console.time('doSomething')

    var currentLocation = window.location;
    const urlArray = currentLocation.toString().split("/");

    $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_collectionview_feed",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counter, id: urlArray[4].replace("?", "")  }),
            success: function(data) {

                if(data[0] == "none"){
                    document.querySelector("#observer").innerHTML = "Nothing else :("
                } else{

                    var doc = new DOMParser().parseFromString(data[0], "text/html")
                    var duplicate = false;

                    if(list_p.includes(doc.getElementById("div-post").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('post_list').insertAdjacentHTML('beforeend', data[0])
                        counter = (Number(data[1]) + 4);
                        duplicate = false;
                        list_p.push(doc.getElementById("div-post").getAttribute("value"))
                    }

                    console.timeEnd('doSomething')

                    observer.observe(boxElement)







                }

            }
        });;


}

function handleIntersect(entries, observer) {
        console.log("here lol")
        observer.unobserve(boxElement)
        entries.forEach((entry) => {

        handleStuff(observer);


    });
}


// control systems for collectionview

function editCollection(collectionId){

    let newName = document.getElementById("name_input").value
    let newDesc = document.getElementById("desc_input").value
    let valueDesc = document.getElementById("value_input").value


    

    function isFloat(n) {
        return n === +n && n !== (n|0);
    }
    
    function isInteger(n) {
        return n === +n && n === (n|0);
    }

    if(!isNaN(valueDesc)) {



            $.ajax({
            type: "POST",
            dataType: "json",
            url: "/edit_collection",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ collection_id: collectionId, name: newName, desc: newDesc, community: $('.js-example-basic-single').val(), value: valueDesc  }),
            
            });;

            document.getElementById("collection_name_text").innerHTML = newName
            document.getElementById("info").innerHTML = newDesc
            document.getElementById("value_id").innerHTML = "$" + valueDesc
            document.getElementById("community_id").innerHTML = $('.js-example-basic-single').val()  

    } else{

        document.getElementById("value_input").value = '';
        document.getElementById("value_input").style.borderColor = "red";
    }

        


}

function autoValue(collectionId){


    document.getElementById("value_input").value = "Loading.. Please Wait!";



    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/value_collection",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ collection_id: collectionId}),
      success: function(data) {
        document.getElementById("value_input").value = data;
        
      }
      
    });;

    


}












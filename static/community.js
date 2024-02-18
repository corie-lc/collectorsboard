var counter = 0;
var id="#observer"
var list_p = []
const numSteps = 20.0;
let boxElement = document.querySelector(id)

var counterCollections = 0;
var idCollections="#observer_collections"
var list_pCollections = []
let boxElementCollection = document.querySelector(idCollections)

var counterTopPosts = 0;
var idTopPosts="#observer_top_posts"
var list_pTopPosts = []
let boxElementTopPosts = document.querySelector(idTopPosts)





function scrolling(handle){


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

        observer = new IntersectionObserver(handle, options);
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
}

function handleIntersect(entries, observer) {
        entries.forEach((entry) => {

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_feed",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counter, type: "community_feed", community: document.getElementById("community_name").innerText,  }),
            success: function(data) {

                if(data[0] == "none"){
                    document.querySelector("#observer").innerHTML = "No More Posts :("
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

                }

            }
        });;

    });
}

function scrollingCollections(handle){


// Set things up
    window.addEventListener(
        "DOMContentLoaded",
        (event) => {
        boxElement = document.querySelector(idCollections);

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

        observer = new IntersectionObserver(handle, options);
        observer.observe(boxElementCollection);
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
}

function handleIntersectCollection(entries, observer) {
        entries.forEach((entry) => {
            console.log("hererererererererererereerererererererererer")

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_feed_collection",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counterCollections, type: "community_feed", community: document.getElementById("community_name").innerText }),
            success: function(data) {

                if(data[0] == "none"){
                    document.querySelector(idCollections).innerHTML = "No More Collections :("
                } else{

                    var doc = new DOMParser().parseFromString(data[0], "text/html")
                    var duplicate = false;

                    if(list_pCollections.includes(doc.getElementById("div-collection").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('collection_list_c').insertAdjacentHTML('beforeend', data[0])
                        counterCollections = (Number(data[1]) + 4);
                        duplicate = false;
                        list_p.push(doc.getElementById("div-collection").getAttribute("value"))
                    }

                }

            }
        });;

    });
}

function scrollingTopPosts(handle){


// Set things up
    window.addEventListener(
        "DOMContentLoaded",
        (event) => {
        boxElement = document.querySelector(idTopPosts);

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

        observer = new IntersectionObserver(handle, options);
        observer.observe(boxElementTopPosts);
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
}

function handleIntersectTopPosts(entries, observer) {
        entries.forEach((entry) => {

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_feed_collection",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counterTopPosts, type: "community_feed", community: document.getElementById("community_name").innerText }),
            success: function(data) {


                if(data[0] == "none"){
                    document.querySelector(idTopPosts).innerHTML = "No More Posts :("
                } else{

                    var doc = new DOMParser().parseFromString(data[0], "text/html")
                    var duplicate = false;

                    if(list_pTopPosts.includes(doc.getElementById("div-collection").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('collection_list_c').insertAdjacentHTML('beforeend', data[0])
                        counterTopPosts = (Number(data[1]) + 4);
                        duplicate = false;
                        list_pTopPosts.push(doc.getElementById("div-collection").getAttribute("value"))
                    }

                }

            }
        });;

    });
}

var counterNewPosts = 0;
var idNewPosts="#observer_new"
var list_pNewPostss = []
let boxElementNewPosts = document.querySelector(idNewPosts)

function scrollingNewPostss(handle){


    // Set things up
        window.addEventListener(
            "DOMContentLoaded",
            (event) => {
            boxElement = document.querySelector(idNewPosts);
    
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
    
            observer = new IntersectionObserver(handle, options);
            observer.observe(boxElementNewPosts);
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
    }

function handleIntersectNewPosts(entries, observer) {
    entries.forEach((entry) => {

    $.ajax({
        type: "POST",
            dataType: "json",
            url: "/more_feed",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counter, type: "community_feed_new", community: document.getElementById("community_name").innerText,  }),
            success: function(data) {



            if(data[0] == "none"){
                document.querySelector(idNewPosts).innerHTML = "No More Posts :("
            } else{

                var doc = new DOMParser().parseFromString(data[0], "text/html")
                var duplicate = false;

                if(list_pNewPostss.includes(doc.getElementById("div-post").getAttribute("value"))){
                    duplicate = true;
                }


                if (duplicate == false){
                    document.getElementById('post_list_new').insertAdjacentHTML('beforeend', data[0])
                    counterNewPosts = (Number(data[1]) + 4);
                    duplicate = false;
                    list_pNewPostss.push(doc.getElementById("div-post").getAttribute("value"))
                    
                    

                }

            }

        }
    });;

});
}

scrolling(handleIntersect)
scrollingCollections(handleIntersectCollection)
scrollingNewPostss(handleIntersectNewPosts)

scrollingTopPosts(handleIntersectTopPosts)






function ajaxSaveCollection(collectionId, username, postType) {

    var fullString = String("save_collection_" + collectionId)


    if(postType === "1"){
        fullString = String("save_collection1_" + collectionId)
    }



      value = document.getElementById(fullString).getAttribute('value')


      if(value == "saved"){

        document.getElementById(fullString).setAttribute('class', 'card-link btn btn-dark')
        document.getElementById(fullString).setAttribute('value', 'unsaved')
      } else{
        document.getElementById(fullString).setAttribute('class', 'card-link btn btn-primary')
        document.getElementById(fullString).setAttribute('value', 'saved')
      }


      $.ajax({
        type: "POST",
        dataType: "json",
        url: "/save_collection",
        contentType: 'application/json; charset=utf-8',
        data: JSON.stringify({ collectionId: collectionId,  username: username}),
        success: function(data) {
        }
      });;
    }
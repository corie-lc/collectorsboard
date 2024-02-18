function scrolling(handle, obId){


// Set things up
    window.addEventListener(
        "DOMContentLoaded",
        (event) => {
        document.querySelector(obId);

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
        try{
            observer.observe(document.querySelector(obId));

        } catch(err){
            console.log("e")
        }
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


// --------------------------------------------- HOME PAGE -----------//

// HOME REGULAR FEED

let counter = 0;
const id = "#observer";
let list_p = [];
const numSteps = 20.0;
let boxElement = document.querySelector(id)
//// END REGULAR FEED


let counterCollections = 0;
const idCollections = "#observer_collections";
const list_pCollections = [];
let boxElementCollection = document.querySelector(idCollections)

let counterTopPosts = 0;
const idTopPosts = "#observer_top_posts";
const list_pTopPosts = [];
let boxElementTopPosts = document.querySelector(idCollections)

let counterRecCommunityPosts = 0;
const idCommunityPosts = "#observer_community_posts";
const list_pCommunityPosts = [];
let boxElementCommunityPosts = document.querySelector(idCommunityPosts)

var current = false

function handleIntersect(entries, observer) {

    console.log("hand;eeee")
    observer.unobserve(document.querySelector(id))
    if (current !== true) {
        entries.forEach((entry) => {
            console.time('doSomething')


            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/get_user_feed",
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify({number: counter, type: "user_feed"}),
                success: function (data) {

                    if (data[0] === "none") {
                        document.querySelector("#observer").innerHTML = "No More Posts :("
                    } else {

                        var doc = new DOMParser().parseFromString(data[0], "text/html")
                        var duplicate = false;

                        try{
                            if (list_p.includes(doc.getElementById("div-post").getAttribute("value"))) {
                                duplicate = true;
                            }
                        } catch {
                            duplicate = false
                        }


                        if (duplicate == false) {
                            document.getElementById('post_list').insertAdjacentHTML('beforeend', data[0])
                            counter = (Number(data[1]) + 4);
                            duplicate = false;
                            list_p.push(doc.getElementById("div-post").getAttribute("value"))
                        }
                        current = false
                        observer.observe(document.querySelector(id))

                        console.timeEnd('doSomething')


                    }

                }

            });





        });
    }
}

function handleIntersectCommunity(entries, observer) {
    observer.unobserve(document.querySelector("#observer_community_posts"))
    if (current !== true) {
        entries.forEach((entry) => {

            $.ajax({
                type: "POST",
                dataType: "json",
                url: "/more_feed",
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify({number: counter, type: "your_communities_posts"}),
                success: function (data) {

                    if (data[0] == "none") {
                        document.querySelector("#observer_community_posts").innerHTML = "No More Posts :("
                    } else {

                        var doc = new DOMParser().parseFromString(data[0], "text/html")
                        var duplicate = false;

                        if (list_pCommunityPosts.includes(doc.getElementById("div-post").getAttribute("value"))) {
                            duplicate = true;
                        }


                        if (duplicate == false) {
                            document.getElementById('rec_community_post_list').insertAdjacentHTML('beforeend', data[0])
                            counterRecCommunityPosts = (Number(data[1]) + 4);
                            duplicate = false;
                            list_pCommunityPosts.push(doc.getElementById("div-post").getAttribute("value"))
                        }
                        current = false
                        observer.observe(document.querySelector("#observer_community_posts"))


                    }

                }

            });
            ;


        });
    }
}


function handleIntersectTopPosts(entries, observer) {
    observer.unobserve(document.querySelector("#observer_top_posts"))
        entries.forEach((entry) => {

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/get_toppost_feed",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counterTopPosts, type: "top_posts_feed"  }),
            success: function(data) {
                if(data[0] === "none"){
                    document.querySelector(idTopPosts).innerHTML = "No More Posts :("
                } else{

                    const doc = new DOMParser().parseFromString(data[0], "text/html");
                    let duplicate = false;

                    if(list_pTopPosts.includes(doc.getElementById("div-post").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate === false){
                        document.getElementById('top_posts_list').insertAdjacentHTML('beforeend', data[0])
                        counterTopPosts = (Number(data[1]) + 4);
                        duplicate = false;
                        list_pTopPosts.push(doc.getElementById("div-post").getAttribute("value"))
                    }

                    observer.observe(document.querySelector("#observer_top_posts"))


                }

            }
        });;

    });
}

function handleIntersectCollection(entries, observer) {
        observer.unobserve(document.querySelector(idCollections))
        entries.forEach((entry) => {

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_feed_collection",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counterCollections  }),
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
                        document.getElementById('collection_list').insertAdjacentHTML('beforeend', data[0])
                        counterCollections = (Number(data[1]) + 8);
                        duplicate = false;
                        list_p.push(doc.getElementById("div-collection").getAttribute("value"))
                    }
                    observer.observe(document.querySelector(idCollections))


                }

            }
        });;

    });
}


scrolling(handleIntersect, id)
scrolling(handleIntersectCommunity, idCommunityPosts)
scrolling(handleIntersectCollection, idCollections)
scrolling(handleIntersectTopPosts, idTopPosts)

// --------------------------------------------- HOME PAGE -----------//

// --------------------------------------------- PROFILE PAGE -----------//

var counterProfileAllPosts = 0;
var idProfileAllPostsID="#observerProfileAllPosts"
listProfileAllPosts = []

// all posts for profile -- first tab --

function handleIntersectProfileAllPosts(entries, observer) {
        entries.forEach((entry) => {
 $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_profile",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counterProfileAllPosts  }),
            success: function(data) {

                if(data[0] == "none"){
                    document.querySelector("#observerProfileAllPosts").innerHTML = "No More Posts :("
                } else{

                    var doc = new DOMParser().parseFromString(data[0], "text/html")
                    var duplicate = false;

                    if(listProfileAllPosts.includes(doc.getElementById("div-post").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('post_list').insertAdjacentHTML('beforeend', data[0])
                        counterProfileAllPosts = (Number(data[1]) + 8);
                        duplicate = false;
                        listProfileAllPosts.push(doc.getElementById("div-post").getAttribute("value"))
                    }





                }

            }
        });;


    });
}

scrolling(handleIntersectProfileAllPosts, idProfileAllPostsID)

// scrollingCollections(handleIntersectCollection)

// --------------------------------------------- VIEW USER PAGE -----------//

var counterViewUserUserPosts = 0;
var idViewUserUserPostsID="#observerViewUserUserPosts"
listViewUserUserPosts = []

function handleIntersectUserPosts(entries, observer) {
    var currentLocation = window.location;
    const urlArray = currentLocation.toString().split("/");

        entries.forEach((entry) => {


        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_viewuser",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: counter, username: urlArray[4]  }),
            success: function(data) {

                if(data == "none"){
                    document.querySelector("#observerViewUserUserPosts").innerHTML = "No More Posts :("
                } else{

                    var doc = new DOMParser().parseFromString(data, "text/html")
                    var duplicate = false;

                    if(list_p.includes(doc.getElementById("div-post").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('post_list').insertAdjacentHTML('beforeend', data)
                        counterViewUserUserPosts += 1;
                        duplicate = false;
                        listViewUserUserPosts.push(doc.getElementById("div-post").getAttribute("value"))
                    }





                }

            }
        });;

    });
}

scrolling(handleIntersectUserPosts, idViewUserUserPostsID)

// search systems

search_posts_counter = 0;
var search_post_id = "#search-post-observer"
list_search_posts = []

function handleIntersectSearchPosts(entries, observer) {
    var currentLocation = window.location;
    const urlArray = currentLocation.toString().split("/");

    q = document.getElementById("search-post-observer").getAttribute('value')


        entries.forEach((entry) => {


        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/more_search_posts",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ number: search_posts_counter, q: q  }),
            success: function(stuff) {
                data = stuff[0]

                if(data === "none"){
                    document.querySelector("#search-post-observer").innerHTML = "No More Posts :("
                } else{

                    var doc = new DOMParser().parseFromString(data, "text/html")
                    var duplicate = false;

                    if(list_search_posts.includes(doc.getElementById("div-post").getAttribute("value"))){
                        duplicate = true;
                    }


                    if (duplicate == false){
                        document.getElementById('search_post_list').insertAdjacentHTML('beforeend', data)
                        search_posts_counter += 4;
                        duplicate = false;
                        list_search_posts.push(doc.getElementById("div-post").getAttribute("value"))
                    }





                }

            }
        });;

    });
}

scrolling(handleIntersectSearchPosts, search_post_id)
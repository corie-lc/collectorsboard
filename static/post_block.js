function goRight(postid){
  document.getElementById('tags-c-' + postid).scrollLeft -= 40;
}

function goLeft(postid){
                document.getElementById('tags-c-' + postid).scrollLeft += 40;
            }

function ajaxFavoritePost(postId, postType) {
      var information = "favorite_post_" + postId;






  if(postType === "1"){
      information = "favorite_post1_" + postId;
    } else if(postType === "2"){
      information = "favorite_post2_" + postId;
    }

    if( document.getElementById(information).getAttribute("value") === "fav"){
      document.getElementById(information).setAttribute('class', 'btn btn-dark')
      document.getElementById(information).setAttribute('value', 'unfav')
    } else{
      document.getElementById(information).setAttribute('class', 'btn btn-primary')
      document.getElementById(information).setAttribute('value', 'fav')
    }



    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/fav_post_button",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ postId: postId  }),
      success: function(data) {
      }
    });;
  }

  function ajaxCall(comment, postId) {
    
    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/add_comment",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ comment : comment, postId: postId  }),
      success: function(data) {
      }
    });;
}




  function ajaxLikePost(postId, postType) {
      var fullString = String("like_post_" + postId)
    var fullStringCounter = String("like_post_counter_" + postId)

    if(postType === "1"){
      fullString = String("like_post1_" + postId)
      var fullStringCounter = String("like_post1_counter_" + postId)
    } else if(postType === "2"){
      fullString = String("like_post2_" + postId)
      var fullStringCounter = String("like_post2_counter_" + postId)
    }



    value = document.getElementById(fullString).getAttribute('value')

    if(value == "liked"){
      document.getElementById(fullStringCounter).innerHTML = (parseInt(document.getElementById(fullStringCounter).innerText) - 1).toString()
      document.getElementById(fullString).setAttribute('class', 'btn btn-dark')
      document.getElementById(fullString).setAttribute('value', 'unliked')


    } else{
      document.getElementById(fullStringCounter).innerHTML = (parseInt(document.getElementById(fullStringCounter).innerText) + 1).toString()
      document.getElementById(fullString).setAttribute('class', 'btn btn-primary')
      document.getElementById(fullString).setAttribute('value', 'liked')
    }


    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/like_post",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ postId: postId  }),
      success: function(data) {
      }
    });;
  }

  function addToCollection(collectionId, postId) {

    var fullString = String("#add_to_collection_" + collectionId + "_" + postId)


    value = document.getElementById(String("add_to_collection_" + collectionId + "_" + postId)).getAttribute('value')

    if(value == "added"){
      var el = document.querySelectorAll(fullString);

        for (var i = 0; i < el.length; i++) {
            var currentEl = el[i];
            currentEl.setAttribute('class', 'btn btn-dark w-100')
            currentEl.setAttribute('value', 'unadded')

        }

      //document.getElementById(fullString).setAttribute('class', 'btn btn-dark w-100')
      //document.getElementById(fullString).setAttribute('value', 'unadded')
    } else{
      var el = document.querySelectorAll(fullString);

        for (var i = 0; i < el.length; i++) {
            var currentEl = el[i];
            currentEl.setAttribute('class', 'btn btn-primary w-100')
            currentEl.setAttribute('value', 'added')

        }

      //document.getElementById(fullString).setAttribute('class', 'btn btn-primary w-100')
      //document.getElementById(fullString).setAttribute('value', 'added')
            //console.log('changed-2')

    }

    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/add_to_collection",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ postId: postId, collectionId: collectionId  }),
      success: function(data) {
      }
    });;
  }


function editPost(postid, selectorId="exampleFormControlSelect1-"){
  

  var details = document.getElementById("edit-details-" + postid).value
  var value = document.getElementById("edit-value-" + postid).value
  var date = document.getElementById("edit-date-" + postid).value
  var country = document.getElementById("edit-country-" + postid).value
  var name = document.getElementById("edit-name-" + postid).value

  var myCollapse = document.getElementById("collapseExample-" + postid)
  var bsCollapse = new bootstrap.Collapse(myCollapse, {
    toggle: true
  })

  bsCollapse.hide()



  

  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/edit_post",
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({ postid: postid, details: details, name: name, value: value, date: date, country: country, community: "" }),
    complete: function(data) {
      // change post inn real time

      document.getElementById("post-subtext-" + postid).innerHTML = details
      document.getElementById("badge1-" + postid).innerHTML = name

      document.getElementById("badge1-" + postid).style.display = "inline-block"

      document.getElementById("badge2-" + postid).innerHTML = country

      document.getElementById("badge2-" + postid).style.display = "inline-block"


      document.getElementById("badge3-" + postid).innerHTML = date

      document.getElementById("badge3-" + postid).style.display = "inline-block"

      document.getElementById("badge4-" + postid).innerHTML = value

      document.getElementById("badge4-" + postid).style.display = "inline-block"




    }
  });;

}


function closeEditPost(postid){
  var myCollapse = document.getElementById("collapseExample-" + postid)
  var bsCollapse = new bootstrap.Collapse(myCollapse, {
    toggle: true
  })

  bsCollapse.hide()
}


function getMarketValueEbayEdit(post_id){
  name   = document.getElementById("edit-name-" + post_id).value
  document.getElementById("edit-value-" + post_id).value = "Loading.. Please Wait"


  const stringArray = name.split(" ");



  var marketEval = "$0"

  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/get_market_eval",
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({ keywords : name}),
    success: function(data) {
        marketEval = data
        document.getElementById("edit-value-" + post_id).value = marketEval
    }
  });


}


function edit_post_modal(post_id,) {
  var modalContainer = document.getElementById('emailModal')
  var myModal = new bootstrap.Modal(modalContainer, { backdrop: 'static' })
  
  modalContainer.querySelector(".modal-body").innerHTML = "Your value is: " + post_id;
  
  myModal.show();
}


function removePhoto(){
  document.getElementById("add_photo_button").style.display = "block"
  document.getElementById("remove_photo").style.display = "none"
  document.getElementById("uploadPreview").src = ""
}


function makePost(){


    details = document.getElementById("exampleFormControlTextarea1")
    visibility =  document.getElementById("visibility")

    off_name = document.getElementById("entry-off-name")
    origin_country = document.getElementById("entry-origin-country")
    date_created = document.getElementById("entry-date")
    value = document.getElementById("entry-value")

    var collection_selector_dropdown = document.getElementById("collection_select");
    var community_selector_dropdown = document.getElementsByName("post-community");


    var photo = new FormData($('#post_info')[0]);

    console.log(new FormData($('#post_info')[0]))

    



    if(!details.value==""){
      document.getElementById("loader_button_icon").style.display = "inline-block";
      document.getElementById("post_button_icon").style.display = "none";
      document.getElementById("make-post-button").disabled = true;
      details.style.borderColor = "white"

      
    



      $.ajax({
        type: 'POST',
        url: '/make_post_ajax',
        data: new FormData($('#post_info')[0]),
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
          console.log("here lol")

          details.value = ""
          off_name.value = ""
          origin_country.value = ""
          date_created.value = ""
          value.value = ""


          collection_selector_dropdown.text = "None"
          community_selector_dropdown.text = "Choose Comunity"

          $('#createPostModal').modal('hide');
          removePhoto()

            var myCollapse = document.getElementById("collapseExample")
            var bsCollapse = new bootstrap.Collapse(myCollapse, {
              toggle: true
            })

            bsCollapse.hide()

            

            document.getElementById("loader_button_icon").style.display = "none";
            document.getElementById("post_button_icon").style.display = "inline-block";
            document.getElementById("make-post-button").disabled = false;





            
        }

        
      });

  } else{
    details.style.borderColor = "red"
  }
}


function pinPostCollection(post_id, collection_id, pin_or_unpin){

  document.getElementById(post_id+"_pin_value").innerHTML = "Loading..Wait"
  document.getElementById(post_id+"_pin_value").disabled = true

  $.ajax({
    type: "POST",
    dataType: "json",
    url: "/pin_or_unpin_post",
    contentType: 'application/json; charset=utf-8',
    data: JSON.stringify({post_id:  post_id, collection_id: collection_id, pin_or_unpin: value}),
    success: function(data) {
      value = document.getElementById(post_id+"_pin_value").getAttribute('value')

      document.getElementById(post_id+"_pin_value").disabled = false
      if(data === "At Max"){
        document.getElementById(post_id+"_pin_value").innerHTML = "Pin (At Max)"
        document.getElementById(post_id+"_pin_value").value = "pin"
      } else{
        if(value === "unpin"){
          document.getElementById(post_id+"_pin_value").className = "dropdown-item"
          document.getElementById("badge5-pinned-" + post_id).style="display: none"
          document.getElementById(post_id+"_pin_value").innerHTML = "Pin"
          document.getElementById(post_id+"_pin_value").value = "pin"
        } else{
          document.getElementById(post_id+"_pin_value").innerHTML = "Unpin"
          document.getElementById("badge5-pinned-" + post_id).style="display: block"
          document.getElementById(post_id+"_pin_value").className = "dropdown-item bg-primary"
          document.getElementById(post_id+"_pin_value").value = "unpin"
        }
      }
        console.log("sucesss done")
    }
  });





}
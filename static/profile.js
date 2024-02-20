

function deleteFollower(follower){
      $.ajax({
            type: "POST",
            dataType: "json",
            url: "/delete_follower",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ username: follower  }),
            success: function(data) {
            }
        });;

        document.getElementById("follower_" + follower).remove()

}

function deleteFollowing(following){
      $.ajax({
            type: "POST",
            dataType: "json",
            url: "/delete_following",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ username: following  }),
            success: function(data) {

        document.getElementById("following_" + following).remove()
            }
        });



}

function changeAvatar(item){
    document.getElementById("user_avatar").src=item
    $.ajax({
            type: "POST",
            dataType: "json",
            url: "/change_avatar",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ avatar: item  }),
            success: function(data) {
            }


        });;
}

function closeAll(tab){
                 $('.collapse').collapse('hide')
                    $(tab).collapse('show')

                    if(tab === "#collapseForYou"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Posts"
                        //document.getElementBy

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonYourStuff").disabled = false


                    } else if(tab === "#collapseForYouCollections"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Personal"
                        document.getElementById("buttonForYouCollections").disabled = true

                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonYourStuff").disabled = false


                    } else if(tab === "#collapseForYouPopular"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Collections"
                        document.getElementById("buttonForYouPopular").disabled = true

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonYourStuff").disabled = false


                    } else if(tab === "#collapseForYouCommunities"){
                        document.getElementById("buttonForYouCommunities").disabled = true
                        document.getElementById("dropdownMenuButton1").innerHTML = "Socials"

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonYourStuff").disabled = false

                    } else if(tab === "#collapseYourStuff"){
                        document.getElementById("buttonYourStuff").disabled = true
                        document.getElementById("dropdownMenuButton1").innerHTML = "Saved"

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                    }



            }



            function acceptRequest(username) {
                console.log("HERE")
            
                $.ajax({
                  type: "POST",
                  dataType: "json",
                  url: "/accept_request",
                  contentType: 'application/json; charset=utf-8',
                  data: JSON.stringify({ username: username, accept: "true"  }),
                  success: function(data) {
                    console.log(String(data[0]))
                    if(String(data[0]) ==  "null"){
                        document.getElementById("request_" + String(data[1])).remove()
                    } else{
                        document.getElementById("request_" + String(data[1])).remove()
                        document.getElementById('followers').insertAdjacentHTML('beforeend', data[0])
                    }
                  }
                });;
              }
            
            
              function declineRequest(username) {
                console.log("HERE")
            
                $.ajax({
                  type: "POST",
                  dataType: "json",
                  url: "/accept_request",
                  contentType: 'application/json; charset=utf-8',
                  data: JSON.stringify({ username: username, accept: "false"  }),
                  success: function(data) {
                    console.log(String(data[0]))
                    if(String(data[0]) ==  "null"){
                        document.getElementById("request_" + String(data[1])).remove()
                    } else{
                        document.getElementById("request_" + String(data[1])).remove()
                        document.getElementById('followers').insertAdjacentHTML('beforeend', data[0])
                    }
                  }
                });;
              }

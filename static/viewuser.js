

function followRequest(followType, username){



       $.ajax({
            type: "POST",
            dataType: "json",
            url: "/follow_request",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ follow_request: followType, username: username  }),
            success: function(data) {
                if (data === "Followed"){
                    document.getElementById("follow_action_button").innerHTML = "Unfollow"
                    document.getElementById("btnGroupDrop1").setAttribute("class", "btn btn-primary dropdown-toggle")
                    document.getElementById("follow_action_button").setAttribute("onclick", "followRequest('unfollow','" + username + "')")


                } else if(data === "Requested") {
                    document.getElementById("btnGroupDrop1").setAttribute("class", "btn btn-info dropdown-toggle")
                    document.getElementById("follow_action_button").innerHTML = "Cancel Request"
                    document.getElementById("follow_action_button").setAttribute("onclick", "followRequest('stop_request','" + username + "')")

                } else{
                   document.getElementById("btnGroupDrop1").setAttribute("class", "btn btn-dark dropdown-toggle")
                   document.getElementById("follow_action_button").innerHTML = "Follow"
                   document.getElementById("follow_action_button").setAttribute("onclick", "followRequest('follow','" + username + "')")


                }
                document.getElementById("btnGroupDrop1").innerHTML = data
            }


        });

}



            document.getElementById("buttonForYouHome").disabled = true

function closeAll(tab){
                 $('.collapse').collapse('hide')
                    $(tab).collapse('show')

                    if(tab === "#collapseForYou"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Home"
                        //document.getElementBy

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false


                    } else if(tab === "#collapseForYouCollections"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Collections"
                        document.getElementById("buttonForYouCollections").disabled = true

                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false

                    } else if(tab === "#collapseForYouPopular"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Followers"
                        document.getElementById("buttonForYouPopular").disabled = true

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false

                    } else if(tab === "#collapseForYouCommunities"){
                        document.getElementById("buttonForYouCommunities").disabled = true
                        document.getElementById("dropdownMenuButton1").innerHTML = "Following"

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false

                    } else if(tab === "#collapseForYouSaved"){
                        document.getElementById("buttonForYouSaved").disabled = true
                        document.getElementById("dropdownMenuButton1").innerHTML = "Saved"

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                    }



            }

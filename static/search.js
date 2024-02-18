

function closeAll(tab){
                 $('.collapse').collapse('hide')
                    $(tab).collapse('show')

                    if(tab === "#collapseForYou"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Filter: Posts"
                        //document.getElementBy

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false


                    } else if(tab === "#collapseForYouCollections"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Filter: Collections"
                        document.getElementById("buttonForYouCollections").disabled = true

                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouPopular").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false

                    } else if(tab === "#collapseForYouPopular"){
                        document.getElementById("dropdownMenuButton1").innerHTML = "Filter: Users"
                        document.getElementById("buttonForYouPopular").disabled = true

                        document.getElementById("buttonForYouCollections").disabled = false
                        document.getElementById("buttonForYouHome").disabled = false
                        document.getElementById("buttonForYouCommunities").disabled = false
                        document.getElementById("buttonForYouSaved").disabled = false

                    } else if(tab === "#collapseForYouCommunities"){
                        document.getElementById("buttonForYouCommunities").disabled = true
                        document.getElementById("dropdownMenuButton1").innerHTML = "Filter: Communities"

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

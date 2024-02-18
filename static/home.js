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
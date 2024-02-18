function launch_comment(idtag, username, post_type){


  var modalId = "exampleModal" + idtag
    var commentId = "comment_list" + idtag
    var commentInput = "comment_input" + idtag
    var postButton = "post_comment_button" + idtag
    var commentLoader = "comment_loader" + idtag

    if(post_type === "1"){
        modalId = "exampleModal1" + idtag
        commentId = "comment_list1" + idtag
        commentInput = "comment_input1" + idtag
        postButton = "post_comment_button1" + idtag
        commentLoader = "comment_loader1" + idtag
    } else if(post_type === "2"){
        modalId = "exampleModal2" + idtag
        commentId = "comment_list2" + idtag
        commentInput = "comment_input2" + idtag
        postButton = "post_comment_button2" + idtag
        commentLoader = "comment_loader2" + idtag
    } 


    var myModalEl = document.getElementById(modalId)
    myModalEl.addEventListener('hidden.bs.modal', function (event) {
        counter = 0
      document.getElementById(commentId).innerHTML = ""
    })

    var myModal = new bootstrap.Modal(document.getElementById(modalId))
    myModal.show()






    

    $.ajax({
      type: "POST",
      dataType: "json",
      url: "/get_comments",
      contentType: 'application/json; charset=utf-8',
      data: JSON.stringify({ postId: idtag  }),
      success: function(data) {



        let i = 0;

        while (i < data.length) {
            var html = `
            <div class="card mt-1" style="background-color: #2c3034" >
          <div class="card-body">
          <p class="my-0"><strong><a style="text-decoration: underline; color: white" href="/viewuser/${data[i][2]}">${data[i][2]} <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
            </svg></a></strong></p>
          <p class="my-0"><small> ${data[i][1]}</small></p>
          </div>
        </div>`

            document.getElementById(commentId).insertAdjacentHTML('beforeend', html)


            i++;
        }


        document.getElementById('beforeend')




      }
    });;

    
}

function expandInfo(idtag, username, post_type){


  
    var modalId = "exampleModal" + idtag
    var commentId = "comment_list" + idtag
    var commentInput = "comment_input" + idtag
    var postButton = "post_comment_button" + idtag

    if(post_type === "1"){
        modalId = "exampleModal1" + idtag
        commentId = "comment_list1" + idtag
        commentInput = "comment_input1" + idtag
        postButton = "post_comment_button1" + idtag
    } else if(post_type === "2"){
        modalId = "exampleModal2" + idtag
        commentId = "comment_list2" + idtag
        commentInput = "comment_input2" + idtag
        postButton = "post_comment_button2" + idtag
    } 




    elementitem =  document.getElementById(postButton)



    var stuff = "<li>" + document.getElementById(commentInput).value +  "</li"
        var html = `
            <div class="card mt-1" style="background-color: #2c3034" >
          <div class="card-body">
          <p class="my-0"><strong><a style="text-decoration: underline; color: white" href="/viewuser/${username}">${username} <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
          <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8z"/>
      </svg></a></strong></p>
          <p class="my-0"><small> ${document.getElementById(commentInput).value}</small></p>
          </div>
        </div>`
        document.getElementById(commentId).insertAdjacentHTML('beforeend', html)

        

        $.ajax({
            type: "POST",
            dataType: "json",
            url: "/add_comment",
            contentType: 'application/json; charset=utf-8',
            data: JSON.stringify({ comment : document.getElementById(commentInput).value, postId: idtag  }),
            success: function(data) {

            }
          });;

                  document.getElementById(commentInput).value = ""




   


  }


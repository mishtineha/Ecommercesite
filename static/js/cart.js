// // var updateBtns = document.getElementsByClassName('update-cart')

var updateBtns = document.getElementsByClassName('update-cart')

for(var i=0; i< updateBtns.length; i++){
    updateBtns[i].addEventListener('click',function(){
      // console.log('abc')

        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId, 'action:',action,"abc")

        console.log('USER:', user)
        if(user === 'AnonymousUser' ){
            addCookieItem(productId, action)
        }
        else{
            updateUserOrder(productId,action)
        }
    })

}

function addCookieItem(productId, action){

    console.log("user not logged in")


    if(action == 'add'){

        if(cart[productId]== undefined){

           cart[productId] = {'quantity':1}
        }
        else{

            cart[productId]['quantity'] +=1
        }
    }
    if(action == 'remove'){
        cart[productId]['quantity'] -=1

        if(cart[productId]['quantity'] <= 0){
            console.log('Item should be deleted')
            delete cart[productId];
        }
    }
    if(action == 'del'){
        delete cart[productId];

    }
    console.log('Cart:', cart[productId])
    document.cookie = 'cart=' +JSON.stringify(cart) + "; domain = ;path=/"
    location.reload()
}

// function addCookieItem(productId, action){
//     console.log('user is not authenticated')
// }

function updateUserOrder(productId,action){
    console.log('User is authenticated, Logged in')

    var url = abc
    fetch(url,{
        method: 'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken': csrftoken,
        },
        body:JSON.stringify({'productId': productId, 'action': action})
    })

    .then((response)=>{

        return response.json()
    })

    .then((data)=>{
       console.log('data:', data)
       location.reload()
    })
}




function delete_cookie(name) {
    document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  }
var clear_session    = $(".logout");
clear_session.click(function(){

    event.preventDefault();
  var href = $(this).attr("href"),
      target = '';

  delete_cookie('cart');

  // wait for data to push and then open link
  setTimeout(function() { // now wait 150 milliseconds...
      window.open(href,(!target?"_self":target)); // ...and open the link as usual
  },150);

});

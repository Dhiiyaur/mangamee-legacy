
function setCookie(cname, cvalue, exdays) {

    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();

    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    
}

function getCookie(cname) {

    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
        c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
        }
    }
    return "";
}

function createCookie(){

    var customValue = [
        {
            ID : window.location.pathname.split('/').slice(-1)[0],
            name : getCookie('mangaName'),
            // name : manga_name,
            link : window.location.href,
            cover_img : document.getElementsByClassName("card-img-top")[0].src,
            latest : "-"
        }
    ]

    
    var jsonValue = JSON.stringify(customValue);
    setCookie('FireBaseHistory', jsonValue, 1);

}
function updateCookie(){

    let cookies = JSON.parse(getCookie('FireBaseHistory'));

    // checking manga is input or not 

    let checkName = window.location.pathname.split('/').slice(-1)[0]
    const findName = cookies.find((item) =>{
        return item.ID === checkName
    })

    if(findName === undefined){
        
        cookies.push(
            {
                ID : window.location.pathname.split('/').slice(-1)[0],
                name : getCookie('mangaName'),
                // name : manga_name,
                link : window.location.href,
                cover_img : document.getElementsByClassName("card-img-top")[0].src,
                latest : "-"
            }
        )

        var jsonValue = JSON.stringify(cookies);
        setCookie('FireBaseHistory', jsonValue, 1);
    }
    
    
}

function checkCookie(){
    var user = getCookie('FireBaseHistory');
    if (user != ""){

        updateCookie();
        
    }else{
        
        createCookie();
    }
}

checkCookie();


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

function setCookie(cname, cvalue, exdays) {

    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();

    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";

}

function oneDelHistory(){

    let cookies = JSON.parse(getCookie('FireBaseHistory'));
    // get target data
    let mangaIDCookies = event.currentTarget.dataset.record;
    // filter with mangaNameCookies

    if(cookies.length == 1){

        setCookie('FireBaseHistory', '', -1);

    }else{

        let cookiesFilter = cookies.filter((item) => item.ID != mangaIDCookies);
        // console.log(cookiesFilter)
        cookiesFilter = JSON.stringify(cookiesFilter);
        setCookie('FireBaseHistory', cookiesFilter, 365);

    }

}



function delHistory(){
    setCookie('FireBaseHistory', '', -1);
}


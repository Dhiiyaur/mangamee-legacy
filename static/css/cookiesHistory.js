
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


function oneDelHistory(){

    let cookies = JSON.parse(getCookie('history'));
    // get target data
    let mangaIDCookies = event.currentTarget.dataset.record;
    // filter with mangaNameCookies

    if(cookies.length == 1){

        setCookie('history', '', -1);

    }else{

        let cookiesFilter = cookies.filter((item) => item.ID != mangaIDCookies);
        // console.log(cookiesFilter)
        cookiesFilter = JSON.stringify(cookiesFilter);
        setCookie('history', cookiesFilter, 365);

    }

}

function setCookie(cname, cvalue, exdays) {

    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();

    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";

}

function delHistory(){
    setCookie('history', '', -1);
}

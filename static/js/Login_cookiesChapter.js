
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

function updateCookiesChapter(){

    // get data
    let idManga = window.location.pathname.split('/').slice(-2)[0]
    let lastChapter = document.getElementsByClassName("navbar-brand")[1].innerHTML;
    let cookies = JSON.parse(getCookie('FireBaseHistory'));

    // update chapter .map cookies

    let newChapter = cookies.map(obj =>
        obj.ID === idManga ? { ...obj, latest: lastChapter } : obj
    );

    // jsonvalue

    let jsonValue = JSON.stringify(newChapter);
    setCookie('FireBaseHistory', jsonValue, 1);
}


updateCookiesChapter();


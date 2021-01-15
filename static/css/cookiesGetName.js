function setCookie(cname, cvalue, exdays) {

    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires="+d.toUTCString();

    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";

}

function getName(){

    console.log('aalaah sia booyy')
    let mangaNameCookies = event.currentTarget.dataset.record
    setCookie('mangaName', mangaNameCookies, 1)
}
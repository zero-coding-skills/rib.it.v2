last_val = 0;

function show(value) {
    let menus = document.getElementById("menus");
    let buttons = document.getElementById("buttons");

    if (menus.style.opacity == 0) {
        menus.style.opacity = 1;
        menus.style.pointerEvents = "all";
        document.getElementById(value).style.opacity = 1;
        buttons.style.top = "90%";
    }
    else if (menus.style.opacity == 1 && document.getElementById(value).style.opacity == 1) {
        menus.style.opacity = 0;
        menus.style.pointerEvents = "none";
        document.getElementById(value).style.opacity = 0;
        buttons.style.top = "calc(50% + 75px)";
    }
    else {
        document.getElementById(last_val).style.opacity = 0;
        document.getElementById(value).style.opacity = 1;
    }
    last_val = value
}

function attention() {
    alert("This feature is not yet available.")
}
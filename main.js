last_val = 0;
function show(value) {
    var menus = document.getElementById("menus")
    var buttons = document.getElementById("buttons")
    var bg = document.getElementById("bg")

    if (menus.style.opacity == 0) {
      menus.style.opacity = 1;
      menus.style.pointerEvents = "all";
      document.getElementById(value).style.opacity = 1;
      buttons.style.top = "90%";
      var bLevel = 0;
      const interval = setInterval(() => {
        bLevel = bLevel + 1;
        bg.style.filter = "blur(" + bLevel + "px)";
        console.log("he");
        if (bLevel >= 10) {
          clearInterval(interval)
        }
      }, 15);
    }
    else if (menus.style.opacity == 1 && document.getElementById(value).style.opacity == 1) {
      menus.style.opacity = 0;
      menus.style.pointerEvents = "none";
      document.getElementById(value).style.opacity = 0;
      buttons.style.top = "calc(50% + 75px)";
      var bLevel = 10;
      const interval = setInterval(() => {
        bLevel = bLevel - 1;
        bg.style.filter = "blur(" + bLevel + "px)";
        console.log("he");
        if (bLevel <= 0) {
          clearInterval(interval)
        }
      }, 15);
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

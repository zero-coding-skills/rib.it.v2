last_val = 0;
function show(value) {
    var menus = document.getElementById("menus")
    var blurElement = document.querySelectorAll(".blur")


    if (menus.style.opacity == 0) {
      menus.style.opacity = 1;
      menus.style.pointerEvents = "all";
      menus.style.zIndex = 2;
      document.getElementById(value).style.opacity = 1;
      document.getElementById(value + "-switch").style.backgroundColor = "#99bb96";
      var bLevel = 0;
      const interval = setInterval(() => {
        bLevel = bLevel + 1;
        blurElement.forEach(element => {
          element.style.filter = "blur(" + bLevel + "px)";
        });
        if (bLevel >= 10) {
          clearInterval(interval)
        }
      }, 15);
    }
    else if (menus.style.opacity == 1 && document.getElementById(value).style.opacity == 1) {
      menus.style.opacity = 0;
      menus.style.pointerEvents = "none";
      menus.style.zIndex = 0;
      document.getElementById(value).style.opacity = 0;
      document.getElementById(value + "-switch").style.backgroundColor = "#242424";
      document.getElementById(last_val + "-switch").style.backgroundColor = "#242424";
      var bLevel = 10;
      const interval = setInterval(() => {
        bLevel = bLevel - 1;
        blurElement.forEach(element => {
          element.style.filter = "blur(" + bLevel + "px)";
        });
        if (bLevel <= 0) {
          clearInterval(interval)
        }
      }, 15);
    }
    else {
      document.getElementById(last_val).style.opacity = 0;
      document.getElementById(last_val).style.pointerEvents = "none";
      document.getElementById(last_val + "-switch").style.backgroundColor = "#242424";
      document.getElementById(value).style.opacity = 1;
      document.getElementById(value).style.pointerEvents = "all";
      document.getElementById(value + "-switch").style.backgroundColor = "#99bb96";
    }
    last_val = value
}

function attention() {
    alert("This feature is not yet available.")
}

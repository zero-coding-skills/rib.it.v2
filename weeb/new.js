function show(what, what_not) {
  const hello = document.getElementById("hello")
  let open = document.getElementById(what)
  let hide = document.getElementById(what_not)
  opacity = 0
  if (open.style.opacity == 0) {
    const interval = setInterval(() => {
      opacity += 0.1;
      open.style.opacity = opacity;
      if (hide.style.opacity != 0) {
        hide.style.opacity = 1 - opacity;
      }
      if (hello.style.opacity != 0) {
        hello.style.opacity = 1 - opacity;
      }
      if (opacity >= 1) {
        hide.style.opacity = 0;
        hello.style.opacity = 0;
        clearInterval(interval)
      }
    }, 10);
    open.style.pointerEvents = "all";
    hide.style.pointerEvents = "none";
  }
}

function home() {
  const hello = document.getElementById("hello")
  const about = document.getElementById("about")
  const download = document.getElementById("download")
  opacity = 0
  if (hello.style.opacity == 0) {
    const interval = setInterval(() => {
      opacity += 0.1;
      if (download.style.opacity != 0) {
        download.style.opacity = 1 - opacity;
      }
      else {
        about.style.opacity = 1 - opacity;
      }
      hello.style.opacity = opacity;
      if (opacity >= 1) {
        about.style.opacity = 0;
        download.style.opacity = 0;
        clearInterval(interval)
      }
    }, 10);
    about.style.pointerEvents = "none";
    download.style.pointerEvents = "none";
  }
}

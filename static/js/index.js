function checkBrowser() {
    var isBadIE = navigator.appName == "Microsoft Internet Explorer";
    if (isBadIE) {
        // IE 10 and earlier not supported, redirect
        window.location = "http://browsehappy.com";
    }
}

function openSidebar() {
    document.getElementById("burger").onclick = closeSidebar;
    document.getElementById("main").style.marginRight = "300px";
    document.getElementById("navbar").style.marginRight = "300px";
    document.getElementById("sidebar").style.width = "300px";
}

function closeSidebar() {
    document.getElementById("burger").onclick = openSidebar;
    document.getElementById("main").style.marginRight = "0";
    document.getElementById("navbar").style.marginRight = "0";
    document.getElementById("sidebar").style.width = "0";
}

function checkForOpenSidebar() {
    if (document.documentElement.clientWidth > 1007) {
        closeSidebar();
    }
}

function handleBackgrounds() {
    var endOfOverview = document.getElementById("overview").clientHeight;

    if (window.pageYOffset > endOfOverview) {
        document.getElementById("overview-background").style.display = "none";
        document.getElementById("sidebar").style.backgroundColor = "rgb(0,0,0)";
        document.getElementById("technical-skills-background").style.display = "block";
    } else if (window.pageYOffset > endOfOverview-50) {
        document.getElementById("overview-background").style.display = "block";
        document.getElementById("sidebar").style.backgroundColor = "rgb(0,0,0)";
        document.getElementById("technical-skills-background").style.display = "none";
    } else {
        document.getElementById("overview-background").style.display = "block";
        document.getElementById("sidebar").style.backgroundColor = "rgba(0,0,0,0.5)";
        document.getElementById("technical-skills-background").style.display = "none";
    }
}

function validateFields() {
  var emailFormat = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;

  var validName = document.getElementById("name").value != "";
  var validEmail = emailFormat.test(document.getElementById("email").value);
  var validMessage = document.getElementById("message").value != "";
  var verified = grecaptcha.getResponse() != "";

  if (validName && validEmail && validMessage && verified) {
    document.getElementById("sendMessageButton").disabled = false;
  } else {
    document.getElementById("sendMessageButton").disabled = true;
  }
}

function resetForm() {
  document.getElementById("name").value = "";
  document.getElementById("email").value = "";
  document.getElementById("phone").value = "";
  document.getElementById("company").value = "";
  document.getElementById("message").value = "";
  grecaptcha.reset();
}

function sendEmail() {
    setTimeout(function() {
        document.getElementById("send-failure").classList.add("show");
    }, 300);
}

var validateFieldsFunction = function() { validateFields(); }
window.onload = function() { checkBrowser(); }
window.onresize = function() { checkForOpenSidebar(); }
window.onscroll = function() { handleBackgrounds(); };
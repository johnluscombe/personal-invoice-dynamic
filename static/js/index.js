function checkBrowser() {
    var isBadIE = navigator.appName == "Microsoft Internet Explorer";
    if (isBadIE) {
        // IE 10 and earlier not supported, redirect
        window.location = "http://browsehappy.com";
    }
}

function openSidebar() {
    document.getElementById("burger").onclick = closeSidebar;
    document.getElementById("main").style.marginLeft = "-350px";
    document.getElementById("main").style.marginRight = "350px";
    document.getElementById("navbar").style.marginRight = "350px";
    document.getElementById("sidebar").style.width = "350px";
}

function closeSidebar() {
    document.getElementById("burger").onclick = openSidebar;
    document.getElementById("main").style.marginLeft = "0";
    document.getElementById("main").style.marginRight = "0";
    document.getElementById("navbar").style.marginRight = "0";
    document.getElementById("sidebar").style.width = "0";
}

function checkForOpenSidebar() {
    if (document.documentElement.clientWidth > 1007) {
        closeSidebar();
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

function showSuccess() {
    document.getElementById("send-success").classList.add("show");
    document.getElementById("send-failure").classList.remove("show");
    document.getElementById("sending").classList.remove("show");
}

function showFailure() {
    document.getElementById("send-success").classList.remove("show");
    document.getElementById("send-failure").classList.add("show");
    document.getElementById("sending").classList.remove("show");
}

function showSending() {
    document.getElementById("send-success").classList.remove("show");
    document.getElementById("send-failure").classList.remove("show");
    document.getElementById("sending").classList.add("show");
}

function hideSuccess() {
    document.getElementById("send-success").classList.remove("show");
}

function hideFailure() {
    document.getElementById("send-failure").classList.remove("show");
}

function hideSending() {
    document.getElementById("sending").classList.remove("show");
}

function sendEmail() {
    var params = {
        "name": document.getElementById("name").value,
        "email": document.getElementById("email").value,
        "phone": document.getElementById("phone").value,
        "company": document.getElementById("company").value,
        "message": document.getElementById("message").value,
        "token": grecaptcha.getResponse()
    }

    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var response = JSON.parse(this.responseText);
            if (response["success"] == "true") {
                showSuccess();
            } else {
                showFailure();
            }
        } else if (this.readyState == 4) {
            showFailure();
        } else {
            showSending();
        }
    }
    xhttp.open("POST", "/send-email");
    xhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    xhttp.send(JSON.stringify(params));
}

var validateFieldsFunction = function() { validateFields(); }
window.onload = function() { checkBrowser(); }
window.onresize = function() { checkForOpenSidebar(); }

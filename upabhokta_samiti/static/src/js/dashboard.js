// var sidebarToggle = document.querySelector("#sidebar-toggle");
// sidebarToggle.addEventListener("click", function () { document.querySelector("#sidebar").classList.toggle("collapsed") });

var notificationCounter = document.getElementsByClassName("notification-counter");
var counterBadge = document.getElementById("counter-badge");
counter = 0;

for (var i = 0; i < notificationCounter.length; i++) {
    counter += 1;
}
counter !== 0 ?
    (counterBadge.innerHTML = counter) :
    (() => {
        counterBadge.style.display = "none";
        notificationCounter.innerHTML = `
                                                <a class="dropdown-item notification-counter" >
                                                    <div class="notification-item">
                                                        <div class="notification-title">
                                                            No notification
                                                        </div>
                                                        <div class="notification-datetime">
                                                            
                                                        </div>
                                                    </div>
                                                </a>
        `;
    })();
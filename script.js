/* =========================================
   THE SR JOURNEY - JAVASCRIPT
   ========================================= */


/* =========================================
   WHATSAPP NUMBER
   ========================================= */

const WHATSAPP_NUMBER = "917979001521";


/* =========================================
   MOBILE MENU
   ========================================= */

function toggleMenu() {

    const navbar = document.getElementById("navbar");

    navbar.classList.toggle("show");

}


/* =========================================
   CLOSE MOBILE MENU
   WHEN NAVIGATION LINK IS CLICKED
   ========================================= */

document.querySelectorAll(".navbar a").forEach(function(link) {

    link.addEventListener("click", function() {

        const navbar = document.getElementById("navbar");

        navbar.classList.remove("show");

    });

});


/* =========================================
   GENERAL WHATSAPP FUNCTION
   ========================================= */

function openWhatsApp() {

    const message =
        "Hello The SR Journey! 👋\n\n" +
        "I want to enquire about your tour packages.\n\n" +
        "Please share the available packages, " +
        "details and pricing.";

    const whatsappURL =
        "https://wa.me/" +
        WHATSAPP_NUMBER +
        "?text=" +
        encodeURIComponent(message);

    window.open(whatsappURL, "_blank");

}


/* =========================================
   PACKAGE BOOKING
   ========================================= */

function bookPackage(packageName) {

    const message =
        "Hello The SR Journey! 👋\n\n" +

        "I am interested in the following package:\n\n" +

        "📦 Package: " +
        packageName +

        "\n\nPlease share:\n" +
        "• Detailed itinerary\n" +
        "• Availability\n" +
        "• Total price\n" +
        "• Vehicle details\n" +
        "• Hotel details\n\n" +

        "Thank you.";

    const whatsappURL =
        "https://wa.me/" +
        WHATSAPP_NUMBER +
        "?text=" +
        encodeURIComponent(message);

    window.open(whatsappURL, "_blank");

}


/* =========================================
   PAGE LOAD MESSAGE
   ========================================= */

document.addEventListener("DOMContentLoaded", function() {

    console.log(
        "The SR Journey website loaded successfully."
    );

});
/* =========================================
   BOOKING FORM
   ========================================= */

const bookingForm =
    document.getElementById("bookingForm");


if (bookingForm) {

    bookingForm.addEventListener(
        "submit",
        function(event) {

            event.preventDefault();


            const name =
                document.getElementById("name").value;

            const phone =
                document.getElementById("phone").value;

            const destination =
                document.getElementById("destination").value;

            const date =
                document.getElementById("date").value;

            const people =
                document.getElementById("people").value;

            const message =
                document.getElementById("message").value;


            const whatsappMessage =

                "Hello The SR Journey! 👋\n\n" +

                "I want to enquire about a tour package.\n\n" +

                "👤 Name: " +
                name +

                "\n📱 Mobile: " +
                phone +

                "\n📦 Package: " +
                destination +

                "\n📅 Travel Date: " +
                date +

                "\n👥 Number of People: " +
                people +

                "\n📝 Special Requirement: " +
                (message || "None") +

                "\n\nPlease share the complete package details and final price.";


            const whatsappURL =
                "https://wa.me/" +
                WHATSAPP_NUMBER +
                "?text=" +
                encodeURIComponent(
                    whatsappMessage
                );


            window.open(
                whatsappURL,
                "_blank"
            );

        }
    );

}
// Register the service worker
if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("./service-worker.js")
            .then(() => {
                console.log("PWA service worker registered.");
            })
            .catch((error) => {
                console.error("Service worker registration failed:", error);
            });
    });
}


// Show an install button when the browser supports the prompt
let deferredInstallPrompt = null;

window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();

    deferredInstallPrompt = event;

    const installButton = document.getElementById("installBtn");

    if (installButton) {
        installButton.hidden = false;
    }
});

const installButton = document.getElementById("installBtn");

if (installButton) {
    installButton.addEventListener("click", async () => {
        if (!deferredInstallPrompt) {
            alert(
                "To install the app, open this website in a supported browser and use its Install App or Add to Home Screen option."
            );
            return;
        }

        deferredInstallPrompt.prompt();

        await deferredInstallPrompt.userChoice;

        deferredInstallPrompt = null;
        installButton.hidden = true;
    });
}
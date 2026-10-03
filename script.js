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
   CAB + PAYMENT BOOKING CALCULATOR
   ========================================= */

const CAB_OPTIONS = {
    hatchback: { name: "Hatchback", seats: 4, extra: 0 },
    sedan: { name: "Sedan", seats: 4, extra: 300 },
    suv: { name: "SUV", seats: 6, extra: 600 },
    premium: { name: "Premium SUV", seats: 6, extra: 1000 },
    tempo: { name: "Tempo Traveller", seats: 12, extra: 800 }
};

const PACKAGE_PRICES = {
    "Darbhanga Local Tour": 999,
    "Darbhanga - Madhubani": 1299,
    "Sitamarhi - Janakpur": 3999,
    "Darbhanga - Muzaffarpur": 1499,
    "Rajgir - Nalanda": 3499,
    "Darbhanga - Patna": 3499,
    "Darbhanga - Bodh Gaya": 4499,
    "Darbhanga - Valmiki Nagar": 4999,
    "Pawapuri - Rajgir": 3999,
    "Darbhanga - Varanasi": 6999
};

function formatINR(amount) {
    return "₹" + Number(amount || 0).toLocaleString("en-IN");
}

function getSelectedCab() {
    const select = document.getElementById("cabCategory");
    return select ? CAB_OPTIONS[select.value] : null;
}

function syncCabSelection(value) {
    const radio = document.querySelector('input[name="cabChoice"][value="' + value + '"]');
    if (radio) radio.checked = true;
}

function updateBookingSummary() {
    const destination = document.getElementById("destination");
    const peopleInput = document.getElementById("people");
    const cabSelect = document.getElementById("cabCategory");
    if (!destination || !peopleInput || !cabSelect) return;

    const packageName = destination.value;
    const people = Math.max(0, parseInt(peopleInput.value, 10) || 0);
    const cab = CAB_OPTIONS[cabSelect.value];
    const packagePerPerson = PACKAGE_PRICES[packageName] || 0;
    const packageFare = packagePerPerson * people;
    const cabExtra = cab ? cab.extra : 0;
    const total = packageFare + cabExtra;

    document.getElementById("summaryPackage").textContent = packageName || "-";
    document.getElementById("summaryCab").textContent = cab ? cab.name : "-";
    document.getElementById("summaryPeople").textContent = people;
    document.getElementById("summaryBase").textContent = formatINR(packageFare);
    document.getElementById("summaryCabExtra").textContent = formatINR(cabExtra);
    document.getElementById("summaryTotal").textContent = formatINR(total);

    return { packageName, people, cab, packageFare, cabExtra, total };
}

const bookingForm = document.getElementById("bookingForm");

if (bookingForm) {
    ["destination", "people", "cabCategory"].forEach(function(id) {
        const element = document.getElementById(id);
        if (element) {
            element.addEventListener("change", function() {
                if (id === "cabCategory") syncCabSelection(element.value);
                updateBookingSummary();
            });
            element.addEventListener("input", updateBookingSummary);
        }
    });

    document.querySelectorAll('input[name="cabChoice"]').forEach(function(radio) {
        radio.addEventListener("change", function() {
            document.getElementById("cabCategory").value = radio.value;
            updateBookingSummary();
        });
    });

    bookingForm.addEventListener("submit", function(event) {
        event.preventDefault();

        const calculation = updateBookingSummary();
        const name = document.getElementById("name").value.trim();
        const phone = document.getElementById("phone").value.trim();
        const date = document.getElementById("date").value;
        const message = document.getElementById("message").value.trim();
        const paymentElement = document.querySelector('input[name="paymentMethod"]:checked');

        if (!calculation || !calculation.cab) {
            alert("Please select a cab category.");
            return;
        }

        if (!paymentElement) {
            alert("Please select a payment method.");
            return;
        }

        if (calculation.people > calculation.cab.seats) {
            alert(calculation.cab.name + " has a maximum capacity of " +
                  calculation.cab.seats + " passengers. Please choose another cab.");
            return;
        }

        const whatsappMessage =
            "Hello The SR Journey! 👋\n\n" +
            "I want to make a cab/tour booking.\n\n" +
            "👤 Name: " + name + "\n" +
            "📱 Mobile: " + phone + "\n" +
            "📦 Package: " + calculation.packageName + "\n" +
            "📅 Travel Date: " + date + "\n" +
            "👥 Passengers: " + calculation.people + "\n" +
            "🚕 Cab Category: " + calculation.cab.name + "\n" +
            "💰 Package Fare: " + formatINR(calculation.packageFare) + "\n" +
            "🚕 Cab Supplement: " + formatINR(calculation.cabExtra) + "\n" +
            "💵 Estimated Total: " + formatINR(calculation.total) + "\n" +
            "💳 Payment Method: " + paymentElement.value + "\n" +
            "📝 Special Requirement: " + (message || "None") +
            "\n\nPlease confirm vehicle availability, final fare, inclusions and payment instructions.";

        const whatsappURL = "https://wa.me/" + WHATSAPP_NUMBER +
            "?text=" + encodeURIComponent(whatsappMessage);

        const status = document.getElementById("bookingStatus");
        if (status) status.textContent = "Opening WhatsApp with your booking details...";

        window.open(whatsappURL, "_blank");
    });

    updateBookingSummary();
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

/* =========================================
   PHASE 1 - PACKAGE FILTER
   ========================================= */

function setupPackageFilters() {
    const search = document.getElementById("packageSearch");
    const duration = document.getElementById("durationFilter");
    const budget = document.getElementById("budgetFilter");
    const reset = document.getElementById("resetPackageFilter");
    const count = document.getElementById("packageResultCount");
    const cards = Array.from(document.querySelectorAll(".package-card"));

    if (!search || !duration || !budget || !reset || !cards.length) return;

    function applyFilters() {
        const query = search.value.trim().toLowerCase();
        const selectedDuration = duration.value;
        const maxBudget = Number(budget.value || 0);
        let visible = 0;

        cards.forEach(function(card) {
            const name = (card.dataset.packageName || card.textContent).toLowerCase();
            const cardDuration = card.dataset.duration || "";
            const price = Number(card.dataset.price || 0);

            const matchesSearch = !query || name.includes(query);
            const matchesDuration = !selectedDuration || cardDuration === selectedDuration;
            const matchesBudget = !maxBudget || price <= maxBudget;
            const show = matchesSearch && matchesDuration && matchesBudget;

            card.classList.toggle("is-hidden", !show);
            if (show) visible++;
        });

        count.textContent = visible === cards.length
            ? "Showing all " + visible + " packages"
            : "Showing " + visible + " of " + cards.length + " packages";
    }

    [search, duration, budget].forEach(function(element) {
        element.addEventListener("input", applyFilters);
        element.addEventListener("change", applyFilters);
    });

    reset.addEventListener("click", function() {
        search.value = "";
        duration.value = "";
        budget.value = "";
        applyFilters();
    });

    applyFilters();
}


/* =========================================
   PHASE 1 - BOOKING ID
   ========================================= */

function generateBookingId(prefix) {
    const now = new Date();
    const datePart = String(now.getFullYear()).slice(-2) +
        String(now.getMonth() + 1).padStart(2, "0") +
        String(now.getDate()).padStart(2, "0");
    const randomPart = Math.floor(1000 + Math.random() * 9000);
    return (prefix || "SRJ") + "-" + datePart + "-" + randomPart;
}


/* =========================================
   PHASE 1 - CAB ONLY BOOKING
   ========================================= */

function setupCabOnlyForm() {
    const form = document.getElementById("cabOnlyForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const name = document.getElementById("cabName").value.trim();
        const phone = document.getElementById("cabPhone").value.trim();
        const pickup = document.getElementById("cabPickup").value.trim();
        const drop = document.getElementById("cabDrop").value.trim();
        const date = document.getElementById("cabDate").value;
        const time = document.getElementById("cabTime").value;
        const passengers = Number(document.getElementById("cabPassengers").value);
        const cab = document.getElementById("cabType").value;
        const requirement = document.getElementById("cabRequirement").value.trim();

        const capacity = {
            "Hatchback": 4,
            "Sedan": 4,
            "SUV": 6,
            "Premium SUV": 6,
            "Tempo Traveller": 12
        };

        if (capacity[cab] && passengers > capacity[cab]) {
            alert(cab + " has capacity for up to " + capacity[cab] + " passengers.");
            return;
        }

        const bookingId = generateBookingId("CAB");

        const message =
            "Hello The SR Journey! 👋\n\n" +
            "🚕 CAB BOOKING REQUEST\n\n" +
            "🎟️ Booking ID: " + bookingId + "\n" +
            "👤 Name: " + name + "\n" +
            "📱 Mobile: " + phone + "\n" +
            "📍 Pickup: " + pickup + "\n" +
            "📍 Drop: " + drop + "\n" +
            "📅 Date: " + date + "\n" +
            "⏰ Pickup Time: " + time + "\n" +
            "👥 Passengers: " + passengers + "\n" +
            "🚗 Cab Category: " + cab + "\n" +
            "📝 Requirement: " + (requirement || "None") +
            "\n\nPlease confirm vehicle availability and final fare.";

        const status = document.getElementById("cabStatus");
        if (status) {
            status.textContent = "Booking ID " + bookingId + " created. Opening WhatsApp...";
        }

        window.open(
            "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(message),
            "_blank"
        );
    });
}


/* =========================================
   PHASE 1 - HOTEL ENQUIRY
   ========================================= */

function setupHotelForm() {
    const form = document.getElementById("hotelForm");
    if (!form) return;

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const name = document.getElementById("hotelName").value.trim();
        const phone = document.getElementById("hotelPhone").value.trim();
        const destination = document.getElementById("hotelDestination").value.trim();
        const rooms = document.getElementById("hotelRooms").value;
        const checkIn = document.getElementById("checkIn").value;
        const checkOut = document.getElementById("checkOut").value;
        const guests = document.getElementById("hotelGuests").value;
        const budget = document.getElementById("hotelBudget").value;
        const requirement = document.getElementById("hotelRequirement").value.trim();

        if (new Date(checkOut) <= new Date(checkIn)) {
            alert("Check-out date must be after check-in date.");
            return;
        }

        const bookingId = generateBookingId("HTL");

        const message =
            "Hello The SR Journey! 👋\n\n" +
            "🏨 HOTEL BOOKING ENQUIRY\n\n" +
            "🎟️ Enquiry ID: " + bookingId + "\n" +
            "👤 Name: " + name + "\n" +
            "📱 Mobile: " + phone + "\n" +
            "📍 Destination: " + destination + "\n" +
            "🛏️ Rooms: " + rooms + "\n" +
            "📅 Check-in: " + checkIn + "\n" +
            "📅 Check-out: " + checkOut + "\n" +
            "👥 Guests: " + guests + "\n" +
            "💰 Budget/Night: " + (budget || "Any") + "\n" +
            "📝 Requirement: " + (requirement || "None") +
            "\n\nPlease share available hotels, room rates and booking terms.";

        const status = document.getElementById("hotelStatus");
        if (status) {
            status.textContent = "Enquiry ID " + bookingId + " created. Opening WhatsApp...";
        }

        window.open(
            "https://wa.me/" + WHATSAPP_NUMBER + "?text=" + encodeURIComponent(message),
            "_blank"
        );
    });
}


/* =========================================
   PHASE 1 - INITIALIZE
   ========================================= */

document.addEventListener("DOMContentLoaded", function() {
    setupPackageFilters();
    setupCabOnlyForm();
    setupHotelForm();

    // Prevent selecting a past date for the new service forms.
    const today = new Date().toISOString().split("T")[0];
    ["cabDate", "checkIn", "checkOut", "date"].forEach(function(id) {
        const input = document.getElementById(id);
        if (input) input.min = today;
    });
});

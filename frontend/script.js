async function loadData() {
    const response = await fetch("http://127.0.0.1:8000/production");
    const data = await response.json();

    document.getElementById("scenes").textContent = data.scenes;

    document.getElementById("crew").textContent =
        data.crew_present + "/" + data.crew_total;

    document.getElementById("equipment").textContent =
        data.equipment_working + "/" + data.equipment_total;

    document.getElementById("delay").textContent =
        "+" + data.delay + " min";

    document.getElementById("incident").textContent =
        "⚠ " + data.incident;

    document.getElementById("incident-text").textContent =
        "Production equipment requires attention.";
}

loadData();
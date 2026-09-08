async function loadData() {
    const response = await fetch("/production");
    const data = await response.json();

    document.getElementById("scenes").textContent = data.scenes.length;

    document.getElementById("crew").textContent =
        data.crew_present + "/" + data.crew_total;

    document.getElementById("equipment").textContent =
        data.equipment_working + "/" + data.equipment_total;

    document.getElementById("delay").textContent =
        "+" + data.delay + " min";

    document.getElementById("incident").textContent =
        "⚠ " + data.incident;

    document.getElementById("recommendation").textContent =
        data.recommendation;

    const scene = data.scenes.find(function(item) {
    return data.incident.includes("Scene " + item.number);
    });

    if (scene) {
        document.getElementById("incident-text").textContent =
        scene.name + " is affected by this equipment failure.";
    } else {
        document.getElementById("incident-text").textContent =
        "Production equipment requires attention.";
    }
}

loadData();

document.getElementById("approve-button").addEventListener("click", async function() {
    const response = await fetch("/approve", {
        method: "POST"
    });
    const data = await response.json();

    document.getElementById("approval-status").textContent =
        "✓ " + data.message;

    document.getElementById("approve-button").disabled = true;
});
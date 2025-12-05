const BACKEND_URL = "http://localhost:8000";

async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error("Request failed");
  return res.json();
}

async function loadSystemInfo() {
  try {
    const data = await fetchJSON(`${BACKEND_URL}/api/system/info`);
    document.getElementById("hostname").textContent = data.hostname;
    document.getElementById("os").textContent = data.os;

    const uptimeSec = data.uptime_seconds;
    const hours = Math.floor(uptimeSec / 3600);
    const minutes = Math.floor((uptimeSec % 3600) / 60);
    document.getElementById("uptime").textContent = `${hours}h ${minutes}m`;

    document.getElementById("cpu").textContent = data.cpu_percent.toFixed(1);
    document.getElementById("memory").textContent = data.memory_percent.toFixed(1);
    document.getElementById("disk").textContent = data.disk_percent.toFixed(1);
  } catch (err) {
    console.error(err);
  }
}

async function loadIncidents() {
  try {
    const rows = await fetchJSON(`${BACKEND_URL}/api/incidents?limit=20`);
    const tbody = document.getElementById("incidents-table");
    tbody.innerHTML = "";
    rows.forEach((inc) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${inc.created_at}</td>
        <td>${inc.severity}</td>
        <td>${inc.source}</td>
        <td>${inc.category}</td>
        <td>${inc.message}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
  }
}

async function loadEvents() {
  try {
    const rows = await fetchJSON(`${BACKEND_URL}/api/events?limit=20`);
    const tbody = document.getElementById("events-table");
    tbody.innerHTML = "";
    rows.forEach((e) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${e.created_at}</td>
        <td>${e.level}</td>
        <td>${e.source}</td>
        <td>${e.message}</td>
      `;
      tbody.appendChild(tr);
    });
  } catch (err) {
    console.error(err);
  }
}

function refreshAll() {
  loadSystemInfo();
  loadIncidents();
  loadEvents();
}

refreshAll();
setInterval(refreshAll, 15000);

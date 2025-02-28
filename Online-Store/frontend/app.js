// Beispiel-Daten: In einer echten Anwendung würden diese per API abgerufen
let laptops = [];
let cart = [];
let selectedLaptop = null;
let filteredLaptops = [];

// Laptops von der API laden
async function fetchLaptops() {
    try {
        const response = await fetch("http://localhost:5000/api/laptops");
        laptops = await response.json();
        filteredLaptops = [...laptops];
        renderLaptopList();
    } catch (error) {
        console.error("Fehler beim Abrufen der Laptops:", error);
    }
}

// Laptop-Detail von API holen
async function fetchLaptopDetails(id) {
    try {
        const response = await fetch(`http://localhost:5000/api/laptop/${id}`);
        selectedLaptop = await response.json();

        document.getElementById("detail-title").innerText = selectedLaptop.name;
        document.getElementById("detail-description").innerText = selectedLaptop.spezifikationen;
        document.getElementById("detail-price").innerText = `Preis: ${selectedLaptop.preis}€`;
        document.getElementById("laptop-detail").style.display = "flex";
    } catch (error) {
        console.error("Fehler beim Abrufen der Laptop-Details:", error);
    }
}

// Detailansicht anzeigen (angepasst)
function showDetail(id) {
    fetchLaptopDetails(id);
}

// Bestellung an API senden
async function purchaseOrder() {
    if (cart.length === 0) {
        alert("Ihr Warenkorb ist leer!");
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/api/order", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ cart }),
        });

        const result = await response.json();
        document.getElementById("order-info").innerHTML = `
            <p>Bestellnummer: ${result.orderId}</p>
            <p>Gesamtbetrag: ${cart.reduce((sum, item) => sum + item.price, 0)}€</p>
        `;
        document.getElementById("order-confirmation").style.display = "flex";

        cart = [];
        renderCart();
    } catch (error) {
        console.error("Fehler bei der Bestellung:", error);
    }
}

  // Initiale Daten laden
  fetchLaptops();

  // Initiale Darstellung der Laptop-Liste
  function renderLaptopList() {
    const listContainer = document.getElementById("laptop-list");
    listContainer.innerHTML = "";
    filteredLaptops.forEach(laptop => {
      const laptopDiv = document.createElement("div");
      laptopDiv.className = "laptop-item";
      laptopDiv.innerHTML = `
        <h3>${laptop.name}</h3>
        <p>${laptop.description}</p>
        <p>Preis: ${laptop.price}€</p>
        <button onclick="showDetail(${laptop.id})">Details</button>
      `;
      listContainer.appendChild(laptopDiv);
    });
  }
  
  // Detailansicht anzeigen
  function showDetail(id) {
    selectedLaptop = laptops.find(l => l.id === id);
    if (selectedLaptop) {
      document.getElementById("detail-title").innerText = selectedLaptop.name;
      document.getElementById("detail-description").innerText = selectedLaptop.description;
      document.getElementById("detail-price").innerText = `Preis: ${selectedLaptop.price}€`;
      document.getElementById("laptop-detail").style.display = "flex";
    }
  }
  
  function closeDetail() {
    document.getElementById("laptop-detail").style.display = "none";
  }
  
  // Laptop zum Warenkorb hinzufügen
  function addToCart(laptop) {
    if (laptop) {
      cart.push(laptop);
      renderCart();
      closeDetail();
    }
  }
  
  // Warenkorb anzeigen
  function renderCart() {
    const cartContainer = document.getElementById("cart-items");
    cartContainer.innerHTML = "";
    let total = 0;
    cart.forEach((item, index) => {
      total += item.price;
      const itemDiv = document.createElement("div");
      itemDiv.className = "cart-item";
      itemDiv.innerHTML = `
        <span>${item.name} - ${item.price}€</span>
        <button onclick="removeFromCart(${index})">Entfernen</button>
      `;
      cartContainer.appendChild(itemDiv);
    });
    document.getElementById("total-price").innerText = `Gesamtpreis: ${total}€`;
  }
  
  function removeFromCart(index) {
    cart.splice(index, 1);
    renderCart();
  }
  
  // Kaufabwicklung
  async function purchaseOrder() {
    if (cart.length === 0) {
      alert("Ihr Warenkorb ist leer!");
      return;
    }
  
    // Simulieren einer erfolgreichen Bestellung:
    const orderId = Math.floor(Math.random() * 10000);
    const totalPrice = cart.reduce((sum, item) => sum + item.price, 0);
  
    // Anzeige der Bestellbestätigung
    document.getElementById("order-info").innerHTML = `
      <p>Bestellnummer: ${orderId}</p>
      <p>Gesamtbetrag: ${totalPrice}€</p>
    `;
    document.getElementById("order-confirmation").style.display = "flex";
  
    // Warenkorb zurücksetzen
    cart = [];
    renderCart();
  }
  
  function closeConfirmation() {
    document.getElementById("order-confirmation").style.display = "none";
  }
  
  function handleSearch() {
    const searchInput = document.getElementById("search-input");
    const searchTerm = searchInput.value.trim().toLowerCase();
  
    // Wenn das Suchfeld leer ist, alle Laptops anzeigen
    if (!searchTerm) {
      filteredLaptops = [...laptops];
    } else {
      filteredLaptops = laptops.filter(laptop =>
        laptop.name.toLowerCase().includes(searchTerm) ||
        laptop.description.toLowerCase().includes(searchTerm)
      );
    }
  
    applySort(); // Sortierung erneut anwenden, falls ausgewählt
    renderLaptopList();
  
    // Falls keine Ergebnisse gefunden wurden, Hinweis anzeigen
    if (filteredLaptops.length === 0) {
      document.getElementById("laptop-list").innerHTML =
        "<p>Keine Ergebnisse gefunden.</p>";
    }
  }
  
  // Sortierfunktion: Sortiert filteredLaptops je nach Auswahl
  function handleSort() {
    applySort();
    renderLaptopList();
  }
  
  function applySort() {
    const sortValue = document.getElementById("sort-select").value;
    if (sortValue === "price-asc") {
      filteredLaptops.sort((a, b) => a.price - b.price);
    } else if (sortValue === "price-desc") {
      filteredLaptops.sort((a, b) => b.price - a.price);
    } else if (sortValue === "name-asc") {
      filteredLaptops.sort((a, b) => a.name.localeCompare(b.name));
    } else if (sortValue === "name-desc") {
      filteredLaptops.sort((a, b) => b.name.localeCompare(a.name));
    }
  }
  
  // Routing über Hash-Wechsel (einfaches Client-seitiges Routing)
  function handleRouting() {
    const hash = window.location.hash;
    const sections = ["laptops", "cart"];
    sections.forEach(section => {
      document.getElementById(section).style.display = (hash === `#${section}`) ? "block" : "none";
    });
    // Bei leerem Hash Standardbereich anzeigen
    if (!hash) {
      document.getElementById("laptops").style.display = "block";
    }
  }
  
  // Event Listener für Suche und Sortierung
  document.getElementById("search-input").addEventListener("input", handleSearch);
  document.getElementById("sort-select").addEventListener("change", handleSort);
  
  // Routing-Listener
  window.addEventListener("hashchange", handleRouting);
  
  // Initiale Render-Funktionen aufrufen
  renderLaptopList();
  handleRouting();
  
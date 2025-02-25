// Beispiel-Daten: In einer echten Anwendung würden diese per API abgerufen
const laptops = [
    { id: 1, name: "Laptop A", description: "Leistungsstarker Laptop", price: 500 },
    { id: 2, name: "Laptop B", description: "Kompakter und leichter Laptop", price: 450 },
    { id: 3, name: "Laptop C", description: "Budget-Option mit guter Performance", price: 400 },
    { id: 4, name: "Laptop D", description: "Gaming-Laptop mit hoher Performance", price: 800 },
    { id: 5, name: "Laptop E", description: "Ultrabook für den Business-Einsatz", price: 700 }
  ];
  
  let cart = [];
  let selectedLaptop = null;
  
  // Kopie der Laptop-Liste für Filterung und Sortierung
  let filteredLaptops = [...laptops];
  
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
  
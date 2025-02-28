require("dotenv").config({ path: '../../.env' });
const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Verbindung zur MySQL-Datenbank
const db = mysql.createPool({
    host: process.env.DB_HOST, // MySQL Host
    user: process.env.DB_USER, // Benutzername
    password: process.env.DB_PASSWORD, // Passwort
    database: process.env.DB_NAME, // Datenbankname
});

// Alle Laptops abrufen
app.get("/api/laptops", (req, res) => {
    const sql = `SELECT p.produkt_id, p.name, p.hersteller, p.spezifikationen, 
                        pe.preis, pe.anbieter 
                 FROM Dim_Produkt p 
                 LEFT JOIN Dim_Preisentwicklung pe ON p.produkt_id = pe.produkt_id 
                 ORDER BY pe.preis ASC;`;
    db.query(sql, (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(result);
    });
});

// Einzelnes Laptop-Detail abrufen
app.get("/api/laptop/:id", (req, res) => {
    const sql = `SELECT * FROM Dim_Produkt WHERE produkt_id = ?`;
    db.query(sql, [req.params.id], (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json(result[0]);
    });
});

// Bestellungen speichern
app.post("/api/order", (req, res) => {
    const { cart } = req.body;
    if (!cart || cart.length === 0) {
        return res.status(400).json({ message: "Der Warenkorb ist leer!" });
    }

    const sql = `INSERT INTO Fakt_Verkauf (produkt_id, datum_id, anzahl_verkauft, preis) VALUES ?`;
    const values = cart.map(item => [item.id, 1, 1, item.price]);

    db.query(sql, [values], (err, result) => {
        if (err) {
            return res.status(500).json({ error: err.message });
        }
        res.json({ message: "Bestellung erfolgreich!", orderId: result.insertId });
    });
});

// Server starten
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
    console.log(`Server läuft auf http://localhost:${PORT}`);
});

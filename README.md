# Refurbished Laptop Shop

This project is a web application for a refurbished laptop shop. It includes a frontend for browsing and purchasing laptops, a backend for handling data, and a dashboard for visualizing sales and trends.

## Project Structure

- `start.py`: Main script to start the application.
- `Scrapper/`: Directory containing scripts for scraping data.
- `Online-Store/frontend/`: Directory containing frontend files (HTML, CSS, JavaScript).
- `dashboard.py`: Streamlit dashboard for visualizing data.
- `requirements.txt`: List of Python dependencies.
- `.gitignore`: Git ignore file to exclude certain files from version control.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <repository-url>
   cd WI22C_BI
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the root directory with the following content:
   ```env
   DB_USER=<your-database-username>
   DB_PASSWORD=<your-database-password>
   DB_HOST=<your-database-host>
   DB_PORT=<your-database-port>
   DB_NAME=<your-database-name>
   ```

4. **Run the application:**
   ```sh
   python start.py
   ```

## Usage

- **Frontend:**
  Open `Online-Store/frontend/index.html` in a web browser to browse and purchase laptops.

- **Dashboard:**
  Access the Streamlit dashboard at `http://localhost:8501` to visualize sales and trends.

## License

This project is licensed under the MIT License.

# TagihanSerampangan

TagihanSerampangan is a terminal-based money management dashboard for Indonesian users. It helps track miscellaneous bills, incomes, savings, and budgets using a colorful Rich-powered interface. The app persists data securely in a JSON file with per-user encryption, supports bilingual UI (Bahasa Indonesia & English), and offers month-by-month budgeting with quick copy tools.

## Highlights

- **Secure profiles**: User accounts with salted passwords and encrypted JSON payloads (AES-like stream + HMAC integrity) ensure only authenticated users can read their data.
- **Rich CLI dashboard**: Panels and tables provide at-a-glance totals, expense progress bars, and formatted Indonesian Rupiah (`Rp`) values.
- **Bilingual experience**: Toggle between Indonesian and English on demand; preferences persist per user.
- **Monthly budgeting**: Each month stores its own income, savings, and expense items; copy previous month’s plan to the current period in one click.
- **Modular menus**: Intuitive navigation for viewing dashboards, managing budgets, changing periods, switching languages, and exiting safely.

## Requirements

- Python **3.9+** (tested with macOS system Python 3.9)
- [`rich`](https://rich.readthedocs.io/en/stable/) library (`pip install rich`)

> **Note**: `rich` is the only external dependency. If you plan to use a virtual environment, create and activate it before installing packages.

## Installation

```bash
# Clone the repository
git clone https://github.com/<your-account>/tagihanserampangan.git
cd tagihanserampangan

# (Optional) create a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install runtime dependency
python3 -m pip install --upgrade pip
python3 -m pip install rich
```

## Usage

```bash
python3 tagihanserampangan.py
```

### First Run

1. Launch the script. You’ll be prompted to log in or sign up.
2. New users provide an email, create & confirm a password (salted + hashed), and receive seeded demo data for May 2025.
3. Returning users enter their password to decrypt their stored profile.

### Main Menu

1. **Lihat Dashboard / View Dashboard** – show the Rich dashboard (income, budgeted vs. actual, savings, expense progress bars).
2. **Menu Anggaran / Budgeting Menu** – add or manage incomes, savings, budgets, copy previous month’s data.
3. **Ubah Bulan/Tahun / Change Month/Year** – choose from previous/current/next year shortcuts and select month via numeric input (1-12).
4. **Ganti Bahasa / Change Language** – switch between Bahasa Indonesia and English.
5. **Keluar / Exit** – persist data and close the session.

### Budgeting Menu Options

1. Add income source
2. Add saving
3. Add budget item (with optional category)
4. Edit realization (manual amount, percentage 1-100%, or auto 100%)
5. Delete item (income, savings, or budget)
6. Copy previous month’s data into the current month
7. Back to main menu

All operations automatically re-encrypt and save data to `tagihan_data.json`.

## Data Storage & Security

- Data lives in `tagihan_data.json` alongside the script.
- File structure includes `users` (email + salted password hash), `profiles` (encrypted payloads), and `months` per profile.
- Encryption uses PBKDF2-HMAC-SHA256 (200k iterations) to derive a 32-byte key from the user’s password + salt, then XOR-based stream cipher with SHA-256 keystream, and an HMAC-SHA256 tag for integrity.
- If the JSON is corrupted, the app recreates default seeds; corrupted encrypted payloads prompt the user to re-enter credentials.

## Localization

- Default language is Bahasa Indonesia. Switch to English via main menu option 4.
- Language choice persists per user.

## Tips

- Run `python3 -B -m py_compile tagihanserampangan.py` to ensure syntax validity before deployment.
- Back up `tagihan_data.json` regularly (encrypted but still crucial for continuity).
- Add `~/Library/Python/3.x/bin` (or equivalent) to `PATH` if pip warns about script locations.

## Contributing

1. Fork the repo and create a feature branch.
2. Install dependencies (`pip install rich`).
3. Make your changes with clear commits.
4. Run linting or additional tests if you add them.
5. Submit a pull request with a concise summary of improvements.

## License

Specify your preferred license (MIT, Apache-2.0, etc.) before publishing. Update this section accordingly.

## Acknowledgements

- [`rich`](https://github.com/Textualize/rich) for the expressive CLI rendering.
- The initial dashboard concept referencing Indonesian budgeting needs.

Selamat mengelola tagihan secara serampangan tapi teratur! 🎉

"""pip install rich if not installed."""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from copy import deepcopy
from dataclasses import dataclass
from getpass import getpass
from pathlib import Path
from typing import Any, Dict, List, Tuple

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

DATA_FILE = Path(__file__).parent / "tagihan_data.json"
console = Console()

LANGUAGE_STRINGS: Dict[str, Dict[str, str]] = {
    "id": {
        "language_name": "Bahasa Indonesia (ID)",
        "dashboard_title": "Dasbor Manajemen Keuangan 💰",
        "year_label": "Tahun",
        "month_label": "Bulan",
        "monthly_report": "Laporan Bulanan 📊",
        "stat_total_income": "Total Pendapatan",
        "stat_budgeted_expenses": "Anggaran Terencana",
        "stat_spending": "Pengeluaran {month}",
        "stat_savings": "Tabungan {month}",
        "expenses_list": "Daftar Pengeluaran",
        "column_name": "Nama",
        "column_allocation": "Alokasi 💰",
        "column_realization": "Realisasi 💵",
        "column_progress": "Progres Penggunaan Anggaran",
        "column_percent_usage": "% Penggunaan",
        "column_amount": "Jumlah",
        "column_category": "Kategori",
        "no_expenses": "Belum ada pengeluaran.",
        "error_positive_int": "Masukkan angka bulat tidak negatif.",
        "prompt_income_name": "Nama sumber pendapatan: ",
        "prompt_amount": "Jumlah (Rp): ",
        "income_added": "Sumber pendapatan berhasil ditambahkan.",
        "prompt_saving_name": "Nama tabungan: ",
        "saving_added": "Tabungan berhasil ditambahkan.",
        "prompt_budget_name": "Nama anggaran: ",
        "prompt_budget_category": "Kategori (opsional): ",
        "budget_added": "Item anggaran berhasil ditambahkan.",
        "no_budget_items": "Belum ada item anggaran.",
        "no_budget_items_edit": "Belum ada item anggaran untuk diedit.",
        "prompt_budget_index": "Pilih nomor item untuk update realisasi: ",
        "prompt_budget_realization": "Realisasi (Rp): ",
        "invalid_choice": "Pilihan tidak dikenal.",
        "realization_updated": "Realisasi berhasil diperbarui.",
        "realization_mode_instruction": "Pilih metode input realisasi:",
        "realization_mode_manual": "1. Masukkan nominal secara manual",
        "realization_mode_percentage": "2. Masukkan berdasarkan persentase (1-100%)",
        "realization_mode_full": "3. Tandai 100% tercapai",
        "prompt_percentage": "Persentase (1-100): ",
        "invalid_percentage": "Persentase harus antara 1 dan 100.",
        "percentage_unavailable": "Alokasi 0, gunakan input manual.",
        "copy_prev_missing": "Tidak ada data untuk {month_label}.",
        "copy_prev_confirm": "Salin data {month_label} ke periode saat ini? (y/n): ",
        "copy_prev_success": "Data dari {month_label} berhasil disalin.",
        "copy_prev_adjust_prompt": "Sesuaikan alokasi anggaran hasil salin? (y/n): ",
        "adjust_budget_header": "Sesuaikan alokasi anggaran",
        "adjust_skip_hint": "Tekan Enter untuk mempertahankan nilai lama.",
        "adjust_budget_prompt": "Alokasi baru untuk {name} (saat ini {allocation}): ",
        "adjust_invalid_amount": "Masukkan angka bulat tidak negatif atau kosong untuk melewati.",
        "adjust_complete": "{count} item diperbarui.",
        "delete_category_prompt": "Pilih kategori untuk dihapus:",
        "delete_income_option": "Sumber pendapatan",
        "delete_saving_option": "Tabungan",
        "delete_budget_option": "Item anggaran",
        "delete_prompt_choice": "Masukkan pilihan: ",
        "delete_no_items": "Tidak ada {category} untuk dihapus.",
        "delete_prompt_index": "Pilih nomor yang akan dihapus: ",
        "invalid_number": "Nomor tidak valid.",
        "delete_success": "{name} berhasil dihapus.",
        "paste_menu_title": "Tempel dari Spreadsheet",
        "paste_menu_option_income": "Tempel sumber pendapatan",
        "paste_menu_option_saving": "Tempel tabungan",
        "paste_menu_option_budget": "Tempel item anggaran",
        "paste_instructions": "Tempel data yang disalin dari spreadsheet. Tekan Enter pada baris kosong untuk selesai.",
        "paste_finish_hint": "Gunakan tab antar kolom agar sistem mudah membaca data.",
        "paste_no_rows": "Tidak ada data yang ditempel.",
        "paste_errors_header": "Baris berikut dilewati:",
        "paste_error": "Baris {line}: {reason}",
        "paste_reason_missing_name": "kolom nama kosong",
        "paste_reason_missing_amount": "kolom jumlah tidak ditemukan",
        "paste_reason_invalid_amount": "jumlah tidak dapat dibaca",
        "paste_reason_invalid_realization": "realisasi tidak dapat dibaca",
        "paste_preview_title": "Pratinjau data yang akan ditambahkan",
        "paste_confirm": "Tambahkan {count} {target}? (y/n): ",
        "paste_success": "{count} {target} berhasil ditambahkan.",
        "paste_no_valid_rows": "Tidak ada baris valid untuk ditambahkan.",
        "paste_target_income": "sumber pendapatan",
        "paste_target_saving": "tabungan",
        "paste_target_budget": "item anggaran",
        "paste_cancelled": "Penambahan dibatalkan.",
        "budgeting_menu_title": "Menu Anggaran",
        "budgeting_menu_add_income": "Tambah sumber pendapatan",
        "budgeting_menu_add_saving": "Tambah tabungan",
        "budgeting_menu_add_budget": "Tambah item anggaran",
        "budgeting_menu_edit_budget": "Edit realisasi anggaran",
        "budgeting_menu_delete_item": "Hapus item",
        "budgeting_menu_copy_prev": "Salin data bulan sebelumnya",
        "budgeting_menu_paste": "Tempel dari spreadsheet",
        "budgeting_menu_back": "Kembali ke menu utama",
        "prompt_choice": "Masukkan pilihan: ",
        "main_menu_title": "Menu Utama",
        "main_menu_dashboard": "Lihat Dashboard",
        "main_menu_budget": "Menu Anggaran",
        "main_menu_period": "Ubah Bulan/Tahun",
        "main_menu_language": "Ganti Bahasa",
        "main_menu_exit": "Keluar",
        "thank_you": "Terima kasih! Data disimpan.",
        "period_updated": "Periode berhasil diperbarui.",
        "prompt_year": "Tahun (contoh 2025): ",
        "prompt_month": "Bulan (contoh Mei): ",
        "language_menu_title": "Ganti Bahasa",
        "language_current": "Bahasa saat ini: {language}",
        "language_menu_prompt": "Pilih bahasa (nomor atau kode): ",
        "language_changed": "Bahasa diperbarui menjadi {language}.",
        "data_corrupt_reset": "File data rusak atau tidak bisa dibaca. Membuat ulang data default.",
        "list_budget_line": "{index}. {name}: Alokasi {allocation}, Realisasi {realization}",
        "default_name": "Tanpa Nama",
        "default_item_name": "Item",
        "auth_title": "Masuk atau Daftar",
        "prompt_email": "Masukkan email: ",
        "email_required": "Email tidak boleh kosong.",
        "user_not_found_signup": "Email belum terdaftar. Membuat akun baru...",
        "prompt_password": "Masukkan kata sandi: ",
        "prompt_password_confirm": "Konfirmasi kata sandi: ",
        "password_mismatch": "Kata sandi tidak cocok. Coba lagi.",
        "signup_success": "Akun baru berhasil dibuat untuk {email}.",
        "login_success": "Berhasil masuk sebagai {email}.",
        "invalid_credentials": "Email atau kata sandi salah.",
        "period_year_instruction": "Pilih tahun (masukkan nomor opsi):",
        "period_year_option_prev": "1. Tahun sebelumnya ({year})",
        "period_year_option_current": "2. Tahun berjalan ({year})",
        "period_year_option_next": "3. Tahun berikutnya ({year})",
        "period_month_instruction": "Pilih bulan dengan memasukkan angka 1-12:",
        "period_month_option": "{number}. {name}",
        "invalid_month": "Nomor bulan tidak valid.",
    },
    "en": {
        "language_name": "English (EN)",
        "dashboard_title": "Money Management Dashboard 💰",
        "year_label": "Year",
        "month_label": "Month",
        "monthly_report": "Monthly Report 📊",
        "stat_total_income": "Total Income",
        "stat_budgeted_expenses": "Budgeted Expenses",
        "stat_spending": "{month} Spending",
        "stat_savings": "{month} Savings",
        "expenses_list": "Expenses List",
        "column_name": "Name",
        "column_allocation": "Allocation 💰",
        "column_realization": "Realization 💵",
        "column_progress": "Budget Usage Progress",
        "column_percent_usage": "% Usage",
        "column_amount": "Amount",
        "column_category": "Category",
        "no_expenses": "No expenses yet.",
        "error_positive_int": "Enter a non-negative whole number.",
        "prompt_income_name": "Income source name: ",
        "prompt_amount": "Amount (Rp): ",
        "income_added": "Income source added successfully.",
        "prompt_saving_name": "Saving name: ",
        "saving_added": "Saving added successfully.",
        "prompt_budget_name": "Budget item name: ",
        "prompt_budget_category": "Category (optional): ",
        "budget_added": "Budget item added successfully.",
        "no_budget_items": "No budget items yet.",
        "no_budget_items_edit": "No budget items available to edit.",
        "prompt_budget_index": "Select item number to update realization: ",
        "prompt_budget_realization": "Realization (Rp): ",
        "invalid_choice": "Unknown choice.",
        "realization_updated": "Realization updated successfully.",
        "realization_mode_instruction": "Choose realization input method:",
        "realization_mode_manual": "1. Enter amount manually",
        "realization_mode_percentage": "2. Enter based on percentage (1-100%)",
        "realization_mode_full": "3. Mark as 100% complete",
        "prompt_percentage": "Percentage (1-100): ",
        "invalid_percentage": "Percentage must be between 1 and 100.",
        "percentage_unavailable": "Allocation is 0, please use manual input.",
        "copy_prev_missing": "No data available for {month_label}.",
        "copy_prev_confirm": "Copy {month_label} data into the current period? (y/n): ",
        "copy_prev_success": "Copied data from {month_label} successfully.",
        "copy_prev_adjust_prompt": "Adjust copied budget allocations? (y/n): ",
        "adjust_budget_header": "Adjust budget allocations",
        "adjust_skip_hint": "Press Enter to keep the current value.",
        "adjust_budget_prompt": "New allocation for {name} (currently {allocation}): ",
        "adjust_invalid_amount": "Enter a non-negative whole number or leave blank to skip.",
        "adjust_complete": "Updated {count} items.",
        "delete_category_prompt": "Choose a category to delete:",
        "delete_income_option": "Income sources",
        "delete_saving_option": "Savings",
        "delete_budget_option": "Budget items",
        "delete_prompt_choice": "Enter your choice: ",
        "delete_no_items": "No {category} to delete.",
        "delete_prompt_index": "Select the number to delete: ",
        "invalid_number": "Number is not valid.",
        "delete_success": "{name} deleted successfully.",
        "paste_menu_title": "Paste from Spreadsheet",
        "paste_menu_option_income": "Paste income sources",
        "paste_menu_option_saving": "Paste savings",
        "paste_menu_option_budget": "Paste budget items",
        "paste_instructions": "Paste data copied from your spreadsheet. Submit an empty line to finish.",
        "paste_finish_hint": "Use tab-separated columns so the parser can read them easily.",
        "paste_no_rows": "No data was pasted.",
        "paste_errors_header": "Skipped rows:",
        "paste_error": "Row {line}: {reason}",
        "paste_reason_missing_name": "missing name column",
        "paste_reason_missing_amount": "amount column not found",
        "paste_reason_invalid_amount": "amount could not be parsed",
        "paste_reason_invalid_realization": "realization could not be parsed",
        "paste_preview_title": "Preview of data to be added",
        "paste_confirm": "Add {count} {target}? (y/n): ",
        "paste_success": "Added {count} {target} successfully.",
        "paste_no_valid_rows": "No valid rows to add.",
        "paste_target_income": "income sources",
        "paste_target_saving": "savings",
        "paste_target_budget": "budget items",
        "paste_cancelled": "Paste cancelled.",
        "budgeting_menu_title": "Budgeting Menu",
        "budgeting_menu_add_income": "Add income source",
        "budgeting_menu_add_saving": "Add saving",
        "budgeting_menu_add_budget": "Add budget item",
        "budgeting_menu_edit_budget": "Edit budget realization",
        "budgeting_menu_delete_item": "Delete item",
        "budgeting_menu_copy_prev": "Copy previous month's data",
        "budgeting_menu_paste": "Paste from spreadsheet",
        "budgeting_menu_back": "Back to main menu",
        "prompt_choice": "Enter your choice: ",
        "main_menu_title": "Main Menu",
        "main_menu_dashboard": "View Dashboard",
        "main_menu_budget": "Budgeting Menu",
        "main_menu_period": "Change Month/Year",
        "main_menu_language": "Change Language",
        "main_menu_exit": "Exit",
        "thank_you": "Thank you! Data saved.",
        "period_updated": "Period updated successfully.",
        "prompt_year": "Year (e.g. 2025): ",
        "prompt_month": "Month (e.g. May): ",
        "language_menu_title": "Change Language",
        "language_current": "Current language: {language}",
        "language_menu_prompt": "Select a language (number or code): ",
        "language_changed": "Language updated to {language}.",
        "data_corrupt_reset": "Data file corrupt or unreadable. Recreating with defaults.",
        "list_budget_line": "{index}. {name}: Allocation {allocation}, Realization {realization}",
        "default_name": "Unnamed",
        "default_item_name": "Item",
        "auth_title": "Log In or Sign Up",
        "prompt_email": "Enter email: ",
        "email_required": "Email cannot be empty.",
        "user_not_found_signup": "Email is not registered. Creating a new account...",
        "prompt_password": "Enter password: ",
        "prompt_password_confirm": "Confirm password: ",
        "password_mismatch": "Passwords do not match. Try again.",
        "signup_success": "New account created for {email}.",
        "login_success": "Logged in as {email}.",
        "invalid_credentials": "Email or password is incorrect.",
        "period_year_instruction": "Select a year option (enter number):",
        "period_year_option_prev": "1. Previous year ({year})",
        "period_year_option_current": "2. Current year ({year})",
        "period_year_option_next": "3. Next year ({year})",
        "period_month_instruction": "Choose a month by entering 1-12:",
        "period_month_option": "{number}. {name}",
        "invalid_month": "Month number is not valid.",
    },
}

MONTH_NAMES = {
    "id": [
        "Januari",
        "Februari",
        "Maret",
        "April",
        "Mei",
        "Juni",
        "Juli",
        "Agustus",
        "September",
        "Oktober",
        "November",
        "Desember",
    ],
    "en": [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ],
}

MONTH_ALIASES: Dict[str, int] = {}
for names in MONTH_NAMES.values():
    for index, label in enumerate(names, 1):
        MONTH_ALIASES[label.lower()] = index
for index in range(1, 13):
    MONTH_ALIASES[str(index)] = index


@dataclass
class Session:
    data: Dict[str, Any]
    email: str
    profile: Dict[str, Any]
    key: bytes


def format_currency(amount: int) -> str:
    return f"Rp{amount:,}" if amount >= 0 else f"-Rp{abs(amount):,}"


def get_language(profile: Dict[str, Any]) -> str:
    language = profile.get("language", "id")
    if language not in LANGUAGE_STRINGS:
        profile["language"] = "id"
        return "id"
    return language


def tr(profile: Dict[str, Any], key: str, **kwargs: Any) -> str:
    language = get_language(profile)
    template = LANGUAGE_STRINGS.get(language, LANGUAGE_STRINGS["id"]).get(key)
    if template is None:
        template = LANGUAGE_STRINGS["en"].get(key, key)
    return template.format(**kwargs)


def get_month_name(profile: Dict[str, Any], month_index: int | None = None) -> str:
    language = get_language(profile)
    month_value = profile.get("current_month", 5) if month_index is None else month_index
    if isinstance(month_value, str):
        month_value = MONTH_ALIASES.get(month_value.lower(), 5)
    if not isinstance(month_value, int):
        month_value = 5
    if 1 <= month_value <= 12:
        return MONTH_NAMES.get(language, MONTH_NAMES["id"])[month_value - 1]
    return MONTH_NAMES.get(language, MONTH_NAMES["id"])[4]


def build_progress_bar(percentage: float, width: int = 20) -> str:
    filled = int(min(percentage, 100) / 100 * width)
    remaining = width - filled
    bar = "#" * filled + "-" * remaining
    color = "bright_magenta" if percentage <= 100 else "red"
    return f"[{color}]{bar}[/]"


def month_key(year: int, month: int) -> str:
    return f"{year:04d}-{month:02d}"


def ensure_month_defaults(month_data: Dict[str, Any]) -> None:
    month_data.setdefault("income_sources", [])
    month_data.setdefault("saving_list", [])
    month_data.setdefault("budgeting_list", [])


def normalize_month_value(value: Any) -> int:
    if isinstance(value, int) and 1 <= value <= 12:
        return value
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered.isdigit():
            number = int(lowered)
            if 1 <= number <= 12:
                return number
        if lowered in MONTH_ALIASES:
            return MONTH_ALIASES[lowered]
    return 5


def get_month_data(profile: Dict[str, Any], year: int, month: int) -> Dict[str, Any]:
    months = profile.setdefault("months", {})
    key = month_key(year, month)
    month_data = months.setdefault(key, {})
    ensure_month_defaults(month_data)
    return month_data


def get_current_month_data(profile: Dict[str, Any]) -> Dict[str, Any]:
    year = profile.get("current_year", 2025)
    month = normalize_month_value(profile.get("current_month", 5))
    profile["current_month"] = month
    return get_month_data(profile, year, month)


def sync_current_month_references(profile: Dict[str, Any]) -> Dict[str, Any]:
    month_data = get_current_month_data(profile)
    profile["income_sources"] = month_data["income_sources"]
    profile["saving_list"] = month_data["saving_list"]
    profile["budgeting_list"] = month_data["budgeting_list"]
    return month_data


def get_next_month(year: int, month: int) -> Tuple[int, int]:
    month = normalize_month_value(month)
    if month >= 12:
        return year + 1, 1
    return year, month + 1


def get_previous_month(year: int, month: int) -> Tuple[int, int]:
    month = normalize_month_value(month)
    if month <= 1:
        return year - 1, 12
    return year, month - 1


def format_month_label(profile: Dict[str, Any], year: int, month: int) -> str:
    month = normalize_month_value(month)
    language = get_language(profile)
    month_names = MONTH_NAMES.get(language, MONTH_NAMES["id"])
    name = month_names[month - 1]
    return f"{name} {year}"


def default_profile() -> Dict[str, Any]:
    year = 2025
    month = 5
    key = month_key(year, month)
    month_payload = {
        "income_sources": [
            {"name": "Gaji Bulanan", "amount": 13_923_161},
            {"name": "Bonus Proyek", "amount": 2_000_000},
        ],
        "saving_list": [
            {"name": "Dana Darurat", "amount": 2_500_000},
            {"name": "Tabungan Pendidikan", "amount": 1_000_000},
        ],
        "budgeting_list": [
            {
                "name": "Bantuan Keluarga",
                "allocation": 500_000,
                "realization": 250_000,
                "category": "Family Aid",
            },
            {
                "name": "Layanan Rumah",
                "allocation": 250_000,
                "realization": 125_000,
                "category": "House Services",
            },
            {
                "name": "Pajak Kendaraan",
                "allocation": 180_000,
                "realization": 0,
                "category": "Pajak",
            },
            {
                "name": "Zakat Wajib",
                "allocation": 325_000,
                "realization": 325_000,
                "category": "Zakat",
            },
        ],
    }
    profile = {
        "months": {key: month_payload},
        "current_year": year,
        "current_month": month,
        "language": "id",
    }
    sync_current_month_references(profile)
    return profile


def default_data() -> Dict[str, Any]:
    return {
        "users": [],
        "profiles": {},
        "pending_profile": default_profile(),
        "default_language": "id",
    }


def ensure_profile_defaults(profile: Dict[str, Any]) -> None:
    profile.setdefault("current_year", 2025)
    profile["current_month"] = normalize_month_value(profile.get("current_month", 5))
    language = profile.get("language", "id")
    if language not in LANGUAGE_STRINGS:
        profile["language"] = "id"

    months = profile.setdefault("months", {})
    if any(key in profile for key in ("income_sources", "saving_list", "budgeting_list")):
        key = month_key(profile["current_year"], profile["current_month"])
        month_entry = months.setdefault(key, {})
        ensure_month_defaults(month_entry)
        if "income_sources" in profile:
            if not month_entry["income_sources"]:
                month_entry["income_sources"] = profile["income_sources"]
            profile.pop("income_sources", None)
        if "saving_list" in profile:
            if not month_entry["saving_list"]:
                month_entry["saving_list"] = profile["saving_list"]
            profile.pop("saving_list", None)
        if "budgeting_list" in profile:
            if not month_entry["budgeting_list"]:
                month_entry["budgeting_list"] = profile["budgeting_list"]
            profile.pop("budgeting_list", None)

    sync_current_month_references(profile)


def migrate_legacy_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    if "users" in raw and "profiles" in raw:
        raw.setdefault("pending_profile", None)
        raw.setdefault("default_language", "id")
        return raw

    year = raw.get("current_year", 2025)
    month = normalize_month_value(raw.get("current_month", 5))
    key = month_key(year, month)
    month_payload = {
        "income_sources": raw.get("income_sources", []),
        "saving_list": raw.get("saving_list", []),
        "budgeting_list": raw.get("budgeting_list", []),
    }

    profile = {
        "months": {key: month_payload},
        "current_year": year,
        "current_month": month,
        "language": raw.get("language", raw.get("default_language", "id")),
    }
    ensure_profile_defaults(profile)
    data = default_data()
    data["pending_profile"] = profile
    return data


def normalize_data(data: Dict[str, Any]) -> None:
    if not isinstance(data.get("users"), list):
        data["users"] = []
    if not isinstance(data.get("profiles"), dict):
        data["profiles"] = {}
    pending_profile = data.get("pending_profile")
    if isinstance(pending_profile, dict):
        ensure_profile_defaults(pending_profile)
    else:
        data["pending_profile"] = None
    default_language = data.get("default_language", "id")
    if default_language not in LANGUAGE_STRINGS:
        data["default_language"] = "id"
    for email, payload in list(data["profiles"].items()):
        if not isinstance(payload, dict):
            data["profiles"].pop(email)
            continue
        if "ciphertext" not in payload:
            ensure_profile_defaults(payload)


def save_data(data: Dict[str, Any]) -> None:
    with DATA_FILE.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)


def load_data() -> Dict[str, Any]:
    if not DATA_FILE.exists():
        data = default_data()
        save_data(data)
        return data

    try:
        with DATA_FILE.open("r", encoding="utf-8") as handle:
            raw = json.load(handle)
    except (json.JSONDecodeError, OSError):
        console.print("[red]Data file corrupt or unreadable. Recreating with defaults.[/]")
        data = default_data()
        save_data(data)
        return data

    data = migrate_legacy_data(raw)
    normalize_data(data)
    save_data(data)
    return data


def calculate_totals(profile: Dict[str, Any]) -> Dict[str, int]:
    month_data = sync_current_month_references(profile)
    total_income = sum(item.get("amount", 0) for item in month_data["income_sources"])
    total_budgeted = sum(item.get("allocation", 0) for item in month_data["budgeting_list"])
    total_spending = sum(item.get("realization", 0) for item in month_data["budgeting_list"])
    savings = total_income - total_spending
    return {
        "total_income": total_income,
        "total_budgeted_expenses": total_budgeted,
        "total_spending": total_spending,
        "savings": savings,
    }


def display_header(profile: Dict[str, Any]) -> None:
    year = profile.get("current_year", 2025)
    month_name = get_month_name(profile)
    title = Text(tr(profile, "dashboard_title"), style="bold white")
    meta = Text.assemble(
        (f"{tr(profile, 'year_label')}: {year}", "bold white"),
        ("\n", ""),
        (f"{tr(profile, 'month_label')}: {month_name}", "bold white"),
    )
    header = Table.grid(expand=True)
    header.add_column(justify="left")
    header.add_column(justify="right")
    header.add_row(title, meta)
    console.print(Panel(header, border_style="green"))
    console.print(Panel(tr(profile, "monthly_report"), border_style="green"))


def display_stats(profile: Dict[str, Any], aggregates: Dict[str, int]) -> None:
    month_name = get_month_name(profile)
    stats_table = Table.grid(expand=True)
    stats_table.add_column()
    stats_table.add_column()
    stats_table.add_column()
    stats_table.add_column()

    panels = [
        (tr(profile, "stat_total_income"), format_currency(aggregates["total_income"])),
        (
            tr(profile, "stat_budgeted_expenses"),
            format_currency(aggregates["total_budgeted_expenses"]),
        ),
        (
            tr(profile, "stat_spending", month=month_name),
            format_currency(aggregates["total_spending"]),
        ),
        (
            tr(profile, "stat_savings", month=month_name),
            format_currency(aggregates["savings"]),
        ),
    ]

    stat_panels: List[Panel] = []
    for title, value in panels:
        stat_panels.append(
            Panel(
                Text.assemble((title, "bold white"), ("\n", ""), (value, "bold green")),
                border_style="green",
            )
        )

    stats_table.add_row(*stat_panels)
    console.print(stats_table)


def display_expenses(profile: Dict[str, Any], items: List[Dict[str, Any]]) -> None:
    expenses_table = Table(
        title=tr(profile, "expenses_list"),
        header_style="bold white",
        show_lines=False,
        expand=True,
    )
    expenses_table.add_column(tr(profile, "column_name"), style="white")
    expenses_table.add_column(tr(profile, "column_allocation"), style="green", justify="right")
    expenses_table.add_column(tr(profile, "column_realization"), style="cyan", justify="right")
    expenses_table.add_column(tr(profile, "column_progress"), style="white")
    expenses_table.add_column(tr(profile, "column_percent_usage"), style="yellow", justify="right")

    if not items:
        expenses_table.add_row(tr(profile, "no_expenses"), "-", "-", "-", "-")
    else:
        for item in sorted(items, key=lambda entry: entry.get("name", "")):
            allocation = int(item.get("allocation", 0))
            realization = int(item.get("realization", 0))
            percent = (realization / allocation * 100) if allocation else 0
            progress_bar = build_progress_bar(percent if allocation else 0)
            percent_text = Text(f"{percent:.2f}%", style="yellow")
            if percent > 100:
                percent_text.stylize("red")
            expenses_table.add_row(
                item.get("name", "-"),
                format_currency(allocation),
                format_currency(realization),
                progress_bar,
                percent_text,
            )

    console.print(expenses_table)


def display_dashboard(profile: Dict[str, Any]) -> None:
    console.clear()
    aggregates = calculate_totals(profile)
    display_header(profile)
    display_stats(profile, aggregates)
    display_expenses(profile, profile["budgeting_list"])


def prompt_positive_int(message: str, error_message: str) -> int:
    while True:
        raw = input(message)
        try:
            value = int(raw)
            if value < 0:
                raise ValueError
            return value
        except ValueError:
            console.print(f"[red]{error_message}[/]")


def parse_amount_value(raw: str) -> int | None:
    cleaned = raw.strip()
    if not cleaned:
        return None
    lowered = cleaned.lower()
    if "-" in lowered or lowered.startswith("("):
        return None
    digits = "".join(ch for ch in lowered if ch.isdigit())
    if not digits:
        return None
    try:
        return int(digits)
    except ValueError:
        return None


def merge_amount_tokens(first: str, rest: List[str]) -> Tuple[str, List[str]]:
    value = first
    remaining = list(rest)
    if parse_amount_value(value) is None:
        return value, remaining
    while remaining:
        fragment = remaining[0].strip()
        if not fragment or not fragment.isdigit() or len(fragment) > 3:
            break
        candidate = value + fragment
        if parse_amount_value(candidate) is None:
            break
        value = candidate
        remaining.pop(0)
    return value, remaining


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def verify_password(stored_hash: str, password: str) -> bool:
    return stored_hash == hash_password(password)


def generate_salt() -> bytes:
    return os.urandom(16)


def derive_key(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=32)


def keystream_bytes(key: bytes, nonce: bytes, length: int) -> bytes:
    blocks: List[bytes] = []
    counter = 0
    while len(b"".join(blocks)) < length:
        counter_bytes = counter.to_bytes(4, "big")
        block = hashlib.sha256(key + nonce + counter_bytes).digest()
        blocks.append(block)
        counter += 1
    return b"".join(blocks)[:length]


def encrypt_profile_payload(key: bytes, profile: Dict[str, Any]) -> Dict[str, str]:
    plaintext = json.dumps(profile, separators=(",", ":")).encode("utf-8")
    nonce = os.urandom(16)
    keystream = keystream_bytes(key, nonce, len(plaintext))
    ciphertext = bytes(p ^ k for p, k in zip(plaintext, keystream))
    tag = hmac.new(key, nonce + ciphertext, hashlib.sha256).digest()
    return {
        "version": 1,
        "nonce": base64.b64encode(nonce).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "tag": base64.b64encode(tag).decode("utf-8"),
    }


def decrypt_profile_payload(key: bytes, payload: Dict[str, Any]) -> Dict[str, Any]:
    if "ciphertext" not in payload:
        ensure_profile_defaults(payload)
        return payload

    try:
        nonce = base64.b64decode(payload["nonce"])
        ciphertext = base64.b64decode(payload["ciphertext"])
        tag = base64.b64decode(payload["tag"])
    except (KeyError, ValueError, TypeError) as error:
        raise ValueError("Invalid encrypted payload") from error

    expected_tag = hmac.new(key, nonce + ciphertext, hashlib.sha256).digest()
    if not hmac.compare_digest(expected_tag, tag):
        raise ValueError("Integrity check failed")

    keystream = keystream_bytes(key, nonce, len(ciphertext))
    plaintext = bytes(c ^ k for c, k in zip(ciphertext, keystream))
    profile = json.loads(plaintext.decode("utf-8"))
    ensure_profile_defaults(profile)
    return profile


def get_user_entry(data: Dict[str, Any], email: str) -> Dict[str, Any]:
    for entry in data["users"]:
        if entry.get("email") == email:
            return entry
    raise KeyError(email)


def persist_session(session: Session) -> None:
    ensure_profile_defaults(session.profile)
    encrypted = encrypt_profile_payload(session.key, session.profile)
    session.data.setdefault("profiles", {})[session.email] = encrypted
    save_data(session.data)


def add_income(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)
    name = input(tr(profile, "prompt_income_name")).strip() or tr(profile, "default_name")
    amount = prompt_positive_int(tr(profile, "prompt_amount"), tr(profile, "error_positive_int"))
    month_data["income_sources"].append({"name": name, "amount": amount})
    persist_session(session)
    console.print(f"[green]{tr(profile, 'income_added')}[/]")


def add_saving(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)
    name = input(tr(profile, "prompt_saving_name")).strip() or tr(profile, "default_name")
    amount = prompt_positive_int(tr(profile, "prompt_amount"), tr(profile, "error_positive_int"))
    month_data["saving_list"].append({"name": name, "amount": amount})
    persist_session(session)
    console.print(f"[green]{tr(profile, 'saving_added')}[/]")


def add_budget_item(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)
    name = input(tr(profile, "prompt_budget_name")).strip() or tr(profile, "default_name")
    allocation = prompt_positive_int(tr(profile, "prompt_amount"), tr(profile, "error_positive_int"))
    category = input(tr(profile, "prompt_budget_category")).strip()
    month_data["budgeting_list"].append(
        {
            "name": name,
            "allocation": allocation,
            "realization": 0,
            "category": category,
        }
    )
    persist_session(session)
    console.print(f"[green]{tr(profile, 'budget_added')}[/]")


def capture_pasted_lines(profile: Dict[str, Any]) -> List[str]:
    console.print()
    console.print(tr(profile, "paste_instructions"))
    console.print(tr(profile, "paste_finish_hint"))
    lines: List[str] = []
    while True:
        try:
            line = input("> ")
        except EOFError:
            break
        if not line.strip():
            break
        lines.append(line)
    return lines


def parse_pasted_rows(
    profile: Dict[str, Any], lines: List[str], data_type: str
) -> Tuple[List[Dict[str, Any]], List[str]]:
    items: List[Dict[str, Any]] = []
    errors: List[str] = []

    for idx, raw_line in enumerate(lines, 1):
        if "\t" in raw_line:
            columns = [part.strip() for part in raw_line.split("\t")]
        elif ";" in raw_line:
            columns = [part.strip() for part in raw_line.split(";")]
        else:
            columns = [part.strip() for part in raw_line.split(",")]

        if data_type in {"income", "saving"}:
            if len(columns) < 2:
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_missing_amount"))
                )
                continue
            name = columns[0].strip() or tr(profile, "default_name")
            amount_text = columns[1]
            if len(columns) > 2:
                amount_text += "".join(columns[2:])
            if not amount_text.strip():
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_missing_amount"))
                )
                continue
            amount = parse_amount_value(amount_text)
            if amount is None:
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_invalid_amount"))
                )
                continue
            items.append({"name": name, "amount": amount})
        else:
            if not columns or len(columns) < 2:
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_missing_amount"))
                )
                continue
            name = columns[0].strip()
            if not name:
                name = tr(profile, "default_name")

            allocation_text, remainder = merge_amount_tokens(columns[1], columns[2:])
            allocation = parse_amount_value(allocation_text)
            if allocation is None:
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_invalid_amount"))
                )
                continue

            category = ""
            realization_text = ""

            if remainder:
                first_remainder = remainder[0]
                if parse_amount_value(first_remainder) is not None:
                    realization_text, leftover = merge_amount_tokens(first_remainder, remainder[1:])
                    if leftover:
                        realization_text = " ".join([realization_text] + leftover).strip()
                else:
                    category = first_remainder.strip()
                    leftover_columns = remainder[1:]
                    if leftover_columns:
                        realization_candidate = leftover_columns[0]
                        realization_text, leftover = merge_amount_tokens(
                            realization_candidate, leftover_columns[1:]
                        )
                        if leftover:
                            realization_text = " ".join([realization_text] + leftover).strip()

            category = category.strip()
            realization_text = realization_text.strip()
            if realization_text and parse_amount_value(realization_text) is None:
                if category:
                    category = f"{category} {realization_text}".strip()
                    realization_text = ""
                else:
                    category = realization_text
                    realization_text = ""

            if realization_text and parse_amount_value(realization_text) is None:
                errors.append(
                    tr(profile, "paste_error", line=idx, reason=tr(profile, "paste_reason_invalid_realization"))
                )
                continue

            realization = parse_amount_value(realization_text) if realization_text else 0
            items.append(
                {
                    "name": name,
                    "allocation": allocation,
                    "realization": realization or 0,
                    "category": category,
                }
            )

    return items, errors


def display_paste_preview(profile: Dict[str, Any], data_type: str, items: List[Dict[str, Any]]) -> None:
    table = Table(title=tr(profile, "paste_preview_title"), header_style="bold white", expand=True)
    table.add_column(tr(profile, "column_name"), style="white")

    if data_type == "budget":
        table.add_column(tr(profile, "column_category"), style="white")
        table.add_column(tr(profile, "column_allocation"), style="green", justify="right")
        table.add_column(tr(profile, "column_realization"), style="cyan", justify="right")
        for item in items:
            table.add_row(
                item.get("name", tr(profile, "default_item_name")),
                item.get("category", ""),
                format_currency(int(item.get("allocation", 0))),
                format_currency(int(item.get("realization", 0))),
            )
    else:
        table.add_column(tr(profile, "column_amount"), style="green", justify="right")
        for item in items:
            table.add_row(
                item.get("name", tr(profile, "default_name")),
                format_currency(int(item.get("amount", 0))),
            )

    console.print(table)


def paste_from_spreadsheet(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)

    console.print(f"\n[bold cyan]{tr(profile, 'paste_menu_title')}[/]")
    console.print(f"1. {tr(profile, 'paste_menu_option_income')}")
    console.print(f"2. {tr(profile, 'paste_menu_option_saving')}")
    console.print(f"3. {tr(profile, 'paste_menu_option_budget')}")

    choice = input(tr(profile, "prompt_choice")).strip()
    option_map = {
        "1": ("income", tr(profile, "paste_target_income")),
        "2": ("saving", tr(profile, "paste_target_saving")),
        "3": ("budget", tr(profile, "paste_target_budget")),
    }

    if choice not in option_map:
        console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")
        return

    data_type, target_label = option_map[choice]
    lines = capture_pasted_lines(profile)
    if not lines:
        console.print(f"[yellow]{tr(profile, 'paste_no_rows')}[/]")
        return

    items, errors = parse_pasted_rows(profile, lines, data_type)

    if errors:
        console.print(f"[yellow]{tr(profile, 'paste_errors_header')}[/]")
        for message in errors:
            console.print(f"[yellow]- {message}[/]")

    if not items:
        console.print(f"[yellow]{tr(profile, 'paste_no_valid_rows')}[/]")
        return

    display_paste_preview(profile, data_type, items)
    confirm = input(tr(profile, "paste_confirm", count=len(items), target=target_label)).strip().lower()
    if confirm not in {"y", "yes", "ya"}:
        console.print(f"[yellow]{tr(profile, 'paste_cancelled')}[/]")
        return

    if data_type == "income":
        month_data["income_sources"].extend(items)
    elif data_type == "saving":
        month_data["saving_list"].extend(items)
    else:
        month_data["budgeting_list"].extend(items)

    persist_session(session)
    console.print(f"[green]{tr(profile, 'paste_success', count=len(items), target=target_label)}[/]")


def list_budget_items(profile: Dict[str, Any]) -> None:
    month_data = sync_current_month_references(profile)
    if not month_data["budgeting_list"]:
        console.print(f"[yellow]{tr(profile, 'no_budget_items')}[/]")
        return
    for idx, item in enumerate(month_data["budgeting_list"], 1):
        line = tr(
            profile,
            "list_budget_line",
            index=idx,
            name=item.get("name", tr(profile, "default_item_name")),
            allocation=format_currency(item.get("allocation", 0)),
            realization=format_currency(item.get("realization", 0)),
        )
        console.print(line)


def edit_realization(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)
    if not month_data["budgeting_list"]:
        console.print(f"[yellow]{tr(profile, 'no_budget_items_edit')}[/]")
        return
    list_budget_items(profile)
    index = prompt_positive_int(tr(profile, "prompt_budget_index"), tr(profile, "error_positive_int"))
    if index == 0 or index > len(month_data["budgeting_list"]):
        console.print(f"[red]{tr(profile, 'invalid_number')}[/]")
        return
    item = month_data["budgeting_list"][index - 1]
    allocation = int(item.get("allocation", 0))

    console.print(f"\n{tr(profile, 'realization_mode_instruction')}")
    console.print(tr(profile, "realization_mode_manual"))
    console.print(tr(profile, "realization_mode_percentage"))
    console.print(tr(profile, "realization_mode_full"))

    mode = input(tr(profile, "prompt_choice")).strip()

    if mode == "1":
        realization = prompt_positive_int(
            tr(profile, "prompt_budget_realization"), tr(profile, "error_positive_int")
        )
    elif mode == "2":
        if allocation <= 0:
            console.print(f"[red]{tr(profile, 'percentage_unavailable')}[/]")
            return
        percentage = prompt_positive_int(
            tr(profile, "prompt_percentage"), tr(profile, "invalid_percentage")
        )
        if not 1 <= percentage <= 100:
            console.print(f"[red]{tr(profile, 'invalid_percentage')}[/]")
            return
        realization = int(round(allocation * percentage / 100))
    elif mode == "3":
        realization = allocation
    else:
        console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")
        return

    month_data["budgeting_list"][index - 1]["realization"] = realization
    persist_session(session)
    console.print(f"[green]{tr(profile, 'realization_updated')}[/]")


def delete_item(session: Session) -> None:
    profile = session.profile
    month_data = sync_current_month_references(profile)
    console.print(f"\n{tr(profile, 'delete_category_prompt')}")
    console.print(f"1. {tr(profile, 'delete_income_option')}")
    console.print(f"2. {tr(profile, 'delete_saving_option')}")
    console.print(f"3. {tr(profile, 'delete_budget_option')}")
    choice = input(tr(profile, "delete_prompt_choice")).strip().lower()

    collections = {
        "1": (month_data["income_sources"], "delete_income_option"),
        "2": (month_data["saving_list"], "delete_saving_option"),
        "3": (month_data["budgeting_list"], "delete_budget_option"),
        "income_sources": (month_data["income_sources"], "delete_income_option"),
        "savings": (month_data["saving_list"], "delete_saving_option"),
        "budget": (month_data["budgeting_list"], "delete_budget_option"),
    }

    if choice not in collections:
        console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")
        return

    collection, label_key = collections[choice]
    category_label = tr(profile, label_key)
    if not collection:
        console.print(f"[yellow]{tr(profile, 'delete_no_items', category=category_label.lower())}[/]")
        return

    for idx, item in enumerate(collection, 1):
        name = item.get("name", tr(profile, "default_item_name"))
        if collection is month_data["budgeting_list"]:
            detail = format_currency(item.get("allocation", 0))
        else:
            detail = format_currency(item.get("amount", 0))
        console.print(f"{idx}. {name} ({detail})")

    index = prompt_positive_int(tr(profile, "delete_prompt_index"), tr(profile, "error_positive_int"))
    if index == 0 or index > len(collection):
        console.print(f"[red]{tr(profile, 'invalid_number')}[/]")
        return

    removed = collection.pop(index - 1)
    persist_session(session)
    removed_name = removed.get("name", tr(profile, "default_item_name"))
    console.print(f"[green]{tr(profile, 'delete_success', name=removed_name)}[/]")


def budgeting_menu(session: Session) -> None:
    profile = session.profile
    while True:
        console.print(f"\n[bold cyan]{tr(profile, 'budgeting_menu_title')}[/]")
        console.print(f"1. {tr(profile, 'budgeting_menu_add_income')}")
        console.print(f"2. {tr(profile, 'budgeting_menu_add_saving')}")
        console.print(f"3. {tr(profile, 'budgeting_menu_add_budget')}")
        console.print(f"4. {tr(profile, 'budgeting_menu_edit_budget')}")
        console.print(f"5. {tr(profile, 'budgeting_menu_delete_item')}")
        console.print(f"6. {tr(profile, 'budgeting_menu_copy_prev')}")
        console.print(f"7. {tr(profile, 'budgeting_menu_paste')}")
        console.print(f"8. {tr(profile, 'budgeting_menu_back')}")
        choice = input(tr(profile, "prompt_choice")).strip()

        if choice == "1":
            add_income(session)
        elif choice == "2":
            add_saving(session)
        elif choice == "3":
            add_budget_item(session)
        elif choice == "4":
            edit_realization(session)
        elif choice == "5":
            delete_item(session)
        elif choice == "6":
            copy_previous_month(session)
        elif choice == "7":
            paste_from_spreadsheet(session)
        elif choice == "8":
            break
        else:
            console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")


def adjust_copied_budget_allocations(session: Session, month_data: Dict[str, Any]) -> None:
    profile = session.profile
    console.print(f"\n[bold cyan]{tr(profile, 'adjust_budget_header')}[/]")
    console.print(tr(profile, "adjust_skip_hint"))

    updated = 0
    for item in month_data.get("budgeting_list", []):
        name = item.get("name", tr(profile, "default_item_name"))
        current_allocation = format_currency(int(item.get("allocation", 0)))
        while True:
            raw = input(tr(profile, "adjust_budget_prompt", name=name, allocation=current_allocation)).strip()
            if not raw:
                break
            amount = parse_amount_value(raw)
            if amount is None:
                console.print(f"[red]{tr(profile, 'adjust_invalid_amount')}[/]")
                continue
            item["allocation"] = amount
            updated += 1
            break

    if updated:
        console.print(f"[green]{tr(profile, 'adjust_complete', count=updated)}[/]")


def copy_previous_month(session: Session) -> None:
    profile = session.profile
    current_year = profile.get("current_year", 2025)
    current_month = normalize_month_value(profile.get("current_month", 5))
    prev_year, prev_month = get_previous_month(current_year, current_month)
    prev_label = format_month_label(profile, prev_year, prev_month)

    months = profile.setdefault("months", {})
    prev_key = month_key(prev_year, prev_month)
    if prev_key not in months:
        console.print(f"[yellow]{tr(profile, 'copy_prev_missing', month_label=prev_label)}[/]")
        return

    prev_data = get_month_data(profile, prev_year, prev_month)
    if not any(prev_data[field] for field in ("income_sources", "saving_list", "budgeting_list")):
        console.print(f"[yellow]{tr(profile, 'copy_prev_missing', month_label=prev_label)}[/]")
        return

    confirmation = input(tr(profile, "copy_prev_confirm", month_label=prev_label)).strip().lower()
    if confirmation not in {"y", "ya", "yes"}:
        return

    current_data = get_month_data(profile, current_year, current_month)
    current_data["income_sources"] = deepcopy(prev_data["income_sources"])
    current_data["saving_list"] = deepcopy(prev_data["saving_list"])
    current_data["budgeting_list"] = deepcopy(prev_data["budgeting_list"])

    sync_current_month_references(profile)
    if current_data["budgeting_list"]:
        adjust_choice = input(tr(profile, "copy_prev_adjust_prompt")).strip().lower()
        if adjust_choice in {"y", "ya", "yes"}:
            adjust_copied_budget_allocations(session, current_data)

    persist_session(session)
    console.print(f"[green]{tr(profile, 'copy_prev_success', month_label=prev_label)}[/]")


def change_period(session: Session) -> None:
    profile = session.profile
    current_year = profile.get("current_year", 2025)
    year_options = {
        "1": current_year - 1,
        "2": current_year,
        "3": current_year + 1,
    }

    console.print(f"\n{tr(profile, 'period_year_instruction')}")
    console.print(tr(profile, "period_year_option_prev", year=year_options["1"]))
    console.print(tr(profile, "period_year_option_current", year=year_options["2"]))
    console.print(tr(profile, "period_year_option_next", year=year_options["3"]))

    year_input = input(tr(profile, "prompt_choice")).strip()
    if year_input in year_options:
        selected_year = year_options[year_input]
    else:
        try:
            selected_year = int(year_input)
        except ValueError:
            console.print(f"[red]{tr(profile, 'invalid_number')}[/]")
            return

    console.print(f"\n{tr(profile, 'period_month_instruction')}")
    language = get_language(profile)
    month_names = MONTH_NAMES.get(language, MONTH_NAMES["id"])
    for idx, name in enumerate(month_names, 1):
        console.print(tr(profile, "period_month_option", number=idx, name=name))

    month_input = input(tr(profile, "prompt_choice")).strip()
    try:
        selected_month = int(month_input)
    except ValueError:
        console.print(f"[red]{tr(profile, 'invalid_month')}[/]")
        return

    if not 1 <= selected_month <= 12:
        console.print(f"[red]{tr(profile, 'invalid_month')}[/]")
        return

    profile["current_year"] = selected_year
    profile["current_month"] = selected_month
    sync_current_month_references(profile)
    persist_session(session)
    console.print(f"[green]{tr(profile, 'period_updated')}[/]")


def change_language(session: Session) -> None:
    profile = session.profile
    console.print(f"\n[bold cyan]{tr(profile, 'language_menu_title')}[/]")
    current_code = get_language(profile)
    console.print(
        tr(
            profile,
            "language_current",
            language=LANGUAGE_STRINGS[current_code]["language_name"],
        )
    )
    codes = list(LANGUAGE_STRINGS.keys())
    for idx, code in enumerate(codes, 1):
        console.print(f"{idx}. {LANGUAGE_STRINGS[code]['language_name']} [{code}]")

    selection = input(tr(profile, "language_menu_prompt")).strip().lower()
    if selection in LANGUAGE_STRINGS:
        chosen_code = selection
    else:
        try:
            index = int(selection)
            if index < 1 or index > len(codes):
                raise ValueError
            chosen_code = codes[index - 1]
        except ValueError:
            console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")
            return

    profile["language"] = chosen_code
    session.data["default_language"] = chosen_code
    persist_session(session)
    console.print(
        f"[green]{tr(profile, 'language_changed', language=LANGUAGE_STRINGS[chosen_code]['language_name'])}[/]"
    )
    display_dashboard(profile)


def add_or_update_salt(user: Dict[str, Any]) -> bytes:
    salt_b64 = user.get("salt")
    if salt_b64:
        try:
            return base64.b64decode(salt_b64)
        except (ValueError, TypeError):
            pass
    salt = generate_salt()
    user["salt"] = base64.b64encode(salt).decode("utf-8")
    return salt


def authenticate_user(data: Dict[str, Any]) -> Session:
    while True:
        language_code = data.get("default_language", "id")
        strings = LANGUAGE_STRINGS.get(language_code, LANGUAGE_STRINGS["id"])

        console.print(f"\n[bold cyan]{strings['auth_title']}[/]")
        email = input(strings["prompt_email"]).strip().lower()
        if not email:
            console.print(f"[red]{strings['email_required']}[/]")
            continue

        user = next((entry for entry in data["users"] if entry.get("email") == email), None)

        if user:
            password = getpass(strings["prompt_password"])
            if not verify_password(user.get("password_hash", ""), password):
                console.print(f"[red]{strings['invalid_credentials']}[/]")
                continue
            salt = add_or_update_salt(user)
            key = derive_key(password, salt)
            payload = data["profiles"].get(email)
            try:
                profile = decrypt_profile_payload(key, payload) if isinstance(payload, dict) else default_profile()
            except ValueError:
                console.print("[red]Gagal membuka data terenkripsi. Coba ulangi atau hubungi admin.[/]")
                continue
            ensure_profile_defaults(profile)
            session = Session(data=data, email=email, profile=profile, key=key)
            persist_session(session)
            console.print(f"[green]{strings['login_success'].format(email=email)}[/]")
            return session

        console.print(f"[yellow]{strings['user_not_found_signup']}[/]")
        while True:
            password = getpass(strings["prompt_password"])
            confirm = getpass(strings["prompt_password_confirm"])
            if password != confirm:
                console.print(f"[red]{strings['password_mismatch']}[/]")
                continue
            break

        salt = generate_salt()
        key = derive_key(password, salt)
        salt_b64 = base64.b64encode(salt).decode("utf-8")
        data["users"].append({"email": email, "password_hash": hash_password(password), "salt": salt_b64})

        pending_profile = data.get("pending_profile")
        if isinstance(pending_profile, dict):
            profile = pending_profile
            data["pending_profile"] = None
        else:
            profile = default_profile()
        ensure_profile_defaults(profile)
        session = Session(data=data, email=email, profile=profile, key=key)
        persist_session(session)
        console.print(f"[green]{strings['signup_success'].format(email=email)}[/]")
        return session


def main_menu(session: Session) -> None:
    profile = session.profile
    while True:
        console.print(f"\n[bold cyan]{tr(profile, 'main_menu_title')}[/]")
        console.print(f"1. {tr(profile, 'main_menu_dashboard')}")
        console.print(f"2. {tr(profile, 'main_menu_budget')}")
        console.print(f"3. {tr(profile, 'main_menu_period')}")
        console.print(f"4. {tr(profile, 'main_menu_language')}")
        console.print(f"5. {tr(profile, 'main_menu_exit')}")
        choice = input(tr(profile, "prompt_choice")).strip()

        if choice == "1":
            display_dashboard(profile)
        elif choice == "2":
            budgeting_menu(session)
        elif choice == "3":
            change_period(session)
        elif choice == "4":
            change_language(session)
        elif choice == "5":
            persist_session(session)
            console.print(f"[green]{tr(profile, 'thank_you')}[/]")
            break
        else:
            console.print(f"[red]{tr(profile, 'invalid_choice')}[/]")


def main() -> None:
    data = load_data()
    session = authenticate_user(data)
    display_dashboard(session.profile)
    main_menu(session)


if __name__ == "__main__":
    main()

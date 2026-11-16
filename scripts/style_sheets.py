import subprocess
import shutil

SPREADSHEET_ID = "11hZOHenib5-hMHXeg4HUWR_QvEE462qON4LtOZMkdvY"

sheets = [
    # (sheet_id, rows, cols, status_col_idx)
    (0, 11, 7, 5),
    (1350203593, 14, 8, 7),
    (761829798, 15, 8, 7),
    (2051392878, 19, 8, -1),
    (2097185628, 8, 8, 1)
]

print("Applying visual polish to Google Sheets...")

for sid, rows, cols, status_col in sheets:
    # 1. Subtle border across entire table
    cmd = f'gsheets mutate borders {SPREADSHEET_ID} --sheet-id {sid} --start-row 0 --end-row {rows} --start-col 0 --end-col {cols} --style SOLID --color "0.80,0.84,0.89"'
    subprocess.run(cmd, shell=True, check=False)
    
    # 2. Alternating zebra row striping
    for r in range(1, rows):
        bg = "#F8FAFC" if r % 2 == 1 else "#FFFFFF"
        cmd = f'gsheets mutate format {SPREADSHEET_ID} --sheet-id {sid} --start-row {r} --end-row {r + 1} --start-col 0 --end-col {cols} --bg-color "{bg}"'
        subprocess.run(cmd, shell=True, check=False)

print("Applying Conditional Formatting for status tags...")

# Status badges conditional formatting on Sheet 0 (RACI) & Sheet 1 (Roadmap) & Sheet 2 (Plugins)
status_rules = [
    # (sheet_id, col_idx, max_rows)
    (0, 5, 11),
    (1350203593, 7, 14),
    (761829798, 7, 15)
]

for sid, col, max_r in status_rules:
    # Completed -> Emerald Green
    cmd = f'gsheets mutate conditional-format {SPREADSHEET_ID} --sheet-id {sid} --start-row 1 --end-row {max_r} --start-col {col} --end-col {col + 1} --condition TEXT_CONTAINS --value "Completed" --color "#DCFCE7"'
    subprocess.run(cmd, shell=True, check=False)
    
    # In Progress -> Amber Yellow
    cmd = f'gsheets mutate conditional-format {SPREADSHEET_ID} --sheet-id {sid} --start-row 1 --end-row {max_r} --start-col {col} --end-col {col + 1} --condition TEXT_CONTAINS --value "In Progress" --color "#FEF3C7"'
    subprocess.run(cmd, shell=True, check=False)

    # Planned / Pending -> Soft Slate Blue
    cmd = f'gsheets mutate conditional-format {SPREADSHEET_ID} --sheet-id {sid} --start-row 1 --end-row {max_r} --start-col {col} --end-col {col + 1} --condition TEXT_CONTAINS --value "Planned" --color "#E2E8F0"'
    subprocess.run(cmd, shell=True, check=False)

    # Critical -> Soft Rose
    cmd = f'gsheets mutate conditional-format {SPREADSHEET_ID} --sheet-id {sid} --start-row 1 --end-row {max_r} --start-col {col} --end-col {col + 1} --condition TEXT_CONTAINS --value "Critical" --color "#FEE2E2"'
    subprocess.run(cmd, shell=True, check=False)

    # High -> Light Orange
    cmd = f'gsheets mutate conditional-format {SPREADSHEET_ID} --sheet-id {sid} --start-row 1 --end-row {max_r} --start-col {col} --end-col {col + 1} --condition TEXT_CONTAINS --value "High" --color "#FFEDD5"'
    subprocess.run(cmd, shell=True, check=False)

print("Formatting completed successfully!")

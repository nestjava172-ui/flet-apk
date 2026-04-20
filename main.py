import flet as ft
import secrets
import os
from datetime import datetime
from collections import Counter

def main(page: ft.Page):
    page.title = "Mesin RNG 4D"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 700

    hasil_list = []
    log_file = "log_undian.txt"

    txt_hasil = ft.TextField(value="0000",text_size=60,weight=ft.FontWeight.BOLD,text_align=ft.TextAlign.CENTER,max_length=4,input_filter=ft.InputFilter(allow=True, regex_string=r"[0-9]", replacement_string=""),border=ft.InputBorder.NONE,filled=True,bgcolor=ft.Colors.BLACK26)
    txt_info = ft.Text("Tekan tombol untuk mulai undi", size=14, color=ft.Colors.GREY_400)
    list_log = ft.ListView(expand=True, spacing=5, auto_scroll=True)
    chart_angka = ft.BarChart(max_y=10, expand=True)

    def update_chart():
        if not hasil_list:
            chart_angka.bar_groups = []
            page.update()
            return
        digit_terakhir = [int(h[-1]) for h in hasil_list]
        frekuensi = Counter(digit_terakhir)
        bars = []
        max_freq = max(frekuensi.values()) if frekuensi else 1
        for i in range(10):
            freq = frekuensi.get(i, 0)
            bars.append(
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[ft.BarChartRod(from_y=0, to_y=freq, width=20, color=ft.Colors.AMBER if freq == max_freq else ft.Colors.BLUE_400, tooltip=f"Angka {i}: {freq}x", border_radius=0)]
                )
            )
        chart_angka.bar_groups = bars
        chart_angka.max_y = max_freq + 2 if max_freq > 0 else 10
        page.update()

    def undi(e, jumlah=1):
        for _ in range(jumlah):
            angka = f"{secrets.randbelow(10000):04d}"
            hasil_list.append(angka)
            waktu = datetime.now().strftime("%H:%M:%S")
            txt_hasil.value = angka
            txt_info.value = f"Total undian: {len(hasil_list)}"
            list_log.controls.insert(0, ft.Text(f"[{waktu}] {angka}", size=13))
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {angka}\n")
        if len(list_log.controls) > 50:
            list_log.controls = list_log.controls[:50]
        update_chart()

    def reset_data(e):
        hasil_list.clear()
        list_log.controls.clear()
        txt_hasil.value = "0000"
        txt_info.value = "Data direset. Siap undi lagi."
        if os.path.exists(log_file):
            os.remove(log_file)
        update_chart()
        page.update()

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("MESIN RNG 4D", size=24, weight=ft.FontWeight.BOLD),
                txt_hasil,
                ft.Container(
    content=ft.Column([
        ft.Text("MESIN RNG 4D", size=24, weight=ft.FontWeight.BOLD),
        txt_hasil,
        ft.ElevatedButton("Simpan Angka Manual", on_click=simpan_manual, expand=True, icon=ft.Icons.SAVE),
        txt_info,
        ft.Row([
            ft.ElevatedButton("Undi 1x", on_click=lambda e: undi(e, 1), expand=True),
            ft.ElevatedButton("Undi 10x", on_click=lambda e: undi(e, 10), expand=True),
            ft.ElevatedButton("Undi 100x", on_click=lambda e: undi(e, 100), expand=True),
        ]),
                txt_info,
                ft.Row([
                    ft.ElevatedButton("Undi 1x", on_click=lambda e: undi(e, 1), expand=True),
                    ft.ElevatedButton("Undi 10x", on_click=lambda e: undi(e, 10), expand=True),
                    ft.ElevatedButton("Undi 100x", on_click=lambda e: undi(e, 100), expand=True),
                ]),
                ft.Divider(),
                ft.Text("Statistik Digit Terakhir", weight=ft.FontWeight.BOLD),
                ft.Container(chart_angka, height=200, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=5, padding=10),
                ft.Row([
                    ft.Text("Log Hasil", weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(ft.Icons.DELETE, on_click=reset_data, tooltip="Reset data"),
                ]),
                ft.Container(list_log, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=5, padding=10, expand=True),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=15
        )
        page.add(
        ft.Container(
            padding=15,
            content=ft.Column([
                ft.Text("MESIN RNG 4D", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                txt_hasil,
                ft.ElevatedButton("Simpan Angka Manual", on_click=simpan_manual, expand=True, icon=ft.Icons.SAVE),
                txt_info,
                ft.Row([
                    ft.ElevatedButton("Undi 1x", on_click=lambda e: undi(e, 1), expand=True),
                    ft.ElevatedButton("Undi 10x", on_click=lambda e: undi(e, 10), expand=True),
                    ft.ElevatedButton("Undi 100x", on_click=lambda e: undi(e, 100), expand=True),
                ]),
                ft.Divider(),
                ft.Text("Statistik Digit Terakhir", weight=ft.FontWeight.BOLD),
                ft.Container(chart_angka, height=150),
                ft.Divider(),
                ft.Row([
                    ft.Text("Log Hasil", weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(icon=ft.Icons.DELETE_FOREVER, on_click=reset_data, tooltip="Reset")
                ]),
                ft.Container(list_log, height=200, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=5, padding=5)
            ], spacing=10)
        )
    )
    def simpan_manual(e):
        angka = txt_hasil.value
        if len(angka) == 4 and angka.isdigit():
            hasil_list.append(angka)
            waktu = datetime.now().strftime("%H:%M:%S")
            list_log.controls.insert(0, ft.Text(f"[{waktu}] {angka} - Manual", size=13))
            txt_info.value = f"Total undian: {len(hasil_list)}"
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {angka} - Manual\n")
            if len(list_log.controls) > 50:
                list_log.controls = list_log.controls[:50]
            update_chart()
        else:
            txt_info.value = "Error: Masukkan 4 digit angka!"
            page.update())

ft.app(target=main    def simpan_manual(e):
        angka = txt_hasil.value
        if len(angka) == 4 and angka.isdigit():
            hasil_list.append(angka)
            waktu = datetime.now().strftime("%H:%M:%S")
            list_log.controls.insert(0, ft.Text(f"[{waktu}] {angka} - Manual", size=13))
            txt_info.value = f"Total undian: {len(hasil_list)}"
            with open(log_file, "a") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {angka} - Manual\n")
            if len(list_log.controls) > 50:
                list_log.controls = list_log.controls[:50]
            update_chart()
        else:
            txt_info.value = "Error: Masukkan 4 digit angka!"
        page.update()

    page.add(
        ft.Container(
            padding=15,
            content=ft.Column([
                ft.Text("MESIN RNG 4D", size=24, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                txt_hasil,
                ft.ElevatedButton("Simpan Angka Manual", on_click=simpan_manual, expand=True, icon=ft.Icons.SAVE),
                txt_info,
                ft.Row([
                    ft.ElevatedButton("Undi 1x", on_click=lambda e: undi(e, 1), expand=True),
                    ft.ElevatedButton("Undi 10x", on_click=lambda e: undi(e, 10), expand=True),
                    ft.ElevatedButton("Undi 100x", on_click=lambda e: undi(e, 100), expand=True),
                ]),
                ft.Divider(),
                ft.Text("Statistik Digit Terakhir", weight=ft.FontWeight.BOLD),
                ft.Container(chart_angka, height=150),
                ft.Divider(),
                ft.Row([
                    ft.Text("Log Hasil", weight=ft.FontWeight.BOLD, expand=True),
                    ft.IconButton(icon=ft.Icons.DELETE_FOREVER, on_click=reset_data, tooltip="Reset")
                ]),
                ft.Container(list_log, height=200, border=ft.border.all(1, ft.Colors.GREY_700), border_radius=5, padding=5)
            ], spacing=10)
        )
    )
    
    load_data()
    page.update()

ft.app(target=main))

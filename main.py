import flet as ft
import random
from datetime import datetime

hasil_list = []

def main(page: ft.Page):
    try:
        page.title = "Mesin RNG 4D"
        page.theme_mode = ft.ThemeMode.DARK
        page.window_width = 400
        page.window_height = 700

        txt_hasil = ft.TextField(
            value="0000",
            text_size=60,
            text_align=ft.TextAlign.CENTER,
            max_length=4,
            input_filter=ft.NumbersOnlyInputFilter(),
            border_color=ft.Colors.BLUE_400
        )
        txt_info = ft.Text("Tekan tombol atau ketik manual", text_align=ft.TextAlign.CENTER)
        list_log = ft.ListView(expand=True, spacing=5, auto_scroll=True)
        chart_angka = ft.BarChart(
            bar_groups=[],
            border=ft.border.all(1, ft.Colors.GREY_700),
            left_axis=ft.ChartAxis(labels_size=40),
            bottom_axis=ft.ChartAxis(labels_size=40),
            horizontal_grid_lines=ft.ChartGridLines(interval=1),
            max_y=10,
            interactive=True,
            expand=True,
        )

        def save_to_storage():
            page.client_storage.set("hasil_list", ",".join(hasil_list))

        def load_from_storage():
            data = page.client_storage.get("hasil_list")
            if data:
                hasil_list.extend(data.split(","))

        def update_chart():
            if not hasil_list:
                chart_angka.bar_groups = []
                chart_angka.max_y = 10
                return
            digit_terakhir = [int(h[-1]) for h in hasil_list]
            counts = [digit_terakhir.count(i) for i in range(10)]
            chart_angka.max_y = max(counts) + 2 if counts else 10
            chart_angka.bar_groups = [
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[ft.BarChartRod(from_y=0, to_y=counts[i], width=16, color=ft.Colors.BLUE_400, tooltip=str(counts[i]))],
                ) for i in range(10)
            ]
            page.update()

        def undi(e, jumlah):
            for _ in range(jumlah):
                angka = f"{random.randint(0, 9999):04d}"
                hasil_list.append(angka)
                waktu = datetime.now().strftime("%H:%M:%S")
                list_log.controls.insert(0, ft.Text(f"[{waktu}] {angka}", size=13))
            txt_hasil.value = hasil_list[-1]
            txt_info.value = f"Total undian: {len(hasil_list)}"
            if len(list_log.controls) > 50:
                list_log.controls = list_log.controls[:50]
            save_to_storage()
            update_chart()
            page.update()

        def load_data():
            load_from_storage()
            for angka in hasil_list:
                list_log.controls.insert(0, ft.Text(f"[LOAD] {angka}", size=13))
            if hasil_list:
                txt_hasil.value = hasil_list[-1]
                txt_info.value = f"Total undian: {len(hasil_list)}"
            update_chart()

        def reset_data(e):
            hasil_list.clear()
            list_log.controls.clear()
            txt_hasil.value = "0000"
            txt_info.value = "Data direset. Siap undi lagi."
            page.client_storage.remove("hasil_list")
            update_chart()
            page.update()

        def simpan_manual(e):
            angka = txt_hasil.value
            if len(angka) == 4 and angka.isdigit():
                hasil_list.append(angka)
                waktu = datetime.now().strftime("%H:%M:%S")
                list_log.controls.insert(0, ft.Text(f"[{waktu}] {angka} - Manual", size=13))
                txt_info.value = f"Total undian: {len(hasil_list)}"
                if len(list_log.controls) > 50:
                    list_log.controls = list_log.controls[:50]
                save_to_storage()
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

    except Exception as e:
        page.clean()
        page.add(ft.Text(f"ERROR: {e}", color="red", selectable=True, size=16))
        page.update()

ft.app(target=main)

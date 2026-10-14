import os
import json
import tkinter as tk
from tkinter import messagebox, filedialog

class FFModToolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FF Weapon & Position Mod Maker - Entimus")
        self.root.geometry("450x650")
        self.root.config(bg="#0b0f19")

        self.selected_file_path = ""

        # Tiêu đề chính
        title_label = tk.Label(root, text="FF AUTO TOOL MAKER", fg="#38bdf8", bg="#0b0f19", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)

        # --- PHẦN 1: CHỌN FILE BUNDLE ---
        frame_file = tk.LabelFrame(root, text=" 1. Chọn file bundle ", fg="#38bdf8", bg="#131b2e", font=("Arial", 10, "bold"))
        frame_file.pack(fill="x", padx=15, pady=5)

        self.btn_select = tk.Button(frame_file, text="Chọn file bundle", bg="#2563eb", fg="white", font=("Arial", 10, "bold"), command=self.select_file)
        self.btn_select.pack(fill="x", padx=10, pady=8)

        self.lbl_file_info = tk.Label(frame_file, text="Chưa chọn file", fg="#94a3b8", bg="#0f172a", font=("Arial", 9), anchor="w", padx=8, pady=5)
        self.lbl_file_info.pack(fill="x", padx=10, pady=5)

        # --- PHẦN 2: CHỌN CHỨC NĂNG ---
        frame_func = tk.LabelFrame(root, text=" 2. Chọn chức năng ", fg="#38bdf8", bg="#131b2e", font=("Arial", 10, "bold"))
        frame_func.pack(fill="x", padx=15, pady=8)

        self.func_var = tk.StringVar(value="gun")
        
        rb_gun = tk.Radiobutton(frame_func, text="Định vị súng\n(Định Vị Súng 2 Lớp Tích Hợp Keo Trong Xuất)", 
                                variable=self.func_var, value="gun", fg="white", bg="#131b2e", selectcolor="#0f172a", 
                                font=("Arial", 9), command=self.toggle_mode, justify="left")
        rb_gun.pack(anchor="w", padx=10, pady=5)

        rb_char = tk.Radiobutton(frame_func, text="Định vị nhân vật\n(Make Màu Tự Động Và Dạng Định Vị New)", 
                                 variable=self.func_var, value="character", fg="white", bg="#131b2e", selectcolor="#0f172a", 
                                 font=("Arial", 9), command=self.toggle_mode, justify="left")
        rb_char.pack(anchor="w", padx=10, pady=5)

        # --- PHẦN 3: TÙY CHỈNH THÔNG SỐ ---
        self.frame_detail = tk.LabelFrame(root, text=" Định vị súng ", fg="#38bdf8", bg="#131b2e", font=("Arial", 10, "bold"))
        self.frame_detail.pack(fill="x", padx=15, pady=8)

        # Màu súng
        row1 = tk.Frame(self.frame_detail, bg="#131b2e")
        row1.pack(fill="x", padx=10, pady=5)
        tk.Label(row1, text="Màu súng", fg="white", bg="#131b2e", font=("Arial", 9)).pack(side="left")
        self.gun_color_entry = tk.Entry(row1, width=10, font=("Arial", 9))
        self.gun_color_entry.pack(side="right")
        self.gun_color_entry.insert(0, "#a56a35")

        # Màu viền
        row2 = tk.Frame(self.frame_detail, bg="#131b2e")
        row2.pack(fill="x", padx=10, pady=5)
        tk.Label(row2, text="Màu viền", fg="white", bg="#131b2e", font=("Arial", 9)).pack(side="left")
        self.border_color_entry = tk.Entry(row2, width=10, font=("Arial", 9))
        self.border_color_entry.pack(side="right")
        self.border_color_entry.insert(0, "#ffffff")

        # Màu keo
        row3 = tk.Frame(self.frame_detail, bg="#131b2e")
        row3.pack(fill="x", padx=10, pady=5)
        tk.Label(row3, text="Màu keo", fg="white", bg="#131b2e", font=("Arial", 9)).pack(side="left")
        self.glue_color_entry = tk.Entry(row3, width=10, font=("Arial", 9))
        self.glue_color_entry.pack(side="right")
        self.glue_color_entry.insert(0, "#e3af34")

        # Độ dày viền (Slider)
        lbl_b_frame = tk.Frame(self.frame_detail, bg="#131b2e")
        lbl_b_frame.pack(fill="x", padx=10, pady=(5,0))
        tk.Label(lbl_b_frame, text="Độ dày viền:", fg="#cbd5e1", bg="#131b2e", font=("Arial", 9)).pack(side="left")
        self.lbl_b_val = tk.Label(lbl_b_frame, text="4.0", fg="#38bdf8", bg="#131b2e", font=("Arial", 9, "bold"))
        self.lbl_b_val.pack(side="right")
        
        self.slider_border = tk.Scale(self.frame_detail, from_=1.0, to=10.0, resolution=0.1, orient="horizontal", bg="#131b2e", fg="white", highlightthickness=0, command=lambda v: self.lbl_b_val.config(text=v))
        self.slider_border.set(4.0)
        self.slider_border.pack(fill="x", padx=10, pady=(0,5))

        # Độ đục màu súng (Slider)
        lbl_o_frame = tk.Frame(self.frame_detail, bg="#131b2e")
        lbl_o_frame.pack(fill="x", padx=10, pady=(5,0))
        tk.Label(lbl_o_frame, text="Độ đục màu súng:", fg="#cbd5e1", bg="#131b2e", font=("Arial", 9)).pack(side="left")
        self.lbl_o_val = tk.Label(lbl_o_frame, text="1.00", fg="#38bdf8", bg="#131b2e", font=("Arial", 9, "bold"))
        self.lbl_o_val.pack(side="right")

        self.slider_opacity = tk.Scale(self.frame_detail, from_=0.0, to=1.0, resolution=0.05, orient="horizontal", bg="#131b2e", fg="white", highlightthickness=0, command=lambda v: self.lbl_o_val.config(text=v))
        self.slider_opacity.set(1.0)
        self.slider_opacity.pack(fill="x", padx=10, pady=(0,5))

        # --- NÚT TẠO FILE ---
        self.btn_create = tk.Button(root, text="Tạo file", bg="#334155", fg="#64748b", font=("Arial", 11, "bold"), state="disabled", command=self.create_file)
        self.btn_create.pack(fill="x", padx=15, pady=15)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Chọn file bundle game", filetypes=[("Bundle files", "*.bundle"), ("All files", "*.*")])
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path) / (1024 * 1024)
            self.lbl_file_info.config(text=f"Đã chọn: {file_name} ({file_size:.2f} MB)")
            self.btn_create.config(bg="#0284c7", fg="white", state="normal")

    def toggle_mode(self):
        mode = self.func_var.get()
        if mode == "gun":
            self.frame_detail.config(text=" Định vị súng ")
        else:
            self.frame_detail.config(text=" Định vị nhân vật ")

    def create_file(self):
        if not self.selected_file_path:
            messagebox.showerror("Lỗi", "Vui lòng chọn file bundle trước!")
            return

        mode = self.func_var.get()
        config_data = {
            "mode": mode,
            "source_bundle": os.path.basename(self.selected_file_path),
            "parameters": {
                "gun_color": self.gun_color_entry.get(),
                "border_color": self.border_color_entry.get(),
                "glue_color": self.glue_color_entry.get(),
                "border_thickness": self.slider_border.get(),
                "opacity": self.slider_opacity.get()
            }
        }

        save_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Config", "*.json"), ("Data file", "*.dat")],
            initialfile="ff_custom_output.json"
        )

        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    json.dump(config_data, f, ensure_ascii=False, indent=4)
                messagebox.showinfo("Thành công", f"Đã tạo file cấu hình thành công tại:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể lưu file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FFModToolApp(root)
    root.mainloop()

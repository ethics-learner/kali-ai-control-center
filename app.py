import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from controller import ToolController


class KaliAIGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kali AI Control Center")
        self.geometry("1100x650")

        self._build_layout()

        self.controller = ToolController(
            self._append_raw_output,
            self._append_ai_output,
            self._confirm_action
        )

    def _build_layout(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        self.input_box = tk.Entry(self, font=("Segoe UI", 12))
        self.input_box.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        self.input_box.insert(0, "Scan 192.168.1.1 | Analyze Tor | use msfconsole")

        btn_frame = tk.Frame(self)
        btn_frame.grid(row=1, column=0, sticky="w", padx=20)

        ttk.Button(btn_frame, text="Run", command=self._run).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Export Report", command=self._export).pack(side="left", padx=5)

        self.raw_output = scrolledtext.ScrolledText(
            self, bg="#0f0f0f", fg="#00ff9c", font=("Consolas", 10)
        )
        self.raw_output.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)

        self.ai_output = scrolledtext.ScrolledText(
            self, bg="#1b1b1b", fg="white", font=("Segoe UI", 11)
        )
        self.ai_output.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))

    def _run(self):
        text = self.input_box.get().strip()
        if not text:
            return
        self.raw_output.insert(tk.END, "\n============================\n")
        self.raw_output.insert(tk.END, f"[REQUEST] {text}\n")
        self.ai_output.delete("1.0", tk.END)
        self.controller.run(text)

    def _export(self):
        path = self.controller.export_report()
        messagebox.showinfo("Report Generated", f"PDF report saved to:\n{path}")

    def _confirm_action(self, msg):
        return messagebox.askyesno("Confirmation Required", msg)

    def _append_raw_output(self, text):
        self.raw_output.insert(tk.END, text)
        self.raw_output.see(tk.END)

    def _append_ai_output(self, text):
        self.ai_output.insert(tk.END, text)
        self.ai_output.see(tk.END)


if __name__ == "__main__":
    KaliAIGUI().mainloop()

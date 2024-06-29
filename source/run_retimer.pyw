from decimal import Decimal;
from decimal import ROUND_HALF_UP;
import tkinter as tk;
import json;

class RetimerRewrite(tk.Frame):
    vfps = None;
    sfdt = None;
    efdt = None;
    def __init__(self, master=None) -> None:
        super().__init__(master);
        
        self.vfps = tk.StringVar();
        self.sfdt = tk.StringVar();
        self.efdt = tk.StringVar();
        
        self.master.geometry("350x250");
        self.master.title("Video Retimer");
        
        self.master["background"] = "black";
        self.master.resizable(False, False)
        
        self._create_gui(master);
        
        self.pack();
    
    def _create_gui(self, master=None) -> None:
        # Create text objects.
        label_vfps = tk.Label(master, text="Video FPS       ", bg="black", fg="white", font=("Consolas", 14));
        label_sfnm = tk.Label(master, text="Start Frame Data", bg="black", fg="white", font=("Consolas", 14));
        label_efnm = tk.Label(master, text="End   Frame Data", bg="black", fg="white", font=("Consolas", 14));
        self.label_edtm = tk.Label(master, text="00h 00m 00s 000ms", bg="black", fg="white", font=("Consolas", 20));
        
        # Create entry objects.
        entry_vfps = tk.Entry(master, width=14, font=("Consolas", 12), justify="right", textvariable=self.vfps);
        entry_sfnm = tk.Entry(master, width=14, font=("Consolas", 12), justify="right", textvariable=self.sfdt);
        entry_efnm = tk.Entry(master, width=14, font=("Consolas", 12), justify="right", textvariable=self.efdt);

        # Create button objects.
        button_copy_edtm = tk.Button(master, command=self._copy_edtm, font=("Consolas", 12), bg="black", fg="gray", text="Copy Time")
        
        self.vfps.trace_add("write", self._on_update);
        self.sfdt.trace_add("write", self._on_update);
        self.efdt.trace_add("write", self._on_update);
        
        # Position objects.
        label_vfps.place(relx=0.28, rely=0.12, anchor="center");
        label_sfnm.place(relx=0.28, rely=0.22, anchor="center");
        label_efnm.place(relx=0.28, rely=0.32, anchor="center");
        self.label_edtm.place(relx=0.50, rely=0.80, anchor="center");
        
        entry_vfps.place(relx=0.76, rely=0.12, anchor="center");
        entry_sfnm.place(relx=0.76, rely=0.22, anchor="center");
        entry_efnm.place(relx=0.76, rely=0.32, anchor="center");

        button_copy_edtm.place(relx=0.27, rely=0.67, anchor="center");
        
    
    def _on_update(self, a, b, c) -> None:
        self._calculate_time();

    def _copy_edtm(self) -> None:
        self.master.clipboard_clear();
        self.master.clipboard_append(self.label_edtm["text"]);
    
    def _calculate_time(self) -> None:
        start_time = Decimal(json.loads(self.sfdt.get())["cmt"]);
        end_time = Decimal(json.loads(self.efdt.get())["cmt"]);

        start_time = Decimal(start_time - start_time % (Decimal(1) / int(self.vfps.get())))
        end_time = Decimal(end_time - end_time % (Decimal(1) / int(self.vfps.get())))
            
        full_time = end_time - start_time;
        print(full_time)
        end_text = "";
            
        h, m, s, ms = 0, 0, 0, 0;
        full_time = full_time.quantize(Decimal('1.111'), rounding=ROUND_HALF_UP);
        ms = (1000 * full_time) % 1000;
        s = (full_time - full_time % 1) % 60;
        m = (((full_time - full_time % 1) - s) / 60) % 60;
        h = (((((full_time - full_time % 1) - s) / 60) % 60) - m) / 60;
            
            
        end_text = "{:02d}h {:02d}m {:02d}s {:03d}ms".format(int(h), int(m), int(s), int(ms));
            
        self.label_edtm["text"] = end_text;
    
if(__name__ == '__main__'):
    root = RetimerRewrite();
    root.mainloop();

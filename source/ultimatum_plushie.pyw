import tkinter as Tkinter;
import pynput  as Pynput;
import json    as JSON;
import os      as OS;

class UltimatumPlushieMemory(Tkinter.Frame):
    full_string = None;
    listener = None;
    options:list = ["Nightmare Bonnie", "Circus Baby     ", "Nightmare Mangle"];
    keybinds:dict = {"RESET": '<38>', "0": '<37>', "1": "<40>", "2": "<39>"};
    def __init__(self, master=None) -> None:
        super().__init__(master);

        self.string_v = '';
        self.full_string = Tkinter.StringVar();
        self.string_amt = 0;

        with open(OS.getcwd()+'\\config_files\\ultimatum_plushie.json', 'r') as f:
            d = JSON.loads(f.read());
            self.keybinds = d["Keybinds"];
            self.font_info = d["Visual"]["FontInfo"];
            self.window_info = d["Visual"]["WindowInfo"];
            
        self.master.geometry("{0}x{1}".format(self.window_info["Size"][0], self.window_info["Size"][1]));
        self.master["background"] = self.window_info["BackgroundColor"];
        self.master.resizable(False, False);
        
        self.master.title("Ultimatum Plushie Thing");
        self.master.attributes('-topmost', True);
        self.master.protocol('WM_DELETE_WINDOW', self._on_closing);

        self.listener = Pynput.keyboard.Listener(on_press=self._on_press);
        self.listener.start();
        
        self._create_gui(master);
        
        self.pack();

    def _on_press(self, key) -> None:
        try:
            print(str(key));
            for kb in self.keybinds:
                if(str(key) == self.keybinds[kb]):
                    if(kb != 'RESET'):
                        if(self.string_amt < 3):
                            self.string_v += self.options[int(kb)] + ' > ';
                        self.string_amt += 1;
                        if(self.string_amt == 3):
                            self.string_v = self.string_v[0:len(self.string_v)-3]
                    else:
                        self.string_amt = 0;
                        self.string_v = '';

                    self.full_string.set(self.string_v);
                    
        except AttributeError:
            print(str(key));

    def _on_closing(self) -> None:
        self.listener.stop();
        self.master.destroy();
        quit();
    
    def _create_gui(self, master=None) -> None:
        self.label_full_string = Tkinter.Label(master, textvariable=self.full_string, bg=self.window_info["BackgroundColor"], fg=self.font_info["Color"], font=(self.font_info["Font"], self.font_info["Size"]));
        self.label_full_string.place(relx=0.0, rely=0.1, anchor="nw");
    

if(__name__ == '__main__'):
    root = UltimatumPlushieMemory();
    root.mainloop();

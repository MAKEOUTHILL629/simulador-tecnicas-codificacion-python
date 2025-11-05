import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
from src.simulation import run_simulation
import threading

class SimulatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Communications Simulator")
        master.geometry("800x600")

        # --- Controls ---
        controls_frame = tk.Frame(master)
        controls_frame.pack(pady=10)

        tk.Label(controls_frame, text="SNR (dB):").pack(side=tk.LEFT, padx=5)
        self.snr_entry = tk.Entry(controls_frame, width=10)
        self.snr_entry.insert(0, "15")
        self.snr_entry.pack(side=tk.LEFT, padx=5)

        self.browse_button = tk.Button(controls_frame, text="Select Input File", command=self.browse_file)
        self.browse_button.pack(side=tk.LEFT, padx=5)
        self.filepath_label = tk.Label(controls_frame, text="data/sample_text.txt")
        self.filepath_label.pack(side=tk.LEFT)
        self.filepath = "data/sample_text.txt"

        self.run_button = tk.Button(controls_frame, text="Run Simulation", command=self.start_simulation_thread)
        self.run_button.pack(side=tk.LEFT, padx=10)

        # --- Results and Plots ---
        results_frame = tk.Frame(master)
        results_frame.pack(pady=10, fill="both", expand=True)

        # Results Text
        tk.Label(results_frame, text="Results:").pack()
        self.results_text = tk.Text(results_frame, height=10, width=80)
        self.results_text.pack(pady=5)

        # Plot Tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(pady=10, fill="both", expand=True)

        self.plot_tabs = {}
        plot_names = ["Transmitted Constellation", "Received Constellation", "LLR Histogram", "Huffman Tree"]
        for name in plot_names:
            tab = tk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            self.plot_tabs[name] = tk.Label(tab)
            self.plot_tabs[name].pack()

    def browse_file(self):
        self.filepath = filedialog.askopenfilename(
            initialdir="./data",
            title="Select a File",
            filetypes=(("Text files", "*.txt*"), ("all files", "*.*"))
        )
        self.filepath_label.config(text=os.path.basename(self.filepath))

    def start_simulation_thread(self):
        # Create and start a new thread to run the simulation
        thread = threading.Thread(target=self._run_simulation_task)
        thread.daemon = True  # Allows main window to exit even if thread is running
        thread.start()

    def _run_simulation_task(self):
        # This function runs in a separate thread

        # Schedule GUI updates to run on the main thread
        self.master.after(0, self._update_gui_before_simulation)

        try:
            snr_db = float(self.snr_entry.get())
            filepath = self.filepath
            if not filepath:
                self.master.after(0, lambda: messagebox.showerror("Error", "Please select a file."))
                return

            # This is the long-running task
            results = run_simulation(snr_db, filepath)

            # Schedule the GUI update with the results
            self.master.after(0, self._update_gui_after_simulation, results)

        except ValueError:
            self.master.after(0, lambda: messagebox.showerror("Error", "Invalid SNR value. Please enter a number."))
        except Exception as e:
            self.master.after(0, lambda: messagebox.showerror("Error", f"An error occurred: {e}"))
        finally:
            # Schedule the button re-enabling
            self.master.after(0, lambda: self.run_button.config(state="normal"))

    def _update_gui_before_simulation(self):
        self.run_button.config(state="disabled")
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Running simulation...\n")

    def _update_gui_after_simulation(self, results):
        # --- Display results ---
        self.results_text.insert(tk.END, f"\n--- Simulation Complete ---\n")
        self.results_text.insert(tk.END, f"Original Text:\n{results['original_text']}\n\n")
        self.results_text.insert(tk.END, f"Decoded Text:\n{results['decoded_text']}\n\n")
        if results['original_text'] == results['decoded_text']:
            self.results_text.insert(tk.END, "Success: Decoded text matches original text.\n")
        else:
            self.results_text.insert(tk.END, "Error: Decoded text does not match original text.\n")

        self.results_text.insert(tk.END, f"Bit Error Rate (BER): {results['ber']:.6f} ({results['num_errors']}/{results['bit_count']})\n")

        # --- Display plots ---
        self.display_image("transmitted_constellation.png", "Transmitted Constellation")
        self.display_image("received_constellation.png", "Received Constellation")
        self.display_image("llr_histogram.png", "LLR Histogram")
        self.display_image("huffman_tree.png", "Huffman Tree")

    def display_image(self, image_path, tab_name):
        if os.path.exists(image_path):
            img = Image.open(image_path)
            img.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(img)
            self.plot_tabs[tab_name].config(image=photo)
            self.plot_tabs[tab_name].image = photo
        else:
            self.plot_tabs[tab_name].config(image=None)


if __name__ == '__main__':
    root = tk.Tk()
    my_gui = SimulatorGUI(root)
    root.mainloop()

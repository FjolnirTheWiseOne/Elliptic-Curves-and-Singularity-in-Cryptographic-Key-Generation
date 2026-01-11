import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import secrets  

class InteractiveECCValidator:
    def __init__(self):
        # 1. Setup the Figure and Grid
        self.fig, self.ax = plt.subplots(figsize=(14, 8))
        self.fig.canvas.manager.set_window_title('ECC Security Validator & Simulator')
        
        # Adjust layout: Left for graph, Right for text, Bottom for sliders
        plt.subplots_adjust(left=0.05, bottom=0.25, right=0.55) 

        # Grid for plotting
        grid_range = 5
        self.x = np.linspace(-grid_range, grid_range, 400)
        self.y = np.linspace(-grid_range, grid_range, 400)
        self.X, self.Y = np.meshgrid(self.x, self.y)


        self.a_init = -3.0
        self.b_init = 2.0

        # 2. Text Areas for Engineering Diagnostics (Right side)
        self.text_ax = self.fig.add_axes([0.60, 0.05, 0.38, 0.9]) 
        self.text_ax.axis('off')
        self.info_text = self.text_ax.text(0, 1, "", va='top', fontsize=10, family='monospace')

        # 3. Setup Widgets (Bottom Left)
        # Slider for 'a'
        ax_a = plt.axes([0.10, 0.1, 0.35, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_a = Slider(ax_a, 'Coeff a', -5.0, 5.0, valinit=self.a_init, valstep=0.1, valfmt='%1.1f')

        # Slider for 'b'
        ax_b = plt.axes([0.10, 0.05, 0.35, 0.03], facecolor='lightgoldenrodyellow')
        self.slider_b = Slider(ax_b, 'Coeff b', -5.0, 5.0, valinit=self.b_init, valstep=0.1, valfmt='%1.1f')

        # 4. Connect Events
        self.slider_a.on_changed(self.update)
        self.slider_b.on_changed(self.update)

        self.update(None)

    def calculate_discriminant(self, a, b):
        """ 
        The Discriminant Formula:
        Δ = -16(4a^3 + 27b^2)
        """
        return -16 * (4 * a**3 + 27 * b**2)

    def get_security_analysis(self, delta, a, b):
        """ 
        Determines if the curve is safe based on Δ.
        Returns: status, color, type, description, action
        """
        # We use a tolerance of 1.0 to make it easy to hit the target with sliders
        if np.abs(delta) < 1.0: 
            status = "INSECURE (SINGULAR)"
            color = 'red'
            
            if np.abs(a) < 0.1 and np.abs(b) < 0.1:
                type_sing = "CUSP (y² = x³)"
                desc = ("Visual: Sharp point at origin (0,0).\n"
                        "Math:   Tangent is undefined.\n"
                        "Risk:   DLP reduces to Additive Group.\n"
                        "        Encryption broken in linear time.")
            else:
                type_sing = "NODE (Self-Intersection)"
                desc = ("Visual: Curve crosses over itself.\n"
                        "Math:   Two tangents at one point.\n"
                        "Risk:   DLP reduces to Multiplicative Group.\n"
                        "        Encryption broken quickly.")
            
            action = "ACTION: KEY GENERATION BLOCKED"
        else:
            status = "SECURE (NON-SINGULAR)"
            color = 'green'
            type_sing = "Elliptic Curve (Smooth)"
            desc = ("Visual: Smooth curve, no crossings.\n"
                    "Math:   Roots are distinct (Δ ≠ 0).\n"
                    "Risk:   Standard ECDLP hardness applies.")
            action = "ACTION: KEY GENERATION PERMITTED"

        return status, color, type_sing, desc, action

    def update(self, val):
        """ Redraws plot and updates text based on sliders """
        a = self.slider_a.val
        b = self.slider_b.val

        # 1. Math Calculation
        delta = self.calculate_discriminant(a, b)
        status, color, type_sing, desc, action = self.get_security_analysis(delta, a, b)

        # 2. Update Plot
        self.ax.clear()
        
        # Plot equation: y^2 - x^3 - ax - b = 0
        F = self.Y**2 - self.X**3 - a * self.X - b
        
        # Draw the curve
        self.ax.contour(self.X, self.Y, F, levels=[0], colors=color, linewidths=2.5)
        
        # Plot styling
        self.ax.grid(True, linestyle=':', alpha=0.6)
        self.ax.axhline(0, color='black', linewidth=0.5)
        self.ax.axvline(0, color='black', linewidth=0.5)
        self.ax.set_title(f"ECC Simulator: $y^2 = x^3 + ({a:.1f})x + ({b:.1f})$", fontsize=14, fontweight='bold')
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        # 3. SIMULATE KEY GENERATION
        if color == 'green':
            # Generate a random 256-bit integer (simulated private key)
            priv_int = secrets.randbits(256)
            priv_hex = hex(priv_int)[2:18]

            pub_hex = secrets.token_hex(16)
            
            key_block = (f"SIMULATED KEY PAIR GENERATED:\n"
                         f"Private (d): 0x{priv_hex}...\n"
                         f"Public  (Q): 04{pub_hex}...\n"
                         f"Result:      SUCCESS")
        else:
            key_block = (f"SIMULATED KEY PAIR GENERATED:\n"
                         f"Private (d): [BLOCKED]\n"
                         f"Public  (Q): [BLOCKED]\n"
                         f"Result:      FAILED (Unsafe Curve) ❌")

        # 4. Update Text Info
        report = (
            f"DIAGNOSTICS REPORT\n"
            f"==================\n"
            f"Input a: {a:.1f}\n"
            f"Input b: {b:.1f}\n"
            f"Discriminant (Δ): {delta:.1f}\n"
            f"------------------\n"
            f"STATUS: {status}\n"
            f"TYPE:   {type_sing}\n\n"
            f"{desc}\n"
            f"------------------\n"
            f"{action}\n\n"
            f"{key_block}\n"
            f"==================\n\n"
            f"DEMO CHEAT SHEET (Set sliders to):\n"
            f"1. Singular Node (RED):\n"
            f"   a = -3.0, b = 2.0\n\n"
            f"2. Singular Cusp (RED):\n"
            f"   a = 0.0,  b = 0.0\n\n"
            f"3. Secure Curve (GREEN):\n"
            f"   a = -1.0, b = 4.0\n"
        )
        self.info_text.set_text(report)
        self.info_text.set_color('darkred' if color == 'red' else 'darkgreen')
        self.info_text.set_weight('bold')

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()

if __name__ == "__main__":
    print("Launching ECC Visualization Module...")
    print("Use the sliders to match the Cheat Sheet values.")
    app = InteractiveECCValidator()
    app.show()
import os 
import base64
import pathlib
import webbrowser
import matplotlib.pyplot as plt 

from io import BytesIO


class BuildHtmlReport:
    def __init__(self, html_output_path : pathlib.Path, report_title : str):
        self.html_output_path = html_output_path 
        
        # Init variables 
        self.html = f"""
        <html>
        <head><title>{report_title}</title></head>
        <body>
            <h1>Report Summary</h1>
            <p>This report contains several plots.</p>
        """


    def ___encodePng___(self, fig) -> str: 
        """
        TODO 
        """
        buffer = BytesIO()
        fig.savefig(buffer, format="png")
        plt.close(fig)
        buffer.seek(0)

        return base64.b64encode(buffer.read()).decode('utf-8')
    

    def finalizeHtml(self):
        self.html += "</body></html>"
        with open('report.html', 'w') as f:
            f.write(self.html)
        
        # TODO: just make this point to og path
        webbrowser.open(f"file://{os.path.abspath('report.html')}")


    def appendFig(self, fig):
        png_str = self.___encodePng___(fig)
        self.html += f'<img src="data:image/png;base64,{png_str}" /><br>'
        
        
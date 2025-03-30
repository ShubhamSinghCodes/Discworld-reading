# Series Reading Order Graph

This project generates a fully self-contained HTML file that displays an interactive, graph-based reading guide for a book series (for example, the Discworld series). Books are represented as nodes and their reading order is shown with directed edges. The graph supports features such as:

- Deterministic initial positioning (nodes are positioned by book id on the x–axis and by subseries on the y–axis).
- Interactive PDF viewer modals with saved reading progress (page numbers) and status tracking (reading, finished, skipped).
- Next book suggestions based on outgoing edges (direct edges are prioritized).
- Dark mode support.
- A responsive layout that scales to the entire viewport.

> **Important:**  
> The PDF files in the `pdfs` folder are **not provided** due to copyright issues.  
> You must supply your own PDFs (named using the required pattern) if you wish to use the PDF viewer feature.

## Files

- **`compile_pdfs.py`**  
  The Python script that:
  - Loads series data from `series.json`.
  - Searches for and compresses PDFs in the `pdfs` folder.
  - Embeds the PDFs (or a placeholder if not found) into a separate PDF store.
  - Renders the interactive HTML file using the Jinja2 template (`template.html`).
  - Outputs the final file as `compiled_series.html`.

- **`series.json`**  
  A JSON file containing your series data, including:
  - **nodes**: an array of book objects (with properties like `id`, `title`, `subseries`, and an optional `start` property).
  - **edges**: an array of objects representing directed reading order connections between books.
  - **subseries_colors**: an object mapping subseries names to color values.

- **`template.html`**  
  A Jinja2 template that defines the HTML structure, CSS, and JavaScript for displaying the interactive graph, PDF modals, status outlines, and next-book suggestions.

- **`pdfs/`**  
  A folder where you must place your PDF files.  
  Files should be named following this pattern:
  ```
  <id>- <title>.pdf
  ```
  For example:  
  `1- The Colour of Magic.pdf`  
  `2- The Light Fantastic.pdf`

- **`placeholderpdf.txt`**  
  A text file containing a placeholder Base64 PDF string that is used when a PDF for a node cannot be found.

## Requirements

- **Python 3**

- The following Python packages (install via pip):
  ```bash
  pip install jinja2 pikepdf htmlmin
  ```

## Usage

1. **Prepare Your PDF Files:**  
   Place your PDF files in the `pdfs` folder. Each file should be named using the pattern:
   ```
   <id>- <title>.pdf
   ```
   For example:
   ```
   1- The Colour of Magic.pdf
   2- The Light Fantastic.pdf
   ```

2. **Prepare Your Series Data:**  
   Edit the `series.json` file to include the correct nodes, edges, and subseries colors for your book series. You can mark a book as a starting book by setting its `start` property to a string (e.g., `"Rincewind"`).

3. **Run the Compiler:**  
   Execute the following command in your terminal:
   ```bash
   python compile_pdfs.py
   ```
   This will process the PDFs and generate a self-contained HTML file named `compiled_series.html`.

4. **Open the HTML File:**  
   Open `compiled_series.html` in your web browser. The interactive graph will load and:
   - Display book nodes according to their deterministic positions.
   - Allow you to click on nodes to open their PDFs (with saved progress if available).
   - Show status outlines (blue for reading, green for finished, red for skipped).
   - Provide next-book suggestions based on the reading order.
   - Allow you to set the current page and save progress.

## Customization

- **Changing the Series:**  
  Simply update the `series.json` file with your new series data. The compiler and template will work with any properly formatted series data.

- **Modifying the Layout:**  
  The force simulation uses a fixed virtual domain (2000×2000) and initial positions are set based on the book id and subseries. You can adjust these parameters in `compile_pdfs.py` if needed.

- **Styling:**  
  Modify the CSS in `template.html` to change colors, fonts, or other visual aspects.

## Notes

- **PDFs:**  
  The PDFs in the `pdfs` folder are not provided due to copyright.  
  You must supply your own PDF files following the naming convention.

- **Offline Usage:**  
  The final generated HTML file is fully self-contained and works offline.

## License

This project is provided for educational purposes. DO NOT copy and distribute this, except for viewing purposes. Respect the copyright clauses of the books.

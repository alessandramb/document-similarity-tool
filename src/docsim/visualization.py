import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .file_handling import   get_author_name_from_path
def save_common_pdf(text1, text2, file1, file2, output_folder="diff_pdfs"):
    os.makedirs(output_folder, exist_ok=True)
    name1 = os.path.basename(file1).replace(".pdf", "").replace(".docx", "")
    name2 = os.path.basename(file2).replace(".pdf", "").replace(".docx", "")
    diff_name = f"{name1}__vs__{name2}.pdf"
    diff_path = os.path.join(output_folder, diff_name)

    try:
        lines1 = set(text1.splitlines())
        lines2 = set(text2.splitlines())
        common_lines = sorted(lines1 & lines2)

        if not common_lines:
            return None

        c = canvas.Canvas(diff_path, pagesize=letter)
        width, height = letter
        y = height - 40
        for line in common_lines:
            if y < 40:
                c.showPage()
                y = height - 40
            c.drawString(30, y, line[:120])
            y -= 12
        c.save()
        return diff_path
    except Exception as e:
        print(f"Error generating common content PDF for {file1} vs {file2}: {e}")
    return None

def generate_html_dashboard(similar_pairs, folder1, folder2, output_html="pdf_similarity_dashboard.html"):
    """Generate HTML dashboard showing similarity results"""
    html_head = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PDF/Word Similarity Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px 12px; border: 1px solid #ccc; text-align: left; }
        th { background-color: #f4f4f4; }
        tr:hover { background-color: #f9f9f9; }

        .sim-0    { background-color: #e0ffe0; }
        .sim-94   { background-color: #fffcc9; }
        .sim-96   { background-color: #ffe29f; }
        .sim-98   { background-color: #ffb380; }
        .sim-100  { background-color: #ff8080; }

        .container { max-width: 1200px; margin: auto; }
        h1 { text-align: center; }
        input { margin: 10px 0; padding: 5px; width: 50%; }
    </style>
</head>
<body>
<div class="container">
    <h1>PDF/Word Similarity Dashboard</h1>
    <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Search author, folder or similarity...">
    <table id="resultsTable">
        <thead>
            <tr>
                <th>Author 1</th>
                <th>Author 2</th>
                <th>Author 1 Folder</th>
                <th>Author 2 Folder</th>
                <th>Similarity (%)</th>
            </tr>
        </thead>
        <tbody>"""

    def get_sim_class(sim):
        if sim < 0.94:
            return "sim-0"
        elif sim < 0.96:
            return "sim-94"
        elif sim < 0.98:
            return "sim-96"
        elif sim < 0.99:
            return "sim-98"
        else:
            return "sim-100"

    html_rows = ""
    best_matches = {}

    for file1_repr, file2_repr, sim in similar_pairs:
        author1_folder_name = os.path.basename(os.path.dirname(file1_repr))
        author2_folder_name = os.path.basename(os.path.dirname(file2_repr))

        author1_display = get_author_name_from_path(file1_repr, folder1)
        author2_display = get_author_name_from_path(file2_repr, folder2)

        key_tuple = tuple(sorted((author1_display, author2_display)))

        abs_path_folder1 = os.path.abspath(os.path.dirname(file1_repr)).replace('\\', '/')
        abs_path_folder2 = os.path.abspath(os.path.dirname(file2_repr)).replace('\\', '/')

        link_folder1 = f'<a href="file:///{abs_path_folder1}" target="_blank">{author1_folder_name}</a>'
        link_folder2 = f'<a href="file:///{abs_path_folder2}" target="_blank">{author2_folder_name}</a>'

        current_sim_percent = sim * 100

        if key_tuple not in best_matches or current_sim_percent > best_matches[key_tuple][0]:
            best_matches[key_tuple] = (current_sim_percent, link_folder1, link_folder2, author1_display, author2_display)

    for pair_key, (sim_percent, link_folder1, link_folder2, author1_display, author2_display) in best_matches.items():
        sim_class = get_sim_class(sim_percent / 100)
        html_rows += f"<tr class='{sim_class}'><td>{author1_display}</td><td>{author2_display}</td><td>{link_folder1}</td><td>{link_folder2}</td><td>{sim_percent:.2f}%</td></tr>\n"

    html_tail = """</tbody>
    </table>
</div>
<script>
function filterTable() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("searchInput");
    filter = input.value.toLowerCase();
    table = document.getElementById("resultsTable");
    tr = table.getElementsByTagName("tr");
    for (i = 1; i < tr.length; i++) {
        var show = false;
        for (var j = 0; j < 5; j++) {
            td = tr[i].getElementsByTagName("td")[j];
            if (td) {
                txtValue = td.textContent || td.innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    show = true;
                    break;
                }
            }
        }
        tr[i].style.display = show ? "" : "none";
    }
}
</script>
</body>
</html>"""

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_head + html_rows + html_tail)

    print(f"HTML dashboard saved at: {output_html}")

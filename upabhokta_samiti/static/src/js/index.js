function load_ckEditor(fieldname) {
    CKEDITOR.replace(fieldname);
}
load_ckEditor('editor');

var downloadBtn = document.getElementsByName("editor");
function func() {

    var editorContent = CKEDITOR.instances.editor.getData();
    var top = 20, left = 15, right = 15, bottom = 20;
    var options = {
        margin: [top, left, bottom, right],
        filename: 'आयोजनाको_प्रस्तावहरु.pdf',
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { scale: 2 },
        jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    };

    pdfContent = `
                ${editorContent}
    `

    // Use html2pdf library to generate PDF from HTML content
    new html2pdf()
        .from(pdfContent)
        .set(options)
        .save();

}


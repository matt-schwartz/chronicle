// Tracks what files you're working on
// Context: which features you're building

const vscode = require('vscode');

function activate(context) {
    // Track active file changes
    vscode.window.onDidChangeActiveTextEditor(editor => {
        if (editor) {
            sendToServer({
                type: 'ide_activity',
                file: editor.document.fileName,
                language: editor.document.languageId,
                timestamp: Date.now()
            });
        }
    });
}


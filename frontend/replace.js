const fs = require('fs');
const path = require('path');

function walkDir(dir, callback) {
  fs.readdirSync(dir).forEach(f => {
    let dirPath = path.join(dir, f);
    let isDirectory = fs.statSync(dirPath).isDirectory();
    isDirectory ? walkDir(dirPath, callback) : callback(path.join(dir, f));
  });
}

function replaceInFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  let originalContent = content;

  content = content.replace(/Synapse/g, 'Paii');
  content = content.replace(/synapse/g, 'paii');
  content = content.replace(/SYNAPSE/g, 'PAII');
  content = content.replace(/SpendPilot/g, 'Paii');
  content = content.replace(/SpendPilot AI/g, 'Paii AI');

  if (content !== originalContent) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated: ${filePath}`);
  }
}

const dirsToCheck = [
  path.join(__dirname, 'src'),
  path.join(__dirname, 'public')
];

dirsToCheck.forEach(dir => {
  walkDir(dir, replaceInFile);
});

replaceInFile(path.join(__dirname, 'tailwind.config.js'));

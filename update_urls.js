const fs = require('fs');
const path = require('path');

const srcDir = path.join(__dirname, 'react travel', 'Bus-Frontend', 'travels', 'src');
const componentsDir = path.join(srcDir, 'components');
const deepcomponentsDir = path.join(srcDir, 'deepcomponents');

function replaceInDir(dir) {
    if (!fs.existsSync(dir)) return;
    const files = fs.readdirSync(dir);
    for (const file of files) {
        const filePath = path.join(dir, file);
        if (fs.statSync(filePath).isDirectory()) {
            replaceInDir(filePath);
        } else if (file.endsWith('.jsx')) {
            let content = fs.readFileSync(filePath, 'utf8');
            let updatedContent = content;

            // Replace "http://localhost:8000..." with `${import.meta.env.VITE_API_URL || 'http://localhost:8000'}...`
            updatedContent = updatedContent.replace(/"http:\/\/localhost:8000(.*)"/g, '`${import.meta.env.VITE_API_URL || \'http://localhost:8000\'}$1`');
            updatedContent = updatedContent.replace(/'http:\/\/localhost:8000(.*)'/g, '`${import.meta.env.VITE_API_URL || \'http://localhost:8000\'}$1`');
            updatedContent = updatedContent.replace(/`http:\/\/localhost:8000(.*)`/g, '`${import.meta.env.VITE_API_URL || \'http://localhost:8000\'}$1`');

            if (content !== updatedContent) {
                fs.writeFileSync(filePath, updatedContent, 'utf8');
                console.log(`Updated: ${filePath}`);
            }
        }
    }
}

replaceInDir(componentsDir);
replaceInDir(deepcomponentsDir);
console.log('Done replacing URLs');

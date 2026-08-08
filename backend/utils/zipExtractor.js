import AdmZip from "adm-zip";
import fs from "fs";
import path from "path";

/**
 * Extracts a ZIP archive into a destination directory.
 *
 * Security:
 * Prevents ZIP Slip attacks by ensuring that every extracted
 * file remains inside the destination directory.
 *
 * @param {string} zipPath - Absolute path of the ZIP file.
 * @param {string} destinationPath - Absolute extraction directory.
 * @returns {Promise<string>} - Extraction directory path.
 */
const extractZip = async (zipPath, destinationPath) => {
    if (!fs.existsSync(zipPath)) {
        throw new Error(`ZIP file not found: ${zipPath}`);
    }

    fs.mkdirSync(destinationPath, {
        recursive: true
    });

    const zip = new AdmZip(zipPath);
    const entries = zip.getEntries();

    const resolvedDestination = path.resolve(destinationPath);

    for (const entry of entries) {
        const entryPath = path.resolve(
            resolvedDestination,
            entry.entryName
        );

        const isInsideDestination =
            entryPath === resolvedDestination ||
            entryPath.startsWith(`${resolvedDestination}${path.sep}`);

        if (!isInsideDestination) {
            throw new Error(
                `Unsafe ZIP entry detected: ${entry.entryName}`
            );
        }

        if (entry.isDirectory) {
            fs.mkdirSync(entryPath, {
                recursive: true
            });
            continue;
        }

        fs.mkdirSync(path.dirname(entryPath), {
            recursive: true
        });

        fs.writeFileSync(
            entryPath,
            entry.getData()
        );
    }

    return resolvedDestination;
};

export default extractZip;
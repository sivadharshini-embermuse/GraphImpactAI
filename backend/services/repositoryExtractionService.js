import AdmZip from "adm-zip";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const projectRoot = path.join(
    __dirname,
    "..",
    ".."
);

const repositoriesRoot = path.join(
    projectRoot,
    "storage",
    "repositories"
);

const originalRepositoryPath = path.join(
    repositoriesRoot,
    "original"
);

const modifiedRepositoryPath = path.join(
    repositoriesRoot,
    "modified"
);

function clearDirectory(directoryPath) {

    if (fs.existsSync(directoryPath)) {
        fs.rmSync(directoryPath, {
            recursive: true,
            force: true
        });
    }

    fs.mkdirSync(directoryPath, {
        recursive: true
    });
}

export function extractRepositoryZip(
    zipPath,
    repositoryType
) {

    let destinationPath;

    if (repositoryType === "original") {

        destinationPath =
            originalRepositoryPath;

    } else if (repositoryType === "modified") {

        destinationPath =
            modifiedRepositoryPath;

    } else {

        throw new Error(
            "Invalid repository type"
        );
    }

    clearDirectory(
        destinationPath
    );

    const zip = new AdmZip(
        zipPath
    );

    zip.extractAllTo(
        destinationPath,
        true
    );

    return destinationPath;
}
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

import extractZip from "../utils/zipExtractor.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const repositoriesRoot = path.resolve(
    __dirname,
    "../../storage/repositories"
);

const extractRepositories = async (
    originalZipPath,
    modifiedZipPath
) => {
    const originalPath = path.join(
        repositoriesRoot,
        "original"
    );

    const modifiedPath = path.join(
        repositoriesRoot,
        "modified"
    );

    // Remove previous extracted repositories
    if (fs.existsSync(originalPath)) {
        fs.rmSync(originalPath, {
            recursive: true,
            force: true
        });
    }

    if (fs.existsSync(modifiedPath)) {
        fs.rmSync(modifiedPath, {
            recursive: true,
            force: true
        });
    }

    const extractedOriginalPath = await extractZip(
        originalZipPath,
        originalPath
    );

    const extractedModifiedPath = await extractZip(
        modifiedZipPath,
        modifiedPath
    );

    return {
        originalPath: extractedOriginalPath,
        modifiedPath: extractedModifiedPath
    };
};

export default {
    extractRepositories
};
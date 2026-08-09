import multer from "multer";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const uploadRoot = path.join(
    __dirname,
    "..",
    "uploads"
);

const originalDir = path.join(
    uploadRoot,
    "original"
);

const modifiedDir = path.join(
    uploadRoot,
    "modified"
);

fs.mkdirSync(originalDir, {
    recursive: true
});

fs.mkdirSync(modifiedDir, {
    recursive: true
});


const storage = multer.diskStorage({

    destination: (req, file, cb) => {

        if (
            file.fieldname ===
            "originalRepository"
        ) {
            cb(null, originalDir);

        } else if (
            file.fieldname ===
            "modifiedRepository"
        ) {
            cb(null, modifiedDir);

        } else {
            cb(
                new Error(
                    "Invalid upload field"
                )
            );
        }
    },

    filename: (req, file, cb) => {

        const timestamp = Date.now();

        const extension = path.extname(
            file.originalname
        );

        const filename =
            `${timestamp}-${file.fieldname}${extension}`;

        cb(null, filename);
    }
});


const fileFilter = (
    req,
    file,
    cb
) => {

    const extension = path
        .extname(file.originalname)
        .toLowerCase();

    if (extension !== ".zip") {
        return cb(
            new Error(
                "Only ZIP files are allowed"
            )
        );
    }

    cb(null, true);
};


const uploadMiddleware = multer({
    storage,
    fileFilter,

    limits: {
        fileSize:
            100 * 1024 * 1024
    }
});


export default uploadMiddleware;
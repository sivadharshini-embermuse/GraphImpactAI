import multer from "multer";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// GraphImpactAI/uploads
const uploadsRoot = path.resolve(__dirname, "../../uploads");

const originalDirectory = path.join(uploadsRoot, "original");
const modifiedDirectory = path.join(uploadsRoot, "modified");

// Create directories if they don't exist
fs.mkdirSync(originalDirectory, { recursive: true });
fs.mkdirSync(modifiedDirectory, { recursive: true });

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        if (file.fieldname === "originalRepository") {
            cb(null, originalDirectory);
        } else if (file.fieldname === "modifiedRepository") {
            cb(null, modifiedDirectory);
        } else {
            cb(new Error("Invalid repository field."));
        }
    },

    filename: (req, file, cb) => {
        const uniqueName = `${Date.now()}-${file.originalname}`;
        cb(null, uniqueName);
    }
});

const fileFilter = (req, file, cb) => {
    const extension = path.extname(file.originalname).toLowerCase();

    if (extension !== ".zip") {
        return cb(new Error("Only ZIP files are allowed."));
    }

    cb(null, true);
};

const upload = multer({
    storage,
    fileFilter,
    limits: {
        fileSize: 100 * 1024 * 1024
    }
});

export default upload;
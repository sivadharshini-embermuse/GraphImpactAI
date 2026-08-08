import express from "express";
import uploadMiddleware from "../middleware/uploadMiddleware.js";
import uploadController from "../controllers/uploadController.js";

const router = express.Router();

// POST /api/v1/repository/upload
router.post(
    "/upload",
    uploadMiddleware.fields([
        { name: "originalRepository", maxCount: 1 },
        { name: "modifiedRepository", maxCount: 1 }
    ]),
    uploadController.uploadRepositories
);

export default router;
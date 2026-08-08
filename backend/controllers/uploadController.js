import repositoryService from "../services/repositoryService.js";

const uploadRepositories = async (req, res) => {
    try {
        if (
            !req.files?.originalRepository ||
            !req.files?.modifiedRepository
        ) {
            return res.status(400).json({
                success: false,
                message: "Both repositories are required."
            });
        }

        const original =
            req.files.originalRepository[0];

        const modified =
            req.files.modifiedRepository[0];

        const extractedRepositories =
            await repositoryService.extractRepositories(
                original.path,
                modified.path
            );

        return res.status(200).json({
            success: true,
            message: "Repositories uploaded and extracted successfully.",
            data: {
                original: {
                    fileName: original.filename,
                    size: original.size,
                    extractedPath:
                        extractedRepositories.originalPath
                },
                modified: {
                    fileName: modified.filename,
                    size: modified.size,
                    extractedPath:
                        extractedRepositories.modifiedPath
                }
            }
        });
    } catch (error) {
        console.error(
            "Repository upload error:",
            error
        );

        return res.status(500).json({
            success: false,
            message: error.message
        });
    }
};

export default {
    uploadRepositories
};
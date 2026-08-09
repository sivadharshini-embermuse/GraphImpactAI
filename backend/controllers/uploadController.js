import fs from "fs/promises";
import path from "path";
import { fileURLToPath } from "url";
import repositoryService from "../services/repositoryService.js";

import pythonAnalysisService from "../services/pythonAnalysisService.js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const projectRoot = path.resolve(
    __dirname,
    "../.."
);

const uploadRepositories = async (
    req,
    res
) => {

    try {

        // ---------------------------------
        // 1. Validate uploaded files
        // ---------------------------------

        if (
            !req.files?.originalRepository ||
            !req.files?.modifiedRepository
        ) {

            return res.status(400).json({
                success: false,
                message:
                    "Both repositories are required."
            });
        }


        // ---------------------------------
        // 2. Get uploaded files
        // ---------------------------------

        const original =
            req.files.originalRepository[0];

        const modified =
            req.files.modifiedRepository[0];


        console.log(
            "\nOriginal ZIP:",
            original.path
        );

        console.log(
            "Modified ZIP:",
            modified.path
        );


        // ---------------------------------
        // 3. Extract repositories
        // ---------------------------------

        console.log(
            "\nExtracting repositories..."
        );

        const extractedRepositories =
            await repositoryService.extractRepositories(
                original.path,
                modified.path
            );


        console.log(
            "Original extracted to:",
            extractedRepositories.originalPath
        );

        console.log(
            "Modified extracted to:",
            extractedRepositories.modifiedPath
        );


        // ---------------------------------
        // 4. Run Python GraphImpact AI
        // ---------------------------------

        console.log(
            "\nStarting GraphImpact AI analysis..."
        );

        const analysisResult =
            await pythonAnalysisService.runPythonAnalysis(
                extractedRepositories.originalPath,
                extractedRepositories.modifiedPath
            );


        console.log(
            "\nGraphImpact AI analysis completed."
        );


        // ---------------------------------
        // 5. Read final analysis report
        // ---------------------------------

        const reportPath = path.join(
            projectRoot,
            "analyzer",
            "data",
            "outputs",
            "final_analysis_report.json"
        );


        const reportContent =
            await fs.readFile(
                reportPath,
                "utf-8"
            );


        const report =
            JSON.parse(
                reportContent
            );


        // ---------------------------------
        // 6. Send final response
        // ---------------------------------

        return res.status(200).json({

            success: true,

            message:
                "Repositories analyzed successfully.",

            data: {

                original: {
                    fileName:
                        original.originalname,

                    size:
                        original.size,

                    extractedPath:
                        extractedRepositories.originalPath
                },

                modified: {
                    fileName:
                        modified.originalname,

                    size:
                        modified.size,

                    extractedPath:
                        extractedRepositories.modifiedPath
                },

                analysis: report
            }

        });

    } catch (error) {

        console.error(
            "\nRepository analysis error:",
            error
        );


        return res.status(500).json({

            success: false,

            message:
                "Repository analysis failed.",

            error:
                error.message

        });
    }
};


export default {
    uploadRepositories
};
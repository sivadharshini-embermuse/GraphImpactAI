import pythonAnalysisService from "./pythonAnalysisService.js";

const originalPath =
    "storage/repositories/original";

const modifiedPath =
    "storage/repositories/modified";

try {

    const result =
        await pythonAnalysisService.runPythonAnalysis(
            originalPath,
            modifiedPath
        );

    console.log(
        "\nPython analysis completed successfully."
    );

    console.log(
        result.output
    );

} catch (error) {

    console.error(
        "\nPython analysis failed:"
    );

    console.error(
        error.message
    );
}
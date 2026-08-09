import { spawn } from "child_process";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const projectRoot = path.resolve(
    __dirname,
    "../.."
);

const runPythonAnalysis = (
    originalRepositoryPath,
    modifiedRepositoryPath
) => {

    return new Promise(
        (resolve, reject) => {

            const pythonProcess = spawn(
                "python",
                [
                    "-m",
                    "analyzer.pipeline.analysis_pipeline",
                    originalRepositoryPath,
                    modifiedRepositoryPath
                ],
                {
                    cwd: projectRoot
                }
            );

            let output = "";
            let errorOutput = "";

            pythonProcess.stdout.on(
                "data",
                (data) => {

                    output += data.toString();

                    console.log(
                        `[Python] ${data.toString()}`
                    );
                }
            );

            pythonProcess.stderr.on(
                "data",
                (data) => {

                    errorOutput += data.toString();

                    console.error(
                        `[Python Error] ${data.toString()}`
                    );
                }
            );

            pythonProcess.on(
                "close",
                (code) => {

                    if (code === 0) {

                        resolve({
                            success: true,
                            output
                        });

                    } else {

                        reject(
                            new Error(
                                errorOutput ||
                                `Python process exited with code ${code}`
                            )
                        );
                    }
                }
            );

            pythonProcess.on(
                "error",
                (error) => {

                    reject(error);
                }
            );
        }
    );
};

export default {
    runPythonAnalysis
};
const express = require("express");

const upload = require(
    "../middleware/uploadMiddleware"
);

const router = express.Router();


router.get("/test", (req, res) => {

    res.json({
        success: true,
        message: "Analysis route is working"
    });

});


router.post(
    "/upload",

    upload.fields([
        {
            name: "originalRepository",
            maxCount: 1
        },
        {
            name: "modifiedRepository",
            maxCount: 1
        }
    ]),

    (req, res) => {

        res.json({
            success: true,

            message:
                "Repositories uploaded successfully",

            files: {
                original:
                    req.files.originalRepository
                        ? req.files.originalRepository[0].filename
                        : null,

                modified:
                    req.files.modifiedRepository
                        ? req.files.modifiedRepository[0].filename
                        : null
            }
        });

    }
);


module.exports = router;
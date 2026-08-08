import express from "express";
import cors from "cors";
import morgan from "morgan";
import uploadRoutes from "./routes/uploadRoutes.js";

const app = express();

// Middlewares
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(morgan("dev"));
app.use("/api/v1/repository", uploadRoutes);


app.get("/", (req, res) => {
    res.json({
        success: true,
        message: "GraphImpact AI Backend Running 🚀"
    });
});

export default app;
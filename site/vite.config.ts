import { defineConfig } from "vite";

export default defineConfig({
  // Relative assets work both at localhost and under a GitHub Pages project path.
  base: "./",
  build: {
    outDir: "dist",
    emptyOutDir: true,
    sourcemap: true,
    rollupOptions: {
      output: {
        manualChunks(id) {
          return id.includes("node_modules/three") ? "three" : undefined;
        },
      },
    },
  },
  server: {
    // The deterministic visualization fixture is shared with the Manim source.
    fs: { allow: [".."] },
  },
});

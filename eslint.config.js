import path from "node:path";
import { fileURLToPath } from "node:url";

import js from "@eslint/js";
import tsParser from "@typescript-eslint/parser";
import tsPlugin from "@typescript-eslint/eslint-plugin";
import reactPlugin from "eslint-plugin-react";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";

const tsconfigRootDir = path.dirname(fileURLToPath(import.meta.url));

export default [
  {
    ignores: ["dist", "coverage", "node_modules"],
  },
  js.configs.recommended,
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        project: "./tsconfig.json",
        tsconfigRootDir,
        ecmaVersion: 2020,
        sourceType: "module",
      },
      globals: {
        ...globals.browser,
        console: "readonly",
      },
    },
    plugins: {
      "@typescript-eslint": tsPlugin,
      react: reactPlugin,
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...tsPlugin.configs["recommended-type-checked"].rules,
      ...reactPlugin.configs.recommended.rules,
      ...reactPlugin.configs["jsx-runtime"].rules,
      ...reactHooks.configs.recommended.rules,
      "react-refresh/only-export-components": "warn",
    },
    settings: {
      react: {
        version: "detect",
      },
    },
  },
];

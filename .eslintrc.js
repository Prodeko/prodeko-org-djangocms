module.exports = {
  root: true,
  parserOptions: {
    ecmaVersion: 8,
    sourceType: "script"
  },
  env: {
    browser: true,
    jquery: true
  },
  globals: {
    dataLayer: "readonly",
    SimpleCrop: "readonly"
  },
  plugins: ["jquery", "prettier"],
  extends: ["eslint:recommended", "prettier", "plugin:prettier/recommended"],
  rules: {
    "prettier/prettier": "error"
  }
};

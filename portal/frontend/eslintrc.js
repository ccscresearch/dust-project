/** @type {import('eslint').Linter.Config} */
// eslint-disable-next-line no-undef
module.exports = {
  env: {
    browser: true,
    es2021: true,
    jest: true,
    node: true,
  },
  ignorePatterns: ['**/*.d.ts', 'dist'],
  extends: [
    'plugin:react/recommended',
    'airbnb',
    'prettier',
    'plugin:@typescript-eslint/recommended',
    'plugin:react-hooks/recommended',
  ],
  parser: '@typescript-eslint/parser',
  parserOptions: {
    ecmaVersion: 2020,
    sourceType: 'module',
    ecmaFeatures: {
      jsx: true,
    },
  },
  plugins: [
    '@typescript-eslint',
    'react',
    'prettier',
    'import',
    'unused-imports',
    'eslint-plugin-import-helpers',
    'react-hooks',
  ],
  settings: {
    react: {
      fragment: 'Fragment',
      version: 'detect',
    },
  },
  rules: {
    'import/extensions': 'off',
    'react/jsx-filename-extension': [
      'error',
      { extensions: ['.js', '.jsx', '.tsx'] },
    ],
    'import/no-unresolved': 'off',
    'prettier/prettier': [
      'error',
      {
        singleQuote: true,
        endOfLine: 'auto',
        parser: 'typescript',
        tabWidth: 2,
        printWidth: 90,
      },
    ],
    'react/no-array-index-key': 'off',
    'react/jsx-props-no-spreading': 'off',
    'import/prefer-default-export': 'off',
    'react/jsx-curly-newline': 'off',
    'react/react-in-jsx-scope': 'off',
    'react/button-has-type': 'off',
    'react/destructuring-assignment': 'off',
    'react/require-default-props': 'off',
    'react/default-props-match-prop-types': 'off',
    'import-helpers/order-imports': [
      'warn',
      {
        newlinesBetween: 'always',
        groups: [
          '/^react/',
          '/^@react/',
          '/prop-types/',
          '/^@/shared/functions/',
          '/^@/shared/components/',
          '/^@/shared/analytics/',
          'module',
          '/^@/redux/',
          '/^@/assets/',
          'sibling',
        ],
        alphabetize: {
          order: 'asc',
          ignoreCase: true,
        },
      },
    ],
    'react/prop-types': 'off',
    '@typescript-eslint/no-unused-vars': [
      'error',
      { ignoreRestSiblings: true },
    ],
    '@typescript-eslint/explicit-module-boundary-types': 'off',
    '@typescript-eslint/no-empty-function': 'off',
    '@typescript-eslint/no-explicit-any': 'error',
    '@typescript-eslint/no-non-null-assertion': 'off',
    'no-console': 1,
    'react-hooks/exhaustive-deps': 'error',
    'no-use-before-define': 'off',
    '@typescript-eslint/no-use-before-define': 'off',
    'no-undef': 'error',
    'no-empty': 'error',
    'no-var': 'error',
    'react/display-name': 'off',
    'react/jsx-curly-brace-presence': [
      1,
      { props: 'never', children: 'never' },
    ],
    'react/no-unescaped-entities': 0,
    'no-nested-ternary': 'error',
  },
  globals: {
    process: true,
    React: true,
    JSX: true,
    global: true,
    Action: true,
    setImmediate: true,
    Buffer: true,
  },
};

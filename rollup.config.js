import resolve from '@rollup/plugin-node-resolve';

export default {
  input: 'C:/Users/massa/Documents/GitHub/PhD/IFCViewer/_app01/app.js',
  output: [
    {
      format: 'esm',
      file: 'C:/Users/massa/Documents/GitHub/PhD/IFCViewer/_app01/bundle.js',
    },
  ],
  plugins: [
    resolve(),
  ]
};
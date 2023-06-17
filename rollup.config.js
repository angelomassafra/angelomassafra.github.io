import resolve from '@rollup/plugin-node-resolve';

export default {
  input: 'C:/Users/massa/Documents/GitHub/PhD/IFCViewer/_app02/app.js',
  output: [
    {
      format: 'esm',
      file: 'C:/Users/massa/Documents/GitHub/PhD/IFCViewer/_app02/bundle.js',
    },
  ],
  plugins: [
    resolve(),
  ]
};
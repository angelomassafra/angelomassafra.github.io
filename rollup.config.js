import resolve from '@rollup/plugin-node-resolve';

export default {
  input: 'C:/Users/massa/Documents/GitHub/PhD/IFC_Viewer/App02/app.js',
  output: [
    {
      format: 'esm',
      file: 'C:/Users/massa/Documents/GitHub/PhD/IFC_Viewer/App02/bundle.js',
    },
  ],
  plugins: [
    resolve(),
  ]
};
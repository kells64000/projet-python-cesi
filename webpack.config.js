const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

module.exports = {
    mode: 'production',
    entry: './static/js/app.js',
    output: {
        path: path.resolve('./static/build/public/'),
        filename: 'js/app.js'
    },
    plugins: [
        new MiniCssExtractPlugin({
          filename: 'css/app.css',
          chunkFilename: '[id].css'
        })
    ],
    resolve: {
        extensions: ['.js', '.scss']
    },
    module: {
        rules: [
            {
                test: /\.js$/i,
                exclude: /node_modules/,
                loader: 'babel-loader'
            },
            {
                test: /\.(sa|sc|c)ss$/i,
                use: [
                 MiniCssExtractPlugin.loader,
                 "css-loader",
                 // 'postcss-loader',
                 "sass-loader"
                ]
            }
        ]
    }
};
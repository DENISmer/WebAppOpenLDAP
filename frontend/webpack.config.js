const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ReactRefreshWebpackPlugin = require('@pmmmwh/react-refresh-webpack-plugin');

let mode = 'development';
let port = process.env.port;
let target = 'web';

if (process.argv[4] !== 'development') {
    mode = 'production';
    target = 'browserslist';
}

console.log("!!!mode =", process.argv[4]);


const cssLoader = (extra) => {
    const loaders = [
        {
            loader: MiniCssExtractPlugin.loader,
            options: {
                //hmr: mode === 'development',
                // reloadAll: true,
                filename: '[name].[contenthash].css'
            }
        },'css-loader',
    ]
    if(extra) {
        loaders.push(extra);
    }
    return loaders;
}

const plugins = [
    new MiniCssExtractPlugin({
        filename: mode === 'production' ? "[name].[contenthash].css" : "[name].css"
    }),
    new HtmlWebpackPlugin({
        template: './src/index.html',
    }),
];

if (process.env.SERVE) {
    plugins.push(new ReactRefreshWebpackPlugin());
}

module.exports = {
    mode,
    target,
    plugins,
    devtool: mode === 'source-map',
    entry: './src/index.tsx',

    devServer: {
        port: port ?? 3000,
        open : true,
        historyApiFallback: true,
        static: './build',
        hot: mode === 'development',
    },

    output: {
        path: path.resolve(__dirname, 'build'),
        filename: "[name].[contenthash].js",
        assetModuleFilename: 'assets/[name][hash][ext][query]',
        clean: true,
        publicPath: '/'
    },
    module: {
        rules: [
            {
                test: /\.(html)$/, use: ['html-loader']
            },
            //loading css
            {
                test: /\.css$/,
                use: cssLoader(),
                exclude: /\.module\.css$/
            },
            //Loading scss/sass
            {
                test: /\.s?css$/,
                oneOf: [
                    {//add scss modules
                        test: /\.module\.s?css$/,
                        use: [
                            MiniCssExtractPlugin.loader,
                            {
                                loader: "css-loader",
                                options: {
                                    modules: {
                                        localIdentName: mode === 'development' ? "[name]__[local]" : "[hash]",
                                    },
                                }
                            },
                            "sass-loader"
                        ]
                    },
                    {
                        use: [MiniCssExtractPlugin.loader, "css-loader", "sass-loader"]
                    }
                ]
            },
            {
                test: /\.(png|jpe?g|gif|svg|webp|ico)$/i,
                type: mode === 'production' ? 'asset' : 'asset/resource',
            },
            {
                test: /\.(woff2?|eot|ttf|otf)$/i,
                type: 'asset/resource',
            },
            {
                test: /\.ts(x?)$/,
                use: [
                    'ts-loader',
                ],
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: ['.js', '.ts', '.tsx','.scss','.module.scss','.css','.png'],
        alias: {
            '@': path.resolve(__dirname,'src')
        }
    },
};

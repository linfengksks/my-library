module.exports = {
    //关闭语法检查
    lintOnSave: false,
    //代理服务器
    devServer: {
        proxy: {
            '/django': {
                target: 'http://127.0.0.1:8000',
                pathRewrite: {'^/django': ''}, //发请求时，正则匹配，将/page变为空
                ws: true,
                changeOrigin: true//当服务器问代理服务的请求头的值是什么的什么的时候，true：返回服务器的端口，false：返回真实的端口
            }
        }
    }
}

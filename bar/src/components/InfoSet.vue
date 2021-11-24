<template>
    <div class="InfoSet Theme">
        <div class="Info"><p class="title">设置个人信息</p>
            <!-- 预览头像 -->
            <p><img class="portrait" :src="lookPortrait()" alt="头像" width="115" height="115"></p>
            <input type="file" id="file" @change="getPortrait()" ref="inputs">
            <button @click="openCropper">裁剪图片</button>
            <button @click="handleFileChange()">提交请求</button>
            <p>昵&nbsp;&nbsp;&nbsp;&nbsp;称 <span v-show="is_active">:{{showData(nick_name)}}</span>
                <el-input v-show="!is_active" class='info_input' placeholder="请输入昵称" v-model="nick_name"
                          clearable></el-input>
            </p>
            <p>年&nbsp;&nbsp;&nbsp;&nbsp;龄<span v-show="is_active">:{{showData(age)}}</span>
                <el-input v-show="!is_active" class='info_input' placeholder="请输入年龄" v-model="age" clearable></el-input>
            </p>
            <p>性&nbsp;&nbsp;&nbsp;&nbsp;别<span v-show="is_active">:{{showData(sex)}}</span>
                <el-input v-show="!is_active" class='info_input' placeholder="请输入性别" v-model="sex" clearable></el-input>
            </p>
            <p>身份证<span v-show="!is_id_card">:{{showData(id_card)}}</span>
                <el-input v-show="is_id_card" class='info_input' placeholder="身份证只能设置一次，请谨慎填写" v-model="id_card"
                          clearable></el-input>
            </p>
            <el-button v-show="is_active" @click="showSet" class="setBut" type="primary">编辑</el-button>
            <el-button v-show="is_active" @click='re_app' class="setBut" type="primary">返回</el-button>
            <el-button v-show='!is_active' @click="preInfo" class="setBut" type="primary">保存</el-button>
            <el-button v-show='!is_active' @click="removeSet" class="setBut" type="primary">取消</el-button>
        </div>
        <!--裁剪功能-->
        <div v-show="cropper" class="cropper">
            <div class="cut">
                <vue-cropper ref="cropper" :img="option.img" :output-size="option.size" :output-type="option.outputType"
                             :info="true" :full="option.full" :fixed="option.fixed" :fixed-number="option.fixedNumber"
                             :can-move="option.canMove" :can-move-box="option.canMoveBox" :fixed-box="option.fixedBox"
                             :original="option.original"
                             :auto-crop="option.autoCrop" :auto-crop-width="option.autoCropWidth"
                             :auto-crop-height="option.autoCropHeight" :center-box="option.centerBox"
                             @real-time="realTime" :high="option.high"
                ></vue-cropper>
                <!--                &lt;!&ndash;图片下载功能&ndash;&gt;-->
                <!--                <a @click="down('base64')" class="btn">download(base64)</a>-->
                <!--                <a @click="down('blob')" class="btn">download(blob)</a>-->
                <div class="preview_s"><p>头像预览</p>
                    <!--显示预览-->
                    <div class="show-preview"
                         :style="{'width': 100+ 'px', 'height': 100 + 'px',  'overflow': 'hidden', 'margin': '5px'}">
                        <div :style="previewStyle">
                            <div :style="previews.div">
                                <img :src="previews.url" :style="previews.img">
                            </div>
                        </div>
                    </div>
                    <button @click="enter">保存图片</button>
                    <br>
                    <button @click="cropper=!cropper">取消裁剪</button>
                </div>

            </div>

            <!-- ---------------------------------------------------- -->
        </div>

    </div>
</template>

<script>
    import axios from 'axios'

    export default {
        name: "InfoSet",
        data() {
            return {
                //判断用户是否执行裁剪
                is_id_card: false,
                is_cropper: false,
                previewStyle: '',
                is_active: true,
                uploadImg: '',
                // 图片裁剪配置
                cropper: false,
                previews: {},
                option: {
                    img: '',
                    size: 1,
                    full: false,
                    outputType: 'png',
                    canMove: true,
                    fixedBox: true,
                    original: true,
                    canMoveBox: true,
                    autoCrop: true,
                    // 只有自动截图开启 宽度高度才生效
                    autoCropWidth: 200,
                    autoCropHeight: 200,
                    centerBox: false,
                    high: true,
                    max: 99999,
                    show: true,
                    fixed: true,
                    fixedNumber: [1, 1]
                },
            }
        },
        methods: {
            // 头像展示
            lookPortrait() {
                // 如果uploadImg没有选择图片就展示用户资料内的头像
                if (!this.uploadImg) {
                    return this.portrait
                }
                // 如果uploadImg有图片，就展示uploadImg
                else if (this.uploadImg) {
                    return this.uploadImg
                }
            },

            // 裁剪功能
            openCropper() {
                this.option.img = this.uploadImg
                if (!this.uploadImg) {
                    alert('图片不存在，请选择图片后再试')
                    return
                }
                this.cropper = true
            },
            startCrop() {
                // start
                this.crap = true
                this.$refs.cropper.startCrop()
            },
            stopCrop() {
                //  stop
                this.crap = false
                this.$refs.cropper.stopCrop()
            },
            // 实时预览函数
            realTime(data) {
                var previews = data
                var h = 0.5

                this.previewStyle = {
                    width: previews.w + "px",
                    height: previews.h + "px",
                    overflow: "hidden",
                    margin: "0",
                    zoom: h // zoom 控制预览图的比例
                }
                this.previews = data
            },
            enter() {
                if (!confirm('确定截图吗？')) {
                    return;
                }
                if (this.uploadImg === "") {
                    return;
                }
                // console.log("开始截图");
                this.$refs.cropper.startCrop(); //开始裁剪
                this.$refs.cropper.stopCrop();//停止裁剪
                this.$refs.cropper.getCropData(data => { //获取截图的base64格式数据
                    this.uploadImg = data;
                });
                this.cropper = false //取消裁剪窗口
                // 当用户裁剪后
                this.is_cropper = true

            },
            //预览头像
            getPortrait() {
                let src = window.URL.createObjectURL(this.$refs.inputs.files[0])
                this.uploadImg = src
                //当用户选择图片后
                this.is_cropper = false
                // this.option.img = src
            },
            //上传文件
            handleFileChange() {
                // 判断当前是否有文件上传
                if (!this.$refs.inputs.files[0]) {
                    alert('错误：请选择图片后上传')
                    return;
                }
                if (!confirm('确认保存头像吗？')) {
                    return;
                }
                //判断下用户是否经过裁剪后提交，如个是执行下面这个
                if (this.is_cropper) {
                    // 原文件的数据
                    let old_file = this.$refs.inputs.files[0]
                    // 将base64转换为文件
                    let arr = this.uploadImg.split(',')
                    let mime = arr[0].match(/:(.*?);/)[1]
                    let bstr = atob(arr[1])
                    let n = bstr.length
                    let u8arr = new Uint8Array(n)
                    while (n--) {
                        u8arr[n] = bstr.charCodeAt(n);
                    }
                    this.file = new File([u8arr], old_file.name, {type: mime})
                }
                if (!this.is_cropper) {
                    this.file = this.$refs.inputs.files[0]
                }
                // console.log(this.file)
                // console.log(this.uploadImg)
                const formData = new FormData()
                // 往 FormData 里面添加文件
                // formData.append('file', this.file)
                formData.append('file', this.file)
         
                //通过get获取csrf_token值并保存
                axios.get('http://localhost:8080/django/user/login').then(res => {
                    const csrf_token = res.data
                    window.sessionStorage.setItem('csrf_token', csrf_token)
                })
                // 上传 formData
                axios({
                    method: 'post',
                    url: 'http://localhost:8080/django/user/post_por',
                    data: formData,
                    // dataType: "formData",
                    // processData: false,
                    headers: {
                        //将csrf_token放在请求头中
                        'X-CSRFToken': window.sessionStorage.getItem("csrf_token"),
                        // 值得注意的是，这个地方一定要把请求头更改一下
                        // "Content-Type": "multipart/form-data; boundary=----WebKitFormBoundarysm4UsABVM6CHmwTw"
                        "Content-Type": "multipart/form-data"
                    }
                }).then(res => {
                    if (res.data['code'] === 400) {
                        alert(res.data['message'])
                    }
                    if (res.data['code'] === 200) {
                        alert(res.data['message'])
                        location.reload()
                    }
                }, err => {
                    console.log('失败：' + err.message)
                })
            },
            // 取消按键，is_active 取反后刷新页面
            removeSet() {
                // 判断下身份证如果有资料就不允许修改

                this.is_id_card = false
                this.is_active = !this.is_active
                location.reload()
            },
            // 显示数据，当数据不存在时，显示无，有的数据显示数据本身
            showData(data) {
                if (!data) {
                    return '无'
                }
                if (data) {
                    return data
                }
            },
            //显示编辑输入框
            showSet() {
                // 判断下身份证如果有资料就不允许修改
                if (this.id_card) {
                    this.is_id_card = false
                }
                if (!this.id_card) {
                    this.is_id_card = true
                }
                this.is_active = !this.is_active
            },
            //返回主页
            re_app() {
                this.$router.push({
                    name: 'app'
                })
            },
            //保存编辑后的个人资料
            preInfo() {
                if (confirm('请确认保存资料吗？')) {
                    //    通过跨域来提交数据
                    axios.get('http://localhost:8080/django/user/info', {
                        params: {
                            nick_name: this.nick_name,
                            age: this.age,
                            sex: this.sex,
                            id_card: this.id_card
                        }
                    }).then(res => {
                        if (res.data['code'] === 200) {
                            alert(res.data['message'])
                            location.reload()
                        }
                        if (res.data['code'] === 400) {
                            alert(res.data['message'])
                        }

                    }, err => {
                        console.log(err.message)
                    })
                }
            }

        },
        // watch: {
        //     uploadImg: {
        //         immediate: true,
        //         handler(newValue, oldValue) {
        //             console.log('ishot被修改了新值：' + newValue + '旧值：' + oldValue)
        //             if (newValue) {
        //                 this.cropper = true
        //             }
        //         }
        //     }
        // },
        computed: {
            nick_name: {
                get() {
                    return this.$store.state.nick_name
                },
                set(value) {
                    this.$store.commit('Set_nick_name', value)
                }
            },
            age: {
                get() {
                    return this.$store.state.age
                },
                set(value) {
                    this.$store.commit('Set_age', value)
                }
            },
            sex: {
                get() {
                    return this.$store.state.sex
                },
                set(value) {
                    this.$store.commit('Set_sex', value)
                }
            },
            id_card: {
                get() {
                    return this.$store.state.id_card
                },
                set(value) {
                    this.$store.commit('Set_id_card', value)
                }
            },
            portrait: {
                // eslint-disable-next-line vue/return-in-computed-property
                get() {
                    if (!this.$store.state.portrait) {
                        return ''
                    } else if (this.$store.state.portrait) {
                        let src = '/django/media/' + this.$store.state.portrait
                        // let src = this.$store.state.portrait
                        return src
                    }

                },
            },
        }
    }
</script>

<style scoped>

    .show-preview {
        position: relative;
        left: 40%;
        border-radius: 5px;
        border: 3px solid white;
        box-shadow: 1px 2px 2px #878787;
    }

    .cut {
        width: 500px;
        height: 500px;
        margin: 30px auto;
        position: relative;
        top: 25px;
        left: -70px;
    }

    .cropper {
        width: 700px;
        height: 550px;
        background-color: #f3f3f3;
        box-shadow: 1px 3px 5px #878787;
        position: relative;
        top: -400px;
        left: 200px;
        border-radius: 10px;

    }

    .preview_s {
        position: relative;
        left: 330px;
        top: -500px;
    }

    @keyframes slide {
        0% {
            background-position: 0 0;
        }
        100% {
            background-position: -100% 0;
        }
    }

    * {
        font-family: 思源黑体R;
        color: #414157;
        text-align: center;
    }

    .title {
        font-size: 30px;
    }

    .InfoSet {
        width: 1160px;
        height: 850px;
        background-color: white;
        border-radius: 5px;
    }

    .Info {
        position: relative;
        top: 100px;
    }

    .info_input {
        width: 300px;
        padding: 0 5px;
    }

    .setBut {
        background-color: #262c3e;
        color: white;
        border-color: #414157;
    }

    .setBut:hover {
        background-color: #414157;
    }

    /*    -------上传样式----------*/
    .avatar-uploader .el-upload {
        border: 1px dashed #d9d9d9;
        border-radius: 6px;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }

    .avatar-uploader .el-upload:hover {
        border-color: #409EFF;
    }

    .avatar-uploader-icon {
        font-size: 28px;
        color: #8c939d;
        width: 178px;
        height: 178px;
        line-height: 178px;
        text-align: center;
    }

    .avatar {
        width: 178px;
        height: 178px;
        display: block;
    }

    .portrait {
        width: 100px;
        height: 100px;
        background-color: white;
        border-radius: 5px;
        border: solid 3px white;
        box-shadow: 1px 2px 2px #878787;
    }
</style>
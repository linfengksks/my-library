<template>
    <div class="MoreInfo">
        <p class="title1">爱逛的主题</p>
        <ul class="bar_ul">
            <li class="bar_name"><span class="purple"></span><span>冒险岛</span></li>
            <li class="bar_name"><span class="purple"></span><span>刀剑神域</span></li>
            <li class="bar_name"><span class="purple"></span><span>爱奇艺</span></li>
        </ul>
        <ul class="bar_ul">
            <li class="bar_name"><span class="purple"></span><span>冒险岛</span></li>
            <li class="bar_name"><span class="purple"></span><span>刀剑神域</span></li>
            <li class="bar_name"><span class="purple"></span><span>爱奇艺</span></li>
        </ul>
        <p class="mores">查看更多</p>
        <div class="ad">
            <img src="../static/广告1.png">
            <img src="../static/广告2.png">
        </div>


    </div>
</template>

<script>
    export default {
        name: "MoreInfo"
    }
</script>

<style scoped>
    * {
        font-family: 思源黑体R;
        font-size: 20px;
    }

    .MoreInfo {
        width: 400px;
        height: 545px;
        background-color: white;
    }

    .bar_name li {
        display: inline;
        padding: 2px 12px;
        border: solid 1px #414157;
        color: #414157;
        margin: 3px 10px;
    }

    .purple {
        float: left;
        position: absolute;
        left: -11px;
        top: 0px;
        height: 25px;
        background-color: #414157;
        border: 0px solid;
        width: 5px;
        margin: 0 10px;
    }


    .bar_name {
        position: relative;
        left: -30px;
        display: inline;
        padding: 2px 12px;
        border: solid 1px #414157;
        color: #414157;
        margin: 3px 10px;
    }

    .title1 {
        position: relative;
        left: 15px;
        color: #414157;
    }

    .mores {
        color: #414157;
        border: solid 1px #414157;
        text-align: center;
        width: 150px;
        border-radius: 5px;
        padding: 3px 5px;
        margin: 0 auto;
    }

    .ad {
        position: relative;
        top: 10px;
        left: 10px;
    }
    .bar_ul{
        position: relative;
        left:20px;
    }
</style>
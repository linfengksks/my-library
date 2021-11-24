import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const actions = {}
const mutations = {
    SetUserName(state, value) {
        state.username = value
    },
    Set_nick_name(state, value) {
        state.nick_name = value
    },
    Set_age(state, value) {
        state.age = value
    },
    Set_sex(state, value) {
        state.sex = value
    },
    Set_id_card(state, value) {
        state.id_card = value
    },
    Set_bar_coin(state, value) {
        state.bar_coin = value
    },
    Set_exp(state, value) {
        state.exp = value
    },
    Set_portrait(state, value) {
        state.portrait = value
    }
}
const state = {
    username: '',
    user_id: '',
    nick_name: '',
    age: '',
    sex: '',
    id_card: '',
    bar_coin: 20,
    exp: 0,
    portrait: '',
    resultData: '',
}

export default new Vuex.Store({
    actions,
    mutations,
    state
})
<template>
    <form v-on:submit.prevent="submit">
        <input v-model="login" placeholder="login">
        <input type="password" v-model="password" placeholder="password">
        <input type="submit" value="login">
    </form>
</template>

<script>
    export default {
        data(){
            return{
                login:"",
                password:"",
            }
        },
        methods:{
            submit(){
                console.log(this.login, this.password)
            }
        }
    }
</script>

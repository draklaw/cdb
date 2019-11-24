<template>
    <div>
        <h2>{{collection.title}}</h2>
        <collection-table v-bind:collection="collection"></collection-table>
    </div>
</template>

<script>
import CollectionTable from '@/components/collection_table.vue'

    export default {
        data(){
            return{
                collection:{
                    headers:[
                        {id:1, label:"Nom", field:"title"},
                        {id:2, label:"Nombre", field:"count"},
                    ],
                    items: [
                        {id:1, title:"test", count:42},
                        {id:2, title:"test2", count:421},
                        {id:3, title:"test3", count:422},
                        {id:4, title:"test4", count:423},
                    ]
                }
            }
        },
        methods:{
        },
        components:{
            CollectionTable,
        }
    }
</script>

<script>
    export default{
        data(){
            return{}
        },
        props:["collection"],
        render(h){
            return h("table",[
                h("thead", [
                    h("tr", this.collection.headers.map((header)=>
                            h("th", {key:header.id}, header.label)
                    ))
                ]),
                h("tbody", this.collection.items.map((item)=>
                    h("tr", {key:item.id},this.collection.headers.map((header)=>
                        h("td", {key:header.id},item[header.field].toString())
                    ))
                ))
            ])
        }
    }
</script>

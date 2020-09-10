<template>
        <div class="container">
                <div class="col-lg-6">
                        <button class="btn btn-success" @click="get_items">Get Items</button>
                        <hr>
                        <ul class="list-group"><Item  v-for="item in items" :item=item :key=item.item_code></Item></ul>
                </div>
                <div class="col-log-6">
                       <OrganizationChart :value="data1" :collapsible="true" class="company" selectionMode="single" :selectionKeys.sync="selection"
                        @node-select="onNodeSelect" @node-unselect="onNodeUnselect" @node-collapse="onNodeCollapse" @node-expand="onNodeExpand">
                        <template #person="slotProps">
                                <div class="node-header ui-corner-top">{{slotProps.node.data.label}}</div>
                                <div class="node-content">
                                <img :src="'demo/images/organization/' + slotProps.node.data.avatar" width="32">
                                <div>{{slotProps.node.data.name}}</div>
                                </div>
                        </template>
                        <template #default="slotProps">
                                <span>{{slotProps.node.data.label}}</span>
                        </template>
                        </OrganizationChart>
                </div>

        </div>
</template>

<script>
        import ButtonCounter from './ButtonCounter.vue'
        import OrganizationChart from './components/organizationchart.umd.min.js';
        // import ToastService from './components/toastservice.umd.min.js';
        // import ToastService from './toastservice';
        // Vue.use(ToastService);

        export default {
                name: "ToolRoot",
                data: function () {
                        return {
                                items: [],
                                  data1: {
                                        key: '0',
                                        type: 'person',
                                        styleClass: 'p-person',
                                        data: {label: 'CEO', name: 'Walter White', avatar: '../../../assets/csf_tz/js/export_tool/saul.jpg'},
                                        children: [
                                                {
                                                        key: '0_0',
                                                        type: 'person',
                                                        styleClass: 'p-person',
                                                        data: {label: 'CFO', name:'Saul Goodman', avatar: '../../../assets/csf_tz/js/export_tool/saul.jpg'},
                                                        children:[{
                                                        key: '0_0_0',
                                                        data: {label: 'Tax'},
                                                        selectable: false,
                                                        styleClass: 'department-cfo'
                                                        },
                                                        {
                                                        key: '0_0_1',
                                                        data: {label: 'Legal'},
                                                        selectable: false,
                                                        styleClass: 'department-cfo'
                                                        }],
                                                },
                                                {
                                                        key: '0_1',
                                                        type: 'person',
                                                        styleClass: 'p-person',
                                                        data: {label: 'COO', name:'Mike E.', avatar: '../../../assets/csf_tz/js/export_tool/saul.jpg'},
                                                        children:[{
                                                        key: '0_1_0',
                                                        data: {label: 'Operations'},
                                                        selectable: false,
                                                        styleClass: 'department-coo'
                                                        }]
                                                },
                                                {
                                                        key: '0_2',
                                                        type: 'person',
                                                        styleClass: 'p-person',
                                                        data: {label: 'CTO', name:'Jesse Pinkman', avatar: '../../../assets/csf_tz/js/export_tool/saul.jpg'},
                                                        children:[{
                                                        key: '0_2_0',
                                                        data: {label: 'Development'},
                                                        selectable: false,
                                                        styleClass: 'department-cto',
                                                        children:[{
                                                                key: '0_2_0_0',
                                                                data: {label: 'Analysis'},
                                                                selectable: false,
                                                                styleClass: 'department-cto'
                                                        },
                                                        {
                                                                key: '0_2_0_1',
                                                                data: {label: 'Front End'},
                                                                selectable: false,
                                                                styleClass: 'department-cto'
                                                        },
                                                        {
                                                                key: '0_2_0_2',
                                                                data: {label: 'Back End'},
                                                                selectable: false,
                                                                styleClass: 'department-cto'
                                                        }]
                                                        },
                                                        {
                                                        key: '0_2_1',
                                                        data: {label: 'QA'},
                                                        selectable: false,
                                                        styleClass: 'department-cto'
                                                        },
                                                        {
                                                        key: '0_2_2',
                                                        data: {label: 'R&D'},
                                                        selectable: false,
                                                        styleClass: 'department-cto'
                                                        }]
                                                }
                                        ]
                                },
                                selection: {},
                        }
                },
                components: {
                       Item : ButtonCounter,
                       OrganizationChart : OrganizationChart,
                //        ToastService : ToastService,
                },
                methods: {
                        get_items() {
                                frappe.xcall('erpnext.selling.page.point_of_sale.point_of_sale.get_items', {
                                        start : 1,
                                        page_length: 100,
                                        price_list: "Standard Selling",
                                        item_group: "All Item Groups",
                                }).then((res) => {
                                        this.items = res.items
                                })
                                
                        },
                        onNodeSelect(node) {
                        // this.$toast.add({severity:'success', summary: 'Node Selected', detail: node.data.label, life: 3000});
                        frappe.msgprint(node.data.label)
                        },
                        onNodeUnselect(node) {
                        // this.$toast.add({severity:'success', summary: 'Node Unselected', detail: node.data.label, life: 3000});
                        frappe.msgprint(node.data.label)
                        },
                        onNodeExpand(node) {
                        // this.$toast.add({severity:'success', summary: 'Node Expanded', detail: node.data.label, life: 3000});
                        frappe.msgprint(node.data.label)
                        },
                        onNodeCollapse(node) {
                        // this.$toast.add({severity:'success', summary: 'Node Collapsed', detail: node.data.label, life: 3000});
                        frappe.msgprint(node.data.label)
                        },
                }
        }
</script>

<style scoped>
        button {
                margin-top: 10px;
        }
        .p-person {
        padding: 0;
        border: 0 none;
        }

        .node-header, .node-content {
                padding: .5em .7rem;
        }

        .node-header {
                background-color: #495ebb;
                color: #ffffff;
        }

        .node-content {
                text-align: center;
                border: 1px solid #495ebb;
        }

        .node-content img {
                border-radius: 50%;
        }

        .department-cfo {
                background-color: #7247bc;
                color: #ffffff;
        }

        .department-coo {
                background-color: #a534b6;
                color: #ffffff;
        }

        .department-cto {
                background-color: #e9286f;
                color: #ffffff;
        }
</style>


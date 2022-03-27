<template>
  <div class="page-add-invoice">

      <a-breadcrumb>
    <a-breadcrumb-item><router-link to="/dashboard">Dashboard</router-link></a-breadcrumb-item>
    <a-breadcrumb-item><router-link to="/dashboard/invoices">Invoices</router-link></a-breadcrumb-item>
    <a-breadcrumb-item aria-current="true"><router-link to="/dashboard/invoices/add">Add</router-link></a-breadcrumb-item>
  </a-breadcrumb>



      <a-form :label-col="labelCol" layout="vertical" :wrapper-col="wrapperCol">
        <a-form-item label="Client" required>
        <a-select v-model:value="modelRef.client" placeholder="please select your client" 
        :options="modelRef.clients" @change="handleChange">
        </a-select>
        </a-form-item>
        <a-descriptions v-if="modelRef.selectedClient" size="small" :column="1">
            <a-descriptions-item label="Name">{{modelRef.selectedClient.name}}</a-descriptions-item>
            <a-descriptions-item v-if="modelRef.selectedClient.address1" label="Address">
            {{modelRef.selectedClient.address1}}
            </a-descriptions-item>
            <a-descriptions-item v-if="modelRef.selectedClient.address2" label="Address 2">
            {{modelRef.selectedClient.address2}}
            </a-descriptions-item>
            <a-descriptions-item v-if="modelRef.selectedClient.zip_code || modelRef.selectedClient.place" label="Zip code">
            {{modelRef.selectedClient.zip_code}} {{modelRef.selectedClient.place}}
            </a-descriptions-item>
            <a-descriptions-item v-if="modelRef.selectedClient.country" label="Country">
            {{modelRef.selectedClient.country}}
            </a-descriptions-item>
        </a-descriptions>
        <h2>Items</h2>
        <item-form 
            v-for="item in modelRef.items"
            :key="item.item_num"
            :initialItem="item"
            v-on:updatePrice="updateTotals"
        />
        <a-form-item class="add-item">
            <a-button type="primary" @click.prevent="addItem">+</a-button>
        </a-form-item>
        <a-form-item ref="due_days" label="Due days" name="due_days">
            <a-input v-model:value="modelRef.due_days" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="sender_reference" label="Sender reference" name="sender_reference">
            <a-input v-model:value="modelRef.sender_reference" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item label="Total">
            <a-space direction="vertical">
                <a-typography-text><strong>Net amount</strong> : {{ modelRef.net_amount }}</a-typography-text>
                <a-typography-text><strong>VAT amount</strong> : {{ modelRef.vat_amount }}</a-typography-text>
                <a-typography-text><strong>Gross amount</strong> : {{ modelRef.gross_amount }}</a-typography-text>
            </a-space>
        </a-form-item>
        <a-form-item class="error-infos" :wrapper-col="{ span: 14, offset: 4 }" v-bind="errorInfos">
        <a-button type="primary" @click.prevent="onSubmit">Create</a-button>
        <a-button style="margin-left: 10px" @click="resetFields">Reset</a-button>
        </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { defineComponent, reactive, computed, ref, toRaw } from 'vue'
import { authAxios } from '../../../utils/auth'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'
import { toArray } from 'lodash-es'
import { Form } from 'ant-design-vue'
const useForm = Form.useForm;
import ItemForm from '@/components/ItemForm.vue'
import filters from '@/helpers/filters'

export default defineComponent ({
    setup() {
        const router = useRouter()

        const modelRef = reactive({
            client: undefined,
            due_days: 14,
            sender_reference: '',
            clientDetail: [],
            selectedClient: undefined,
            net_amount: 0,
            vat_amount: 0,
            gross_amount: 0,
            discount_amount: 0,
            clients: [],
            items: [
                {
                    item_num: 0,
                    title: '',
                    unit_price: '',
                    quantity: 1,
                    vat_rate: 0,
                    net_amount: 0,
                }
            ]
        });

        const rulesRef = reactive({
            client: [
                {
                required: true,
                message: 'Please select client',
                },
            ],
            due_days: [
                {
                required: false,
                message: 'Please Due days input',
                },
            ],
            sender_reference: [
                {
                required: false,
                message: 'Please Sender reference input',
                },
            ],
        });

        const handleChange = (value) => {
            console.log(`selected ${value}`);
            modelRef.client = value
            const reqObject = JSON.parse(JSON.stringify(modelRef.clientDetail));
            modelRef.selectedClient = reqObject.find(c => value == c.id)
        };
        const { resetFields, validate, validateInfos, mergeValidateInfo } = useForm(modelRef, rulesRef);

        const onSubmit = () => {
        validate()
            .then(() => {
            console.log(toRaw(modelRef));
            const formData = {
                client_name: toRaw(modelRef).selectedClient.name,
                client_email: toRaw(modelRef).selectedClient.email,
                client_org_number: toRaw(modelRef).selectedClient.org_number,
                client_address1: toRaw(modelRef).selectedClient.address1,
                client_address2: toRaw(modelRef).selectedClient.address2,
                client_zip_code: toRaw(modelRef).selectedClient.zip_code,
                client_place: toRaw(modelRef).selectedClient.place,
                client_country: toRaw(modelRef).selectedClient.country,
                client_contact_person: toRaw(modelRef).selectedClient.contact_person,
                client_contact_reference: toRaw(modelRef).selectedClient.contact_reference,
                client: toRaw(modelRef).client,
                discount_amount: filters.decimal(toRaw(modelRef).discount_amount),
                gross_amount: filters.decimal(toRaw(modelRef).gross_amount),
                net_amount: filters.decimal(toRaw(modelRef).net_amount),
                vat_amount: filters.decimal(toRaw(modelRef).vat_amount),
                items: toRaw(modelRef).items,
                due_days: toRaw(modelRef).due_days,
                sender_reference: toRaw(modelRef).sender_reference
            }
            authAxios.post('api/v1/invoices/', JSON.stringify(formData))
                .then(response => {
                    message.success(`Invoice ${response.data.invoice_number} created !`)

                    router.push('/dashboard/invoices')
                })
                .catch(error => {
                    message.error(JSON.stringify(error.message))
                })
            })
            .catch(err => {
            console.log('error', err);
            });
        };

        const addItem = () => {
            modelRef.items.push({
                item_num: modelRef.items.length,
                title: '',
                unit_price: '',
                quantity: 1,
                vat_rate: 0,
                net_amount: 0,
            })
        };

        const updateTotals = (changedItem) => {
            let net_amount = 0
            let vat_amount = 0

            let item = modelRef.items.filter(i => i.item_num === changedItem.item_num)

            item = changedItem

            for (let i = 0; i < modelRef.items.length; i++) {
                const vat_rate = modelRef.items[i].vat_rate
                
                vat_amount += modelRef.items[i].net_amount * (vat_rate / 100)
                net_amount += modelRef.items[i].net_amount
            }

            modelRef.net_amount = net_amount
            modelRef.vat_amount = vat_amount
            modelRef.gross_amount = net_amount + vat_amount
            modelRef.discount_amount = 0
        };

        const errorInfos = computed(() => {
        return mergeValidateInfo(toArray(validateInfos));
        });

        authAxios.get('api/v1/clients/')
            .then(response => {
                const data = response.data.map(c => ({
                    label: `${c.name}`,
                    value: c.id,
                }));
                modelRef.clients = data
                for (let i = 0; i < response.data.length; i++) {
                    modelRef.clientDetail.push(response.data[i])
                    
                }
            })
            .catch(error => {
                message.error(JSON.stringify(error));
            })

        return {
            router,
            labelCol: {
                span: 4,
            },
            wrapperCol: {
                span: 14,
            },
            validateInfos,
            resetFields,
            modelRef,
            onSubmit,
            errorInfos,
            handleChange,
            updateTotals,
            addItem,
            filters
        }
    },
    components: {
        ItemForm
    }
})
</script>

<style>
.error-infos :deep(.ant-form-explain) {
  white-space: pre-line;
}
</style>
<template>
  <div class="page-team">
    <a-page-header
    style="border: 1px solid rgb(235, 237, 240); margin-bottom: 16px"
    :title="formState.name"
    sub-title="Team details"
    @back="() => $router.go(-1)"
    />
    <a-form ref="formRef" layout="vertical" :model="formState" :rules="rules">
        <a-form-item ref="name" label="Name" name="name">
        <a-input v-model:value="formState.name" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="org_number" label="Organization number" name="org_number">
        <a-input v-model:value="formState.org_number" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="first_invoice_number" label="First invoice number" name="first_invoice_number">
        <a-input v-model:value="formState.first_invoice_number" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="email" label="Email" name="email">
        <a-input v-model:value="formState.email" type="email" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="address1" label="Address 1" name="address1">
        <a-input v-model:value="formState.address1" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="address2" label="Address 2" name="address2">
        <a-input v-model:value="formState.address2" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="zip_code" label="Zip code" name="zip_code">
        <a-input v-model:value="formState.zip_code" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="place" label="Place" name="place">
        <a-input v-model:value="formState.place" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item ref="bankaccount" label="Bank account" name="bankaccount">
        <a-input v-model:value="formState.bankaccount" placeholder="input placeholder" />
        </a-form-item>
        <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button type="primary" @click="onSubmit">Save changes</a-button>
        </a-form-item>
    </a-form>
  </div>
</template>

<script>
import { authAxios } from '../../../utils/auth'
import { defineComponent, reactive, ref, toRaw } from 'vue'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'

export default defineComponent ({
    setup() {

        const router = useRouter()
        const formRef = ref()
        const formState = reactive({
            id: null,
            name: '',
            org_number: '',
            first_invoice_number: '',
            email: '',
            address1: '',
            address2: '',
            zip_code: '',
            place: '',
            bankaccount: ''
        })

        authAxios.get('api/v1/teams/')
            .then(response => {
                formState.id = response.data[0].id
                formState.name = response.data[0].name
                formState.org_number = response.data[0].org_number
                formState.first_invoice_number = response.data[0].first_invoice_number
                formState.email = response.data[0].email
                formState.address1 = response.data[0].address1
                formState.address2 = response.data[0].address2
                formState.zip_code = response.data[0].zip_code
                formState.place = response.data[0].place
                formState.bankaccount = response.data[0].bankaccount
            })
            .catch(error => {
                console.log(JSON.stringify(error))
            })

        const rules = {
            name: [
                {
                    required: true,
                    message: 'Please input Name',
                    trigger: 'blur',
                }
            ],
            org_number: [
                {
                    required: false,
                    message: 'Please input Organization number',
                    trigger: 'blur',
                }
            ],
            email: [
                {
                    required: false,
                    message: 'Please input Email',
                    trigger: 'blur',
                }
            ],
            address1: [
                {
                    required: false,
                    message: 'Please input Address',
                    trigger: 'blur',
                }
            ],
            address2: [
                {
                    required: false,
                    message: 'Please input Address',
                    trigger: 'blur',
                }
            ],
            zip_code: [
                {
                    required: false,
                    message: 'Please input Zip code number',
                    trigger: 'blur',
                }
            ],
            place: [
                {
                    required: false,
                    message: 'Please input Place',
                    trigger: 'blur',
                }
            ],
            bankaccount: [
                {
                    required: true,
                    message: 'Please input Bank account',
                    trigger: 'blur',
                }
            ]
        }

        const onSubmit = () => {
            formRef.value
                .validate()
                .then(() => {
                console.log('values', formState, toRaw(formState));
                authAxios.patch(`api/v1/teams/${formState.id}/`, toRaw(formState))
                    .then(response => {
                        message.success(`Client ${response.data.name} edited !`)

                    })
                    .catch(error => {
                        message.error(JSON.stringify(error));
                    })
                })
                .catch(error => {
                console.log('error', error);
                });
        };


        return {
            formState,
            router,
            onSubmit,
            rules,
            formRef,
        }
    }
})
</script>

<style scoped>
.demo-page-header :deep(tr:last-child td) {
  padding-bottom: 0;
}
</style>
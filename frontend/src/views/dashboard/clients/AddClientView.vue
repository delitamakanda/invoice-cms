<template>
<div>

    <a-page-header
    style="border: 1px solid rgb(235, 237, 240); margin-bottom: 16px"
    title="Add client"
    sub-title=""
    @back="() => $router.go(-1)"
  />
  <a-form ref="formRef" layout="vertical" :model="formState" :rules="rules">
    <a-form-item ref="name" label="Name" name="name">
      <a-input v-model:value="formState.name" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item ref="email" label="Email" name="email">
      <a-input type="email" v-model:value="formState.email" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item ref="org_number" label="Organization number" name="org_number">
      <a-input v-model:value="formState.org_number" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item ref="address1" label="Address" name="address1">
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
    <a-form-item ref="country" label="Country" name="country">
      <a-input v-model:value="formState.country" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item ref="contact_person" label="Contact person" name="contact_person">
      <a-input v-model:value="formState.contact_person" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item ref="contact_reference" label="Contact reference" name="contact_reference">
      <a-input v-model:value="formState.contact_reference" placeholder="input placeholder" />
    </a-form-item>
    <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
      <a-button type="primary" @click="onSubmit">Create</a-button>
      <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
    </a-form-item>
  </a-form>
</div>
</template>

<script>
import { defineComponent, reactive, ref, toRaw } from 'vue'
import { authAxios } from '../../../utils/auth'
import { message } from 'ant-design-vue'
import { useRouter } from 'vue-router'

export default defineComponent ({
    setup() {
        const router = useRouter()
        const formRef = ref()
        const formState = reactive({
            name: '',
            email: '',
            org_number: '',
            address1: '',
            address2: '',
            zip_code: '',
            place: '',
            country: '',
            contact_person: '',
            contact_reference: '',
        })

        const rules = {
            name: [
                {
                    required: true,
                    message: 'Please input Name',
                    trigger: 'blur',
                }
            ],
            email: [
                {
                    required: true,
                    message: 'Please input Email',
                    trigger: 'blur',
                }
            ],
            org_number: [
                {
                    required: true,
                    message: 'Please input Organization number',
                    trigger: 'blur',
                }
            ],
            address1: [
                {
                    required: true,
                    message: 'Please input Address',
                    trigger: 'blur',
                }
            ],
            zip_code: [
                {
                    required: true,
                    message: 'Please input Zip code',
                    trigger: 'blur',
                }
            ],
            place: [
                {
                    required: true,
                    message: 'Please input Place',
                    trigger: 'blur',
                }
            ],
            country: [
                {
                    required: true,
                    message: 'Please input Country',
                    trigger: 'blur',
                }
            ],
            contact_person: [
                {
                    required: true,
                    message: 'Please input Contact person',
                    trigger: 'blur',
                }
            ],
            contact_reference: [
                {
                    required: true,
                    message: 'Please input Contact reference',
                    trigger: 'blur',
                }
            ],
        }

        const onSubmit = () => {
            formRef.value
                .validate()
                .then(() => {
                console.log('values', formState, toRaw(formState));
                authAxios.post('api/v1/clients/', toRaw(formState))
                    .then(response => {
                        message.success(`Client ${response.data.name} added !`)
                        router.push('/dashboard/clients')

                    })
                    .catch(error => {
                        message.error(JSON.stringify(error));
                    })
                })
                .catch(error => {
                console.log('error', error);
                });
        };

        const resetForm = () => {
            formRef.value.resetFields();
        };

        return {
            router,
            formRef,
            rules,
            onSubmit,
            resetForm,
            formState,
        }
    }
})
</script>

<style>

</style>